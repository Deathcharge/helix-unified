#!/usr/bin/env python3
"""
Enable Missing Command Modules
Adds fun_minigames and role_system to the bot's command modules list.
"""

import sys
from pathlib import Path

# Path to discord_bot_manus.py
BOT_FILE = Path(__file__).parent.parent / "backend" / "discord_bot_manus.py"

# New modules to add
NEW_MODULES = [
    "        ('commands.fun_minigames', 'Fun commands (8ball, horoscope, coinflip, wisdom, fortune, agent-advice)'),",
    "        ('commands.role_system', 'Role management (roles, subscribe, my-roles, setup-roles, setup-all-roles)'),"
]

def main():
    """Add missing command modules to bot file."""

    if not BOT_FILE.exists():
        print(f"❌ Error: {BOT_FILE} not found")
        sys.exit(1)

    # Read file
    with open(BOT_FILE, 'r') as f:
        lines = f.readlines()

    # Find the command_modules list
    module_list_start = None
    module_list_end = None

    for i, line in enumerate(lines):
        if 'command_modules = [' in line:
            module_list_start = i
        if module_list_start is not None and line.strip() == ']':
            module_list_end = i
            break

    if module_list_start is None or module_list_end is None:
        print("❌ Error: Could not find command_modules list")
        sys.exit(1)

    # Check if already added
    content = ''.join(lines)
    if 'fun_minigames' in content:
        print("ℹ️  fun_minigames already loaded")
    else:
        print("✅ Adding fun_minigames...")

    if 'role_system' in content:
        print("ℹ️  role_system already loaded")
    else:
        print("✅ Adding role_system...")

    # Insert new modules before the closing bracket
    if 'fun_minigames' not in content or 'role_system' not in content:
        insert_lines = []
        if 'fun_minigames' not in content:
            insert_lines.append(NEW_MODULES[0] + '\n')
        if 'role_system' not in content:
            insert_lines.append(NEW_MODULES[1] + '\n')

        # Insert at the end of the list
        lines = lines[:module_list_end] + insert_lines + lines[module_list_end:]

        # Write back
        with open(BOT_FILE, 'w') as f:
            f.writelines(lines)

        print("\n✨ Success! Missing command modules added.")
        print("\n📋 Added modules:")
        for module in insert_lines:
            print(f"  • {module.strip()}")

        print("\n⚠️  Next steps:")
        print("  1. Review the changes in backend/discord_bot_manus.py")
        print("  2. Restart your Discord bot")
        print("  3. Test commands like !8ball, !wisdom, !roles")
        print("  4. Commit changes: git add backend/discord_bot_manus.py")
    else:
        print("\n✅ All command modules already loaded!")

    return 0

if __name__ == '__main__':
    sys.exit(main())
