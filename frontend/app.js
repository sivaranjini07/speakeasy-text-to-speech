const API_BASE = "http://127.0.0.1:8000";

const textInput = document.getElementById("text-input");
const counter = document.getElementById("counter");
const generateButton = document.getElementById("generate");
const statusMessage = document.getElementById("status");
const result = document.getElementById("result");
const audioPlayer = document.getElementById("audio-player");
const downloadLink = document.getElementById("download");

textInput.addEventListener("input", () => {
  counter.textContent = `${textInput.value.length} / 5000`;
});

generateButton.addEventListener("click", async () => {
  const text = textInput.value.trim();
  const language = document.getElementById("language").value;
  const slow = document.getElementById("slow").checked;

  if (!text) {
    showStatus("Please enter some text before generating speech.", true);
    textInput.focus();
    return;
  }

  generateButton.disabled = true;
  generateButton.querySelector("span").textContent = "Generating audio...";
  showStatus("Connecting to the speech service. This may take a moment.");
  result.classList.add("hidden");

  try {
    const response = await fetch(`${API_BASE}/api/tts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, language, slow })
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Speech generation failed.");
    }

    const audioUrl = `${API_BASE}${data.audio_url}`;
    audioPlayer.src = audioUrl;
    downloadLink.href = audioUrl;
    result.classList.remove("hidden");
    showStatus("Your speech is ready. Press play to listen.");
    result.scrollIntoView({ behavior: "smooth", block: "nearest" });
  } catch (error) {
    showStatus(error.message || "Could not connect to the backend. Is the API running?", true);
  } finally {
    generateButton.disabled = false;
    generateButton.querySelector("span").textContent = "Generate speech";
  }
});

function showStatus(message, isError = false) {
  statusMessage.textContent = message;
  statusMessage.classList.toggle("error", isError);
}
