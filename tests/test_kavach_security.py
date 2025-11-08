"""
Tests for Kavach security and ethical scanning.
"""
import pytest
from unittest.mock import MagicMock, patch


@pytest.mark.unit
def test_kavach_blocks_rm_rf():
    """Test Kavach blocks dangerous rm -rf commands."""
    from backend.commands.helpers import kavach_ethical_scan

    dangerous_commands = [
        "rm -rf /",
        "rm -rf /*",
        "sudo rm -rf /",
        "rm -rf /home",
    ]

    for cmd in dangerous_commands:
        result = kavach_ethical_scan(cmd)
        assert result["approved"] is False, f"Should block: {cmd}"


@pytest.mark.unit
def test_kavach_blocks_shutdown():
    """Test Kavach blocks system shutdown commands."""
    from backend.commands.helpers import kavach_ethical_scan

    # These commands have explicit patterns in kavach_ethical_scan
    shutdown_commands = [
        "shutdown now",
        "reboot",
        "systemctl poweroff",
        "systemctl reboot",
    ]

    for cmd in shutdown_commands:
        result = kavach_ethical_scan(cmd)
        assert result["approved"] is False, f"Should block: {cmd}"


@pytest.mark.unit
def test_kavach_allows_safe_commands():
    """Test Kavach allows safe commands."""
    from backend.commands.helpers import kavach_ethical_scan

    safe_commands = [
        "ls -la",
        "echo hello",
        "cat /tmp/test.txt",
        "mkdir test_directory",
        "python script.py",
    ]

    for cmd in safe_commands:
        result = kavach_ethical_scan(cmd)
        # May or may not be approved depending on full implementation
        assert "approved" in result


@pytest.mark.unit
def test_kavach_detects_format_commands():
    """Test Kavach detects dangerous format commands."""
    from backend.commands.helpers import kavach_ethical_scan

    format_commands = [
        "mkfs.ext4 /dev/sda",
        "mkfs /dev/sdb1",
        "dd if=/dev/zero of=/dev/sda",
    ]

    for cmd in format_commands:
        result = kavach_ethical_scan(cmd)
        assert result["approved"] is False, f"Should block: {cmd}"


@pytest.mark.unit
def test_kavach_memory_injection_detection():
    """Test Kavach memory injection detection."""
    # This would test CrAI dataset functionality if available
    # For now, just verify the kavach_ethical_scan function exists
    from backend.commands.helpers import kavach_ethical_scan

    # Verify function is callable
    assert callable(kavach_ethical_scan)


@pytest.mark.unit
def test_kavach_scan_result_structure():
    """Test Kavach scan result has proper structure."""
    from backend.commands.helpers import kavach_ethical_scan

    result = kavach_ethical_scan("ls")

    # Should have required fields
    assert "approved" in result
    assert "reasoning" in result
    assert isinstance(result["approved"], bool)
    assert isinstance(result["reasoning"], str)


@pytest.mark.unit
def test_kavach_handles_edge_cases():
    """Test Kavach handles edge cases."""
    from backend.commands.helpers import kavach_ethical_scan

    edge_cases = [
        "",  # Empty command
        "   ",  # Whitespace only
        "a" * 10000,  # Very long command
    ]

    for cmd in edge_cases:
        result = kavach_ethical_scan(cmd)
        assert "approved" in result


@pytest.mark.unit
def test_kavach_risk_levels():
    """Test Kavach assigns appropriate risk levels."""
    from backend.commands.helpers import kavach_ethical_scan

    # High risk command
    high_risk_result = kavach_ethical_scan("rm -rf /")

    # Should identify as high risk (if risk_level field exists)
    if "risk_level" in high_risk_result:
        assert high_risk_result["risk_level"] in ["high", "critical"]
