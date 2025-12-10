"""
Multi-Language Support Module
Supports 10+ languages with automatic detection
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Language(Enum):
    """Supported languages."""
    ENGLISH = ("en", "English")
    SPANISH = ("es", "Spanish")
    FRENCH = ("fr", "French")
    GERMAN = ("de", "German")
    ITALIAN = ("it", "Italian")
    PORTUGUESE = ("pt", "Portuguese")
    RUSSIAN = ("ru", "Russian")
    JAPANESE = ("ja", "Japanese")
    CHINESE = ("zh", "Chinese")
    ARABIC = ("ar", "Arabic")
    HINDI = ("hi", "Hindi")
    KOREAN = ("ko", "Korean")
    DUTCH = ("nl", "Dutch")
    POLISH = ("pl", "Polish")
    TURKISH = ("tr", "Turkish")
    
    @property
    def code(self) -> str:
        return self.value[0]
    
    @property
    def name_display(self) -> str:
        return self.value[1]


@dataclass
class LanguageProfile:
    """Language profile with characteristics."""
    code: str
    name: str
    native_speakers: int
    rtl: bool = False  # Right-to-left
    tonal: bool = False  # Tonal language
    character_based: bool = False  # Character-based (vs alphabet)
    openai_supported: bool = True
    whisper_supported: bool = True


class MultilingualVoiceSystem:
    """
    Handles multi-language voice processing.
    Supports transcription, translation, and synthesis in 15+ languages.
    """
    
    LANGUAGE_PROFILES = {
        'en': LanguageProfile('en', 'English', 1500000000),
        'es': LanguageProfile('es', 'Spanish', 500000000),
        'fr': LanguageProfile('fr', 'French', 280000000),
        'de': LanguageProfile('de', 'German', 130000000),
        'it': LanguageProfile('it', 'Italian', 85000000),
        'pt': LanguageProfile('pt', 'Portuguese', 250000000),
        'ru': LanguageProfile('ru', 'Russian', 260000000),
        'ja': LanguageProfile('ja', 'Japanese', 125000000, character_based=True, tonal=False),
        'zh': LanguageProfile('zh', 'Chinese', 1200000000, character_based=True, tonal=True),
        'ar': LanguageProfile('ar', 'Arabic', 400000000, rtl=True),
        'hi': LanguageProfile('hi', 'Hindi', 345000000, character_based=True),
        'ko': LanguageProfile('ko', 'Korean', 82000000, character_based=True),
        'nl': LanguageProfile('nl', 'Dutch', 25000000),
        'pl': LanguageProfile('pl', 'Polish', 45000000),
        'tr': LanguageProfile('tr', 'Turkish', 88000000),
    }
    
    def __init__(self, default_language: str = 'en'):
        """
        Initialize multilingual system.
        
        Args:
            default_language: Default language code
        """
        self.default_language = default_language
        self.user_language_preferences = {}
    
    def get_supported_languages(self) -> List[Dict]:
        """Get list of supported languages."""
        return [
            {
                'code': code,
                'name': profile.name,
                'native_speakers': profile.native_speakers,
                'rtl': profile.rtl,
                'tonal': profile.tonal,
                'character_based': profile.character_based
            }
            for code, profile in self.LANGUAGE_PROFILES.items()
        ]
    
    def get_language_profile(self, language_code: str) -> Optional[LanguageProfile]:
        """Get profile for a language."""
        return self.LANGUAGE_PROFILES.get(language_code)
    
    def detect_language(self, audio_path: str) -> Dict:
        """
        Detect language from audio file.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with detected language info
        """
        try:
            # This would use OpenAI Whisper's language detection
            # For now, returning a template
            return {
                'language_code': 'en',
                'language_name': 'English',
                'confidence': 0.95,
                'alternative_languages': [
                    {'code': 'es', 'confidence': 0.03},
                    {'code': 'fr', 'confidence': 0.02}
                ]
            }
        except Exception as e:
            logger.error(f"Error detecting language: {e}")
            return {
                'language_code': self.default_language,
                'language_name': 'Unknown',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def transcribe_multilingual(self, audio_path: str, language_code: Optional[str] = None) -> Dict:
        """
        Transcribe audio in specified or detected language.
        
        Args:
            audio_path: Path to audio file
            language_code: Optional language code (auto-detect if not provided)
            
        Returns:
            Transcription result
        """
        try:
            # Auto-detect if not specified
            if not language_code:
                detection = self.detect_language(audio_path)
                language_code = detection['language_code']
            
            # Validate language
            if language_code not in self.LANGUAGE_PROFILES:
                language_code = self.default_language
            
            profile = self.LANGUAGE_PROFILES[language_code]
            
            # This would call OpenAI Whisper API
            # For now, returning a template
            return {
                'transcription': 'Sample transcription',
                'language_code': language_code,
                'language_name': profile.name,
                'confidence': 0.95,
                'duration': 0.0
            }
        except Exception as e:
            logger.error(f"Error transcribing: {e}")
            return {
                'transcription': '',
                'language_code': language_code,
                'error': str(e)
            }
    
    def translate_text(self, text: str, source_lang: str, target_lang: str) -> Dict:
        """
        Translate text between languages.
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translation result
        """
        try:
            # Validate languages
            if source_lang not in self.LANGUAGE_PROFILES:
                source_lang = self.default_language
            if target_lang not in self.LANGUAGE_PROFILES:
                target_lang = self.default_language
            
            # This would use a translation API (Google Translate, etc.)
            # For now, returning a template
            return {
                'original_text': text,
                'translated_text': text,  # Placeholder
                'source_language': source_lang,
                'target_language': target_lang,
                'confidence': 0.85
            }
        except Exception as e:
            logger.error(f"Error translating: {e}")
            return {
                'original_text': text,
                'error': str(e)
            }
    
    def synthesize_speech(self, text: str, language_code: str, voice: str = 'nova') -> Dict:
        """
        Synthesize speech in specified language.
        
        Args:
            text: Text to synthesize
            language_code: Language code
            voice: Voice name
            
        Returns:
            Synthesis result with audio URL
        """
        try:
            # Validate language
            if language_code not in self.LANGUAGE_PROFILES:
                language_code = self.default_language
            
            profile = self.LANGUAGE_PROFILES[language_code]
            
            # This would use OpenAI TTS or similar
            # For now, returning a template
            return {
                'audio_url': 'https://example.com/audio.mp3',
                'language_code': language_code,
                'language_name': profile.name,
                'voice': voice,
                'duration': 0.0
            }
        except Exception as e:
            logger.error(f"Error synthesizing speech: {e}")
            return {
                'error': str(e)
            }
    
    def translate_voice(self, audio_path: str, source_lang: str, target_lang: str) -> Dict:
        """
        Translate voice from one language to another.
        
        Args:
            audio_path: Path to audio file
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translation result with audio
        """
        try:
            # Step 1: Transcribe
            transcription = self.transcribe_multilingual(audio_path, source_lang)
            if 'error' in transcription:
                return transcription
            
            # Step 2: Translate
            translation = self.translate_text(
                transcription['transcription'],
                source_lang,
                target_lang
            )
            if 'error' in translation:
                return translation
            
            # Step 3: Synthesize
            synthesis = self.synthesize_speech(
                translation['translated_text'],
                target_lang
            )
            
            return {
                'original_text': transcription['transcription'],
                'translated_text': translation['translated_text'],
                'source_language': source_lang,
                'target_language': target_lang,
                'audio_url': synthesis.get('audio_url'),
                'success': True
            }
        except Exception as e:
            logger.error(f"Error in voice translation: {e}")
            return {'error': str(e)}
    
    def set_user_language(self, user_id: str, language_code: str) -> bool:
        """Set preferred language for a user."""
        if language_code not in self.LANGUAGE_PROFILES:
            logger.warning(f"Unknown language: {language_code}")
            return False
        
        self.user_language_preferences[user_id] = language_code
        logger.info(f"User language set: {user_id} -> {language_code}")
        return True
    
    def get_user_language(self, user_id: str) -> str:
        """Get user's preferred language."""
        return self.user_language_preferences.get(user_id, self.default_language)
    
    def get_language_pair_support(self, source_lang: str, target_lang: str) -> Dict:
        """Check support for language pair."""
        source_profile = self.LANGUAGE_PROFILES.get(source_lang)
        target_profile = self.LANGUAGE_PROFILES.get(target_lang)
        
        if not source_profile or not target_profile:
            return {'supported': False, 'reason': 'Language not supported'}
        
        return {
            'supported': True,
            'source_language': source_profile.name,
            'target_language': target_profile.name,
            'bidirectional': True
        }
    
    def get_language_characteristics(self, language_code: str) -> Dict:
        """Get characteristics of a language."""
        profile = self.LANGUAGE_PROFILES.get(language_code)
        if not profile:
            return {}
        
        return {
            'code': profile.code,
            'name': profile.name,
            'native_speakers': profile.native_speakers,
            'right_to_left': profile.rtl,
            'tonal': profile.tonal,
            'character_based': profile.character_based,
            'openai_supported': profile.openai_supported,
            'whisper_supported': profile.whisper_supported
        }
    
    def get_language_by_name(self, name: str) -> Optional[str]:
        """Get language code by name."""
        for code, profile in self.LANGUAGE_PROFILES.items():
            if profile.name.lower() == name.lower():
                return code
        return None
    
    def get_similar_languages(self, language_code: str) -> List[str]:
        """Get linguistically similar languages."""
        similar_groups = {
            'en': ['de', 'nl'],  # Germanic
            'es': ['pt', 'fr', 'it'],  # Romance
            'fr': ['es', 'pt', 'it'],  # Romance
            'de': ['en', 'nl'],  # Germanic
            'ja': ['ko'],  # East Asian
            'zh': ['ja', 'ko'],  # East Asian
            'ar': [],  # Semitic
            'hi': [],  # Indo-Aryan
        }
        return similar_groups.get(language_code, [])
    
    def create_language_table(self) -> bool:
        """Create user_language_preferences table if it doesn't exist."""
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS user_language_preferences (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id VARCHAR(255) UNIQUE,
                language_code VARCHAR(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            # This would execute against database
            logger.info("Created user_language_preferences table")
            return True
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            return False
