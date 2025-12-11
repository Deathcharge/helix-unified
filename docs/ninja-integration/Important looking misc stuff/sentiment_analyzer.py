"""
Advanced Sentiment Analysis and Emotion Detection System
Analyzes user messages for sentiment, emotion, and engagement metrics
"""
import logging
import re
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Advanced sentiment and emotion analysis for Discord messages"""
    
    def __init__(self):
        self.user_sentiment_history = defaultdict(lambda: deque(maxlen=100))
        self.channel_sentiment_history = defaultdict(lambda: deque(maxlen=500))
        self.guild_sentiment_history = defaultdict(lambda: deque(maxlen=1000))
        
        # Emotion keywords (can be enhanced with ML models)
        self.emotion_keywords = {
            'joy': ['happy', 'excited', 'love', 'amazing', 'awesome', 'great', 'wonderful', '😊', '😄', '❤️', '🎉', '✨'],
            'sadness': ['sad', 'depressed', 'unhappy', 'disappointed', 'crying', '😢', '😭', '💔'],
            'anger': ['angry', 'mad', 'furious', 'hate', 'annoyed', 'frustrated', '😠', '😡', '🤬'],
            'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous', '😨', '😰', '😱'],
            'surprise': ['wow', 'omg', 'shocked', 'surprised', 'amazing', '😮', '😲', '🤯'],
            'disgust': ['gross', 'disgusting', 'eww', 'yuck', '🤢', '🤮'],
            'neutral': ['okay', 'fine', 'alright', 'sure', 'maybe']
        }
        
        # Sentiment indicators
        self.positive_indicators = [
            'thanks', 'thank you', 'appreciate', 'love', 'awesome', 'great', 'excellent',
            'perfect', 'amazing', 'wonderful', 'fantastic', 'brilliant', 'good', 'nice',
            '👍', '❤️', '😊', '🎉', '✨', '🔥', '💯'
        ]
        
        self.negative_indicators = [
            'hate', 'terrible', 'awful', 'bad', 'worst', 'horrible', 'sucks', 'disappointed',
            'angry', 'frustrated', 'annoyed', 'upset', 'sad', 'depressed',
            '👎', '😠', '😡', '😢', '💔', '🤬'
        ]
        
        # Toxicity patterns
        self.toxicity_patterns = [
            r'\b(stupid|idiot|dumb|moron|loser)\b',
            r'\b(shut up|stfu|gtfo)\b',
            r'\b(kill yourself|kys)\b',
            r'\b(f+u+c+k+|s+h+i+t+)\b'
        ]
    
    def analyze_message(
        self, 
        message: str, 
        user_id: str,
        channel_id: str,
        guild_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Comprehensive message sentiment analysis"""
        
        message_lower = message.lower()
        
        # Detect emotions
        emotions = self._detect_emotions(message_lower)
        
        # Calculate sentiment score (-1 to 1)
        sentiment_score = self._calculate_sentiment_score(message_lower)
        
        # Detect toxicity
        toxicity_score = self._detect_toxicity(message_lower)
        
        # Determine overall sentiment
        if sentiment_score > 0.3:
            sentiment = 'positive'
        elif sentiment_score < -0.3:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Detect engagement indicators
        engagement = self._analyze_engagement(message)
        
        result = {
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'emotions': emotions,
            'toxicity_score': toxicity_score,
            'is_toxic': toxicity_score > 0.5,
            'engagement': engagement,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Store in history
        self.user_sentiment_history[user_id].append(result)
        self.channel_sentiment_history[channel_id].append(result)
        if guild_id:
            self.guild_sentiment_history[guild_id].append(result)
        
        return result
    
    def _detect_emotions(self, message: str) -> Dict[str, float]:
        """Detect emotions in message"""
        
        emotions = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in message:
                    score += 1
            
            if score > 0:
                emotions[emotion] = min(score / len(keywords), 1.0)
        
        # Normalize scores
        if emotions:
            total = sum(emotions.values())
            emotions = {k: v/total for k, v in emotions.items()}
        
        return emotions
    
    def _calculate_sentiment_score(self, message: str) -> float:
        """Calculate sentiment score from -1 (negative) to 1 (positive)"""
        
        positive_count = sum(1 for indicator in self.positive_indicators if indicator in message)
        negative_count = sum(1 for indicator in self.negative_indicators if indicator in message)
        
        total = positive_count + negative_count
        
        if total == 0:
            return 0.0
        
        score = (positive_count - negative_count) / total
        
        return max(-1.0, min(1.0, score))
    
    def _detect_toxicity(self, message: str) -> float:
        """Detect toxic content in message"""
        
        toxicity_count = 0
        
        for pattern in self.toxicity_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                toxicity_count += 1
        
        # Calculate toxicity score (0 to 1)
        toxicity_score = min(toxicity_count / len(self.toxicity_patterns), 1.0)
        
        return toxicity_score
    
    def _analyze_engagement(self, message: str) -> Dict[str, Any]:
        """Analyze message engagement indicators"""
        
        return {
            'has_question': '?' in message,
            'has_mention': '@' in message,
            'has_emoji': any(char in message for char in '😀😁😂🤣😃😄😅😆😉😊😋😎😍'),
            'has_link': 'http' in message.lower() or 'www.' in message.lower(),
            'word_count': len(message.split()),
            'character_count': len(message),
            'has_caps': any(word.isupper() and len(word) > 2 for word in message.split())
        }
    
    def get_user_sentiment_trend(self, user_id: str, hours: int = 24) -> Dict[str, Any]:
        """Get sentiment trend for a user over time"""
        
        history = list(self.user_sentiment_history[user_id])
        
        if not history:
            return {
                'average_sentiment': 0.0,
                'trend': 'neutral',
                'message_count': 0,
                'dominant_emotion': None
            }
        
        # Filter by time window
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent_history = [
            h for h in history 
            if datetime.fromisoformat(h['timestamp']) > cutoff
        ]
        
        if not recent_history:
            return {
                'average_sentiment': 0.0,
                'trend': 'neutral',
                'message_count': 0,
                'dominant_emotion': None
            }
        
        # Calculate average sentiment
        avg_sentiment = sum(h['sentiment_score'] for h in recent_history) / len(recent_history)
        
        # Determine trend
        if len(recent_history) >= 2:
            first_half = recent_history[:len(recent_history)//2]
            second_half = recent_history[len(recent_history)//2:]
            
            first_avg = sum(h['sentiment_score'] for h in first_half) / len(first_half)
            second_avg = sum(h['sentiment_score'] for h in second_half) / len(second_half)
            
            if second_avg > first_avg + 0.2:
                trend = 'improving'
            elif second_avg < first_avg - 0.2:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'
        
        # Find dominant emotion
        all_emotions = defaultdict(float)
        for h in recent_history:
            for emotion, score in h['emotions'].items():
                all_emotions[emotion] += score
        
        dominant_emotion = max(all_emotions.items(), key=lambda x: x[1])[0] if all_emotions else None
        
        return {
            'average_sentiment': avg_sentiment,
            'trend': trend,
            'message_count': len(recent_history),
            'dominant_emotion': dominant_emotion,
            'positive_ratio': sum(1 for h in recent_history if h['sentiment'] == 'positive') / len(recent_history),
            'negative_ratio': sum(1 for h in recent_history if h['sentiment'] == 'negative') / len(recent_history),
            'toxicity_incidents': sum(1 for h in recent_history if h['is_toxic'])
        }
    
    def get_channel_sentiment(self, channel_id: str, hours: int = 24) -> Dict[str, Any]:
        """Get overall sentiment for a channel"""
        
        history = list(self.channel_sentiment_history[channel_id])
        
        if not history:
            return {
                'average_sentiment': 0.0,
                'activity_level': 'inactive',
                'message_count': 0
            }
        
        # Filter by time window
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent_history = [
            h for h in history 
            if datetime.fromisoformat(h['timestamp']) > cutoff
        ]
        
        if not recent_history:
            return {
                'average_sentiment': 0.0,
                'activity_level': 'inactive',
                'message_count': 0
            }
        
        avg_sentiment = sum(h['sentiment_score'] for h in recent_history) / len(recent_history)
        
        # Determine activity level
        msg_count = len(recent_history)
        if msg_count > 100:
            activity = 'very_active'
        elif msg_count > 50:
            activity = 'active'
        elif msg_count > 10:
            activity = 'moderate'
        else:
            activity = 'low'
        
        return {
            'average_sentiment': avg_sentiment,
            'activity_level': activity,
            'message_count': msg_count,
            'positive_ratio': sum(1 for h in recent_history if h['sentiment'] == 'positive') / len(recent_history),
            'negative_ratio': sum(1 for h in recent_history if h['sentiment'] == 'negative') / len(recent_history),
            'toxicity_rate': sum(1 for h in recent_history if h['is_toxic']) / len(recent_history)
        }
    
    def get_guild_health_score(self, guild_id: str) -> Dict[str, Any]:
        """Calculate overall health score for a guild"""
        
        history = list(self.guild_sentiment_history[guild_id])
        
        if not history:
            return {
                'health_score': 50.0,
                'status': 'unknown',
                'recommendations': []
            }
        
        # Recent history (last 24 hours)
        cutoff = datetime.utcnow() - timedelta(hours=24)
        recent_history = [
            h for h in history 
            if datetime.fromisoformat(h['timestamp']) > cutoff
        ]
        
        if not recent_history:
            return {
                'health_score': 50.0,
                'status': 'inactive',
                'recommendations': ['Increase community engagement']
            }
        
        # Calculate health components
        avg_sentiment = sum(h['sentiment_score'] for h in recent_history) / len(recent_history)
        toxicity_rate = sum(1 for h in recent_history if h['is_toxic']) / len(recent_history)
        engagement_rate = sum(1 for h in recent_history if h['engagement']['has_question'] or h['engagement']['has_mention']) / len(recent_history)
        
        # Calculate health score (0-100)
        sentiment_component = (avg_sentiment + 1) * 25  # 0-50 points
        toxicity_component = (1 - toxicity_rate) * 30  # 0-30 points
        engagement_component = engagement_rate * 20  # 0-20 points
        
        health_score = sentiment_component + toxicity_component + engagement_component
        
        # Determine status
        if health_score >= 80:
            status = 'excellent'
        elif health_score >= 60:
            status = 'good'
        elif health_score >= 40:
            status = 'fair'
        else:
            status = 'needs_attention'
        
        # Generate recommendations
        recommendations = []
        if avg_sentiment < 0:
            recommendations.append('Address negative sentiment in community')
        if toxicity_rate > 0.1:
            recommendations.append('Increase moderation to reduce toxicity')
        if engagement_rate < 0.2:
            recommendations.append('Encourage more community interaction')
        
        return {
            'health_score': health_score,
            'status': status,
            'average_sentiment': avg_sentiment,
            'toxicity_rate': toxicity_rate,
            'engagement_rate': engagement_rate,
            'recommendations': recommendations
        }

# Global sentiment analyzer instance
sentiment_analyzer = SentimentAnalyzer()