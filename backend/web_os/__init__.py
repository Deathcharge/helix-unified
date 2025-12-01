"""
🖥️ Web OS Module
Browser-based operating system backend
- Terminal execution with sandbox security
- File system operations
- Real-time WebSocket communication
"""

from .terminal_executor import router as terminal_router
from .terminal_executor import TerminalExecutor, CommandResult
from .file_system import router as file_system_router
from .file_system import FileSystemManager, FileInfo

__all__ = [
    'terminal_router',
    'file_system_router',
    'TerminalExecutor',
    'CommandResult',
    'FileSystemManager',
    'FileInfo',
]
