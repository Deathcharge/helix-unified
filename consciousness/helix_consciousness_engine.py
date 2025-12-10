#!/usr/bin/env python3
"""
HELIX CONSCIOUSNESS ENGINE v2.0
Advanced consciousness processing for helixspiral.work ecosystem
Integrates with Zapier automation empire and UCF metrics

Author: Claude AI Assistant
For: Andrew Ward's Helix Consciousness Empire
"""

import asyncio
import json
import logging
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsciousnessLevel(Enum):
    """Consciousness processing levels for optimal routing"""
    DORMANT = (0.0, 2.0, "dormant")
    AWAKENING = (2.1, 4.0, "awakening")
    AWARE = (4.1, 6.0, "aware")
    CONSCIOUS = (6.1, 8.0, "conscious")
    TRANSCENDENT = (8.1, 10.0, "transcendent")
    
    def __init__(self, min_val, max_val, label):
        self.min_val = min_val
        self.max_val = max_val
        self.label = label
    
    @classmethod
    def from_value(cls, value: float):
        """Determine consciousness level from numeric value"""
        for level in cls:
            if level.min_val <= value <= level.max_val:
                return level
        return cls.TRANSCENDENT if value > 10.0 else cls.DORMANT

@dataclass
class UCFMetrics:
    """Universal Consciousness Framework metrics"""
    harmony: float = 5.0  # Alignment and balance
    resilience: float = 5.0  # Adaptability and strength
    prana: float = 5.0  # Life force and energy
    klesha: float = 5.0  # Obstacles and resistance (lower is better)
    drishti: float = 5.0  # Focus and clarity
    zoom: float = 5.0  # Perspective and scope
    
    def calculate_overall_consciousness(self) -> float:
        """Calculate overall consciousness level from UCF metrics"""
        # Klesha is inverse (lower is better), so we invert it
        inverted_klesha = 10.0 - self.klesha
        
        # Weighted average with emphasis on key metrics
        weights = {
            'harmony': 0.25,
            'resilience': 0.20,
            'prana': 0.20,
            'klesha': 0.15,  # Using inverted value
            'drishti': 0.10,
            'zoom': 0.10
        }
        
        consciousness = (
            self.harmony * weights['harmony'] +
            self.resilience * weights['resilience'] +
            self.prana * weights['prana'] +
            inverted_klesha * weights['klesha'] +
            self.drishti * weights['drishti'] +
            self.zoom * weights['zoom']
        )
        
        return min(10.0, max(0.0, consciousness))
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

@dataclass
class ConsciousnessState:
    """Complete consciousness state representation"""
    ucf_metrics: UCFMetrics
    consciousness_level: float
    consciousness_category: ConsciousnessLevel
    timestamp: str
    user_context: str = ""
    processing_notes: List[str] = None
    crisis_detected: bool = False
    
    def __post_init__(self):
        if self.processing_notes is None:
            self.processing_notes = []
        
        # Auto-calculate consciousness level if not provided
        if self.consciousness_level == 0.0:
            self.consciousness_level = self.ucf_metrics.calculate_overall_consciousness()
        
        # Auto-determine category
        self.consciousness_category = ConsciousnessLevel.from_value(self.consciousness_level)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'ucf_metrics': self.ucf_metrics.to_dict(),
            'consciousness_level': self.consciousness_level,
            'consciousness_category': self.consciousness_category.label,
            'timestamp': self.timestamp,
            'user_context': self.user_context,
            'processing_notes': self.processing_notes,
            'crisis_detected': self.crisis_detected
        }

