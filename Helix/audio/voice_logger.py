"""
Voice Message Logger Module
Stores all voice transcriptions for audit trail and analysis
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class VoiceMessage:
    """Voice message record."""
    user_id: str
    agent_name: str
    transcription: str
    audio_url: str
    duration: float
    confidence: float
    language: str = 'en'
    sentiment: Optional[str] = None
    timestamp: Optional[datetime] = None
    message_id: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class VoiceMessageLogger:
    """
    Logs and manages voice messages.
    Provides audit trail, search, and export functionality.
    """
    
    def __init__(self, database_connection=None):
        """
        Initialize voice message logger.
        
        Args:
            database_connection: Optional database connection for persistence
        """
        self.db = database_connection
        self.message_cache = {}  # In-memory cache
    
    def log_message(self, message: VoiceMessage) -> Optional[str]:
        """
        Log a voice message.
        
        Args:
            message: VoiceMessage object
            
        Returns:
            Message ID if successful, None otherwise
        """
        try:
            # Generate message ID
            message_id = self._generate_message_id(message.user_id, message.timestamp)
            message.message_id = message_id
            
            # Store in cache
            self.message_cache[message_id] = message
            
            # Store in database
            if self.db:
                self.db.insert('voice_messages', {
                    'message_id': message_id,
                    'user_id': message.user_id,
                    'agent_name': message.agent_name,
                    'transcription': message.transcription,
                    'audio_url': message.audio_url,
                    'duration': message.duration,
                    'confidence': message.confidence,
                    'language': message.language,
                    'sentiment': message.sentiment,
                    'timestamp': message.timestamp,
                    'created_at': datetime.utcnow()
                })
            
            logger.info(f"Voice message logged: {message_id}")
            return message_id
        except Exception as e:
            logger.error(f"Error logging voice message: {e}")
            return None
    
    def get_message(self, message_id: str) -> Optional[VoiceMessage]:
        """
        Get a voice message by ID.
        
        Args:
            message_id: Message identifier
            
        Returns:
            VoiceMessage if found, None otherwise
        """
        # Check cache first
        if message_id in self.message_cache:
            return self.message_cache[message_id]
        
        # Check database
        if self.db:
            try:
                result = self.db.query_one(
                    'SELECT * FROM voice_messages WHERE message_id = ?',
                    [message_id]
                )
                if result:
                    return self._dict_to_message(result)
            except Exception as e:
                logger.error(f"Error retrieving message: {e}")
        
        return None
    
    def get_user_messages(self, user_id: str, limit: int = 100, offset: int = 0) -> List[VoiceMessage]:
        """
        Get all messages for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of messages to return
            offset: Offset for pagination
            
        Returns:
            List of VoiceMessage objects
        """
        if not self.db:
            return []
        
        try:
            results = self.db.query(
                'SELECT * FROM voice_messages WHERE user_id = ? ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                [user_id, limit, offset]
            )
            return [self._dict_to_message(r) for r in results]
        except Exception as e:
            logger.error(f"Error retrieving user messages: {e}")
            return []
    
    def get_agent_messages(self, user_id: str, agent_name: str, limit: int = 100) -> List[VoiceMessage]:
        """
        Get all messages for a specific agent.
        
        Args:
            user_id: User identifier
            agent_name: Agent name
            limit: Maximum number of messages
            
        Returns:
            List of VoiceMessage objects
        """
        if not self.db:
            return []
        
        try:
            results = self.db.query(
                'SELECT * FROM voice_messages WHERE user_id = ? AND agent_name = ? ORDER BY timestamp DESC LIMIT ?',
                [user_id, agent_name, limit]
            )
            return [self._dict_to_message(r) for r in results]
        except Exception as e:
            logger.error(f"Error retrieving agent messages: {e}")
            return []
    
    def search_messages(self, user_id: str, query: str, limit: int = 50) -> List[VoiceMessage]:
        """
        Search voice messages by transcription content.
        
        Args:
            user_id: User identifier
            query: Search query
            limit: Maximum results
            
        Returns:
            List of matching VoiceMessage objects
        """
        if not self.db:
            return []
        
        try:
            results = self.db.query(
                'SELECT * FROM voice_messages WHERE user_id = ? AND transcription LIKE ? ORDER BY timestamp DESC LIMIT ?',
                [user_id, f'%{query}%', limit]
            )
            return [self._dict_to_message(r) for r in results]
        except Exception as e:
            logger.error(f"Error searching messages: {e}")
            return []
    
    def get_messages_by_date_range(self, user_id: str, start_date: datetime, end_date: datetime) -> List[VoiceMessage]:
        """
        Get messages within a date range.
        
        Args:
            user_id: User identifier
            start_date: Start date
            end_date: End date
            
        Returns:
            List of VoiceMessage objects
        """
        if not self.db:
            return []
        
        try:
            results = self.db.query(
                'SELECT * FROM voice_messages WHERE user_id = ? AND timestamp BETWEEN ? AND ? ORDER BY timestamp DESC',
                [user_id, start_date, end_date]
            )
            return [self._dict_to_message(r) for r in results]
        except Exception as e:
            logger.error(f"Error retrieving messages by date: {e}")
            return []
    
    def get_messages_by_sentiment(self, user_id: str, sentiment: str) -> List[VoiceMessage]:
        """
        Get messages by sentiment.
        
        Args:
            user_id: User identifier
            sentiment: Sentiment type (e.g., 'positive', 'negative', 'neutral')
            
        Returns:
            List of VoiceMessage objects
        """
        if not self.db:
            return []
        
        try:
            results = self.db.query(
                'SELECT * FROM voice_messages WHERE user_id = ? AND sentiment = ? ORDER BY timestamp DESC',
                [user_id, sentiment]
            )
            return [self._dict_to_message(r) for r in results]
        except Exception as e:
            logger.error(f"Error retrieving messages by sentiment: {e}")
            return []
    
    def delete_message(self, message_id: str, user_id: str) -> bool:
        """
        Delete a voice message (GDPR compliance).
        
        Args:
            message_id: Message identifier
            user_id: User identifier (for authorization)
            
        Returns:
            True if successful
        """
        try:
            # Verify ownership
            message = self.get_message(message_id)
            if not message or message.user_id != user_id:
                logger.warning(f"Unauthorized delete attempt: {message_id}")
                return False
            
            # Remove from cache
            if message_id in self.message_cache:
                del self.message_cache[message_id]
            
            # Remove from database
            if self.db:
                self.db.execute(
                    'DELETE FROM voice_messages WHERE message_id = ? AND user_id = ?',
                    [message_id, user_id]
                )
            
            logger.info(f"Voice message deleted: {message_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting message: {e}")
            return False
    
    def delete_user_messages(self, user_id: str, before_date: Optional[datetime] = None) -> int:
        """
        Delete all messages for a user (GDPR right to be forgotten).
        
        Args:
            user_id: User identifier
            before_date: Optional date to delete messages before
            
        Returns:
            Number of messages deleted
        """
        try:
            # Remove from cache
            keys_to_delete = [k for k, v in self.message_cache.items() if v.user_id == user_id]
            for key in keys_to_delete:
                del self.message_cache[key]
            
            # Remove from database
            if self.db:
                if before_date:
                    result = self.db.execute(
                        'DELETE FROM voice_messages WHERE user_id = ? AND timestamp < ?',
                        [user_id, before_date]
                    )
                else:
                    result = self.db.execute(
                        'DELETE FROM voice_messages WHERE user_id = ?',
                        [user_id]
                    )
                
                logger.info(f"Deleted messages for user: {user_id}")
                return result.rowcount
            
            return len(keys_to_delete)
        except Exception as e:
            logger.error(f"Error deleting user messages: {e}")
            return 0
    
    def export_messages(self, user_id: str, format: str = 'json') -> str:
        """
        Export user messages.
        
        Args:
            user_id: User identifier
            format: Export format ('json' or 'csv')
            
        Returns:
            Exported data as string
        """
        messages = self.get_user_messages(user_id, limit=10000)
        
        if format == 'json':
            return json.dumps([asdict(m) for m in messages], default=str, indent=2)
        elif format == 'csv':
            import csv
            from io import StringIO
            
            output = StringIO()
            if messages:
                writer = csv.DictWriter(output, fieldnames=asdict(messages[0]).keys())
                writer.writeheader()
                for msg in messages:
                    writer.writerow(asdict(msg))
            
            return output.getvalue()
        
        return ""
    
    def get_message_statistics(self, user_id: str) -> Dict:
        """
        Get statistics about user's voice messages.
        
        Args:
            user_id: User identifier
            
        Returns:
            Statistics dictionary
        """
        if not self.db:
            return {}
        
        try:
            messages = self.get_user_messages(user_id, limit=10000)
            
            if not messages:
                return {
                    'total_messages': 0,
                    'total_duration': 0.0,
                    'avg_duration': 0.0,
                    'avg_confidence': 0.0
                }
            
            total_duration = sum(m.duration for m in messages)
            avg_duration = total_duration / len(messages)
            avg_confidence = sum(m.confidence for m in messages) / len(messages)
            
            # Agent breakdown
            agent_counts = {}
            for msg in messages:
                agent_counts[msg.agent_name] = agent_counts.get(msg.agent_name, 0) + 1
            
            # Language breakdown
            language_counts = {}
            for msg in messages:
                language_counts[msg.language] = language_counts.get(msg.language, 0) + 1
            
            return {
                'total_messages': len(messages),
                'total_duration': total_duration,
                'avg_duration': avg_duration,
                'avg_confidence': avg_confidence,
                'agent_breakdown': agent_counts,
                'language_breakdown': language_counts,
                'date_range': {
                    'earliest': min(m.timestamp for m in messages).isoformat(),
                    'latest': max(m.timestamp for m in messages).isoformat()
                }
            }
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {}
    
    def _generate_message_id(self, user_id: str, timestamp: datetime) -> str:
        """Generate unique message ID."""
        import hashlib
        content = f"{user_id}:{timestamp.isoformat()}:{datetime.utcnow().timestamp()}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _dict_to_message(self, data: Dict) -> VoiceMessage:
        """Convert database row to VoiceMessage object."""
        return VoiceMessage(
            user_id=data.get('user_id'),
            agent_name=data.get('agent_name'),
            transcription=data.get('transcription'),
            audio_url=data.get('audio_url'),
            duration=data.get('duration'),
            confidence=data.get('confidence'),
            language=data.get('language', 'en'),
            sentiment=data.get('sentiment'),
            timestamp=data.get('timestamp'),
            message_id=data.get('message_id')
        )
    
    def create_logger_table(self) -> bool:
        """Create voice_messages table if it doesn't exist."""
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS voice_messages (
                id INT PRIMARY KEY AUTO_INCREMENT,
                message_id VARCHAR(255) UNIQUE,
                user_id VARCHAR(255) NOT NULL,
                agent_name VARCHAR(100) NOT NULL,
                transcription TEXT,
                audio_url VARCHAR(500),
                duration FLOAT,
                confidence FLOAT,
                language VARCHAR(10),
                sentiment VARCHAR(20),
                timestamp DATETIME,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_user_id (user_id),
                INDEX idx_agent_name (agent_name),
                INDEX idx_timestamp (timestamp)
            )
            """
            self.db.execute(sql)
            logger.info("Created voice_messages table")
            return True
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            return False
