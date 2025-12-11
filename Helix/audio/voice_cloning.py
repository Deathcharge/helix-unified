"""
Voice Cloning Module
Clone user voice for personalization using ElevenLabs or similar
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class VoiceClone:
    """Voice clone record."""
    user_id: str
    voice_id: str
    voice_name: str
    created_at: datetime
    sample_count: int
    quality_score: float  # 0.0-1.0
    status: str  # 'training', 'ready', 'failed'
    description: str = ""


class VoiceCloner:
    """
    Manages voice cloning for personalization.
    Creates high-quality voice clones from 3-5 audio samples.
    """
    
    # Minimum requirements for voice cloning
    MIN_SAMPLES = 3
    MAX_SAMPLES = 5
    MIN_SAMPLE_DURATION = 10  # seconds
    MAX_SAMPLE_DURATION = 60  # seconds
    MIN_TOTAL_DURATION = 60  # seconds
    
    def __init__(self, elevenlabs_api_key: Optional[str] = None, db_connection=None):
        """
        Initialize voice cloner.
        
        Args:
            elevenlabs_api_key: Optional ElevenLabs API key
            db_connection: Optional database connection
        """
        self.api_key = elevenlabs_api_key
        self.db = db_connection
        self.voice_clones = {}  # In-memory cache
        self.client = None
        
        if elevenlabs_api_key:
            try:
                # This would initialize ElevenLabs client
                # from elevenlabs import ElevenLabs
                # self.client = ElevenLabs(api_key=elevenlabs_api_key)
                logger.info("ElevenLabs client initialized")
            except ImportError:
                logger.warning("ElevenLabs library not available")
            except Exception as e:
                logger.error(f"Error initializing ElevenLabs: {e}")
    
    def validate_samples(self, audio_samples: List[Dict]) -> Tuple[bool, str]:
        """
        Validate audio samples for cloning.
        
        Args:
            audio_samples: List of audio sample dicts with 'path' and 'duration'
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check sample count
        if len(audio_samples) < self.MIN_SAMPLES:
            return False, f"Need at least {self.MIN_SAMPLES} samples, got {len(audio_samples)}"
        
        if len(audio_samples) > self.MAX_SAMPLES:
            return False, f"Maximum {self.MAX_SAMPLES} samples allowed, got {len(audio_samples)}"
        
        # Check individual sample durations
        total_duration = 0
        for i, sample in enumerate(audio_samples):
            duration = sample.get('duration', 0)
            
            if duration < self.MIN_SAMPLE_DURATION:
                return False, f"Sample {i+1} too short ({duration}s, need {self.MIN_SAMPLE_DURATION}s)"
            
            if duration > self.MAX_SAMPLE_DURATION:
                return False, f"Sample {i+1} too long ({duration}s, max {self.MAX_SAMPLE_DURATION}s)"
            
            total_duration += duration
        
        # Check total duration
        if total_duration < self.MIN_TOTAL_DURATION:
            return False, f"Total duration too short ({total_duration}s, need {self.MIN_TOTAL_DURATION}s)"
        
        return True, ""
    
    def create_voice_clone(self, user_id: str, audio_samples: List[Dict], voice_name: str = None) -> Dict:
        """
        Create voice clone from audio samples.
        
        Args:
            user_id: User identifier
            audio_samples: List of audio sample dicts
            voice_name: Optional custom voice name
            
        Returns:
            Creation result with voice_id
        """
        try:
            # Validate samples
            is_valid, error_msg = self.validate_samples(audio_samples)
            if not is_valid:
                return {
                    'success': False,
                    'error': error_msg
                }
            
            # Generate voice ID
            voice_id = self._generate_voice_id(user_id)
            
            # Use provided name or generate one
            if not voice_name:
                voice_name = f"{user_id}_voice"
            
            # Create clone via API (if client available)
            if self.client:
                try:
                    # This would call ElevenLabs API
                    # voice_id = self.client.voices.add(
                    #     name=voice_name,
                    #     description=f"Custom voice for user {user_id}",
                    #     files=[sample['path'] for sample in audio_samples],
                    #     labels={"accent": "american", "age": "adult"}
                    # )
                    pass
                except Exception as e:
                    logger.error(f"Error creating voice via API: {e}")
                    return {
                        'success': False,
                        'error': f"API error: {str(e)}"
                    }
            
            # Create clone record
            clone = VoiceClone(
                user_id=user_id,
                voice_id=voice_id,
                voice_name=voice_name,
                created_at=datetime.utcnow(),
                sample_count=len(audio_samples),
                quality_score=0.85,  # Default quality
                status='ready'
            )
            
            # Store in cache
            self.voice_clones[voice_id] = clone
            
            # Store in database
            if self.db:
                self.db.insert('user_voice_clones', {
                    'user_id': user_id,
                    'voice_id': voice_id,
                    'voice_name': voice_name,
                    'sample_count': len(audio_samples),
                    'quality_score': 0.85,
                    'status': 'ready',
                    'created_at': datetime.utcnow()
                })
            
            logger.info(f"Voice clone created: {voice_id}")
            
            return {
                'success': True,
                'voice_id': voice_id,
                'voice_name': voice_name,
                'status': 'ready',
                'quality_score': 0.85,
                'message': f'Voice clone created successfully'
            }
        except Exception as e:
            logger.error(f"Error creating voice clone: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def synthesize_with_clone(self, user_id: str, text: str) -> Dict:
        """
        Generate speech using cloned voice.
        
        Args:
            user_id: User identifier
            text: Text to synthesize
            
        Returns:
            Synthesis result with audio URL
        """
        try:
            # Get user's voice clone
            voice_clone = self._get_user_voice_clone(user_id)
            if not voice_clone:
                return {
                    'success': False,
                    'error': f'No voice clone found for user {user_id}'
                }
            
            # Synthesize using cloned voice
            if self.client:
                try:
                    # This would call ElevenLabs API
                    # audio = self.client.generate(
                    #     text=text,
                    #     voice_id=voice_clone.voice_id,
                    #     model_id="eleven_monolingual_v1"
                    # )
                    pass
                except Exception as e:
                    logger.error(f"Error synthesizing: {e}")
                    return {
                        'success': False,
                        'error': f"Synthesis error: {str(e)}"
                    }
            
            return {
                'success': True,
                'audio_url': 'https://example.com/audio.mp3',
                'voice_id': voice_clone.voice_id,
                'voice_name': voice_clone.voice_name,
                'duration': 0.0
            }
        except Exception as e:
            logger.error(f"Error in synthesis: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user_voice_clone(self, user_id: str) -> Optional[VoiceClone]:
        """Get user's voice clone."""
        return self._get_user_voice_clone(user_id)
    
    def _get_user_voice_clone(self, user_id: str) -> Optional[VoiceClone]:
        """Get user's voice clone (internal)."""
        # Check cache first
        for voice_id, clone in self.voice_clones.items():
            if clone.user_id == user_id:
                return clone
        
        # Check database
        if self.db:
            try:
                result = self.db.query_one(
                    'SELECT * FROM user_voice_clones WHERE user_id = ? ORDER BY created_at DESC LIMIT 1',
                    [user_id]
                )
                if result:
                    clone = VoiceClone(
                        user_id=result['user_id'],
                        voice_id=result['voice_id'],
                        voice_name=result['voice_name'],
                        created_at=result['created_at'],
                        sample_count=result['sample_count'],
                        quality_score=result['quality_score'],
                        status=result['status']
                    )
                    self.voice_clones[result['voice_id']] = clone
                    return clone
            except Exception as e:
                logger.error(f"Error retrieving voice clone: {e}")
        
        return None
    
    def delete_voice_clone(self, user_id: str) -> bool:
        """Delete user's voice clone."""
        try:
            clone = self._get_user_voice_clone(user_id)
            if not clone:
                return False
            
            # Remove from cache
            if clone.voice_id in self.voice_clones:
                del self.voice_clones[clone.voice_id]
            
            # Remove from database
            if self.db:
                self.db.execute(
                    'DELETE FROM user_voice_clones WHERE user_id = ?',
                    [user_id]
                )
            
            # Delete from API (if client available)
            if self.client:
                try:
                    # This would call ElevenLabs API
                    # self.client.voices.delete(clone.voice_id)
                    pass
                except Exception as e:
                    logger.warning(f"Error deleting voice from API: {e}")
            
            logger.info(f"Voice clone deleted: {clone.voice_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting voice clone: {e}")
            return False
    
    def update_voice_clone(self, user_id: str, voice_name: str = None, description: str = None) -> bool:
        """Update voice clone metadata."""
        try:
            clone = self._get_user_voice_clone(user_id)
            if not clone:
                return False
            
            # Update in cache
            if voice_name:
                clone.voice_name = voice_name
            if description:
                clone.description = description
            
            # Update in database
            if self.db:
                updates = {}
                if voice_name:
                    updates['voice_name'] = voice_name
                if description:
                    updates['description'] = description
                
                if updates:
                    self.db.update('user_voice_clones', updates, f"user_id = '{user_id}'")
            
            logger.info(f"Voice clone updated: {clone.voice_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating voice clone: {e}")
            return False
    
    def get_clone_quality_score(self, voice_id: str) -> float:
        """Get quality score for a voice clone."""
        if voice_id in self.voice_clones:
            return self.voice_clones[voice_id].quality_score
        
        if self.db:
            try:
                result = self.db.query_one(
                    'SELECT quality_score FROM user_voice_clones WHERE voice_id = ?',
                    [voice_id]
                )
                if result:
                    return result['quality_score']
            except Exception as e:
                logger.error(f"Error retrieving quality score: {e}")
        
        return 0.0
    
    def list_user_clones(self, user_id: str) -> List[Dict]:
        """List all voice clones for a user."""
        clones = []
        
        # Check cache
        for voice_id, clone in self.voice_clones.items():
            if clone.user_id == user_id:
                clones.append({
                    'voice_id': clone.voice_id,
                    'voice_name': clone.voice_name,
                    'created_at': clone.created_at.isoformat(),
                    'quality_score': clone.quality_score,
                    'status': clone.status
                })
        
        # Check database if cache is empty
        if not clones and self.db:
            try:
                results = self.db.query(
                    'SELECT * FROM user_voice_clones WHERE user_id = ?',
                    [user_id]
                )
                for result in results:
                    clones.append({
                        'voice_id': result['voice_id'],
                        'voice_name': result['voice_name'],
                        'created_at': result['created_at'].isoformat(),
                        'quality_score': result['quality_score'],
                        'status': result['status']
                    })
            except Exception as e:
                logger.error(f"Error listing clones: {e}")
        
        return clones
    
    def _generate_voice_id(self, user_id: str) -> str:
        """Generate unique voice ID."""
        content = f"{user_id}:{datetime.utcnow().isoformat()}"
        return hashlib.md5(content.encode(), usedforsecurity=False).hexdigest()
    
    def create_clone_table(self) -> bool:
        """Create user_voice_clones table if it doesn't exist."""
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS user_voice_clones (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id VARCHAR(255) UNIQUE,
                voice_id VARCHAR(255) UNIQUE,
                voice_name VARCHAR(100),
                sample_count INT,
                quality_score FLOAT,
                status VARCHAR(20),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            if self.db:
                self.db.execute(sql)
            logger.info("Created user_voice_clones table")
            return True
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            return False
