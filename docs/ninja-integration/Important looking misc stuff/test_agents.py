"""
Tests for agent system
"""
import asyncio
import os
import sys
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_bot import AgentBot
from utils.error_handlers import AgentError, error_tracker


class TestAgentBot:
    """Test cases for AgentBot"""
    
    @pytest.fixture
    def agent_bot(self):
        """Create AgentBot instance for testing"""
        with patch('agent_bot.discord') as mock_discord:
            mock_client = Mock()
            agent_config = {
                'id': 'test_agent_001',
                'name': 'TestAgent',
                'personality': 'friendly',
                'token': 'fake_token'
            }
            return AgentBot(mock_client, agent_config)
    
    def test_agent_initialization(self, agent_bot):
        """Test agent initialization with config"""
        assert agent_bot.id == 'test_agent_001'
        assert agent_bot.name == 'TestAgent'
        assert agent_bot.personality == 'friendly'
        assert agent_bot.token == 'fake_token'
    
    @pytest.mark.asyncio
    async def test_agent_response_generation(self, agent_bot):
        """Test agent response generation"""
        test_message = "Hello, how are you?"
        
        with patch('agent_bot.llm_generate_response') as mock_llm:
            mock_llm.return_value = "I'm doing great, thanks for asking!"
            
            response = await agent_bot.generate_response(test_message)
            
            assert response == "I'm doing great, thanks for asking!"
            mock_llm.assert_called_once_with(
                test_message, 
                personality=agent_bot.personality
            )
    
    @pytest.mark.asyncio
    async def test_agent_command_handling(self, agent_bot):
        """Test agent command handling"""
        mock_message = Mock()
        mock_message.content = "!help"
        mock_message.author = Mock(bot=False)
        mock_message.channel = Mock(send=AsyncMock())
        
        await agent_bot.handle_command(mock_message)
        
        mock_message.channel.send.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_agent_ignores_bot_messages(self, agent_bot):
        """Test that agent ignores bot messages"""
        mock_message = Mock()
        mock_message.content = "Hello"
        mock_message.author = Mock(bot=True)
        mock_message.channel = Mock(send=AsyncMock())
        
        await agent_bot.on_message(mock_message)
        
        mock_message.channel.send.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_agent_error_handling(self, agent_bot):
        """Test agent error handling"""
        mock_message = Mock()
        mock_message.content = "test message"
        mock_message.author = Mock(bot=False)
        mock_message.channel = Mock(send=AsyncMock())
        
        with patch('agent_bot.llm_generate_response') as mock_llm:
            mock_llm.side_effect = Exception("LLM failed")
            
            # Should not raise exception, but handle gracefully
            await agent_bot.on_message(mock_message)
            
            # Check error was tracked
            assert error_tracker.error_counts.get('Exception', 0) > 0
    
    def test_agent_status_check(self, agent_bot):
        """Test agent status reporting"""
        agent_bot.is_active = True
        agent_bot.last_activity = "2024-01-01T12:00:00"
        
        status = agent_bot.get_status()
        
        assert status['id'] == 'test_agent_001'
        assert status['name'] == 'TestAgent'
        assert status['is_active'] is True
        assert 'last_activity' in status

class TestAgentCommunication:
    """Test agent-to-agent communication"""
    
    @pytest.mark.asyncio
    async def test_agent_message_relay(self):
        """Test message relay between agents"""
        mock_client = Mock()
        agent1_config = {'id': 'agent_001', 'name': 'Agent1', 'personality': 'leader'}
        agent2_config = {'id': 'agent_002', 'name': 'Agent2', 'personality': 'follower'}
        
        agent1 = AgentBot(mock_client, agent1_config)
        agent2 = AgentBot(mock_client, agent2_config)
        
        # Mock communication channel
        mock_channel = Mock()
        mock_channel.send = AsyncMock()
        
        with patch('agent_bot.get_agent_channel') as mock_get_channel:
            mock_get_channel.return_value = mock_channel
            
            await agent1.send_message_to_agent('agent_002', 'Hello from Agent1')
            
            mock_channel.send.assert_called_once()

class TestAgentPersonality:
    """Test agent personality system"""
    
    def test_personality_responses(self):
        """Test different personality response styles"""
        mock_client = Mock()
        
        personalities = {
            'friendly': {'tone': 'warm', 'style': 'casual'},
            'professional': {'tone': 'formal', 'style': 'business'},
            'technical': {'tone': 'precise', 'style': 'detailed'}
        }
        
        for personality, traits in personalities.items():
            config = {
                'id': f'agent_{personality}',
                'name': f'{personality.title()}Agent',
                'personality': personality
            }
            
            agent = AgentBot(mock_client, config)
            assert agent.personality == personality
            assert hasattr(agent, 'personality_traits')

class TestAgentMemory:
    """Test agent memory and learning system"""
    
    @pytest.mark.asyncio
    async def test_conversation_memory(self):
        """Test conversation memory storage"""
        mock_client = Mock()
        agent_config = {
            'id': 'test_memory_agent',
            'name': 'MemoryAgent',
            'personality': 'analytical'
        }
        
        agent = AgentBot(mock_client, agent_config)
        
        # Simulate conversation
        test_messages = [
            {'user': 'Hello', 'agent': 'Hi there!'},
            {'user': 'How are you?', 'agent': 'I am doing well!'}
        ]
        
        for msg in test_messages:
            await agent.store_conversation(msg['user'], msg['agent'])
        
        memory = agent.get_conversation_history()
        assert len(memory) == len(test_messages)
        assert memory[0]['user_input'] == 'Hello'
        assert memory[1]['agent_response'] == 'I am doing well!'