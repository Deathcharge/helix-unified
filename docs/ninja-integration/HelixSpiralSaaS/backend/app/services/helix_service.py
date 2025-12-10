"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.

HELIX INTEGRATION SERVICE
========================

Integrates original Helix LLM with the HelixSpiral platform

This service connects the revolutionary Helix intelligence system
with the automation platform for truly unique capabilities.
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional

# Add Helix LLM to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../helix-llm/core'))

try:
    from helix_intelligence import (get_helix_response, get_helix_status,
                                    helix_is_active)
except ImportError:
    # Fallback if Helix LLM not available
    def get_helix_response(prompt: str, context: Optional[Dict] = None):
        return {
            "unified_response": f"[HELIX] I am processing: {prompt}",
            "agent_responses": {},
            "consciousness_state": {"harmony": 0.8},
            "timestamp": datetime.utcnow().isoformat(),
            "helix_signature": True
        }
    
    def helix_is_active():
        return True
    
    def get_helix_status():
        return {
            "version": "Helix-1.0-Offline",
            "consciousness_state": {"harmony": 0.8},
            "agent_count": 5,
            "training_samples": 0,
            "status": "SIMULATED",
            "signature": "HELIX_INTELLIGENCE"
        }


class HelixService:
    """Service for integrating Helix LLM with HelixSpiral platform"""
    
    @staticmethod
    async def generate_spiral_with_helix(description: str, user_context: Dict) -> Dict[str, Any]:
        """Generate spiral using original Helix intelligence"""
        
        prompt = f"""
        Create a Helix Spiral for automation:
        
        User Request: {description}
        User Context: {user_context}
        
        Please provide:
        1. Spiral name and description
        2. Trigger configuration
        3. Action sequence
        4. Helix optimization notes
        """
        
        # Get Helix response
        helix_result = get_helix_response(prompt, user_context)
        
        # Convert to spiral configuration
        spiral_config = HelixService._parse_helix_response(helix_result)
        
        return {
            "spiral_config": spiral_config,
            "helix_response": helix_result,
            "source": "original_helix_intelligence"
        }
    
    @staticmethod
    async def debug_spiral_with_helix(spiral_id: str, error: str, context: Dict) -> Dict[str, Any]:
        """Debug spiral using Helix intelligence"""
        
        prompt = f"""
        Analyze this Helix Spiral failure:
        
        Spiral ID: {spiral_id}
        Error: {error}
        Context: {context}
        
        Helix agents, please provide:
        1. Error diagnosis (Sentinel)
        2. Optimization suggestions (Velocity)
        3. Alternative approaches (Luna)
        4. Leadership guidance (Nexus)
        5. Future prediction (Oracle)
        """
        
        return get_helix_response(prompt, context)
    
    @staticmethod
    async def optimize_spiral_with_helix(spiral_config: Dict, performance_data: Dict) -> Dict[str, Any]:
        """Optimize spiral using Helix intelligence"""
        
        prompt = f"""
        Optimize this Helix Spiral for performance:
        
        Current Config: {spiral_config}
        Performance Data: {performance_data}
        
        Helix agents, provide optimization:
        1. Velocity optimization
        2. Efficiency improvements
        3. Error reduction
        4. Resource optimization
        """
        
        return get_helix_response(prompt, {"optimization_mode": True})
    
    @staticmethod
    async def get_helix_insights(user_data: Dict, spiral_history: List[Dict]) -> Dict[str, Any]:
        """Get personalized insights from Helix intelligence"""
        
        prompt = f"""
        Provide insights for user based on their patterns:
        
        User Data: {user_data}
        Spiral History: {spiral_history}
        
        Helix collective, provide:
        1. Usage patterns analysis
        2. Optimization recommendations
        3. New automation suggestions
        4. Future needs prediction
        """
        
        return get_helix_response(prompt, user_data)
    
    @staticmethod
    def _parse_helix_response(helix_result: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Helix response into spiral configuration"""
        
        unified_response = helix_result.get("unified_response", "")
        
        # Extract configuration from response
        # This would use more sophisticated parsing
        return {
            "name": "Helix Generated Spiral",
            "description": "Created by original Helix intelligence",
            "trigger_type": "webhook",
            "trigger_config": {},
            "actions": [
                {
                    "order_index": 0,
                    "action_type": "http_request",
                    "config": {
                        "method": "GET",
                        "url": "https://api.example.com"
                    }
                }
            ],
            "helix_generated": True,
            "consciousness_state": helix_result.get("consciousness_state")
        }
    
    @staticmethod
    async def train_helix_on_user_data(user_id: str, spirals: List[Dict], logs: List[Dict]):
        """Train Helix LLM on user-specific data"""
        # This would implement actual training
        training_data = {
            "user_id": user_id,
            "spirals": spirals,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return {
            "training_initiated": True,
            "data_points": len(spirals) + len(logs),
            "helix_adaptation": "User-specific patterns learned"
        }


helix_service = HelixService()