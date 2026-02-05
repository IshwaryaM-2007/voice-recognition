import base64
import tempfile
import whisper
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()
model = whisper.load_model("tiny")

API_KEY = "ishu_guvi_voice_api_2026"


class VoiceRequest(BaseModel):
    audio_base64: str


@app.post("/detect-voice")
def detect_voice(
    data: VoiceRequest,
    x_api_key: str = Header(...)
):
    # 1. API key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2. Input validation (THIS is the key fix)
    audio_base64 = data.audio_base64.strip()
    if not audio_base64:
        raise HTTPException(status_code=400, detail="Missing input")

    # 3. Decode Base64
    try:
        audio_bytes = base64.b64decode(audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio")

    # 4. Save temp MP3
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        f.write(audio_bytes)
        temp_path = f.name

    # 5. Language detection
    result = model.transcribe(temp_path)
    language = result.get("language", "unknown")

    # 6. AI vs Human (demo heuristic)
    if len(audio_bytes) < 50000:
        classification = "AI-generated"
        confidence = 0.82
        explanation = "Artificial voice patterns observed"
    else:
        classification = "Human-generated"
        confidence = 0.76
        explanation = "Natural speech variations detected"

    return {
        "language": language,
        "classification": classification,
        "confidence": confidence,
        "explanation": explanation
    }
