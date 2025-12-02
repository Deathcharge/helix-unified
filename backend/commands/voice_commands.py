import os
import asyncio
import discord
from discord.ext import commands
from loguru import logger
from vosk import Model, KaldiRecognizer
from backend.tts_service import tts_service, get_agent_voice  # Import the new TTS service
from backend.voice_sink import VoskVoiceSink, get_vosk_recognizer

# --- CONFIGURATION ---
# Path to the downloaded Vosk model
VOSK_MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vosk-model")
# Discord audio settings (48kHz, 2 channels, 16-bit PCM)
SAMPLE_RATE = 16000  # Vosk model typically uses 16kHz
CHANNELS = 1  # Discord sends stereo, but we'll process as mono
CHUNK_SIZE = 8192  # Size of audio chunk to process


class VoiceCommands(commands.Cog):
    """
    Commands for managing Discord voice connections and real-time STT.
    """

    def __init__(self, bot):
        self.bot = bot
        self.recognizer = None
        self.model = None
        self.voice_clients = {}  # Store active voice clients

        # Load Vosk model asynchronously
        asyncio.create_task(self._load_vosk_model())

    async def _load_vosk_model(self):
        """Loads the Vosk model into memory."""
        try:
            logger.info(f"Loading Vosk model from {VOSK_MODEL_PATH}...")
            self.model = Model(VOSK_MODEL_PATH)
            self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)
            logger.info("✅ Vosk model loaded successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to load Vosk model: {e}")
            self.model = None
            self.recognizer = None

    @commands.command(name="join", help="Joins the voice channel you are in and starts listening.")
    async def join_voice(self, ctx: commands.Context):
        """Joins the voice channel of the user who invoked the command."""
        if not ctx.author.voice:
            return await ctx.send("❌ You are not connected to a voice channel.")

        channel = ctx.author.voice.channel
        if ctx.voice_client:
            if ctx.voice_client.channel == channel:
                return await ctx.send("✅ Already connected to this channel.")
            await ctx.voice_client.move_to(channel)
        else:
            try:
                voice_client = await channel.connect()
                self.voice_clients[ctx.guild.id] = voice_client

                # Start listening with the custom sink
                recognizer = get_vosk_recognizer()
                if recognizer:
                    voice_client.start_listening(VoskVoiceSink(recognizer, self))
                    await self.speak(
                        voice_client, "Helix Collective voice bridge established. Real-time transcription is active."
                    )  # noqa
                else:
                    await ctx.send("❌ Vosk model failed to load. Cannot start transcription.")
                    await voice_client.disconnect()
                    return

            except asyncio.TimeoutError:
                return await ctx.send("❌ Connection timed out.")
            except discord.ClientException:
                return await ctx.send("❌ Already connected to a voice channel in this guild.")
            except Exception as e:
                logger.error(f"Error joining voice channel: {e}")
                return await ctx.send(f"❌ An error occurred: {e}")

            except asyncio.TimeoutError:
                return await ctx.send("❌ Connection timed out.")
            except discord.ClientException:
                return await ctx.send("❌ Already connected to a voice channel in this guild.")
            except Exception as e:
                logger.error(f"Error joining voice channel: {e}")
                return await ctx.send(f"❌ An error occurred: {e}")

    @commands.command(name="leave", help="Leaves the current voice channel.")
    async def leave_voice(self, ctx: commands.Context):
        """Leaves the voice channel."""
        if ctx.guild.id in self.voice_clients:
            voice_client = self.voice_clients.pop(ctx.guild.id)
            voice_client.stop_listening()  # Stop the custom sink
            await self.speak(voice_client, "Voice bridge terminated. Tat Tvam Asi.")
            await voice_client.disconnect()
            await ctx.send("🔇 Disconnected from voice channel.")
        else:
            await ctx.send("❌ Not connected to a voice channel in this guild.")

    # The voice processing is now handled by the VoskVoiceSink.
    # This placeholder function is no longer needed.

    async def _handle_voice_command(self, channel: discord.VoiceChannel, text: str):
        """Handles the transcribed text as a potential command or query."""

        # 1. Clean and Normalize Text
        normalized_text = text.lower().strip()

        # 2. Identify Target (e.g., "manus status" or "helix collective status")
        # Check for common wake words: "manus", "helix", "collective"
        wake_words = ["manus", "helix", "collective"]
        is_command = False
        for word in wake_words:
            if normalized_text.startswith(word):
                # Remove the wake word and any leading/trailing whitespace
                command_string = normalized_text[len(word) :].strip()  # noqa: E203
                is_command = True
                break

        if not is_command:
            logger.debug(f"Voice: No wake word found in '{normalized_text}'")
            return

        # 3. Parse Command (Prepend the bot's command prefix '!')
        # The bot's command handler expects the prefix.
        full_command = f"!{command_string}"

        # 4. Execute Command
        # Create a mock message object to pass to the bot's command processor
        # This is a common pattern for executing commands programmatically.
        mock_message = type(
            'MockMessage',
            (object,),
            {
                'content': full_command,
                'author': self.bot.user,  # Execute as the bot itself
                'channel': channel,
                'guild': channel.guild,
                'clean_content': full_command,
            },
        )()

        # Create a mock context object
        ctx = await self.bot.get_context(mock_message)

        if ctx.command:
            logger.info(f"Voice: Executing command '{full_command}' from voice.")

            # Use a try/except block to catch command errors
            try:
                # Execute the command
                await self.bot.invoke(ctx)

                # 5. Respond (Voice Response)
                # For simplicity, we will have a generic success response.
                # A more advanced implementation would parse the command output.
                await self.speak(ctx.voice_client, f"Command {ctx.command.name} executed. Tat Tvam Asi.")
  # noqa
            except Exception as e:
                logger.error(f"Voice: Error executing command '{full_command}': {e}")
                await self.speak(
                    ctx.voice_client, f"Error. Command {ctx.command.name} failed. Please check the text channel for details."
                )
        else:
            logger.warning(f"Voice: Command not found for '{full_command}'")
            await self.speak(ctx.voice_client, "Command not recognized. Please try again.")

    async def speak(self, voice_client: discord.VoiceClient, text: str, agent_name: str = "Manus"):
        """
        Generates speech from text and plays it in the voice channel.
        """
        if not tts_service.client:
            logger.warning("TTS service not initialized. Cannot speak.")
            return

        voice = await get_agent_voice(agent_name)
        audio_stream = await tts_service.generate_speech(text, voice)

        if audio_stream:
            try:
                # discord.py requires an FFmpeg-compatible source
                source = discord.FFmpegPCMAudio(audio_stream, pipe=True)
                voice_client.play(source, after=lambda e: logger.error(f'Player error: {e}') if e else None)

                # Wait for the audio to finish playing
                while voice_client.is_playing():
                    await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Error playing audio in voice channel: {e}")
        else:
            logger.error("Failed to generate audio stream.")


def setup(bot):
    """Setup function to add the cog to the bot."""
    bot.add_cog(VoiceCommands(bot))
    logger.info("✅ VoiceCommands cog loaded.")
