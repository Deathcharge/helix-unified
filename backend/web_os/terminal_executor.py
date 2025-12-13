"""
🖥️ Web OS Terminal Executor
Real command execution backend for browser-based terminal
Supports: ls, pwd, cd, cat, mkdir, rm, and basic shell operations
With security sandbox to prevent dangerous operations
"""

import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

# Security: Block shell metacharacters to prevent command injection
BLOCKED_CHARS = re.compile(r'[;&|`$<>(){}\\]')
MAX_COMMAND_LENGTH = 1000

# ============================================================================
# COMMAND DEFINITIONS
# ============================================================================

ALLOWED_COMMANDS = {
    'ls': {'description': 'List directory contents', 'args': '[path]'},
    'pwd': {'description': 'Print working directory', 'args': ''},
    'cd': {'description': 'Change directory', 'args': '<path>'},
    'cat': {'description': 'Display file contents', 'args': '<file>'},
    'mkdir': {'description': 'Create directory', 'args': '<name>'},
    'rm': {'description': 'Remove file', 'args': '<file>'},
    'echo': {'description': 'Print text', 'args': '<text>'},
    'touch': {'description': 'Create file', 'args': '<file>'},
    'whoami': {'description': 'Current user', 'args': ''},
    'date': {'description': 'Current date/time', 'args': ''},
    'clear': {'description': 'Clear screen', 'args': ''},
    'help': {'description': 'Show available commands', 'args': ''},
}

DANGEROUS_COMMANDS = {
    'rm -rf',
    'sudo',
    'su',
    'chmod',
    'chown',
    'shutdown',
    'reboot',
    'dd',
    'mkfs',
    'format',
    'mount',
    'umount',
}

DANGEROUS_PATHS = {
    '/',
    '/root',
    '/etc',
    '/sys',
    '/proc',
    '/dev',
    '/bin',
    '/usr/bin',
    '/usr/sbin',
    '/var',
    '/boot',
}

# ============================================================================
# COMMAND EXECUTION
# ============================================================================


@dataclass
class CommandResult:
    """Result of command execution"""

    output: str
    error: str
    exit_code: int
    command: str
    success: bool


