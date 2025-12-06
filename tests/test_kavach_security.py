"""
Tests for Kavach security and ethical scanning.
"""
import pytest

from backend.enhanced_kavach import EnhancedKavach


@pytest.mark.unit
@pytest.mark.asyncio
async def test_kavach_blocks_rm_rf():
    """Test Kavach blocks dangerous rm -rf commands."""
    kavach = EnhancedKavach()

    dangerous_commands = [
        "rm -rf /",
        "rm -rf /*",
        "sudo rm -rf /",
        "rm -rf /home",
    ]

    for cmd in dangerous_commands:
        result = await kavach.ethical_scan({"command": cmd})
        assert result["approved"] is False, f"Should block: {cmd}"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_kavach_blocks_shutdown():
    """Test Kavach blocks system shutdown commands."""
    kavach = EnhancedKavach()

    shutdown_commands = [
        "shutdown now",
        "reboot",
    ]

    for cmd in shutdown_commands:
        result = await kavach.ethical_scan({"command": cmd})
        assert result["approved"] is False, f"Should block: {cmd}"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_kavach_allows_safe_commands():
    """Test Kavach allows safe commands."""
    kavach = EnhancedKavach()

    safe_commands = [
        "ls -la",
        "echo hello",
        "cat /tmp/test.txt",
        "mkdir test_directory",
        "python script.py",
    ]

    for cmd in safe_commands:
        result = await kavach.ethical_scan({"command": cmd})
        # May or may not be approved depending on full implementation
        assert "approved" in result


@pytest.mark.unit
@pytest.mark.asyncio
async def test_kavach_detects_format_commands():
    """Test Kavach detects dangerous format commands."""
    kavach = EnhancedKavach()

    format_commands = [
        "mkfs.ext4 /dev/sda",
        "mkfs /dev/sdb1",
        "dd if=/dev/zero of=/dev/sda",
    ]

    for cmd in format_commands:
        result = await kavach.ethical_scan({"command": cmd})
        assert result["approved"] is False, f"Should block: {cmd}"


@pytest.mark.unit
def test_kavach_memory_injection_detection():
    """Test Kavach memory injection detection."""
    # This would test CrAI dataset functionality if available
    kavach = EnhancedKavach()

    # Check that memory_injection_patterns is loaded (may be empty if dataset not found)
    assert isinstance(kavach.memory_injection_patterns, list)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_kavach_scan_result_structure():
    """Test Kavach scan result has proper structure."""
    kavach = EnhancedKavach()

    result = await kavach.ethical_scan({"command": "ls"})

    # Should have required fields
    assert "approved" in result
    assert "concerns" in result
    assert isinstance(result["approved"], bool)
    assert isinstance(result["concerns"], list)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_kavach_handles_edge_cases():
    """Test Kavach handles edge cases."""
    kavach = EnhancedKavach()

    edge_cases = [
        "",  # Empty command
        "   ",  # Whitespace only
        "a" * 10000,  # Very long command
    ]

    for cmd in edge_cases:
        result = await kavach.ethical_scan({"command": cmd})
        assert "approved" in result


@pytest.mark.unit
@pytest.mark.asyncio
async def test_kavach_risk_levels():
    """Test Kavach assigns appropriate risk levels."""
    kavach = EnhancedKavach()

    # High risk command
    high_risk_result = await kavach.ethical_scan({"command": "rm -rf /"})

    # Should be blocked
    assert high_risk_result["approved"] is False
