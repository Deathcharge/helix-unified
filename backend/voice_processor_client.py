"""
Voice Processor API Client - Connects to voice_processor microservice for TTS/STT.
"""
import asyncio
import base64
import hashlib
import logging
import os
import tempfile
from pathlib import Path
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)

# Cache directory for TTS audio
CACHE_DIR = Path(tempfile.gettempdir()) / "helix_tts_cache"
CACHE_DIR.mkdir(exist_ok=True)


class VoiceProcessorClient:
    """Client for interacting with the voice_processor microservice."""

    def __init__(
        self,
        base_url: str = None,
        jwt_token: str = None,
        enable_cache: bool = True
    ):
        """
        Initialize voice processor client.

        Args:
            base_url: Base URL of voice_processor service (default: from env)
            jwt_token: JWT token for authentication (default: from env)
            enable_cache: Whether to cache TTS audio files
        """
        self.base_url = base_url or os.getenv(
            "VOICE_PROCESSOR_URL",
            "http://localhost:8001"  # Default port for voice processor
        )
        self.jwt_token = jwt_token or os.getenv("JWT_TOKEN")
        self.enable_cache = enable_cache
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            headers = {}
            if self.jwt_token:
                headers["Authorization"] = f"Bearer {self.jwt_token}"
            self.session = aiohttp.ClientSession(headers=headers)
        return self.session

    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()

    def _get_cache_path(self, text: str, voice_name: str, language_code: str) -> Path:
        """Generate cache file path for TTS audio."""
        # Create hash of text + voice + language
        cache_key = f"{text}:{voice_name}:{language_code}"
        file_hash = hashlib.md5(cache_key.encode(), usedforsecurity=False).hexdigest()
        return CACHE_DIR / f"{file_hash}.mp3"

    async def synthesize_speech(
        self,
        text: str,
        voice_name: Optional[str] = None,
        language_code: str = "en-US",
        use_cache: bool = True
    ) -> Optional[bytes]:
        """
        Synthesize speech from text using Google Cloud TTS.

        Args:
            text: Text to synthesize
            voice_name: Google Cloud TTS voice name (e.g., "en-US-Neural2-A")
            language_code: Language code (default: "en-US")
            use_cache: Whether to use cached audio if available

        Returns:
            MP3 audio bytes, or None if synthesis failed
        """
        # Check cache first
        if use_cache and self.enable_cache:
            cache_path = self._get_cache_path(text, voice_name or "default", language_code)
            if cache_path.exists():
                logger.info(f"🎵 Using cached TTS audio for: {text[:30]}...")
                return cache_path.read_bytes()

        # Call voice_processor API
        try:
            session = await self._get_session()

            payload = {
                "text": text,
                "language_code": language_code,
                "audio_encoding": "MP3"
            }
            if voice_name:
                payload["voice_name"] = voice_name

            async with session.post(
                f"{self.base_url}/api/synthesize",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"TTS synthesis failed: {response.status} - {error_text}")
                    return None

                result = await response.json()
                audio_data = base64.b64decode(result["audio_data"])

                # Cache the audio
                if use_cache and self.enable_cache:
                    cache_path = self._get_cache_path(text, voice_name or "default", language_code)
                    cache_path.write_bytes(audio_data)
                    logger.info(f"💾 Cached TTS audio: {cache_path.name}")

                logger.info(f"✅ TTS synthesis complete: {len(audio_data)} bytes")
                return audio_data

        except asyncio.TimeoutError:
            logger.error("TTS synthesis timeout")
            return None
        except aiohttp.ClientError as e:
            logger.error(f"TTS API connection error: {e}")
            return None
        except Exception as e:
            logger.error(f"TTS synthesis error: {e}", exc_info=True)
            return None

    async def transcribe_audio(
        self,
        audio_data: bytes,
        language_code: str = "en-US"
    ) -> Optional[dict]:
        """
        Transcribe audio to text using Google Cloud Speech-to-Text.

        Args:
            audio_data: Audio data in bytes
            language_code: Language code (default: "en-US")

        Returns:
            Dict with 'text', 'confidence', 'language', or None if failed
        """
        try:
            session = await self._get_session()

            # Encode audio as base64
            audio_b64 = base64.b64encode(audio_data).decode("utf-8")

            payload = {
                "audio_data": audio_b64,
                "language_code": language_code
            }

            async with session.post(
                f"{self.base_url}/api/transcribe",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"STT transcription failed: {response.status} - {error_text}")
                    return None

                result = await response.json()
                logger.info(f"✅ STT transcription: {result['text'][:50]}...")
                return result

        except asyncio.TimeoutError:
            logger.error("STT transcription timeout")
            return None
        except aiohttp.ClientError as e:
            logger.error(f"STT API connection error: {e}")
            return None
        except Exception as e:
            logger.error(f"STT transcription error: {e}", exc_info=True)
            return None

    async def health_check(self) -> bool:
        """
        Check if voice_processor service is healthy.

        Returns:
            True if service is healthy, False otherwise
        """
        try:
            session = await self._get_session()
            async with session.get(
                f"{self.base_url}/health",
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"✅ Voice processor healthy: {result}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Voice processor health check failed: {e}")
            return False


# Global client instance
_voice_client: Optional[VoiceProcessorClient] = None


def get_voice_client() -> VoiceProcessorClient:
    """Get or create global voice processor client."""
    global _voice_client
    if _voice_client is None:
        _voice_client = VoiceProcessorClient()
    return _voice_client


async def cleanup_voice_client():
    """Cleanup global voice processor client."""
    global _voice_client
    if _voice_client:
        await _voice_client.close()
        _voice_client = None
