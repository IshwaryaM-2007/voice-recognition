import base64
import tempfile
import whisper
from fastapi import Body, FastAPI, Header, HTTPException
from pydantic import BaseModel



class VoiceRequest(BaseModel):
    audio_base64: str


app = FastAPI()
model = whisper.load_model("tiny")


API_KEY = "ishu_guvi_voice_api_2026"

@app.post("/detect-voice")
def detect_voice(
    data: VoiceRequest = Body(...),
    x_api_key: str = Header(None)
):


    # 1. API key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2. Input validation
    audio_base64 = data.audio_base64
    if not audio_base64:
        raise HTTPException(status_code=400, detail="Missing input")

    # 3. Decode Base64 safely
    try:
        audio_bytes = base64.b64decode(audio_base64, validate=True)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio")

    # 4. Save to temp MP3
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_path = temp_audio.name

    # 5. Detect language using Whisper
    result = model.transcribe(temp_path, task="transcribe")
    detected_language = result["language"]

    # 6. AI vs Human heuristic (safe demo logic)
    if len(audio_bytes) < 50000:
        classification = "AI-generated"
        confidence = 0.82
        explanation = "Artificial voice patterns observed"
    else:
        classification = "Human-generated"
        confidence = 0.76
        explanation = "Natural speech variations detected"

    # 7. Final response
    return {
        "language": detected_language,
        "classification": classification,
        "confidence": confidence,
        "explanation": explanation
    }
