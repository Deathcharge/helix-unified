"""
Enhanced Text-to-Speech system with multiple provider support
"""
import os
import asyncio
import logging
from typing import Dict, Any, Optional, Union
import json
import tempfile
import requests
from google.cloud import texttospeech
from elevenlabs import ElevenLabs
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class TTSSystem:
    """Multi-provider Text-to-Speech system"""
    
    def __init__(self):
        self.provider = os.getenv('TTS_PROVIDER', 'google_cloud').lower()
        self.providers = {}
        self._initialize_providers()
        
        logger.info(f"TTS system initialized with provider: {self.provider}")
    
    def _initialize_providers(self):
        """Initialize all available TTS providers"""
        
        # Google Cloud TTS
        try:
            api_key = os.getenv('GOOGLE_CLOUD_TTS_API_KEY')
            key_path = os.getenv('GOOGLE_CLOUD_TTS_KEY_PATH')
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
            
            if api_key and not key_path:
                # Use API key directly
                self.providers['google_cloud'] = GoogleCloudTTS(api_key=api_key, project_id=project_id)
            elif key_path:
                # Use service account key file
                self.providers['google_cloud'] = GoogleCloudTTS(key_path=key_path, project_id=project_id)
            else:
                logger.warning("Google Cloud TTS credentials not found")
        except Exception as e:
            logger.error(f"Failed to initialize Google Cloud TTS: {e}")
        
        # ElevenLabs TTS
        try:
            elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
            if elevenlabs_key:
                self.providers['elevenlabs'] = ElevenLabsTTS(api_key=elevenlabs_key)
        except Exception as e:
            logger.error(f"Failed to initialize ElevenLabs TTS: {e}")
        
        # AWS Polly TTS
        try:
            aws_key = os.getenv('AWS_ACCESS_KEY_ID')
            aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
            aws_region = os.getenv('AWS_REGION', 'us-east-1')
            
            if aws_key and aws_secret:
                self.providers['aws_polly'] = AWSPollyTTS(
                    access_key=aws_key,
                    secret_key=aws_secret,
                    region=aws_region
                )
        except Exception as e:
            logger.error(f"Failed to initialize AWS Polly TTS: {e}")
    
    async def synthesize_speech(
        self,
        text: str,
        voice: Optional[str] = None,
        language_code: Optional[str] = None,
        provider: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Synthesize speech using the specified or default provider"""
        
        target_provider = provider or self.provider
        
        if target_provider not in self.providers:
            available = list(self.providers.keys())
            return {
                'success': False,
                'error': f'TTS provider {target_provider} not available. Available: {available}',
                'audio_data': None
            }
        
        try:
            result = await self.providers[target_provider].synthesize(
                text=text,
                voice=voice,
                language_code=language_code,
                **kwargs
            )
            
            # Add provider info to result
            result['provider'] = target_provider
            
            logger.info(f"TTS synthesis completed via {target_provider}", extra={
                'text_length': len(text),
                'voice': voice,
                'success': result['success']
            })
            
            return result
            
        except Exception as e:
            logger.error(f"TTS synthesis failed with {target_provider}: {e}")
            return {
                'success': False,
                'error': f'Synthesis failed: {str(e)}',
                'audio_data': None,
                'provider': target_provider
            }
    
    def get_available_providers(self) -> Dict[str, bool]:
        """Get status of all TTS providers"""
        return {name: provider.is_available() for name, provider in self.providers.items()}
    
    def get_provider_voices(self, provider: Optional[str] = None) -> Dict[str, List[str]]:
        """Get available voices for providers"""
        target_provider = provider or self.provider
        
        if target_provider not in self.providers:
            return {}
        
        return self.providers[target_provider].get_available_voices()
    
    async def test_provider(self, provider: str) -> Dict[str, Any]:
        """Test a specific TTS provider"""
        if provider not in self.providers:
            return {
                'success': False,
                'error': f'Provider {provider} not available'
            }
        
        return await self.providers[provider].test_connection()

class GoogleCloudTTS:
    """Google Cloud Text-to-Speech provider"""
    
    def __init__(self, api_key: Optional[str] = None, key_path: Optional[str] = None, project_id: Optional[str] = None):
        self.api_key = api_key
        self.key_path = key_path
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT_ID')
        
        try:
            if key_path:
                self.client = texttospeech.TextToSpeechClient.from_service_account_file(key_path)
            elif api_key:
                # For API key usage, we'd need to implement REST API calls
                self.client = None
                self.use_rest_api = True
            else:
                raise ValueError("No credentials provided")
            
            self.use_rest_api = api_key is not None
            
        except Exception as e:
            logger.error(f"Google Cloud TTS initialization failed: {e}")
            self.client = None
    
    async def synthesize(self, text: str, voice: Optional[str] = None, language_code: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Synthesize speech using Google Cloud TTS"""
        
        if self.use_rest_api:
            return await self._synthesize_via_rest(text, voice, language_code)
        elif self.client:
            return await self._synthesize_via_client(text, voice, language_code)
        else:
            return {
                'success': False,
                'error': 'Google Cloud TTS client not initialized',
                'audio_data': None
            }
    
    async def _synthesize_via_client(self, text: str, voice: Optional[str], language_code: Optional[str]) -> Dict[str, Any]:
        """Synthesize using Google Cloud client library"""
        
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice_params = texttospeech.VoiceSelectionParams(
                language_code=language_code or os.getenv('GOOGLE_CLOUD_TTS_LANGUAGE_CODE', 'en-US'),
                name=voice or os.getenv('GOOGLE_CLOUD_TTS_VOICE', 'en-US-Standard-C')
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            response = await asyncio.to_thread(
                self.client.synthesize_speech,
                input=synthesis_input,
                voice=voice_params,
                audio_config=audio_config
            )
            
            return {
                'success': True,
                'audio_data': response.audio_content,
                'format': 'mp3'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Google Cloud TTS synthesis failed: {str(e)}',
                'audio_data': None
            }
    
    async def _synthesize_via_rest(self, text: str, voice: Optional[str], language_code: Optional[str]) -> Dict[str, Any]:
        """Synthesize using Google Cloud REST API"""
        
        try:
            url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={self.api_key}"
            
            payload = {
                'input': {'text': text},
                'voice': {
                    'languageCode': language_code or 'en-US',
                    'name': voice or 'en-US-Standard-C'
                },
                'audioConfig': {'audioEncoding': 'MP3'}
            }
            
            response = await asyncio.to_thread(
                requests.post,
                url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                audio_content = data.get('audioContent')
                
                if audio_content:
                    import base64
                    audio_data = base64.b64decode(audio_content)
                    
                    return {
                        'success': True,
                        'audio_data': audio_data,
                        'format': 'mp3'
                    }
                else:
                    return {
                        'success': False,
                        'error': 'No audio content in response',
                        'audio_data': None
                    }
            else:
                return {
                    'success': False,
                    'error': f'API request failed: {response.status_code} - {response.text}',
                    'audio_data': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'ReST API synthesis failed: {str(e)}',
                'audio_data': None
            }
    
    def get_available_voices(self) -> Dict[str, List[str]]:
        """Get available Google Cloud voices"""
        # This would require additional API calls to list voices
        return {
            'english': ['en-US-Standard-C', 'en-US-Standard-D', 'en-US-Wavenet-A', 'en-US-Wavenet-B'],
            'other': ['en-GB-Standard-A', 'en-GB-Wavenet-A']
        }
    
    def is_available(self) -> bool:
        """Check if Google Cloud TTS is available"""
        return self.client is not None or self.use_rest_api
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Google Cloud TTS connection"""
        test_result = await self.synthesize("Hello, this is a test.", "en-US-Standard-C")
        return {
            'success': test_result['success'],
            'provider': 'google_cloud',
            'error': test_result.get('error')
        }

class ElevenLabsTTS:
    """ElevenLabs Text-to-Speech provider"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        
        try:
            self.client = ElevenLabs(api_key=api_key)
        except Exception as e:
            logger.error(f"ElevenLabs TTS initialization failed: {e}")
    
    async def synthesize(self, text: str, voice: Optional[str] = None, language_code: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Synthesize speech using ElevenLabs"""
        
        if not self.client:
            return {
                'success': False,
                'error': 'ElevenLabs client not initialized',
                'audio_data': None
            }
        
        try:
            voice_id = voice or os.getenv('ELEVENLABS_VOICE_ID', 'Rachel')
            
            audio = await asyncio.to_thread(
                self.client.generate,
                text=text,
                voice=voice_id
            )
            
            return {
                'success': True,
                'audio_data': audio,
                'format': 'mp3'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'ElevenLabs synthesis failed: {str(e)}',
                'audio_data': None
            }
    
    def get_available_voices(self) -> Dict[str, List[str]]:
        """Get available ElevenLabs voices"""
        return {
            'premium': ['Rachel', 'Domi', 'Bella', 'Antoni', 'Elli'],
            'cloned': ['Custom voice IDs']
        }
    
    def is_available(self) -> bool:
        """Check if ElevenLabs TTS is available"""
        return self.client is not None
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test ElevenLabs connection"""
        test_result = await self.synthesize("Hello, this is a test.")
        return {
            'success': test_result['success'],
            'provider': 'elevenlabs',
            'error': test_result.get('error')
        }

class AWSPollyTTS:
    """AWS Polly Text-to-Speech provider"""
    
    def __init__(self, access_key: str, secret_key: str, region: str = 'us-east-1'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        
        try:
            self.client = boto3.client(
                'polly',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
        except Exception as e:
            logger.error(f"AWS Polly initialization failed: {e}")
            self.client = None
    
    async def synthesize(self, text: str, voice: Optional[str] = None, language_code: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Synthesize speech using AWS Polly"""
        
        if not self.client:
            return {
                'success': False,
                'error': 'AWS Polly client not initialized',
                'audio_data': None
            }
        
        try:
            voice_id = voice or 'Joanna'
            
            response = await asyncio.to_thread(
                self.client.synthesize_speech,
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_id
            )
            
            audio_data = response['AudioStream'].read()
            
            return {
                'success': True,
                'audio_data': audio_data,
                'format': 'mp3'
            }
            
        except ClientError as e:
            return {
                'success': False,
                'error': f'AWS Polly synthesis failed: {str(e)}',
                'audio_data': None
            }
    
    def get_available_voices(self) -> Dict[str, List[str]]:
        """Get available AWS Polly voices"""
        return {
            'english': ['Joanna', 'Matthew', 'Kimberly', 'Justin', 'Amy'],
            'neural': ['Joanna', 'Matthew', 'Lupe', 'Ayanda']
        }
    
    def is_available(self) -> bool:
        """Check if AWS Polly is available"""
        return self.client is not None
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test AWS Polly connection"""
        test_result = await self.synthesize("Hello, this is a test.")
        return {
            'success': test_result['success'],
            'provider': 'aws_polly',
            'error': test_result.get('error')
        }

# Global TTS system instance
tts_system = TTSSystem()