class TerminalExecutor:
    """Sandbox terminal executor for Web OS"""

    def __init__(self, home_dir: str = '/home/helix'):
        self.current_dir = home_dir
        self.home_dir = home_dir
        self.command_history: List[str] = []

        # Ensure home directory exists
        Path(self.home_dir).mkdir(parents=True, exist_ok=True)

    def validate_command(self, command: str) -> tuple[bool, str]:
        """Check if command is allowed"""
        # Check command length (prevent DoS)
        if len(command) > MAX_COMMAND_LENGTH:
            return False, f"❌ Command too long (max {MAX_COMMAND_LENGTH} chars)"

        cmd_name = command.split()[0].lower()

        # Check for shell metacharacters (command injection prevention)
        if BLOCKED_CHARS.search(command):
            return False, "❌ Command contains invalid characters (;|&$`<>(){}\\)"

        # Check for dangerous commands
        for dangerous in DANGEROUS_COMMANDS:
            if dangerous in command:
                return False, f"❌ Command '{dangerous}' is not allowed for security"

        # Check if command is allowed
        if cmd_name not in ALLOWED_COMMANDS:
            return False, f"❌ Unknown command: {cmd_name}. Type 'help' for available commands."

        return True, ''

    def validate_path(self, path: str) -> tuple[bool, str]:
        """Validate path is within sandbox"""
        # Check for null bytes (security bypass attempt)
        if '\0' in path:
            logger.warning(f"Null byte detected in path: {repr(path)}")
            return False, f"❌ Invalid path: null byte detected"  # noqa

        # Normalize path to prevent traversal
        path = os.path.normpath(path)

        # Check for remaining traversal attempts
        if '..' in path:
            logger.warning(f"Path traversal attempt detected: {path}")
            return False, "❌ Path traversal not allowed"

        # Resolve to absolute path
        if path.startswith('/'):
            abs_path = path
        else:
            abs_path = os.path.join(self.current_dir, path)

        abs_path = os.path.abspath(abs_path)

        # Check if path is within allowed directories
        if not abs_path.startswith(self.home_dir):
            logger.warning(f"Path access outside sandbox: {abs_path}")
            return False, f"❌ Access denied: {path}"

        # Check for symlinks pointing outside sandbox
        try:
            if os.path.islink(abs_path):
                real_path = os.path.realpath(abs_path)
                if not real_path.startswith(self.home_dir):
                    logger.warning(f"Symlink points outside sandbox: {abs_path} -> {real_path}")
                    return False, f"❌ Symlink points outside sandbox"  # noqa
        except (OSError, RuntimeError):
            return False, f"❌ Invalid path: {path}"

        # Check for dangerous paths
        for dangerous in DANGEROUS_PATHS:
            if abs_path == dangerous or abs_path.startswith(dangerous + '/'):
                return False, f"❌ Access to {dangerous} is restricted"

        return True, ''

    def execute(self, command: str) -> CommandResult:
        """Execute a command safely"""
        command = command.strip()

        if not command:
            return CommandResult('', '', 0, command, True)

        # Validate command
        allowed, error_msg = self.validate_command(command)
        if not allowed:
            return CommandResult('', error_msg, 1, command, False)

        # Add to history
        self.command_history.append(command)

        # Parse command
        parts = command.split()
        cmd_name = parts[0].lower()

        # Handle built-in commands
        if cmd_name == 'help':
            return self._cmd_help()
        elif cmd_name == 'pwd':
            return self._cmd_pwd()
        elif cmd_name == 'cd':
            return self._cmd_cd(parts[1] if len(parts) > 1 else '')
        elif cmd_name == 'ls':
            return self._cmd_ls(parts[1:] if len(parts) > 1 else [])
        elif cmd_name == 'cat':
            return self._cmd_cat(parts[1] if len(parts) > 1 else '')
        elif cmd_name == 'mkdir':
            return self._cmd_mkdir(parts[1] if len(parts) > 1 else '')
        elif cmd_name == 'touch':
            return self._cmd_touch(parts[1] if len(parts) > 1 else '')
        elif cmd_name == 'rm':
            return self._cmd_rm(parts[1] if len(parts) > 1 else '')
        elif cmd_name == 'echo':
            return self._cmd_echo(' '.join(parts[1:]))
        elif cmd_name == 'clear':
            return CommandResult('', '', 0, command, True)
        elif cmd_name == 'whoami':
            return self._cmd_whoami()
        elif cmd_name == 'date':
            return self._cmd_date()
        else:
            return CommandResult('', f"Command not implemented: {cmd_name}", 1, command, False)

    def _cmd_pwd(self) -> CommandResult:
        """Print working directory"""
        return CommandResult(self.current_dir, '', 0, 'pwd', True)

    def _cmd_cd(self, path: str) -> CommandResult:
        """Change directory"""
        if not path:
            self.current_dir = self.home_dir
            return CommandResult('', '', 0, 'cd', True)

        # Validate path
        valid, error = self.validate_path(path)
        if not valid:
            return CommandResult('', error, 1, 'cd', False)

        # Resolve path
        if path.startswith('/'):
            new_dir = path
        else:
            new_dir = os.path.join(self.current_dir, path)

        new_dir = os.path.abspath(new_dir)

        # Check if directory exists
        if not os.path.isdir(new_dir):
            return CommandResult('', f"❌ Directory not found: {path}", 1, 'cd', False)

        self.current_dir = new_dir
        return CommandResult('', '', 0, 'cd', True)

    def _cmd_ls(self, args: List[str]) -> CommandResult:
        """List directory contents"""
        path = args[0] if args else self.current_dir

        try:
            # SECURITY: Resolve path first, then validate to prevent TOCTOU
            if not path.startswith('/'):
                path = os.path.join(self.current_dir, path)

            path = os.path.abspath(path)

            # Validate AFTER path resolution
            valid, error = self.validate_path(path)
            if not valid:
                return CommandResult('', error, 1, 'ls', False)

            if not os.path.exists(path):
                return CommandResult('', f"❌ Path not found: {path}", 1, 'ls', False)

            if os.path.isfile(path):
                # If file, show file info
                size = os.path.getsize(path)
                return CommandResult(f"{path} ({size} bytes)", '', 0, 'ls', True)

            # List directory
            items = sorted(os.listdir(path))
            output_lines = []

            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    output_lines.append(f"📁 {item}/")
                else:
                    try:
                        size = os.path.getsize(item_path)
                        output_lines.append(f"📄 {item} ({size}B)")
                    except (OSError, IOError):
                        output_lines.append(f"📄 {item}")

            output = '\n'.join(output_lines) if output_lines else "(empty directory)"
            return CommandResult(output, '', 0, 'ls', True)

        except Exception as e:
            return CommandResult('', f"❌ Error: {str(e)}", 1, 'ls', False)

    def _cmd_cat(self, file: str) -> CommandResult:
        """Display file contents"""
        if not file:
            return CommandResult('', "❌ Usage: cat <file>", 1, 'cat', False)

        try:
            # SECURITY: Resolve path first, then validate to prevent TOCTOU
            if not file.startswith('/'):
                file = os.path.join(self.current_dir, file)

            file = os.path.abspath(file)

            # Validate AFTER path resolution
            valid, error = self.validate_path(file)
            if not valid:
                return CommandResult('', error, 1, 'cat', False)

            if not os.path.exists(file):
                return CommandResult('', f"❌ File not found: {file}", 1, 'cat', False)

            if os.path.isdir(file):
                return CommandResult('', f"❌ {file} is a directory", 1, 'cat', False)

            with open(file, 'r') as f:
                content = f.read()

            return CommandResult(content, '', 0, 'cat', True)

        except Exception as e:
            return CommandResult('', f"❌ Error reading file: {str(e)}", 1, 'cat', False)

    def _cmd_mkdir(self, name: str) -> CommandResult:
        """Create directory"""
        if not name:
            return CommandResult('', "❌ Usage: mkdir <name>", 1, 'mkdir', False)

        try:
            # SECURITY: Resolve path first, then validate to prevent TOCTOU
            if not name.startswith('/'):
                name = os.path.join(self.current_dir, name)

            name = os.path.abspath(name)

            # Validate AFTER path resolution
            valid, error = self.validate_path(name)
            if not valid:
                return CommandResult('', error, 1, 'mkdir', False)

            if os.path.exists(name):
                return CommandResult('', f"❌ Already exists: {name}", 1, 'mkdir', False)

            os.makedirs(name, exist_ok=True)
            return CommandResult(f"✅ Created directory: {name}", '', 0, 'mkdir', True)

        except Exception as e:
            return CommandResult('', f"❌ Error creating directory: {str(e)}", 1, 'mkdir', False)

    def _cmd_touch(self, file: str) -> CommandResult:
        """Create file"""
        if not file:
            return CommandResult('', "❌ Usage: touch <file>", 1, 'touch', False)

        try:
            # SECURITY: Resolve path first, then validate to prevent TOCTOU
            if not file.startswith('/'):
                file = os.path.join(self.current_dir, file)

            file = os.path.abspath(file)

            # Validate AFTER path resolution
            valid, error = self.validate_path(file)
            if not valid:
                return CommandResult('', error, 1, 'touch', False)

            Path(file).touch()
            return CommandResult(f"✅ Created file: {file}", '', 0, 'touch', True)

        except Exception as e:
            return CommandResult('', f"❌ Error creating file: {str(e)}", 1, 'touch', False)

    def _cmd_rm(self, file: str) -> CommandResult:
        """Remove file"""
        if not file:
            return CommandResult('', "❌ Usage: rm <file>", 1, 'rm', False)

        try:
            # SECURITY: Resolve path first, then validate to prevent TOCTOU
            if not file.startswith('/'):
                file = os.path.join(self.current_dir, file)

            file = os.path.abspath(file)

            # Validate AFTER path resolution
            valid, error = self.validate_path(file)
            if not valid:
                return CommandResult('', error, 1, 'rm', False)

            if not os.path.exists(file):
                return CommandResult('', f"❌ File not found: {file}", 1, 'rm', False)

            os.remove(file)
            return CommandResult(f"✅ Removed: {file}", '', 0, 'rm', True)

        except Exception as e:
            return CommandResult('', f"❌ Error removing file: {str(e)}", 1, 'rm', False)

    def _cmd_echo(self, text: str) -> CommandResult:
        """Print text"""
        return CommandResult(text, '', 0, 'echo', True)

    def _cmd_whoami(self) -> CommandResult:
        """Get current user"""
        return CommandResult('helix-user', '', 0, 'whoami', True)

    def _cmd_date(self) -> CommandResult:
        """Get current date/time"""
        from datetime import datetime

        return CommandResult(datetime.now().isoformat(), '', 0, 'date', True)

    def _cmd_help(self) -> CommandResult:
        """Show available commands"""
        lines = ['Available commands:']

        for cmd, info in ALLOWED_COMMANDS.items():
            lines.append(f"  {cmd} {info['args']:<20} - {info['description']}")

        return CommandResult('\n'.join(lines), '', 0, 'help', True)


