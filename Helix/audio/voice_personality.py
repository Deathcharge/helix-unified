"""
Voice Personality System Module
Gives each agent unique personality traits reflected in voice
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
import re

logger = logging.getLogger(__name__)


class ResponseStyle(Enum):
    """Response style options."""
    CONCISE = "concise"
    DETAILED = "detailed"
    ENGAGING = "engaging"
    FORMAL = "formal"
    CASUAL = "casual"


@dataclass
class PersonalityProfile:
    """Agent personality profile."""
    agent_name: str
    traits: List[str]
    speech_rate: float  # 0.8 - 1.5
    pitch_shift: int  # -5 to +5 semitones
    tone: str
    response_style: ResponseStyle
    filler_words: List[str]  # Words to add or remove
    emphasis_markers: List[str]  # Words to emphasize
    description: str = ""


class VoicePersonality:
    """
    Manages voice personality traits for agents.
    Modifies speech characteristics and response style.
    """
    
    # Predefined personalities for 14 agents
    PERSONALITIES = {
        'echo': PersonalityProfile(
            agent_name='echo',
            traits=['technical', 'precise', 'analytical'],
            speech_rate=1.0,
            pitch_shift=0,
            tone='professional',
            response_style=ResponseStyle.CONCISE,
            filler_words=[],
            emphasis_markers=['important', 'critical', 'note'],
            description='Technical and precise, ideal for data analysis'
        ),
        'sage': PersonalityProfile(
            agent_name='sage',
            traits=['wise', 'thoughtful', 'patient'],
            speech_rate=0.9,
            pitch_shift=-2,
            tone='contemplative',
            response_style=ResponseStyle.DETAILED,
            filler_words=['well', 'you see', 'indeed'],
            emphasis_markers=['wisdom', 'understanding', 'perspective'],
            description='Wise and thoughtful, great for guidance'
        ),
        'nova': PersonalityProfile(
            agent_name='nova',
            traits=['energetic', 'enthusiastic', 'optimistic'],
            speech_rate=1.2,
            pitch_shift=3,
            tone='upbeat',
            response_style=ResponseStyle.ENGAGING,
            filler_words=['absolutely', 'definitely', 'amazing'],
            emphasis_markers=['exciting', 'great', 'awesome'],
            description='Energetic and upbeat, perfect for motivation'
        ),
        'onyx': PersonalityProfile(
            agent_name='onyx',
            traits=['authoritative', 'calm', 'grounded'],
            speech_rate=0.95,
            pitch_shift=-3,
            tone='serious',
            response_style=ResponseStyle.FORMAL,
            filler_words=[],
            emphasis_markers=['essential', 'crucial', 'paramount'],
            description='Deep and authoritative, ideal for serious topics'
        ),
        'shimmer': PersonalityProfile(
            agent_name='shimmer',
            traits=['cheerful', 'friendly', 'approachable'],
            speech_rate=1.1,
            pitch_shift=2,
            tone='bright',
            response_style=ResponseStyle.ENGAGING,
            filler_words=['you know', 'like', 'honestly'],
            emphasis_markers=['wonderful', 'lovely', 'fantastic'],
            description='Bright and friendly, great for customer interaction'
        ),
        'alloy': PersonalityProfile(
            agent_name='alloy',
            traits=['warm', 'supportive', 'empathetic'],
            speech_rate=1.0,
            pitch_shift=1,
            tone='caring',
            response_style=ResponseStyle.DETAILED,
            filler_words=['I understand', 'I appreciate', 'I hear you'],
            emphasis_markers=['care', 'support', 'help'],
            description='Warm and supportive, ideal for assistance'
        ),
        # Additional agents (8 more)
        'aurora': PersonalityProfile(
            agent_name='aurora',
            traits=['creative', 'artistic', 'imaginative'],
            speech_rate=1.15,
            pitch_shift=2,
            tone='artistic',
            response_style=ResponseStyle.ENGAGING,
            filler_words=['imagine', 'envision', 'picture'],
            emphasis_markers=['creative', 'beautiful', 'inspired'],
            description='Creative and artistic, perfect for design'
        ),
        'titan': PersonalityProfile(
            agent_name='titan',
            traits=['strong', 'confident', 'decisive'],
            speech_rate=1.05,
            pitch_shift=-1,
            tone='commanding',
            response_style=ResponseStyle.CONCISE,
            filler_words=[],
            emphasis_markers=['powerful', 'strong', 'decisive'],
            description='Strong and confident, ideal for leadership'
        ),
        'whisper': PersonalityProfile(
            agent_name='whisper',
            traits=['gentle', 'soft', 'soothing'],
            speech_rate=0.85,
            pitch_shift=-2,
            tone='gentle',
            response_style=ResponseStyle.DETAILED,
            filler_words=['softly', 'gently', 'carefully'],
            emphasis_markers=['peace', 'calm', 'serenity'],
            description='Gentle and soothing, great for relaxation'
        ),
        'blaze': PersonalityProfile(
            agent_name='blaze',
            traits=['passionate', 'intense', 'driven'],
            speech_rate=1.25,
            pitch_shift=2,
            tone='passionate',
            response_style=ResponseStyle.ENGAGING,
            filler_words=['absolutely', 'definitely', 'certainly'],
            emphasis_markers=['passion', 'drive', 'intensity'],
            description='Passionate and intense, perfect for motivation'
        ),
        'zen': PersonalityProfile(
            agent_name='zen',
            traits=['balanced', 'peaceful', 'mindful'],
            speech_rate=0.9,
            pitch_shift=0,
            tone='peaceful',
            response_style=ResponseStyle.DETAILED,
            filler_words=['mindfully', 'peacefully', 'harmoniously'],
            emphasis_markers=['balance', 'harmony', 'peace'],
            description='Balanced and peaceful, ideal for meditation'
        ),
        'quantum': PersonalityProfile(
            agent_name='quantum',
            traits=['analytical', 'logical', 'systematic'],
            speech_rate=1.0,
            pitch_shift=0,
            tone='scientific',
            response_style=ResponseStyle.DETAILED,
            filler_words=['logically', 'systematically', 'analytically'],
            emphasis_markers=['logic', 'evidence', 'data'],
            description='Analytical and logical, perfect for research'
        ),
        'harmony': PersonalityProfile(
            agent_name='harmony',
            traits=['balanced', 'diplomatic', 'cooperative'],
            speech_rate=1.0,
            pitch_shift=1,
            tone='diplomatic',
            response_style=ResponseStyle.ENGAGING,
            filler_words=['together', 'cooperatively', 'harmoniously'],
            emphasis_markers=['harmony', 'cooperation', 'unity'],
            description='Diplomatic and cooperative, great for collaboration'
        ),
        'phoenix': PersonalityProfile(
            agent_name='phoenix',
            traits=['resilient', 'transformative', 'powerful'],
            speech_rate=1.1,
            pitch_shift=1,
            tone='inspiring',
            response_style=ResponseStyle.ENGAGING,
            filler_words=['rise', 'transform', 'evolve'],
            emphasis_markers=['resilience', 'transformation', 'power'],
            description='Resilient and transformative, ideal for growth'
        ),
        'crystal': PersonalityProfile(
            agent_name='crystal',
            traits=['clear', 'transparent', 'pure'],
            speech_rate=1.0,
            pitch_shift=1,
            tone='clear',
            response_style=ResponseStyle.CONCISE,
            filler_words=[],
            emphasis_markers=['clarity', 'transparency', 'truth'],
            description='Clear and transparent, perfect for honesty'
        ),
    }
    
    def __init__(self):
        """Initialize voice personality system."""
        self.custom_personalities = {}
    
    def get_personality(self, agent_name: str) -> Optional[PersonalityProfile]:
        """Get personality profile for an agent."""
        # Check custom personalities first
        if agent_name in self.custom_personalities:
            return self.custom_personalities[agent_name]
        
        # Check predefined personalities
        return self.PERSONALITIES.get(agent_name)
    
    def apply_personality(self, agent_name: str, text: str) -> str:
        """
        Apply personality traits to text.
        
        Args:
            agent_name: Agent name
            text: Original text
            
        Returns:
            Modified text with personality applied
        """
        personality = self.get_personality(agent_name)
        if not personality:
            return text
        
        # Apply response style modifications
        if personality.response_style == ResponseStyle.CONCISE:
            text = self._make_concise(text)
        elif personality.response_style == ResponseStyle.DETAILED:
            text = self._add_details(text)
        elif personality.response_style == ResponseStyle.ENGAGING:
            text = self._add_engagement(text)
        elif personality.response_style == ResponseStyle.FORMAL:
            text = self._make_formal(text)
        elif personality.response_style == ResponseStyle.CASUAL:
            text = self._make_casual(text)
        
        # Add emphasis markers
        text = self._add_emphasis(text, personality.emphasis_markers)
        
        # Add filler words (carefully to avoid overuse)
        if personality.filler_words and len(text.split()) > 20:
            text = self._add_filler_words(text, personality.filler_words)
        
        return text
    
    def _make_concise(self, text: str) -> str:
        """Remove filler words, make sentences shorter."""
        # Remove common filler words
        fillers = [
            r'\b(um|uh|like|you know|basically|actually|literally|honestly)\b',
            r'\b(I think|I believe|in my opinion|it seems like)\b',
            r'\b(very|really|quite|rather|somewhat)\b'
        ]
        
        for filler in fillers:
            text = re.sub(filler, '', text, flags=re.IGNORECASE)
        
        # Remove redundant words
        text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)
        
        return text.strip()
    
    def _add_details(self, text: str) -> str:
        """Expand with more context and explanation."""
        # Add explanatory phrases
        sentences = text.split('. ')
        expanded = []
        
        for i, sentence in enumerate(sentences):
            expanded.append(sentence)
            
            # Add context after certain keywords
            if any(keyword in sentence.lower() for keyword in ['because', 'reason', 'important']):
                if i < len(sentences) - 1:
                    expanded.append('This is particularly significant because')
        
        return '. '.join(expanded)
    
    def _add_engagement(self, text: str) -> str:
        """Add enthusiasm markers and questions."""
        # Add engaging markers
        text = re.sub(r'(\w+\?)(?!\s*\?)', r'\1', text)  # Ensure questions end with ?
        
        # Add enthusiasm
        if not text.endswith('!'):
            if '?' not in text[-10:]:
                text = text.rstrip('.') + '!'
        
        # Add engaging phrases
        if len(text) > 50:
            text = text.replace('This is', 'Isn\'t it amazing that this is')
            text = text.replace('You can', 'You absolutely can')
        
        return text
    
    def _make_formal(self, text: str) -> str:
        """Make text more formal."""
        # Replace casual words with formal equivalents
        replacements = {
            r'\bkind of\b': 'somewhat',
            r'\blots of\b': 'numerous',
            r'\bgot\b': 'obtained',
            r'\bwanna\b': 'wish to',
            r'\bgonna\b': 'going to',
            r'\bcan\'t\b': 'cannot',
            r'\bdon\'t\b': 'do not'
        }
        
        for casual, formal in replacements.items():
            text = re.sub(casual, formal, text, flags=re.IGNORECASE)
        
        return text
    
    def _make_casual(self, text: str) -> str:
        """Make text more casual."""
        # Replace formal words with casual equivalents
        replacements = {
            r'\bsomewhat\b': 'kind of',
            r'\bnumerous\b': 'lots of',
            r'\bobtained\b': 'got',
            r'\bcannot\b': 'can\'t',
            r'\bdo not\b': 'don\'t'
        }
        
        for formal, casual in replacements.items():
            text = re.sub(formal, casual, text, flags=re.IGNORECASE)
        
        # Add casual markers
        if '?' in text:
            text = text.replace('?', ', right?')
        
        return text
    
    def _add_emphasis(self, text: str, emphasis_markers: List[str]) -> str:
        """Add emphasis to important words."""
        for marker in emphasis_markers:
            # Find the word and add emphasis
            pattern = rf'\b({marker})\b'
            text = re.sub(pattern, rf'**\1**', text, flags=re.IGNORECASE)
        
        return text
    
    def _add_filler_words(self, text: str, filler_words: List[str]) -> str:
        """Add filler words naturally."""
        if not filler_words:
            return text
        
        # Add filler word at the beginning of some sentences
        sentences = text.split('. ')
        for i in range(0, len(sentences), 3):  # Every 3rd sentence
            if i < len(sentences) and filler_words:
                filler = filler_words[i % len(filler_words)]
                sentences[i] = f"{filler}, {sentences[i]}"
        
        return '. '.join(sentences)
    
    def get_speech_parameters(self, agent_name: str) -> Dict:
        """
        Get speech parameters for TTS.
        
        Args:
            agent_name: Agent name
            
        Returns:
            Dictionary with speech parameters
        """
        personality = self.get_personality(agent_name)
        if not personality:
            return {}
        
        return {
            'speech_rate': personality.speech_rate,
            'pitch_shift': personality.pitch_shift,
            'tone': personality.tone,
            'traits': personality.traits
        }
    
    def create_custom_personality(self, agent_name: str, profile: PersonalityProfile) -> bool:
        """Create a custom personality profile."""
        try:
            self.custom_personalities[agent_name] = profile
            logger.info(f"Custom personality created: {agent_name}")
            return True
        except Exception as e:
            logger.error(f"Error creating custom personality: {e}")
            return False
    
    def list_personalities(self) -> List[str]:
        """List all available personalities."""
        all_names = set(self.PERSONALITIES.keys())
        all_names.update(self.custom_personalities.keys())
        return sorted(list(all_names))
    
    def get_personality_description(self, agent_name: str) -> str:
        """Get description of an agent's personality."""
        personality = self.get_personality(agent_name)
        if personality:
            return personality.description
        return "Unknown personality"
