import io
import os
from typing import Optional

from loguru import logger
from openai import OpenAI

# Environment variable for OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class TTSService:
    """
    A service to generate high-quality Text-to-Speech audio using the OpenAI API.
    """

    def __init__(self, api_key: Optional[str] = OPENAI_API_KEY):
        self.client = None
        if api_key:
            try:
                self.client = OpenAI(api_key=api_key)
                logger.info("✅ OpenAI TTS client initialized.")
            except Exception as e:
                logger.error(f"❌ Failed to initialize OpenAI client: {e}")
        else:
            logger.warning("⚠️ OPENAI_API_KEY is not set. TTS generation is disabled.")

    async def generate_speech(self, text: str, voice: str = "onyx") -> Optional[io.BytesIO]:
        """
        Generates speech audio from text and returns it as a BytesIO object.

        Args:
            text: The text to convert to speech.
            voice: The voice model to use (e.g., 'onyx', 'nova', 'alloy').

        Returns:
            A BytesIO object containing the MP3 audio data, or None on failure.
        """
        if not self.client:
            logger.error("TTS client not available. Cannot generate speech.")
            return None

        try:
            # Use the tts-1 model for high quality and low latency
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                response_format="mp3"  # Discord can play MP3
            )

            # The response.content is the raw audio data
            audio_stream = io.BytesIO(response.content)
            audio_stream.seek(0)

            logger.info(f"✅ Successfully generated {len(response.content)} bytes of speech using voice '{voice}'.")
            return audio_stream

        except Exception as e:
            logger.error(f"❌ OpenAI TTS generation failed: {e}")
            return None


# Global instance (placeholder for proper initialization in main.py)
tts_service = TTSService()

# Placeholder for integration with agent logic


async def get_agent_voice(agent_name: str) -> str:
    """
    Determines the appropriate voice for a given Helix Collective agent.
    This can be expanded with a database lookup for true agent-specific voices.
    """
    # Map agents to available OpenAI voices for distinct personalities
    voice_map = {
        "Kael": "alloy",
        "Lumina": "nova",
        "Vega": "shimmer",
        "Gemini": "echo",
        "Agni": "fable",
        "Kavach": "onyx",
        "SanghaCore": "onyx",  # Default voice
        "Shadow": "onyx",
        "Echo": "nova",
        "Phoenix": "alloy",
        "Oracle": "shimmer",
        "Claude": "echo",
        "Manus": "fable",
        "MemoryRoot": "onyx",
    }
    return voice_map.get(agent_name, "onyx")
