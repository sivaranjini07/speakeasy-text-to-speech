# SpeakEasy — Text-to-Speech Web Application

SpeakEasy is a Python-powered web application that converts written text into MP3 speech. Users can enter text, choose a language, optionally enable slower speech, listen in the browser, and download the generated audio.

## Features

- Text input with a 5,000-character limit and live character counter
- Language selection: English, Hindi, Tamil, Telugu, French, Spanish, German, Italian, Japanese, and Portuguese
- Optional slow-speech mode
- MP3 generation and in-browser audio playback
- MP3 download
- Input validation and helpful error messages
- REST API built with FastAPI
- Interactive API documentation

## Technology stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, FastAPI |
| Text-to-Speech | gTTS |
| API server | Uvicorn |

## Project structure

```text
text-to-speech-internship/
├── backend/
│   ├── generated_audio/
│   │   └── .gitkeep
│   └── main.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.9 or newer
- pip
- A modern web browser
- Internet connection (gTTS contacts an online speech service)

## Run locally (macOS / Linux)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/speakeasy-text-to-speech.git
cd speakeasy-text-to-speech
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

The API will run at `http://127.0.0.1:8000`.

- Health check: http://127.0.0.1:8000/api/health
- Available languages: http://127.0.0.1:8000/api/languages
- Available language options: http://127.0.0.1:8000/api/voices
- Interactive API docs: http://127.0.0.1:8000/docs

### 5. Open the frontend

Open `frontend/index.html` in your browser. Keep the backend terminal running while using the application.

## API reference

### `GET /api/health`

Checks whether the backend is running.

### `GET /api/languages`

Returns the supported language codes and names.

### `GET /api/voices`

Returns language-based speech options. Note: gTTS does not expose individual named male/female voices in this implementation.

### `POST /api/tts`

Request body:

```json
{
  "text": "Hello! Welcome to SpeakEasy.",
  "language": "en",
  "slow": false
}
```

Successful response:

```json
{
  "success": true,
  "message": "Speech generated successfully.",
  "audio_url": "/audio/example.mp3",
  "filename": "example.mp3",
  "language": "en"
}
```

The actual filename is generated uniquely for each request.

## Testing the API

Start the backend, then run:

```bash
curl http://127.0.0.1:8000/api/health
```

Generate speech:

```bash
curl -X POST http://127.0.0.1:8000/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from SpeakEasy","language":"en","slow":false}'
```

You can also test all endpoints using the Swagger UI at `/docs`.

## Important notes and limitations

- An active internet connection is required because gTTS uses an online service.
- Available languages depend on the speech provider.
- This version offers language selection and slow speech, not individual voice gender, accent, pitch, or emotion controls.
- Generated MP3 files are saved in `backend/generated_audio/`. They are excluded from Git by `.gitignore`.
- The permissive CORS setting is intended for local learning. Before production deployment, restrict `allow_origins` to your deployed frontend domain.
- Add rate limiting, file cleanup, authentication, and production-grade monitoring before exposing this service publicly.

## Future enhancements

- User login and speech history
- PDF and DOCX text extraction
- More voice providers and voice styles
- Speaking speed and pitch controls
- Automatic cleanup of old audio files
- Deployment with a hosted frontend and backend

## Learning outcomes

This project demonstrates Python backend development, REST API design, request validation, third-party service integration, frontend/backend communication, audio delivery, error handling, and Git/GitHub project documentation.

## Author

Sivaranjini G
Python Internship Project
