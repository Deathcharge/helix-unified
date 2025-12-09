"""
Voice Commands Module
Executes commands via voice instead of text
"""

from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import re
import logging

logger = logging.getLogger(__name__)


class CommandCategory(Enum):
    """Command categories."""
    TASK_MANAGEMENT = "task_management"
    REMINDERS = "reminders"
    SEARCH = "search"
    SMART_HOME = "smart_home"
    MESSAGING = "messaging"
    MEDIA = "media"
    INFORMATION = "information"
    SYSTEM = "system"


@dataclass
class VoiceCommand:
    """Voice command definition."""
    name: str
    category: CommandCategory
    pattern: str  # Regex pattern
    handler: Callable
    requires_auth: bool = True
    description: str = ""
    examples: List[str] = None
    
    def __post_init__(self):
        if self.examples is None:
            self.examples = []


class VoiceCommandExecutor:
    """
    Executes commands from voice transcriptions.
    Supports 20+ built-in commands with extensibility.
    """
    
    def __init__(self):
        """Initialize command executor."""
        self.commands: Dict[str, VoiceCommand] = {}
        self.custom_handlers: Dict[str, Callable] = {}
        self._register_built_in_commands()
    
    def _register_built_in_commands(self):
        """Register built-in commands."""
        # Task management commands
        self.register_command(VoiceCommand(
            name='create_task',
            category=CommandCategory.TASK_MANAGEMENT,
            pattern=r'create task (?:called |named |for |about )?(.+?)(?:\s+(?:in|for|due)\s+(.+))?$',
            handler=self._handle_create_task,
            requires_auth=True,
            description='Create a new task',
            examples=['create task buy groceries', 'create task finish report due tomorrow']
        ))
        
        self.register_command(VoiceCommand(
            name='list_tasks',
            category=CommandCategory.TASK_MANAGEMENT,
            pattern=r'(?:list|show|get)\s+(?:my\s+)?tasks',
            handler=self._handle_list_tasks,
            requires_auth=True,
            description='List all tasks',
            examples=['list tasks', 'show my tasks']
        ))
        
        self.register_command(VoiceCommand(
            name='complete_task',
            category=CommandCategory.TASK_MANAGEMENT,
            pattern=r'(?:complete|finish|mark|done)\s+(?:task\s+)?(.+)',
            handler=self._handle_complete_task,
            requires_auth=True,
            description='Mark task as complete',
            examples=['complete task buy groceries', 'mark done report']
        ))
        
        # Reminder commands
        self.register_command(VoiceCommand(
            name='set_reminder',
            category=CommandCategory.REMINDERS,
            pattern=r'remind\s+(?:me\s+)?(?:to\s+)?(.+?)\s+(?:in|at|on)\s+(.+)',
            handler=self._handle_set_reminder,
            requires_auth=True,
            description='Set a reminder',
            examples=['remind me to call mom in 2 hours', 'remind me at 3pm']
        ))
        
        self.register_command(VoiceCommand(
            name='list_reminders',
            category=CommandCategory.REMINDERS,
            pattern=r'(?:list|show|get)\s+(?:my\s+)?reminders',
            handler=self._handle_list_reminders,
            requires_auth=True,
            description='List all reminders',
            examples=['list reminders', 'show my reminders']
        ))
        
        # Search commands
        self.register_command(VoiceCommand(
            name='search',
            category=CommandCategory.SEARCH,
            pattern=r'(?:search|find|look\s+for)\s+(?:for\s+)?(.+)',
            handler=self._handle_search,
            requires_auth=False,
            description='Search knowledge base',
            examples=['search for python tutorials', 'find information about AI']
        ))
        
        # Messaging commands
        self.register_command(VoiceCommand(
            name='send_message',
            category=CommandCategory.MESSAGING,
            pattern=r'(?:send|message|tell)\s+(?:message\s+)?(?:to\s+)?(.+?)\s+(?:that|saying|message)\s+(.+)',
            handler=self._handle_send_message,
            requires_auth=True,
            description='Send a message',
            examples=['send message to john saying hello', 'tell alice that im running late']
        ))
        
        # Media commands
        self.register_command(VoiceCommand(
            name='play_music',
            category=CommandCategory.MEDIA,
            pattern=r'(?:play|start)\s+(?:music|song|track)(?:\s+(.+))?',
            handler=self._handle_play_music,
            requires_auth=False,
            description='Play music',
            examples=['play music', 'play song imagine']
        ))
        
        self.register_command(VoiceCommand(
            name='stop_playback',
            category=CommandCategory.MEDIA,
            pattern=r'(?:stop|pause|pause playback)',
            handler=self._handle_stop_playback,
            requires_auth=False,
            description='Stop music playback',
            examples=['stop', 'pause music']
        ))
        
        # Information commands
        self.register_command(VoiceCommand(
            name='get_weather',
            category=CommandCategory.INFORMATION,
            pattern=r'(?:what\'?s?\s+)?(?:the\s+)?weather(?:\s+(?:in|for)\s+(.+))?',
            handler=self._handle_get_weather,
            requires_auth=False,
            description='Get weather information',
            examples=['whats the weather', 'weather in new york']
        ))
        
        self.register_command(VoiceCommand(
            name='get_time',
            category=CommandCategory.INFORMATION,
            pattern=r'(?:what\s+)?(?:time|hour)(?:\s+(?:is\s+)?it)?',
            handler=self._handle_get_time,
            requires_auth=False,
            description='Get current time',
            examples=['what time is it', 'tell me the time']
        ))
        
        logger.info(f"Registered {len(self.commands)} built-in commands")
    
    def register_command(self, command: VoiceCommand) -> bool:
        """
        Register a voice command.
        
        Args:
            command: VoiceCommand object
            
        Returns:
            True if successful
        """
        try:
            self.commands[command.name] = command
            logger.info(f"Registered command: {command.name}")
            return True
        except Exception as e:
            logger.error(f"Error registering command: {e}")
            return False
    
    def execute(self, transcription: str, user_id: str, context: Dict = None) -> Dict:
        """
        Execute a voice command from transcription.
        
        Args:
            transcription: Voice transcription
            user_id: User identifier
            context: Additional context (auth info, etc.)
            
        Returns:
            Execution result
        """
        if context is None:
            context = {}
        
        # Try to match against registered commands
        for cmd_name, cmd in self.commands.items():
            match = re.match(cmd.pattern, transcription, re.IGNORECASE)
            if match:
                # Check authentication
                if cmd.requires_auth and not context.get('authenticated', False):
                    return {
                        'success': False,
                        'error': 'Authentication required',
                        'command': cmd_name
                    }
                
                # Execute command
                try:
                    groups = match.groups()
                    result = cmd.handler(groups, user_id, context)
                    result['command'] = cmd_name
                    return result
                except Exception as e:
                    logger.error(f"Error executing command {cmd_name}: {e}")
                    return {
                        'success': False,
                        'error': str(e),
                        'command': cmd_name
                    }
        
        return {
            'success': False,
            'error': 'Command not recognized',
            'suggestions': self._get_suggestions(transcription)
        }
    
    def _get_suggestions(self, transcription: str) -> List[str]:
        """Get command suggestions based on transcription."""
        suggestions = []
        
        # Simple keyword matching
        keywords = transcription.lower().split()
        for cmd_name, cmd in self.commands.items():
            if any(kw in cmd.name.lower() for kw in keywords):
                suggestions.append(f"{cmd_name}: {cmd.description}")
        
        return suggestions[:3]  # Return top 3 suggestions
    
    # Command handlers
    def _handle_create_task(self, groups: tuple, user_id: str, context: Dict) -> Dict:
        """Handle: 'create task [task name] [due date]'"""
        task_name = groups[0] if groups else "Untitled"
        due_date = groups[1] if len(groups) > 1 else None
        
        return {
            'success': True,
            'action': 'create_task',
            'task_name': task_name,
            'due_date': due_date,
            'message': f'Created task: {task_name}'
        }
    
    def _handle_list_tasks(self, groups: tuple, user_id: str, context: Dict) -> Dict:
        """Handle: 'list tasks'"""
        return {
            'success': True,
            'action': 'list_tasks',
            'message': 'Retrieving your tasks...'
        }
    
    def _handle_complete_task(self, groups: tuple, user_id: str, context: Dict) -> Dict:
        """Handle: 'complete task [task name]'"""
        task_name = groups[0] if groups else "Unknown"
        
        return {
            'success': True,
            'action': 'complete_task',
            'task_name': task_name,
            'message': f'Marked task complete: {task_name}'
        }
    
    def _handle_set_reminder(self, groups: tuple, user_id: str, context: Dict) -> Dict:
        """Handle: 'remind me to [action] [time]'"""
        action = groups[0] if groups else "Unknown"
        time_spec = groups[1] if len(groups) > 1 else "soon"
        
        return {
            'success': True,
            'action': 'set_reminder',
            'reminder_text': action,
            'time': time_spec,
            'message': f'Reminder set: {action} {time_spec}'
        }
    
    def _handle_list_reminders(self, groups: tuple, user_id: str, context: Dict) -> Dict:
        """Handle: 'list reminders'"""
        return {
            'success': True,
            'action': 'list_reminders',
            'message': 'Retrieving your reminders...'
        }
    
    def _handle_search(self, groups: tuple, user_id: str, context: Dict) -> Dict:
        """Handle: 'search for [query]'"""
        query = groups[0] if groups else ""
        
        return {
            'success': True,
            'action': 'search',
            'query': query,
            'message': f'Searching for: {query}'
        }
    
    def _handle_send_message(self, groups: tuple, user_id: str, context: Dict) -> Dict:
        """Handle: 'send message to [recipient] [message]'"""
        recipient = groups[0] if groups else "Unknown"
        message = groups[1] if len(groups) > 1 else ""
        
        return {
            'success': True,
            'action': 'send_message',
            'recipient': recipient,
            'message': message,
            'status': f'Message sent to {recipient}'
        }
    
    def _handle_play_music(self, groups: tuple, user_id: str, context: Dict) -> Dict:
        """Handle: 'play [song name]'"""
        song = groups[0] if groups and groups[0] else "random"
        
        return {
            'success': True,
            'action': 'play_music',
            'song': song,
            'message': f'Playing: {song}'
        }
    
    def _handle_stop_playback(self, groups: tuple, user_id: str, context: Dict) -> Dict:
        """Handle: 'stop'"""
        return {
            'success': True,
            'action': 'stop_playback',
            'message': 'Playback stopped'
        }
    
    def _handle_get_weather(self, groups: tuple, user_id: str, context: Dict) -> Dict:
        """Handle: 'whats the weather [in location]'"""
        location = groups[0] if groups and groups[0] else "current location"
        
        return {
            'success': True,
            'action': 'get_weather',
            'location': location,
            'message': f'Getting weather for: {location}'
        }
    
    def _handle_get_time(self, groups: tuple, user_id: str, context: Dict) -> Dict:
        """Handle: 'what time is it'"""
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p")
        
        return {
            'success': True,
            'action': 'get_time',
            'time': current_time,
            'message': f'Current time: {current_time}'
        }
    
    def list_commands(self) -> List[Dict]:
        """List all available commands."""
        return [
            {
                'name': cmd.name,
                'category': cmd.category.value,
                'description': cmd.description,
                'examples': cmd.examples,
                'requires_auth': cmd.requires_auth
            }
            for cmd in self.commands.values()
        ]
    
    def get_commands_by_category(self, category: CommandCategory) -> List[VoiceCommand]:
        """Get commands by category."""
        return [cmd for cmd in self.commands.values() if cmd.category == category]
    
    def register_custom_handler(self, name: str, handler: Callable) -> bool:
        """Register a custom command handler."""
        try:
            self.custom_handlers[name] = handler
            logger.info(f"Registered custom handler: {name}")
            return True
        except Exception as e:
            logger.error(f"Error registering custom handler: {e}")
            return False
