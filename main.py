from fastapi import FastAPI, Header, HTTPException
import base64

app = FastAPI()

API_KEY = "ishu_guvi_voice_api_2026"

@app.post("/detect-voice")
def detect_voice(data: dict, x_api_key: str = Header(None)):
    # 1. Check API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2. Read input
    audio_base64 = data.get("audio_base64")
    language = data.get("language")

    if not audio_base64 or not language:
        raise HTTPException(status_code=400, detail="Missing input")

    # 3. Decode audio (no real AI yet)
    audio_bytes = base64.b64decode(audio_base64)

    # 4. Dummy logic
    if len(audio_bytes) < 50000:
        classification = "AI-generated"
        confidence = 0.82
        explanation = "Artificial voice patterns observed"
    else:
        classification = "Human-generated"
        confidence = 0.76
        explanation = "Natural speech variations detected"

    # 5. Return response
    return {
        "classification": classification,
        "confidence": confidence,
        "explanation": explanation
    }
