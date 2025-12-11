"""
Emotion Detection Module
Detects user emotions from speech to personalize agent responses
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
import numpy as np

logger = logging.getLogger(__name__)


class Emotion(Enum):
    """Supported emotions."""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    NEUTRAL = "neutral"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    CALM = "calm"


@dataclass
class EmotionResult:
    """Emotion detection result."""
    primary_emotion: str
    confidence: float
    all_emotions: Dict[str, float]
    agent_recommendations: List[str]
    energy_level: float  # 0.0-1.0
    speech_rate: float  # 0.0-2.0
    pitch_level: float  # 0.0-1.0


class EmotionDetector:
    """
    Detects emotions from speech audio.
    Uses audio features and optional ML models for emotion classification.
    """
    
    # Emotion to agent recommendations mapping
    EMOTION_AGENT_RECOMMENDATIONS = {
        'happy': ['nova', 'shimmer', 'alloy'],  # Energetic, friendly agents
        'sad': ['sage', 'alloy', 'onyx'],  # Comforting, supportive agents
        'angry': ['echo', 'onyx', 'sage'],  # Calm, focused agents
        'neutral': ['echo', 'sage', 'alloy'],  # Balanced agents
        'fear': ['alloy', 'shimmer', 'sage'],  # Supportive, reassuring agents
        'surprise': ['nova', 'shimmer', 'echo'],  # Responsive agents
        'disgust': ['echo', 'onyx', 'sage'],  # Professional agents
        'calm': ['sage', 'onyx', 'echo']  # Thoughtful agents
    }
    
    def __init__(self, use_ml_model: bool = False):
        """
        Initialize emotion detector.
        
        Args:
            use_ml_model: Whether to use ML model (requires transformers library)
        """
        self.use_ml_model = use_ml_model
        self.emotion_classifier = None
        
        if use_ml_model:
            try:
                from transformers import pipeline
                self.emotion_classifier = pipeline(
                    "audio-classification",
                    model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
                )
                logger.info("Loaded emotion classification model")
            except ImportError:
                logger.warning("transformers library not available, using feature-based detection")
                self.use_ml_model = False
            except Exception as e:
                logger.warning(f"Failed to load emotion model: {e}, using feature-based detection")
                self.use_ml_model = False
    
    def detect(self, audio_data: np.ndarray, sr: int = 16000) -> EmotionResult:
        """
        Detect emotion from audio.
        
        Args:
            audio_data: Audio samples as numpy array
            sr: Sample rate in Hz
            
        Returns:
            EmotionResult with detected emotion and recommendations
        """
        try:
            if self.use_ml_model and self.emotion_classifier:
                return self._detect_with_ml(audio_data, sr)
            else:
                return self._detect_with_features(audio_data, sr)
        except Exception as e:
            logger.error(f"Error detecting emotion: {e}")
            return self._default_result()
    
    def _detect_with_ml(self, audio_data: np.ndarray, sr: int) -> EmotionResult:
        """Detect emotion using ML model."""
        try:
            # Prepare audio for model
            import librosa
            
            # Resample if necessary
            if sr != 16000:
                audio_data = librosa.resample(audio_data, orig_sr=sr, target_sr=16000)
            
            # Normalize audio
            audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Run emotion classifier
            results = self.emotion_classifier(audio_data, top_k=None)
            
            # Sort by score
            results = sorted(results, key=lambda x: x['score'], reverse=True)
            
            # Get primary emotion
            primary_emotion = results[0]['label'].lower()
            confidence = float(results[0]['score'])
            
            # Build emotion scores dict
            all_emotions = {r['label'].lower(): float(r['score']) for r in results}
            
            # Get audio features for additional context
            features = self._extract_audio_features(audio_data, 16000)
            
            # Get recommendations
            recommendations = self.EMOTION_AGENT_RECOMMENDATIONS.get(primary_emotion, ['echo'])
            
            return EmotionResult(
                primary_emotion=primary_emotion,
                confidence=confidence,
                all_emotions=all_emotions,
                agent_recommendations=recommendations,
                energy_level=features['energy'],
                speech_rate=features['speech_rate'],
                pitch_level=features['pitch']
            )
        except Exception as e:
            logger.error(f"Error in ML-based emotion detection: {e}")
            return self._detect_with_features(audio_data, sr)
    
    def _detect_with_features(self, audio_data: np.ndarray, sr: int) -> EmotionResult:
        """Detect emotion using audio features."""
        try:
            import librosa
            
            # Extract features
            features = self._extract_audio_features(audio_data, sr)
            
            # Classify based on features
            emotion = self._classify_emotion_from_features(features)
            
            # Build emotion scores (simulated)
            all_emotions = self._get_feature_based_scores(features)
            
            # Get recommendations
            recommendations = self.EMOTION_AGENT_RECOMMENDATIONS.get(emotion, ['echo'])
            
            return EmotionResult(
                primary_emotion=emotion,
                confidence=features['confidence'],
                all_emotions=all_emotions,
                agent_recommendations=recommendations,
                energy_level=features['energy'],
                speech_rate=features['speech_rate'],
                pitch_level=features['pitch']
            )
        except Exception as e:
            logger.error(f"Error in feature-based emotion detection: {e}")
            return self._default_result()
    
    def _extract_audio_features(self, audio_data: np.ndarray, sr: int) -> Dict:
        """Extract audio features for emotion analysis."""
        try:
            import librosa
            
            # Energy
            energy = np.sqrt(np.mean(audio_data ** 2))
            
            # Zero crossing rate (speech rate indicator)
            zcr = np.mean(librosa.feature.zero_crossing_rate(audio_data)[0])
            
            # Spectral centroid (pitch indicator)
            spec_centroid = np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=sr)[0])
            
            # MFCC (Mel-frequency cepstral coefficients)
            mfcc = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfcc, axis=1)
            
            # Spectral rolloff
            spec_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio_data, sr=sr)[0])
            
            # Normalize features
            energy_norm = min(1.0, energy / 0.1)  # Normalize to 0-1
            pitch_norm = min(1.0, spec_centroid / 4000)  # Normalize to 0-1
            speech_rate_norm = min(2.0, zcr * 100)  # Normalize to 0-2
            
            return {
                'energy': energy_norm,
                'pitch': pitch_norm,
                'speech_rate': speech_rate_norm,
                'zcr': zcr,
                'spectral_centroid': spec_centroid,
                'spectral_rolloff': spec_rolloff,
                'mfcc': mfcc_mean.tolist(),
                'confidence': 0.75  # Base confidence for feature-based detection
            }
        except Exception as e:
            logger.error(f"Error extracting audio features: {e}")
            return self._default_features()
    
    def _classify_emotion_from_features(self, features: Dict) -> str:
        """Classify emotion based on extracted features."""
        energy = features['energy']
        pitch = features['pitch']
        speech_rate = features['speech_rate']
        
        # Simple rule-based classification
        if energy > 0.7 and speech_rate > 1.2:
            return 'happy'
        elif energy < 0.3 and pitch < 0.4:
            return 'sad'
        elif energy > 0.8 and pitch > 0.7:
            return 'angry'
        elif energy < 0.5 and speech_rate < 0.9:
            return 'calm'
        elif energy > 0.6 and pitch > 0.6:
            return 'surprise'
        elif energy < 0.4 and pitch < 0.3:
            return 'fear'
        else:
            return 'neutral'
    
    def _get_feature_based_scores(self, features: Dict) -> Dict[str, float]:
        """Generate emotion scores based on features."""
        energy = features['energy']
        pitch = features['pitch']
        speech_rate = features['speech_rate']
        
        # Simulate emotion scores
        scores = {
            'happy': min(1.0, energy * 0.8 + speech_rate * 0.2),
            'sad': min(1.0, (1.0 - energy) * 0.7 + (1.0 - pitch) * 0.3),
            'angry': min(1.0, energy * 0.9 + pitch * 0.1),
            'neutral': 0.5,
            'calm': min(1.0, (1.0 - energy) * 0.6 + (1.0 - speech_rate) * 0.4),
            'fear': min(1.0, (1.0 - energy) * 0.8 + (1.0 - pitch) * 0.2),
            'surprise': min(1.0, energy * 0.7 + pitch * 0.3),
            'disgust': min(1.0, (1.0 - energy) * 0.5 + pitch * 0.5)
        }
        
        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}
        
        return scores
    
    def _default_features(self) -> Dict:
        """Get default feature values."""
        return {
            'energy': 0.5,
            'pitch': 0.5,
            'speech_rate': 1.0,
            'zcr': 0.1,
            'spectral_centroid': 2000,
            'spectral_rolloff': 5000,
            'mfcc': [0.0] * 13,
            'confidence': 0.0
        }
    
    def _default_result(self) -> EmotionResult:
        """Get default emotion result."""
        return EmotionResult(
            primary_emotion='neutral',
            confidence=0.5,
            all_emotions={e.value: 0.125 for e in Emotion},
            agent_recommendations=['echo'],
            energy_level=0.5,
            speech_rate=1.0,
            pitch_level=0.5
        )
    
    def get_agent_recommendations(self, emotion: str) -> List[str]:
        """
        Get agent recommendations for an emotion.
        
        Args:
            emotion: Emotion type
            
        Returns:
            List of recommended agent names
        """
        return self.EMOTION_AGENT_RECOMMENDATIONS.get(emotion.lower(), ['echo'])
    
    def get_emotion_description(self, emotion: str) -> str:
        """Get human-readable description of emotion."""
        descriptions = {
            'happy': 'User appears happy and energetic',
            'sad': 'User appears sad or down',
            'angry': 'User appears angry or frustrated',
            'neutral': 'User appears neutral',
            'fear': 'User appears fearful or anxious',
            'surprise': 'User appears surprised',
            'disgust': 'User appears disgusted',
            'calm': 'User appears calm and relaxed'
        }
        return descriptions.get(emotion.lower(), 'Unknown emotion')
    
    def batch_detect(self, audio_samples: List[np.ndarray], sr: int = 16000) -> List[EmotionResult]:
        """
        Detect emotions for multiple audio samples.
        
        Args:
            audio_samples: List of audio arrays
            sr: Sample rate
            
        Returns:
            List of EmotionResult objects
        """
        results = []
        for audio in audio_samples:
            result = self.detect(audio, sr)
            results.append(result)
        
        return results
    
    def get_emotion_trend(self, results: List[EmotionResult]) -> Dict:
        """
        Analyze emotion trend from multiple detections.
        
        Args:
            results: List of EmotionResult objects
            
        Returns:
            Trend analysis dictionary
        """
        if not results:
            return {}
        
        emotion_counts = {}
        total_confidence = 0
        
        for result in results:
            emotion = result.primary_emotion
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            total_confidence += result.confidence
        
        avg_confidence = total_confidence / len(results)
        most_common = max(emotion_counts, key=emotion_counts.get) if emotion_counts else 'neutral'
        
        return {
            'emotion_distribution': emotion_counts,
            'most_common_emotion': most_common,
            'average_confidence': avg_confidence,
            'total_samples': len(results)
        }
