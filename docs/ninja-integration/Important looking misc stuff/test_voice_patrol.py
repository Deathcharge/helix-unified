"""
Tests for voice patrol system
"""
import asyncio
import os
import sys
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.error_handlers import VoiceError
from voice_patrol_system import VoicePatrolSystem


class TestVoicePatrolSystem:
    """Test cases for VoicePatrolSystem"""
    
    @pytest.fixture
    def voice_patrol(self):
        """Create VoicePatrolSystem instance for testing"""
        with patch('voice_patrol_system.discord') as mock_discord:
            mock_client = Mock()
            return VoicePatrolSystem(mock_client)
    
    @pytest.mark.asyncio
    async def test_join_voice_channel_success(self, voice_patrol):
        """Test successful voice channel join"""
        mock_channel = Mock()
        mock_channel.connect = AsyncMock(return_value=Mock())
        
        result = await voice_patrol.join_voice_channel(mock_channel)
        
        assert result is not None
        mock_channel.connect.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_join_voice_channel_failure(self, voice_patrol):
        """Test voice channel join failure"""
        mock_channel = Mock()
        mock_channel.connect = AsyncMock(side_effect=Exception("Connection failed"))
        
        with pytest.raises(VoiceError):
            await voice_patrol.join_voice_channel(mock_channel)
    
    @pytest.mark.asyncio
    async def test_leave_voice_channel(self, voice_patrol):
        """Test leaving voice channel"""
        mock_voice_client = Mock()
        mock_voice_client.disconnect = AsyncMock()
        voice_patrol.voice_clients[12345] = mock_voice_client
        
        await voice_patrol.leave_voice_channel(12345)
        
        mock_voice_client.disconnect.assert_called_once()
        assert 12345 not in voice_patrol.voice_clients
    
    @pytest.mark.asyncio
    async def test_speak_in_channel(self, voice_patrol):
        """Test speaking in voice channel"""
        mock_voice_client = Mock()
        mock_voice_client.play = AsyncMock()
        
        with patch('voice_patrol_system.tts_synthesize') as mock_tts:
            mock_tts.return_value = b"fake_audio_data"
            
            await voice_patrol.speak_in_channel(mock_voice_client, "Hello world")
            
            mock_tts.assert_called_once_with("Hello world")
            mock_voice_client.play.assert_called_once()
    
    def test_get_active_channels(self, voice_patrol):
        """Test getting active voice channels"""
        voice_patrol.voice_clients = {
            12345: Mock(channel=Mock(id=111, name="channel1")),
            67890: Mock(channel=Mock(id=222, name="channel2"))
        }
        
        channels = voice_patrol.get_active_channels()
        
        assert len(channels) == 2
        assert 111 in [c['id'] for c in channels]
        assert 222 in [c['id'] for c in channels]
    
    @pytest.mark.asyncio
    async def test_monitor_voice_activity(self, voice_patrol):
        """Test voice activity monitoring"""
        mock_guild = Mock()
        mock_guild.voice_channels = [
            Mock(name="vc1", members=[]),
            Mock(name="vc2", members=[Mock(bot=False), Mock(bot=True)])
        ]
        
        activity = await voice_patrol.monitor_voice_activity(mock_guild)
        
        assert 'total_channels' in activity
        assert 'active_channels' in activity
        assert 'user_count' in activity
        assert activity['total_channels'] == 2
        assert activity['user_count'] == 1  # Only non-bot users

class TestVoiceErrorHandling:
    """Test error handling in voice system"""
    
    @pytest.mark.asyncio
    async def test_tts_failure_handling(self):
        """Test handling of TTS synthesis failures"""
        mock_client = Mock()
        voice_patrol = VoicePatrolSystem(mock_client)
        
        with patch('voice_patrol_system.tts_synthesize') as mock_tts:
            mock_tts.side_effect = Exception("TTS failed")
            mock_voice_client = Mock()
            
            with pytest.raises(VoiceError):
                await voice_patrol.speak_in_channel(mock_voice_client, "Test")
    
    @pytest.mark.asyncio
    async def test_connection_timeout(self):
        """Test handling of connection timeouts"""
        mock_client = Mock()
        voice_patrol = VoicePatrolSystem(mock_client)
        mock_channel = Mock()
        mock_channel.connect = AsyncMock(side_effect=asyncio.TimeoutError())
        
        with pytest.raises(VoiceError):
            await voice_patrol.join_voice_channel(mock_channel)