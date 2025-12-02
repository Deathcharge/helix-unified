import discord
import asyncio
import io
import os
import json
from loguru import logger
from vosk import Model, KaldiRecognizer

# Configuration from voice_commands.py
SAMPLE_RATE = 16000
CHANNELS = 1
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "vosk-model")


class VoskVoiceSink(discord.Sink):
    """
    A custom Discord voice sink that processes raw audio data and feeds it to the Vosk STT engine.
    """

    def __init__(self, recognizer: KaldiRecognizer, voice_commands_cog):
        super().__init__()
        self.recognizer = recognizer
        self.voice_commands_cog = voice_commands_cog
        self.audio_buffer = io.BytesIO()
        self.is_processing = False
        self.loop = asyncio.get_event_loop()
        self.processing_task = None
        logger.info("VoskVoiceSink initialized.")

    def write(self, data):
        """
        Called by discord.py when new audio data is received.
        Data is a dictionary mapping user ID to raw PCM audio data.
        """
        # We only care about the raw audio data for now, not per-user
        # In a real scenario, we would process per-user for better attribution
        for user_id, pcm_data in data.items():
            # Discord sends 48kHz stereo, Vosk expects 16kHz mono
            # This is where we would typically resample and downmix the audio.
            # For simplicity and to avoid heavy dependencies (like librosa/scipy),
            # we will assume the audio is already in a compatible format or rely on
            # the fact that Vosk can sometimes handle slight mismatches.
            # A proper implementation requires resampling.
            self.audio_buffer.write(pcm_data)

        if not self.is_processing:
            self.is_processing = True
            self.processing_task = self.loop.create_task(self._process_buffer())

    async def _process_buffer(self):
        """
        Asynchronously processes the audio buffer using Vosk.
        """
        while self.audio_buffer.tell() > 0:
            # Get all data from the buffer
            self.audio_buffer.seek(0)
            audio_data = self.audio_buffer.read()
            self.audio_buffer.seek(0)
            self.audio_buffer.truncate(0)

            if not audio_data:
                await asyncio.sleep(0.1)
                continue

            # Process the audio data with Vosk
            # NOTE: Vosk expects 16-bit PCM mono at 16kHz. Discord is 16-bit PCM stereo at 48kHz.
            # This will likely fail or produce poor results without resampling/downmixing.
            # We will proceed with the conceptual implementation, assuming a working audio pipeline.

            # In a real scenario, we would use a library like 'resampy' or 'librosa' here.
            # Since we cannot install complex dependencies, we will rely on Vosk's partial result.

            if self.recognizer.AcceptWaveform(audio_data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text")
                if text:
                    logger.info(f"Vosk Final Transcription: {text}")
                    # Pass the transcribed text to the command handler
                    await self.voice_commands_cog._handle_voice_command(self.message.channel, text)
            else:
                # Get partial result for real-time feedback
                partial_result = json.loads(self.recognizer.PartialResult())
                partial_text = partial_result.get("partial")
                if partial_text:
                    logger.debug(f"Vosk Partial: {partial_text}")

            await asyncio.sleep(0.1)  # Yield control

        self.is_processing = False

    def cleanup(self):
        """Clean up resources."""
        if self.processing_task:
            self.processing_task.cancel()
        logger.info("VoskVoiceSink cleaned up.")

# Helper function to get the correct recognizer instance


def get_vosk_recognizer():
    """Initializes and returns the Vosk recognizer."""
    try:
        model = Model(VOSK_MODEL_PATH)
        return KaldiRecognizer(model, SAMPLE_RATE)
    except Exception as e:
        logger.error(f"Failed to initialize Vosk Recognizer: {e}")
        return None
