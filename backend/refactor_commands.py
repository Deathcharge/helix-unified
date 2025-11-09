#!/usr/bin/env python3
"""
Script to refactor discord_bot_manus.py into modular command files.
Automatically extracts commands and creates module files.
"""
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Command categorization based on refactoring plan
COMMAND_MAP = {
    'admin_commands.py': [
        'setup', 'verify-setup', 'webhooks', 'clean', 'refresh', 'seed'
    ],
    'monitoring_commands.py': [
        'status', 'health', 'discovery', 'storage', 'sync'
    ],
    'content_commands.py': [
        'update_manifesto', 'update_codex', 'update_rules', 'update_ritual_guide', 'codex_version', 'ucf'
    ],
    'execution_commands.py': [
        'ritual', 'run', 'halt'
    ],
    'consciousness_commands_ext.py': [
        'consciousness', 'emotions', 'agent', 'ethics', 'help_consciousness'
    ],
    'context_commands.py': [
        'backup', 'load', 'contexts'
    ],
    'visualization_commands.py': [
        'visualize', 'icon'
    ],
    'testing_commands.py': [
        'test-integrations', 'zapier_test', 'welcome-test'
    ],
    'help_commands.py': [
        'commands', 'agents'
    ],
}

def extract_command_blocks(source_file: Path) -> Dict[str, Tuple[int, int, str]]:
    """Extract command blocks with their line ranges and content."""
    with open(source_file, 'r') as f:
        lines = f.readlines()

    commands = {}
    current_command = None
    start_line = 0

    for i, line in enumerate(lines, 1):
        # Check if this is a command decorator
        if '@bot.command(name=' in line:
            # Save previous command if exists
            if current_command:
                end_line = i - 1
                content = ''.join(lines[start_line-1:end_line])
                commands[current_command] = (start_line, end_line, content)

            # Extract command name
            match = re.search(r'name="([^"]+)"', line)
            if match:
                current_command = match.group(1)
                start_line = i

        # Check for next decorator or EOF
        elif line.strip().startswith('@') and current_command and i > start_line:
            if not line.strip().startswith('@commands.'):
                # End of current command
                end_line = i - 1
                content = ''.join(lines[start_line-1:end_line])
                commands[current_command] = (start_line, end_line, content)
                current_command = None

    # Handle last command
    if current_command:
        end_line = len(lines)
        content = ''.join(lines[start_line-1:end_line])
        commands[current_command] = (start_line, end_line, content)

    return commands

def generate_module_template(module_name: str, commands_data: List[Tuple[str, str]]) -> str:
    """Generate a module file template with extracted commands."""
    module_desc = {
        'admin_commands.py': 'Admin and setup commands',
        'monitoring_commands.py': 'Status and health monitoring commands',
        'content_commands.py': 'Content management commands',
        'execution_commands.py': 'Ritual execution commands',
        'consciousness_commands_ext.py': 'Consciousness feature commands',
        'context_commands.py': 'Context and backup management commands',
        'visualization_commands.py': 'Visual feature commands',
        'testing_commands.py': 'Testing utility commands',
        'help_commands.py': 'Help system commands',
    }

    template = f'''"""
{module_desc.get(module_name, 'Commands')} for Helix Discord bot.
"""
import asyncio
import datetime
import json
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from discord.ext.commands import Bot

logger = logging.getLogger(__name__)

# Import helpers as needed
from backend.commands.helpers import (
    log_to_shadow,
    queue_directive,
    kavach_ethical_scan,
    get_uptime,
    build_storage_report,
    save_command_to_history,
)
from z88_ritual_engine import execute_ritual, load_ucf_state

# Path constants
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATE_DIR = Path("Helix/state")
HELIX_ROOT = Path("Helix")
SHADOW_DIR = Path("Shadow/manus_archive")

# Environment variables
STATUS_CHANNEL_ID = int(os.getenv("DISCORD_STATUS_CHANNEL_ID", 0))
TELEMETRY_CHANNEL_ID = int(os.getenv("DISCORD_TELEMETRY_CHANNEL_ID", 0))
ARCHITECT_ID = int(os.getenv("ARCHITECT_ID", 0))

'''

    # Add command implementations
    for cmd_name, cmd_content in commands_data:
        # Replace @bot.command with @commands.command
        cmd_content = cmd_content.replace('@bot.command(', '@commands.command(')
        template += '\n' + cmd_content + '\n'

    # Add setup function
    cmd_names = [name for name, _ in commands_data]
    cmd_function_names = []
    for name in cmd_names:
        # Convert command name to function name (heuristic)
        func_name = name.replace('-', '_')
        cmd_function_names.append(func_name)

    template += '''

async def setup(bot: 'Bot') -> None:
    """Register commands with the bot."""
'''

    for name, content in commands_data:
        # Extract actual function name from content
        match = re.search(r'async def (\w+)\(', content)
        if match:
            func_name = match.group(1)
            template += f'    bot.add_command({func_name})\n'

    return template

def main():
    source_file = Path('backend/discord_bot_manus.py')
    output_dir = Path('backend/commands')
    output_dir.mkdir(exist_ok=True)

    print("📖 Reading discord_bot_manus.py...")
    commands_data = extract_command_blocks(source_file)

    print(f"✅ Found {len(commands_data)} commands")

    # Create module files
    for module_name, command_names in COMMAND_MAP.items():
        print(f"\\n📝 Creating {module_name}...")

        # Get command implementations for this module
        module_commands = []
        for cmd_name in command_names:
            if cmd_name in commands_data:
                start, end, content = commands_data[cmd_name]
                module_commands.append((cmd_name, content))
                print(f"  ✓ {cmd_name} (lines {start}-{end})")
            else:
                print(f"  ⚠ {cmd_name} not found")

        if module_commands:
            # Generate module file
            module_content = generate_module_template(module_name, module_commands)
            module_path = output_dir / module_name

            with open(module_path, 'w') as f:
                f.write(module_content)

            print(f"  💾 Saved {module_path} ({len(module_commands)} commands)")

    print("\\n✅ Refactoring complete!")
    print(f"📁 Created {len(COMMAND_MAP)} command modules in {output_dir}/")

if __name__ == '__main__':
    main()
