"""
🖥️ Web OS Module
Browser-based operating system backend
- Terminal execution with sandbox security
- File system operations
- Real-time WebSocket communication
"""

from .file_system import FileInfo, FileSystemManager
from .file_system import router as file_system_router
from .terminal_executor import CommandResult, TerminalExecutor
from .terminal_executor import router as terminal_router

__all__ = [
    'terminal_router',
    'file_system_router',
    'TerminalExecutor',
    'CommandResult',
    'FileSystemManager',
    'FileInfo',
]