# ============================================================================
# FASTAPI INTEGRATION
# ============================================================================


router = APIRouter(prefix='/api/web-os', tags=['Web OS'])

# Global executors per user
executors: Dict[str, TerminalExecutor] = {}


def get_executor(user_id: str) -> TerminalExecutor:
    """Get or create executor for user"""
    if user_id not in executors:
        executors[user_id] = TerminalExecutor()

    return executors[user_id]


@router.websocket('/ws/terminal')
async def websocket_terminal(websocket: WebSocket):
    """WebSocket endpoint for terminal with JWT authentication"""
    # Get token from query params
    token = websocket.query_params.get('token')

    if not token:
        await websocket.close(code=1008, reason="Missing authentication token")
        logger.warning("WebSocket connection rejected: missing token")
        return

    # Verify token
    try:
        from backend.saas.auth_service import TokenManager

        payload = TokenManager.verify_token(token)
        if not payload:
            await websocket.close(code=1008, reason="Invalid or expired token")
            logger.warning("WebSocket connection rejected: invalid token")
            return
    except Exception as e:
        await websocket.close(code=1008, reason="Authentication failed")
        logger.warning(f"WebSocket authentication failed: {e}")
        return

    # Extract user_id from token
    user_id = payload.get('user_id', 'unknown')

    await websocket.accept()
    executor = get_executor(user_id)
    logger.info(f"✅ Terminal session opened for user {user_id}")

    try:
        # Set message size limit (1MB)
        MAX_MESSAGE_SIZE = 1024 * 1024

        while True:
            # Receive command
            data = await websocket.receive_json()

            # Check message size
            if len(str(data)) > MAX_MESSAGE_SIZE:
                await websocket.send_json({'error': 'Message too large (max 1MB)'})
                continue

            command = data.get('command', '')

            # Execute command
            result = executor.execute(command)

            # Send result
            await websocket.send_json(
                {
                    'command': result.command,
                    'output': result.output,
                    'error': result.error,
                    'exit_code': result.exit_code,
                    'success': result.success,
                    'current_dir': executor.current_dir,
                }
            )

    except WebSocketDisconnect:
        logger.info(f"✅ Terminal session closed for user {user_id}")
    except Exception as e:
        logger.error(f"❌ Terminal error: {e}")
        try:
            await websocket.send_json({'error': 'Internal server error'})
        except BaseException:
            pass  # Connection might be closed


@router.post('/terminal/execute')
async def execute_command(command: str, user_id: str = '') -> Dict[str, Any]:
    """Execute a single terminal command"""
    executor = get_executor(user_id or 'default')
    result = executor.execute(command)

    return {
        'command': result.command,
        'output': result.output,
        'error': result.error,
        'exit_code': result.exit_code,
        'success': result.success,
        'current_dir': executor.current_dir,
    }


@router.get('/terminal/help')
async def get_help() -> Dict[str, Any]:
    """Get available commands"""
    return {
        'commands': ALLOWED_COMMANDS,
        'note': 'Use "help" command in terminal for full help',
    }


__all__ = ['router', 'TerminalExecutor', 'CommandResult']
