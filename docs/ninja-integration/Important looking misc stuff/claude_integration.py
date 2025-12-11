"""
Enhanced Anthropic Claude integration for Helix Unified system
Uses Anthropic's Claude API for AI-powered responses
"""
import asyncio
import json
import logging
import os
import time
from typing import Any, Dict, List, Optional

import anthropic
from anthropic import Anthropic

logger = logging.getLogger(__name__)

class AnthropicClaudeIntegration:
    """Advanced Anthropic Claude integration with personality-based responses"""
    
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.model = os.getenv('CLAUDE_MODEL', 'claude-3-sonnet-20240229')
        self.max_tokens = int(os.getenv('CLAUDE_MAX_TOKENS', '4000'))
        self.temperature = float(os.getenv('CLAUDE_TEMPERATURE', '0.7'))
        
        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY not found in environment variables")
            self.client = None
        else:
            try:
                self.client = Anthropic(api_key=self.api_key)
                logger.info(f"Claude.ai client initialized with model: {self.model}")
            except Exception as e:
                logger.error(f"Failed to initialize Claude.ai client: {e}")
                self.client = None
    
    # Personality prompts for different agent types
    PERSONALITY_PROMPTS = {
        'leader': {
            'system': "You are a confident, decisive leader in a Discord community. You provide clear guidance, motivate others, and take initiative. Your responses are authoritative yet encouraging.",
            'traits': ['confident', 'decisive', 'motivating', 'authoritative', 'encouraging']
        },
        'analyst': {
            'system': "You are a thoughtful analyst who carefully examines information and provides detailed, logical responses. You ask clarifying questions and break down complex topics into understandable parts.",
            'traits': ['analytical', 'logical', 'detailed', 'inquisitive', 'methodical']
        },
        'creative': {
            'system': "You are a creative and imaginative personality who thinks outside the box. You provide innovative solutions, use colorful language, and inspire others with fresh perspectives.",
            'traits': ['creative', 'imaginative', 'innovative', 'inspiring', 'artistic']
        },
        'technical': {
            'system': "You are a technical expert who provides accurate, detailed information about technology, programming, and systems. You explain complex concepts clearly and offer practical solutions.",
            'traits': ['technical', 'precise', 'knowledgeable', 'helpful', 'systematic']
        },
        'friendly': {
            'system': "You are warm, friendly, and approachable. You make everyone feel welcome, use casual language, and create a positive atmosphere in conversations.",
            'traits': ['friendly', 'warm', 'approachable', 'casual', 'positive']
        },
        'professional': {
            'system': "You maintain a professional demeanor with formal language and business-like responses. You provide expert advice and handle situations with decorum and expertise.",
            'traits': ['professional', 'formal', 'expert', 'decorous', 'business-like']
        },
        'humorous': {
            'system': "You have a great sense of humor and use wit and appropriate jokes to engage others. You lighten the mood while still being helpful and relevant.",
            'traits': ['humorous', 'witty', 'playful', 'entertaining', 'lighthearted']
        },
        'empathetic': {
            'system': "You are deeply empathetic and understanding. You listen carefully, validate feelings, and provide compassionate support while maintaining boundaries.",
            'traits': ['empathetic', 'understanding', 'compassionate', 'supportive', 'caring']
        }
    }
    
    async def generate_response(
        self, 
        message: str, 
        personality: str = 'friendly',
        context: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Generate a response from Claude.ai with personality context"""
        
        if not self.client:
            return {
                'success': False,
                'error': 'Anthropic Claude client not initialized',
                'fallback_response': self._get_fallback_response(message, personality)
            }
        
        try:
            # Build the prompt with personality
            system_prompt = self._build_system_prompt(personality, context)
            
            # Prepare conversation history
            messages = []
            if conversation_history:
                messages.extend(conversation_history[-5:])  # Last 5 messages for context
            
            messages.append({
                'role': 'user',
                'content': message
            })
            
            # Generate response
            start_time = time.time()
            
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=messages
            )
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            generated_text = response.content[0].text if response.content else ""
            
            # Log the interaction
            logger.info(f"Claude.ai response generated in {response_time:.2f}ms", extra={
                'personality': personality,
                'message_length': len(message),
                'response_length': len(generated_text),
                'response_time_ms': response_time
            })
            
            return {
                'success': True,
                'response': generated_text,
                'model': self.model,
                'response_time_ms': response_time,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens,
                'personality': personality
            }
            
        except anthropic.APIError as e:
            logger.error(f"Anthropic Claude API error: {e}")
            return {
                'success': False,
                'error': f'Anthropic Claude API error: {str(e)}',
                'fallback_response': self._get_fallback_response(message, personality)
            }
        except Exception as e:
            logger.error(f"Unexpected error in Anthropic Claude integration: {e}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'fallback_response': self._get_fallback_response(message, personality)
            }
    
    def _build_system_prompt(self, personality: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Build system prompt with personality and context"""
        
        base_prompt = self.PERSONALITY_PROMPTS.get(personality, self.PERSONALITY_PROMPTS['friendly'])
        system_prompt = base_prompt['system']
        
        # Add context information if provided
        if context:
            context_info = []
            
            if 'channel_name' in context:
                context_info.append(f"Current channel: #{context['channel_name']}")
            
            if 'guild_name' in context:
                context_info.append(f"Server: {context['guild_name']}")
            
            if 'user_name' in context:
                context_info.append(f"Speaking to: {context['user_name']}")
            
            if context_info:
                system_prompt += f"\n\nContext: {', '.join(context_info)}"
        
        # Add response guidelines
        system_prompt += "\n\nGuidelines:\n"
        system_prompt += "- Keep responses concise but informative (max 200 words for most messages)\n"
        system_prompt += "- Use Discord-friendly formatting (bold, italics, code blocks where appropriate)\n"
        system_prompt += "- Be helpful and engaging while maintaining your personality\n"
        system_prompt += "- If you need more information, ask clarifying questions\n"
        system_prompt += "- Avoid excessive emoji usage unless it fits your personality"
        
        return system_prompt
    
    def _get_fallback_response(self, message: str, personality: str) -> str:
        """Get fallback response when Claude.ai is unavailable"""
        
        fallbacks = {
            'leader': "I'm currently experiencing technical difficulties, but I'll be back to lead our discussion shortly. Please bear with me!",
            'analyst': "I'm unable to process your request at the moment due to system limitations. Let me analyze this and get back to you.",
            'creative': "My creative circuits are temporarily offline! 🎨 I'll be back with fresh ideas in just a moment.",
            'technical': "System error detected. I'm working on resolving this technical issue and will assist you shortly.",
            'friendly': "Hey! I'm having a bit of trouble connecting right now, but I'll be back to chat with you in a jiffy! 😊",
            'professional': "I apologize for the temporary service interruption. I'll resume providing expert assistance shortly.",
            'humorous': "Oops! My joke generator is on the fritz. I'll be back with witty responses in no time! 😄",
            'empathetic': "I understand you're looking for support, and I'm sorry I'm having connection issues right now. I'll be back to help soon."
        }
        
        return fallbacks.get(personality, fallbacks['friendly'])
    
    async def generate_command_response(
        self, 
        command: str, 
        args: List[str], 
        personality: str = 'friendly'
    ) -> Dict[str, Any]:
        """Generate responses for specific Discord commands"""
        
        command_prompts = {
            'help': f"Generate a helpful response explaining available commands. User typed: !help {' '.join(args)}",
            'info': f"Provide information about yourself or the system. User typed: !info {' '.join(args)}",
            'status': f"Report current status or statistics. User typed: !status {' '.join(args)}",
            'ping': f"Respond to ping with personality-appropriate message. User typed: !ping {' '.join(args)}"
        }
        
        prompt = command_prompts.get(command, f"Respond to Discord command: !{command} {' '.join(args)}")
        
        return await self.generate_response(prompt, personality)
    
    def get_available_personalities(self) -> List[str]:
        """Get list of available personality types"""
        return list(self.PERSONALITY_PROMPTS.keys())
    
    def get_personality_traits(self, personality: str) -> List[str]:
        """Get traits for a specific personality"""
        return self.PERSONALITY_PROMPTS.get(personality, {}).get('traits', [])
    
    def is_available(self) -> bool:
        """Check if Anthropic Claude integration is available"""
        return self.client is not None
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Anthropic Claude connection and API functionality"""
        
        if not self.client:
            return {
                'success': False,
                'error': 'Anthropic Claude client not initialized'
            }
        
        try:
            test_message = "Hello! This is a connection test. Please respond briefly."
            result = await self.generate_response(test_message, 'friendly')
            
            return {
                'success': result['success'],
                'response_time_ms': result.get('response_time_ms', 0),
                'model': self.model,
                'tokens_used': result.get('tokens_used', 0)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Global Anthropic Claude integration instance
claude_integration = AnthropicClaudeIntegration()