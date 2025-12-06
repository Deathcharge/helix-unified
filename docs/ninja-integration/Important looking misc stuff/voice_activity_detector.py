"""
Voice Activity Detection and Transcription System
Real-time voice activity monitoring and speech-to-text
"""
import asyncio
import io
import logging
import os
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class VoiceActivityDetector:
    """Advanced voice activity detection and transcription"""
    
    def __init__(self):
        self.google_credentials = os.getenv('GOOGLE_CLOUD_TTS_KEY_PATH')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.assemblyai_key = os.getenv('ASSEMBLYAI_API_KEY')
        
        # Voice activity tracking
        self.voice_sessions = defaultdict(dict)
        self.user_speaking_time = defaultdict(float)
        self.channel_activity = defaultdict(lambda: deque(maxlen=100))
        
        # Transcription history
        self.transcription_history = deque(maxlen=500)
        
        # Activity thresholds
        self.silence_threshold = 5.0  # seconds
        self.speaking_threshold = 0.5  # seconds
        
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize transcription providers"""
        
        # Google Speech-to-Text
        if self.google_credentials:
            try:
                from google.cloud import speech
                self.providers['google'] = GoogleSpeechToText(self.google_credentials)
                logger.info("Google Speech-to-Text initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Google STT: {e}")
        
        # OpenAI Whisper
        if self.openai_key:
            try:
                self.providers['whisper'] = WhisperTranscription(self.openai_key)
                logger.info("OpenAI Whisper initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Whisper: {e}")
        
        # AssemblyAI
        if self.assemblyai_key:
            try:
                self.providers['assemblyai'] = AssemblyAITranscription(self.assemblyai_key)
                logger.info("AssemblyAI initialized")
            except Exception as e:
                logger.error(f"Failed to initialize AssemblyAI: {e}")
    
    async def detect_voice_activity(
        self,
        user_id: str,
        channel_id: str,
        is_speaking: bool,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Detect and track voice activity"""
        
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        session_key = f"{channel_id}:{user_id}"
        
        if is_speaking:
            # User started speaking
            if session_key not in self.voice_sessions:
                self.voice_sessions[session_key] = {
                    'start_time': timestamp,
                    'last_activity': timestamp,
                    'speaking_duration': 0.0,
                    'silence_duration': 0.0
                }
            else:
                # Update last activity
                session = self.voice_sessions[session_key]
                time_since_last = (timestamp - session['last_activity']).total_seconds()
                
                if time_since_last > self.silence_threshold:
                    # New speaking session after silence
                    session['silence_duration'] += time_since_last
                
                session['last_activity'] = timestamp
        else:
            # User stopped speaking
            if session_key in self.voice_sessions:
                session = self.voice_sessions[session_key]
                speaking_time = (timestamp - session['last_activity']).total_seconds()
                
                if speaking_time > self.speaking_threshold:
                    session['speaking_duration'] += speaking_time
                    self.user_speaking_time[user_id] += speaking_time
                
                session['last_activity'] = timestamp
        
        # Record activity
        self.channel_activity[channel_id].append({
            'user_id': user_id,
            'is_speaking': is_speaking,
            'timestamp': timestamp.isoformat()
        })
        
        return {
            'user_id': user_id,
            'channel_id': channel_id,
            'is_speaking': is_speaking,
            'total_speaking_time': self.user_speaking_time[user_id],
            'session_info': self.voice_sessions.get(session_key, {})
        }
    
    async def transcribe_audio(
        self,
        audio_data: bytes,
        provider: str = 'whisper',
        language: str = 'en'
    ) -> Dict[str, Any]:
        """Transcribe audio to text"""
        
        if provider not in self.providers:
            available = list(self.providers.keys())
            return {
                'success': False,
                'error': f'Provider {provider} not available. Available: {available}',
                'text': ''
            }
        
        try:
            result = await self.providers[provider].transcribe(audio_data, language)
            
            if result['success']:
                # Store in history
                self.transcription_history.append({
                    'text': result['text'],
                    'provider': provider,
                    'language': language,
                    'timestamp': datetime.utcnow().isoformat(),
                    'confidence': result.get('confidence', 0.0)
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Transcription failed with {provider}: {e}")
            return {
                'success': False,
                'error': str(e),
                'text': ''
            }
    
    def get_channel_activity_stats(self, channel_id: str, hours: int = 1) -> Dict[str, Any]:
        """Get voice activity statistics for a channel"""
        
        activity = list(self.channel_activity[channel_id])
        
        if not activity:
            return {
                'total_events': 0,
                'unique_speakers': 0,
                'activity_level': 'inactive'
            }
        
        # Filter by time window
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent_activity = [
            a for a in activity
            if datetime.fromisoformat(a['timestamp']) > cutoff
        ]
        
        if not recent_activity:
            return {
                'total_events': 0,
                'unique_speakers': 0,
                'activity_level': 'inactive'
            }
        
        unique_speakers = len(set(a['user_id'] for a in recent_activity))
        speaking_events = sum(1 for a in recent_activity if a['is_speaking'])
        
        # Determine activity level
        if speaking_events > 50:
            activity_level = 'very_active'
        elif speaking_events > 20:
            activity_level = 'active'
        elif speaking_events > 5:
            activity_level = 'moderate'
        else:
            activity_level = 'low'
        
        return {
            'total_events': len(recent_activity),
            'unique_speakers': unique_speakers,
            'speaking_events': speaking_events,
            'activity_level': activity_level,
            'events_per_hour': len(recent_activity) / hours
        }
    
    def get_user_speaking_stats(self, user_id: str) -> Dict[str, Any]:
        """Get speaking statistics for a user"""
        
        total_time = self.user_speaking_time[user_id]
        
        # Find active sessions
        active_sessions = [
            session for key, session in self.voice_sessions.items()
            if key.endswith(f":{user_id}")
        ]
        
        return {
            'total_speaking_time': total_time,
            'active_sessions': len(active_sessions),
            'average_session_duration': total_time / len(active_sessions) if active_sessions else 0
        }
    
    def get_transcription_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent transcription history"""
        
        return list(self.transcription_history)[-limit:]

class GoogleSpeechToText:
    """Google Cloud Speech-to-Text provider"""
    
    def __init__(self, credentials_path: str):
        from google.cloud import speech
        self.client = speech.SpeechClient.from_service_account_file(credentials_path)
    
    async def transcribe(self, audio_data: bytes, language: str = 'en') -> Dict[str, Any]:
        """Transcribe audio using Google Speech-to-Text"""
        
        try:
            from google.cloud import speech
            
            audio = speech.RecognitionAudio(content=audio_data)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=f'{language}-US',
                enable_automatic_punctuation=True
            )
            
            response = await asyncio.to_thread(
                self.client.recognize,
                config=config,
                audio=audio
            )
            
            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                confidence = response.results[0].alternatives[0].confidence
                
                return {
                    'success': True,
                    'text': transcript,
                    'confidence': confidence,
                    'provider': 'google'
                }
            else:
                return {
                    'success': False,
                    'error': 'No transcription results',
                    'text': ''
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': ''
            }

class WhisperTranscription:
    """OpenAI Whisper transcription provider"""
    
    def __init__(self, api_key: str):
        import openai
        self.api_key = api_key
        openai.api_key = api_key
    
    async def transcribe(self, audio_data: bytes, language: str = 'en') -> Dict[str, Any]:
        """Transcribe audio using OpenAI Whisper"""
        
        try:
            import openai

            # Create file-like object
            audio_file = io.BytesIO(audio_data)
            audio_file.name = "audio.wav"
            
            response = await asyncio.to_thread(
                openai.audio.transcriptions.create,
                model="whisper-1",
                file=audio_file,
                language=language
            )
            
            return {
                'success': True,
                'text': response.text,
                'confidence': 1.0,  # Whisper doesn't provide confidence
                'provider': 'whisper'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': ''
            }

class AssemblyAITranscription:
    """AssemblyAI transcription provider"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.assemblyai.com/v2"
    
    async def transcribe(self, audio_data: bytes, language: str = 'en') -> Dict[str, Any]:
        """Transcribe audio using AssemblyAI"""
        
        try:
            import requests
            
            headers = {'authorization': self.api_key}
            
            # Upload audio
            upload_response = await asyncio.to_thread(
                requests.post,
                f"{self.base_url}/upload",
                headers=headers,
                data=audio_data,
                timeout=30
            )
            
            if upload_response.status_code != 200:
                return {
                    'success': False,
                    'error': f'Upload failed: {upload_response.status_code}',
                    'text': ''
                }
            
            audio_url = upload_response.json()['upload_url']
            
            # Request transcription
            transcript_request = {
                'audio_url': audio_url,
                'language_code': language
            }
            
            transcript_response = await asyncio.to_thread(
                requests.post,
                f"{self.base_url}/transcript",
                headers=headers,
                json=transcript_request,
                timeout=10
            )
            
            if transcript_response.status_code != 200:
                return {
                    'success': False,
                    'error': f'Transcription request failed: {transcript_response.status_code}',
                    'text': ''
                }
            
            transcript_id = transcript_response.json()['id']
            
            # Poll for completion
            max_attempts = 30
            for _ in range(max_attempts):
                await asyncio.sleep(2)
                
                status_response = await asyncio.to_thread(
                    requests.get,
                    f"{self.base_url}/transcript/{transcript_id}",
                    headers=headers,
                    timeout=10
                )
                
                if status_response.status_code == 200:
                    result = status_response.json()
                    
                    if result['status'] == 'completed':
                        return {
                            'success': True,
                            'text': result['text'],
                            'confidence': result.get('confidence', 0.0),
                            'provider': 'assemblyai'
                        }
                    elif result['status'] == 'error':
                        return {
                            'success': False,
                            'error': result.get('error', 'Transcription failed'),
                            'text': ''
                        }
            
            return {
                'success': False,
                'error': 'Transcription timeout',
                'text': ''
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': ''
            }

# Global voice activity detector instance
voice_activity_detector = VoiceActivityDetector()