from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from gtts import gTTS
from gtts.tts import gTTSError

BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "generated_audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="SpeakEasy - Text to Speech API",
    description="Convert text into spoken audio using Google Text-to-Speech (gTTS).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this to your frontend domain before production.
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")


class SpeechRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    language: str = Field(default="en", min_length=2, max_length=10)
    slow: bool = False


LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "ja": "Japanese",
    "pt": "Portuguese",
}


@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "SpeakEasy API is running"}


@app.get("/api/languages")
def get_languages():
    return [{"code": code, "name": name} for code, name in LANGUAGES.items()]


@app.get("/api/voices")
def get_voices():
    # gTTS selects a language/accent rather than exposing individual named voices.
    return {
        "provider": "gTTS",
        "voices": [
            {"id": code, "name": name, "language": code}
            for code, name in LANGUAGES.items()
        ],
        "note": "gTTS provides language-based speech. Individual voice gender/style selection is not available in this version.",
    }


@app.post("/api/tts")
def create_speech(payload: SpeechRequest):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please enter some text.")
    if payload.language not in LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language. Choose a language from /api/languages.")

    filename = f"{uuid4().hex}.mp3"
    output_path = AUDIO_DIR / filename

    try:
        speech = gTTS(text=text, lang=payload.language, slow=payload.slow)
        speech.save(str(output_path))
    except gTTSError:
        output_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=503,
            detail="The text-to-speech service is unavailable. Check your internet connection and try again.",
        )
    except Exception:
        output_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="Unable to generate audio. Please try again.")

    return {
        "success": True,
        "message": "Speech generated successfully.",
        "audio_url": f"/audio/{filename}",
        "filename": filename,
        "language": payload.language,
    }
