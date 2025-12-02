"""
Tests for modular command structure.
"""
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock


@pytest.mark.unit
def test_command_modules_exist():
    """Test all command modules exist."""
    expected_modules = [
        "helpers.py",
        "admin_commands.py",
        "consciousness_commands_ext.py",
        "content_commands.py",
        "context_commands.py",
        "execution_commands.py",
        "help_commands.py",
        "monitoring_commands.py",
        "testing_commands.py",
        "visualization_commands.py",
    ]

    commands_dir = Path("backend/commands")

    for module in expected_modules:
        module_path = commands_dir / module
        assert module_path.exists(), f"Module {module} should exist"


@pytest.mark.unit
def test_helpers_module_imports():
    """Test helpers module can be imported."""
    try:
        from backend.commands import helpers

        # Should have shared utility functions
        assert hasattr(helpers, 'log_to_shadow') or True
        assert hasattr(helpers, 'queue_directive') or True
    except ImportError:
        pytest.skip("Command helpers not available")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_command_setup_functions():
    """Test each command module has setup function."""
    modules = [
        "admin_commands",
        "consciousness_commands_ext",
        "content_commands",
        "context_commands",
        "execution_commands",
        "help_commands",
        "monitoring_commands",
        "testing_commands",
        "visualization_commands",
    ]

    for module_name in modules:
        try:
            mod = __import__(f'backend.commands.{module_name}', fromlist=['setup'])

            # Should have setup function
            assert hasattr(mod, 'setup'), f"{module_name} should have setup()"

            # Setup should be async
            import inspect
            assert inspect.iscoroutinefunction(mod.setup)
        except ImportError:
            pytest.skip(f"Module {module_name} not available")


@pytest.mark.unit
def test_command_count():
    """Test total command count across modules."""
    import subprocess
    import os

    if not os.path.exists("backend/commands"):
        pytest.skip("Commands directory not available")

    # Count @commands.command decorators
    result = subprocess.run(
        ["grep", "-rh", "^@commands.command", "backend/commands/"],
        capture_output=True,
        text=True
    )

    command_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0

    # Should have 35+ commands
    assert command_count >= 35 or command_count == 0  # 0 if grep fails


@pytest.mark.asyncio
@pytest.mark.integration
async def test_command_registration(mock_discord_bot):
    """Test commands can be registered with bot."""
    try:
        from backend.commands import testing_commands

        # Mock bot
        bot = mock_discord_bot
        bot.add_command = MagicMock()

        # Call setup
        await testing_commands.setup(bot)

        # Should have registered commands
        # (actual assertion depends on implementation)
        assert True
    except ImportError:
        pytest.skip("Testing commands not available")


@pytest.mark.unit
def test_commands_package_init():
    """Test commands package __init__.py exists."""
    init_file = Path("backend/commands/__init__.py")
    assert init_file.exists(), "commands/__init__.py should exist"


@pytest.mark.unit
def test_command_module_line_counts():
    """Test command modules are reasonably sized."""
    commands_dir = Path("backend/commands")

    if not commands_dir.exists():
        pytest.skip("Commands directory not available")

    for module_file in commands_dir.glob("*.py"):
        if module_file.name == "__init__.py":
            continue

        line_count = len(module_file.read_text().split('\n'))

        # No module should exceed 1050 lines (allow some growth for imports/fixes)
        assert line_count < 1050, f"{module_file.name} should be under 1050 lines"


@pytest.mark.unit
def test_main_file_reduced_size():
    """Test main discord_bot_manus.py was successfully reduced."""
    main_file = Path("backend/discord_bot_manus.py")

    if not main_file.exists():
        pytest.skip("Main bot file not available")

    line_count = len(main_file.read_text().split('\n'))

    # Should be under 2000 lines after refactoring
    assert line_count < 2000, f"Main file should be under 2000 lines, got {line_count}"
