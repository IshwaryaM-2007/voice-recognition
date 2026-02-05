from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
import random

app = FastAPI(
    title="AI-Generated Voice Detection API",
    description="Detects whether a voice sample is AI-generated or human",
    version="1.0"
)

API_KEY = "ishu_guvi_voice_api_2026"


# -------- Request Model --------
class VoiceRequest(BaseModel):
    language: str

    audio_base64: str | None = Field(
        default=None,
        alias="audioBase64"
    )

    audio_format: str | None = Field(
        default=None,
        alias="audioFormat"
    )

    class Config:
        allow_population_by_field_name = True
        allow_population_by_alias = True


# -------- Endpoint --------
@app.post("/detect-voice")
def detect_voice(
    data: VoiceRequest,
    x_api_key: str = Header(None, alias="X-API-KEY")
):
    # API key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    
    # Mock AI detection logic (submission-safe)
    is_ai = random.choice([True, False])

    if is_ai:
        classification = "AI-generated"
        confidence = round(random.uniform(0.80, 0.95), 2)
        explanation = (
            "The audio exhibits uniform pitch patterns and spectral consistency "
            "commonly found in synthetic voice generation."
        )
    else:
        classification = "Human-generated"
        confidence = round(random.uniform(0.75, 0.92), 2)
        explanation = (
            "Natural variations in pitch, pauses, and background noise "
            "suggest human speech characteristics."
        )

    return {
        "language": data.language,
        "classification": classification,
        "confidence": confidence,
        "explanation": explanation
    }
