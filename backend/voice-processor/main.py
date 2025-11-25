from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import redis
import json
import jwt
import os
from datetime import datetime
import io
from pydub import AudioSegment
from google.cloud import speech, texttospeech
import asyncio

# Initialize FastAPI app
app = FastAPI(title="Voice Processing Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL)

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable is required for production")
ALGORITHM = "HS256"

# Google Cloud clients
# Note: In production, you would need to set up authentication properly
# For now, we'll initialize them but handle exceptions gracefully
try:
    speech_client = speech.SpeechClient()
    tts_client = texttospeech.TextToSpeechClient()
except Exception as e:
    print(f"Warning: Google Cloud clients not initialized: {e}")
    speech_client = None
    tts_client = None

# Data models
class TranscriptionRequest(BaseModel):
    audio_data: str  # Base64 encoded audio data
    language_code: str = "en-US"

class TranscriptionResponse(BaseModel):
    text: str
    confidence: float
    language: str

class SynthesisRequest(BaseModel):
    text: str
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    audio_encoding: str = "MP3"

class SynthesisResponse(BaseModel):
    audio_data: str  # Base64 encoded audio data
    audio_encoding: str
    duration: float

class TokenData(BaseModel):
    user_id: str

# JWT token verification
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TokenData(user_id=user_id)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Voice Processing"}

# Transcribe audio endpoint
@app.post("/api/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(request: TranscriptionRequest, token: TokenData = Depends(verify_token)):
    if not speech_client:
        raise HTTPException(status_code=500, detail="Google Cloud Speech-to-Text not configured")
    
    try:
        # Decode base64 audio data
        import base64
        audio_bytes = base64.b64decode(request.audio_data)
        
        # Create audio object
        audio = speech.RecognitionAudio(content=audio_bytes)
        
        # Configure recognition
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=request.language_code,
        )
        
        # Perform transcription
        response = speech_client.recognize(config=config, audio=audio)
        
        if not response.results:
            raise HTTPException(status_code=400, detail="No speech detected")
        
        # Get the most confident result
        result = response.results[0]
        transcript = result.alternatives[0].transcript
        confidence = result.alternatives[0].confidence
        
        # Publish transcription event to Redis
        transcription_event = {
            "event": "transcription_completed",
            "text": transcript,
            "confidence": confidence,
            "language": request.language_code,
            "timestamp": datetime.utcnow().isoformat()
        }
        redis_client.publish("voice_events", json.dumps(transcription_event))
        
        return TranscriptionResponse(
            text=transcript,
            confidence=confidence,
            language=request.language_code
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

# Test transcription endpoint
@app.get("/api/transcribe/test")
async def test_transcription(token: TokenData = Depends(verify_token)):
    # This is a simple test endpoint that returns a mock response
    return {"status": "Transcription service is available", "test": "successful"}

# Synthesize speech endpoint
@app.post("/api/synthesize", response_model=SynthesisResponse)
async def synthesize_speech(request: SynthesisRequest, token: TokenData = Depends(verify_token)):
    if not tts_client:
        raise HTTPException(status_code=500, detail="Google Cloud Text-to-Speech not configured")
    
    try:
        # Configure synthesis
        synthesis_input = texttospeech.SynthesisInput(text=request.text)
        
        # Configure voice
        voice = texttospeech.VoiceSelectionParams(
            language_code=request.language_code,
            name=request.voice_name if request.voice_name else None,
        )
        
        # Configure audio
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        # Perform synthesis
        response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        # Encode audio data as base64
        import base64
        audio_data = base64.b64encode(response.audio_content).decode("utf-8")
        
        # Calculate approximate duration (simplified)
        # In a real implementation, you would calculate this more accurately
        duration = len(request.text) * 0.1  # Rough approximation
        
        # Publish synthesis event to Redis
        synthesis_event = {
            "event": "synthesis_completed",
            "text_length": len(request.text),
            "duration": duration,
            "timestamp": datetime.utcnow().isoformat()
        }
        redis_client.publish("voice_events", json.dumps(synthesis_event))
        
        return SynthesisResponse(
            audio_data=audio_data,
            audio_encoding="MP3",
            duration=duration
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")

# Process uploaded audio file
@app.post("/api/process-audio")
async def process_audio_file(
    file: UploadFile = File(...),
    language_code: str = "en-US",
    token: TokenData = Depends(verify_token)
):
    if not speech_client:
        raise HTTPException(status_code=500, detail="Google Cloud Speech-to-Text not configured")
    
    try:
        # Read uploaded file
        contents = await file.read()
        
        # Convert to WAV if necessary
        audio = AudioSegment.from_file(io.BytesIO(contents))
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_data = wav_io.getvalue()
        
        # Create audio object for Google Cloud
        audio_obj = speech.RecognitionAudio(content=wav_data)
        
        # Configure recognition
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=audio.frame_rate,
            language_code=language_code,
        )
        
        # Perform transcription
        response = speech_client.recognize(config=config, audio=audio_obj)
        
        if not response.results:
            raise HTTPException(status_code=400, detail="No speech detected")
        
        # Get the most confident result
        result = response.results[0]
        transcript = result.alternatives[0].transcript
        confidence = result.alternatives[0].confidence
        
        # Publish processing event to Redis
        processing_event = {
            "event": "audio_processed",
            "filename": file.filename,
            "text_length": len(transcript),
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }
        redis_client.publish("voice_events", json.dumps(processing_event))
        
        return {
            "filename": file.filename,
            "transcript": transcript,
            "confidence": confidence,
            "language": language_code
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")

# Get voice events
@app.get("/api/events")
async def get_voice_events(token: TokenData = Depends(verify_token)):
    # This would typically be a WebSocket endpoint for real-time events
    # For now, we'll return recent events from Redis
    events = []
    for key in redis_client.lrange("voice_events_log", 0, 9):  # Last 10 events
        events.append(json.loads(key))
    return {"events": events}

# Endpoint to get service information
@app.get("/api/info")
async def get_service_info():
    return {
        "name": "Voice Processing Service",
        "version": "1.0.0",
        "description": "Handles speech-to-text transcription and text-to-speech synthesis"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)