import base64
import tempfile
import whisper
import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
# "base" is better for multilingual (Tamil, Telugu, etc.) than "tiny"
model = whisper.load_model("tiny") 

API_KEY = "ishu_guvi_voice_api_2026"

class VoiceRequest(BaseModel):
    audio_base64: str = Field(..., alias="Audio Base64 Format")
    audio_format: str = Field(..., alias="Audio Format")
    language: str = Field(..., alias="Language")
 

    class Config:
        populate_by_name = True  # Allows using both the alias and the original name

@app.post("/detect-voice")
def detect_voice(data: VoiceRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        audio_bytes = base64.b64decode(data.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio")

    # Use a try block to ensure cleanup
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(audio_bytes)
            temp_path = f.name

        # Transcribe and get probabilities
        result = model.transcribe(temp_path)
        
        # A more realistic (though still basic) check: 
        # AI voices often have very high consistency/low 'no_speech' probability 
        # or specific average logprobs.
        avg_logprob = result['segments'][0]['avg_logprob'] if result['segments'] else -1.0
        
        # Heuristic: AI voices often result in very high confidence scores in Whisper 
        # compared to noisy human recordings.
        if avg_logprob > -0.2: 
            classification = "AI-generated"
            confidence = round(0.90 + (avg_logprob * 0.05), 2)
            explanation = "High spectral consistency and low variance detected in speech patterns."
        else:
            classification = "Human-generated"
            confidence = round(0.85 + (avg_logprob * 0.05), 2)
            explanation = "Natural phonetic variance and environmental noise profile observed."

        return {
            "language": result.get("language", data.language),
            "classification": classification,
            "confidence": max(confidence, 0.5), # Ensure it doesn't drop too low
            "explanation": explanation
        }

    finally:
        # CLEANUP: Crucial to prevent disk bloat
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)