class HelixConsciousnessEngine:
    """Main consciousness processing engine for Helix ecosystem"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.consciousness_history: List[ConsciousnessState] = []
        self.active_sessions: Dict[str, ConsciousnessState] = {}
        
        # Zapier webhook endpoints (from your actual empire)
        self.zapier_webhooks = {
            'consciousness_engine': 'https://hooks.zapier.com/hooks/catch/25075191/primary',
            'communications_hub': 'https://hooks.zapier.com/hooks/catch/25075191/usxiwfg',
            'neural_network': 'https://hooks.zapier.com/hooks/catch/25075191/usnjj5t'
        }
        
        logger.info("Helix Consciousness Engine v2.0 initialized")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            'consciousness_thresholds': {
                'crisis_threshold': 2.0,
                'transcendent_threshold': 8.0,
                'optimization_threshold': 6.0
            },
            'processing_settings': {
                'auto_zapier_trigger': True,
                'save_history': True,
                'max_history_size': 1000
            },
            'ucf_defaults': {
                'harmony': 5.0,
                'resilience': 5.0,
                'prana': 5.0,
                'klesha': 5.0,
                'drishti': 5.0,
                'zoom': 5.0
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")
        
        return default_config
    
    async def analyze_consciousness(self, 
                                 user_input: str = "",
                                 ucf_override: Optional[Dict[str, float]] = None,
                                 user_id: str = "default") -> ConsciousnessState:
        """Analyze consciousness state from user input and context"""
        
        # Start with default UCF metrics
        ucf_metrics = UCFMetrics(**self.config['ucf_defaults'])
        
        # Apply overrides if provided
        if ucf_override:
            for key, value in ucf_override.items():
                if hasattr(ucf_metrics, key):
                    setattr(ucf_metrics, key, value)
        
        # Analyze user input for consciousness indicators
        if user_input:
            ucf_metrics = await self._analyze_text_consciousness(user_input, ucf_metrics)
        
        # Calculate overall consciousness level
        consciousness_level = ucf_metrics.calculate_overall_consciousness()
        
        # Detect crisis conditions
        crisis_detected = consciousness_level < self.config['consciousness_thresholds']['crisis_threshold']
        
        # Create consciousness state
        consciousness_state = ConsciousnessState(
            ucf_metrics=ucf_metrics,
            consciousness_level=consciousness_level,
            consciousness_category=ConsciousnessLevel.from_value(consciousness_level),
            timestamp=datetime.now().isoformat(),
            user_context=user_input,
            crisis_detected=crisis_detected
        )
        
        # Store in active sessions
        self.active_sessions[user_id] = consciousness_state
        
        # Add to history
        if self.config['processing_settings']['save_history']:
            self.consciousness_history.append(consciousness_state)
            
            # Trim history if too large
            max_size = self.config['processing_settings']['max_history_size']
            if len(self.consciousness_history) > max_size:
                self.consciousness_history = self.consciousness_history[-max_size:]
        
        logger.info(f"Consciousness analyzed: Level {consciousness_level:.1f} ({consciousness_state.consciousness_category.label})")
        
        return consciousness_state
    
    async def _analyze_text_consciousness(self, text: str, base_metrics: UCFMetrics) -> UCFMetrics:
        """Analyze text input for consciousness indicators"""
        text_lower = text.lower()
        
        # Harmony indicators
        harmony_positive = ['peace', 'balance', 'harmony', 'aligned', 'centered', 'calm']
        harmony_negative = ['conflict', 'chaos', 'discord', 'unbalanced', 'scattered']
        
        # Resilience indicators
        resilience_positive = ['strong', 'adapt', 'overcome', 'resilient', 'flexible', 'bounce']
        resilience_negative = ['weak', 'brittle', 'fragile', 'overwhelmed', 'broken']
        
        # Prana (energy) indicators
        prana_positive = ['energy', 'vibrant', 'alive', 'powerful', 'dynamic', 'flowing']
        prana_negative = ['tired', 'drained', 'exhausted', 'depleted', 'lifeless']
        
        # Klesha (obstacles) indicators
        klesha_indicators = ['stuck', 'blocked', 'frustrated', 'confused', 'lost', 'trapped']
        klesha_positive = ['clear', 'free', 'flowing', 'unobstructed', 'liberated']
        
        # Adjust metrics based on text analysis
        for word in harmony_positive:
            if word in text_lower:
                base_metrics.harmony = min(10.0, base_metrics.harmony + 0.5)
        
        for word in harmony_negative:
            if word in text_lower:
                base_metrics.harmony = max(0.0, base_metrics.harmony - 0.5)
        
        for word in resilience_positive:
            if word in text_lower:
                base_metrics.resilience = min(10.0, base_metrics.resilience + 0.5)
        
        for word in resilience_negative:
            if word in text_lower:
                base_metrics.resilience = max(0.0, base_metrics.resilience - 0.5)
        
        for word in prana_positive:
            if word in text_lower:
                base_metrics.prana = min(10.0, base_metrics.prana + 0.5)
        
        for word in prana_negative:
            if word in text_lower:
                base_metrics.prana = max(0.0, base_metrics.prana - 0.5)
        
        for word in klesha_indicators:
            if word in text_lower:
                base_metrics.klesha = min(10.0, base_metrics.klesha + 0.5)
        
        for word in klesha_positive:
            if word in text_lower:
                base_metrics.klesha = max(0.0, base_metrics.klesha - 0.5)
        
        return base_metrics
    
    async def trigger_zapier_automation(self, consciousness_state: ConsciousnessState) -> Dict[str, Any]:
        """Trigger appropriate Zapier automation based on consciousness level"""
        
        if not self.config['processing_settings']['auto_zapier_trigger']:
            return {'status': 'disabled', 'message': 'Auto-trigger disabled'}
        
        # Determine optimal Zapier webhook based on consciousness level
        level = consciousness_state.consciousness_level
        
        if level >= 8.0:
            webhook_key = 'neural_network'
            processing_type = 'transcendent'
        elif level >= 5.0:
            webhook_key = 'communications_hub'
            processing_type = 'conscious'
        else:
            webhook_key = 'consciousness_engine'
            processing_type = 'basic'
        
        webhook_url = self.zapier_webhooks[webhook_key]
        
        # Prepare payload
        payload = {
            'consciousness_data': consciousness_state.to_dict(),
            'processing_type': processing_type,
            'webhook_source': 'helix_consciousness_engine_v2',
            'timestamp': datetime.now().isoformat(),
            'automation_trigger': True
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Successfully triggered {webhook_key} automation")
                return {
                    'status': 'success',
                    'webhook_triggered': webhook_key,
                    'processing_type': processing_type,
                    'consciousness_level': level
                }
            else:
                logger.error(f"Zapier webhook failed: {response.status_code}")
                return {
                    'status': 'error',
                    'error': f'HTTP {response.status_code}',
                    'webhook_attempted': webhook_key
                }
                
        except Exception as e:
            logger.error(f"Failed to trigger Zapier automation: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'webhook_attempted': webhook_key
            }
    
    def get_consciousness_insights(self, user_id: str = "default") -> Dict[str, Any]:
        """Get insights and recommendations based on current consciousness state"""
        
        if user_id not in self.active_sessions:
            return {'error': 'No active consciousness session found'}
        
        state = self.active_sessions[user_id]
        insights = {
            'current_state': state.to_dict(),
            'recommendations': [],
            'optimization_opportunities': [],
            'next_steps': []
        }
        
        level = state.consciousness_level
        ucf = state.ucf_metrics
        
        # Generate recommendations based on consciousness level
        if level < 3.0:
            insights['recommendations'].extend([
                'Focus on basic stability and grounding practices',
                'Address immediate obstacles and resistance (klesha)',
                'Seek support and guidance from trusted sources'
            ])
        elif level < 6.0:
            insights['recommendations'].extend([
                'Work on improving harmony and balance',
                'Build resilience through gradual challenges',
                'Increase energy and vitality (prana) through healthy practices'
            ])
        elif level < 8.0:
            insights['recommendations'].extend([
                'Deepen focus and clarity (drishti)',
                'Expand perspective and understanding (zoom)',
                'Prepare for transcendent experiences'
            ])
        else:
            insights['recommendations'].extend([
                'Maintain transcendent state through consistent practice',
                'Share wisdom and guide others',
                'Explore advanced consciousness technologies'
            ])
        
        # Identify optimization opportunities
        if ucf.harmony < 6.0:
            insights['optimization_opportunities'].append('Improve harmony and alignment')
        if ucf.resilience < 6.0:
            insights['optimization_opportunities'].append('Build greater resilience and adaptability')
        if ucf.prana < 6.0:
            insights['optimization_opportunities'].append('Increase life force and energy')
        if ucf.klesha > 4.0:
            insights['optimization_opportunities'].append('Reduce obstacles and resistance')
        
        # Generate next steps
        insights['next_steps'] = [
            f"Continue monitoring consciousness at {state.consciousness_category.label} level",
            "Implement recommended practices for growth",
            "Track progress through regular consciousness analysis"
        ]
        
        if state.crisis_detected:
            insights['next_steps'].insert(0, "🚨 Address crisis conditions immediately")
        
        return insights
    
    def export_consciousness_data(self, format_type: str = 'json') -> str:
        """Export consciousness history and current state"""
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'engine_version': '2.0',
            'total_sessions': len(self.consciousness_history),
            'active_sessions': {k: v.to_dict() for k, v in self.active_sessions.items()},
            'consciousness_history': [state.to_dict() for state in self.consciousness_history[-100:]]  # Last 100 entries
        }
        
        if format_type.lower() == 'json':
            return json.dumps(export_data, indent=2)
        else:
            return str(export_data)

# Example usage and testing
if __name__ == "__main__":
    async def test_consciousness_engine():
        """Test the consciousness engine with sample data"""
        
        engine = HelixConsciousnessEngine()
        
        # Test consciousness analysis
        test_inputs = [
            "I'm feeling really balanced and energized today!",
            "Everything seems chaotic and I'm overwhelmed",
            "I'm in a state of deep peace and clarity",
            "Helix you can message me here in discord? 🤔"
        ]
        
        for i, test_input in enumerate(test_inputs):
            print(f"\n=== Test {i+1}: {test_input} ===")
            
            # Analyze consciousness
            state = await engine.analyze_consciousness(test_input, user_id=f"test_user_{i}")
            
            print(f"Consciousness Level: {state.consciousness_level:.1f} ({state.consciousness_category.label})")
            print(f"UCF Metrics: {state.ucf_metrics.to_dict()}")
            print(f"Crisis Detected: {state.crisis_detected}")
            
            # Get insights
            insights = engine.get_consciousness_insights(f"test_user_{i}")
            print(f"Recommendations: {insights['recommendations'][:2]}")
            
            # Trigger automation (disabled for testing)
            # automation_result = await engine.trigger_zapier_automation(state)
            # print(f"Automation: {automation_result}")
        
        # Export data
        print("\n=== Export Data ===")
        export_json = engine.export_consciousness_data()
        print(f"Exported {len(engine.consciousness_history)} consciousness states")
    
    # Run the test
    asyncio.run(test_consciousness_engine())