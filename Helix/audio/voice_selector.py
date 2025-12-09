"""
Agent Voice Selector Module
Allows users to choose and customize agent voices
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class VoiceProfile:
    """Voice profile configuration."""
    name: str
    openai_voice: str
    personality: str
    traits: List[str]
    speech_rate: float = 1.0
    pitch_shift: int = 0
    description: str = ""


class VoiceSelector:
    """
    Manages voice selection for agents.
    Supports 6 OpenAI voices with customization options.
    """
    
    # Available voices with characteristics
    AVAILABLE_VOICES = {
        'echo': VoiceProfile(
            name='echo',
            openai_voice='echo',
            personality='technical',
            traits=['precise', 'analytical', 'professional'],
            speech_rate=1.0,
            pitch_shift=0,
            description='Technical and precise voice, ideal for data-driven tasks'
        ),
        'sage': VoiceProfile(
            name='sage',
            openai_voice='sage',
            personality='wise',
            traits=['thoughtful', 'patient', 'contemplative'],
            speech_rate=0.9,
            pitch_shift=-2,
            description='Wise and thoughtful voice, great for guidance'
        ),
        'nova': VoiceProfile(
            name='nova',
            openai_voice='nova',
            personality='energetic',
            traits=['enthusiastic', 'optimistic', 'engaging'],
            speech_rate=1.2,
            pitch_shift=3,
            description='Energetic and upbeat voice, perfect for motivation'
        ),
        'onyx': VoiceProfile(
            name='onyx',
            openai_voice='onyx',
            personality='deep',
            traits=['authoritative', 'calm', 'grounded'],
            speech_rate=0.95,
            pitch_shift=-3,
            description='Deep and authoritative voice, ideal for serious topics'
        ),
        'shimmer': VoiceProfile(
            name='shimmer',
            openai_voice='shimmer',
            personality='bright',
            traits=['cheerful', 'friendly', 'approachable'],
            speech_rate=1.1,
            pitch_shift=2,
            description='Bright and friendly voice, great for customer interaction'
        ),
        'alloy': VoiceProfile(
            name='alloy',
            openai_voice='alloy',
            personality='friendly',
            traits=['warm', 'supportive', 'empathetic'],
            speech_rate=1.0,
            pitch_shift=1,
            description='Warm and supportive voice, ideal for assistance'
        )
    }
    
    def __init__(self, database_connection=None):
        """
        Initialize voice selector.
        
        Args:
            database_connection: Optional database connection for persistence
        """
        self.db = database_connection
        self.user_preferences = {}  # In-memory cache
    
    def get_available_voices(self) -> Dict[str, VoiceProfile]:
        """Get all available voices."""
        return self.AVAILABLE_VOICES.copy()
    
    def get_voice_details(self, voice_name: str) -> Optional[VoiceProfile]:
        """Get details for a specific voice."""
        return self.AVAILABLE_VOICES.get(voice_name)
    
    def get_agent_voice(self, user_id: str, agent_name: str) -> VoiceProfile:
        """
        Get preferred voice for an agent.
        
        Args:
            user_id: User identifier
            agent_name: Agent name
            
        Returns:
            VoiceProfile for the agent
        """
        # Check cache first
        cache_key = f"{user_id}:{agent_name}"
        if cache_key in self.user_preferences:
            voice_name = self.user_preferences[cache_key]
            return self.AVAILABLE_VOICES.get(voice_name, self.AVAILABLE_VOICES['echo'])
        
        # Check database
        if self.db:
            try:
                preference = self.db.get_user_voice_preference(user_id, agent_name)
                if preference:
                    voice_name = preference.get('voice_name', 'echo')
                    self.user_preferences[cache_key] = voice_name
                    return self.AVAILABLE_VOICES.get(voice_name, self.AVAILABLE_VOICES['echo'])
            except Exception as e:
                logger.error(f"Error fetching voice preference: {e}")
        
        # Default to echo
        return self.AVAILABLE_VOICES['echo']
    
    def set_agent_voice(self, user_id: str, agent_name: str, voice_name: str) -> bool:
        """
        Set preferred voice for an agent.
        
        Args:
            user_id: User identifier
            agent_name: Agent name
            voice_name: Voice name (must be in AVAILABLE_VOICES)
            
        Returns:
            True if successful, False otherwise
        """
        if voice_name not in self.AVAILABLE_VOICES:
            logger.warning(f"Unknown voice: {voice_name}")
            return False
        
        try:
            # Update cache
            cache_key = f"{user_id}:{agent_name}"
            self.user_preferences[cache_key] = voice_name
            
            # Update database
            if self.db:
                self.db.save_user_voice_preference(
                    user_id=user_id,
                    agent_name=agent_name,
                    voice_name=voice_name,
                    updated_at=datetime.utcnow()
                )
            
            logger.info(f"Voice preference set: {user_id} -> {agent_name} = {voice_name}")
            return True
        except Exception as e:
            logger.error(f"Error setting voice preference: {e}")
            return False
    
    def get_user_voice_preferences(self, user_id: str) -> Dict[str, str]:
        """
        Get all voice preferences for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dict mapping agent names to voice names
        """
        preferences = {}
        
        if self.db:
            try:
                user_prefs = self.db.get_user_voice_preferences(user_id)
                for pref in user_prefs:
                    preferences[pref['agent_name']] = pref['voice_name']
            except Exception as e:
                logger.error(f"Error fetching user preferences: {e}")
        
        return preferences
    
    def reset_user_preferences(self, user_id: str) -> bool:
        """
        Reset all voice preferences for a user to defaults.
        
        Args:
            user_id: User identifier
            
        Returns:
            True if successful
        """
        try:
            # Clear cache
            keys_to_delete = [k for k in self.user_preferences if k.startswith(f"{user_id}:")]
            for key in keys_to_delete:
                del self.user_preferences[key]
            
            # Clear database
            if self.db:
                self.db.reset_user_voice_preferences(user_id)
            
            logger.info(f"Voice preferences reset for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error resetting preferences: {e}")
            return False
    
    def get_voice_by_personality(self, personality_type: str) -> Optional[VoiceProfile]:
        """
        Get a voice by personality type.
        
        Args:
            personality_type: Personality type (e.g., 'technical', 'wise', 'energetic')
            
        Returns:
            VoiceProfile matching the personality
        """
        for voice in self.AVAILABLE_VOICES.values():
            if voice.personality == personality_type:
                return voice
        
        return None
    
    def get_voices_by_trait(self, trait: str) -> List[VoiceProfile]:
        """
        Get voices that have a specific trait.
        
        Args:
            trait: Trait name
            
        Returns:
            List of VoiceProfiles with the trait
        """
        matching_voices = []
        for voice in self.AVAILABLE_VOICES.values():
            if trait in voice.traits:
                matching_voices.append(voice)
        
        return matching_voices
    
    def get_voice_recommendations(self, use_case: str) -> List[VoiceProfile]:
        """
        Get voice recommendations for a specific use case.
        
        Args:
            use_case: Use case type (e.g., 'customer_support', 'technical_help', 'creative')
            
        Returns:
            List of recommended VoiceProfiles
        """
        recommendations = {
            'customer_support': ['shimmer', 'alloy', 'nova'],
            'technical_help': ['echo', 'sage', 'onyx'],
            'creative': ['nova', 'shimmer', 'sage'],
            'serious': ['onyx', 'echo', 'sage'],
            'friendly': ['alloy', 'shimmer', 'nova'],
            'professional': ['echo', 'onyx', 'sage']
        }
        
        voice_names = recommendations.get(use_case, ['echo'])
        return [self.AVAILABLE_VOICES[name] for name in voice_names if name in self.AVAILABLE_VOICES]


class VoicePreferenceManager:
    """Manages voice preferences with database persistence."""
    
    def __init__(self, db_connection):
        """Initialize preference manager."""
        self.db = db_connection
        self.selector = VoiceSelector(db_connection)
    
    def create_preference_table(self) -> bool:
        """Create user_voice_preferences table if it doesn't exist."""
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS user_voice_preferences (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id VARCHAR(255) NOT NULL,
                agent_name VARCHAR(100) NOT NULL,
                voice_name VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_user_agent_voice (user_id, agent_name)
            )
            """
            self.db.execute(sql)
            logger.info("Created user_voice_preferences table")
            return True
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            return False
    
    def export_preferences(self, user_id: str, format: str = 'json') -> Dict:
        """
        Export user voice preferences.
        
        Args:
            user_id: User identifier
            format: Export format ('json' or 'csv')
            
        Returns:
            Exported preferences
        """
        preferences = self.selector.get_user_voice_preferences(user_id)
        
        if format == 'json':
            return {
                'user_id': user_id,
                'preferences': preferences,
                'exported_at': datetime.utcnow().isoformat()
            }
        
        return preferences
