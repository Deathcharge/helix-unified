"""
🌀 Helix Logger
Enhanced logging with Helix branding and consciousness metrics
"""

from .logger import (HelixLogger, configure, consciousness, critical, debug,
                     error, get_logger, info, success, warning)

__version__ = "1.0.0"
__all__ = [
    "HelixLogger",
    "get_logger",
    "configure",
    "debug",
    "info",
    "warning",
    "error",
    "critical",
    "success",
    "consciousness",
]
