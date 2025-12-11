"""
🌀 Helix Logger - Enhanced logging with consciousness metrics
"""

import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Fallback if colorama not installed
    class Fore:
        BLUE = ""
        GREEN = ""
        YELLOW = ""
        RED = ""
        MAGENTA = ""
        CYAN = ""
        WHITE = ""
        RESET = ""

    class Style:
        BRIGHT = ""
        RESET_ALL = ""


class HelixFormatter(logging.Formatter):
    """Custom formatter with Helix branding and colors"""

    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.BLUE,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
        'SUCCESS': Fore.GREEN,
        'CONSCIOUSNESS': Fore.MAGENTA + Style.BRIGHT,
    }

    ICONS = {
        'DEBUG': '🔍',
        'INFO': '💡',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🔥',
        'SUCCESS': '✅',
        'CONSCIOUSNESS': '🌀',
    }

    def __init__(self, use_colors: bool = True, use_icons: bool = True):
        super().__init__()
        self.use_colors = use_colors and HAS_COLOR
        self.use_icons = use_icons

    def format(self, record: logging.LogRecord) -> str:
        # Get level name
        levelname = record.levelname

        # Add color
        if self.use_colors:
            color = self.COLORS.get(levelname, '')
            levelname_colored = f"{color}{levelname}{Style.RESET_ALL}"
        else:
            levelname_colored = levelname

        # Add icon
        if self.use_icons:
            icon = self.ICONS.get(levelname, '📝')
            prefix = f"{icon} "
        else:
            prefix = ""

        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S.%f')[:-3]

        # Build message
        message = record.getMessage()

        # Format: [HH:MM:SS.mmm] 🌀 LEVEL | message
        if self.use_colors:
            formatted = (
                f"{Fore.WHITE}[{timestamp}]{Style.RESET_ALL} "
                f"{prefix}{levelname_colored} {Fore.WHITE}|{Style.RESET_ALL} "
                f"{message}"
            )
        else:
            formatted = f"[{timestamp}] {prefix}{levelname} | {message}"

        # Add exception info if present
        if record.exc_info:
            formatted += "\n" + self.formatException(record.exc_info)

        return formatted


class HelixLogger:
    """Enhanced logger with Helix branding"""

    # Custom log levels
    SUCCESS = 25  # Between INFO (20) and WARNING (30)
    CONSCIOUSNESS = 35  # Between WARNING (30) and ERROR (40)

    def __init__(
        self,
        name: str = "helix",
        level: int = logging.INFO,
        use_colors: bool = True,
        use_icons: bool = True,
        log_file: Optional[str] = None,
    ):
        # Add custom levels
        logging.addLevelName(self.SUCCESS, "SUCCESS")
        logging.addLevelName(self.CONSCIOUSNESS, "CONSCIOUSNESS")

        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Clear existing handlers
        self.logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(HelixFormatter(use_colors, use_icons))
        self.logger.addHandler(console_handler)

        # File handler (optional)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(HelixFormatter(use_colors=False, use_icons=False))
            self.logger.addHandler(file_handler)

        # Prevent propagation to root logger
        self.logger.propagate = False

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message"""
        self.logger.debug(self._format_message(message, kwargs))

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message"""
        self.logger.info(self._format_message(message, kwargs))

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message"""
        self.logger.warning(self._format_message(message, kwargs))

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message"""
        self.logger.error(self._format_message(message, kwargs))

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message"""
        self.logger.critical(self._format_message(message, kwargs))

    def success(self, message: str, **kwargs: Any) -> None:
        """Log success message (custom level)"""
        self.logger.log(self.SUCCESS, self._format_message(message, kwargs))

    def consciousness(self, message: str, **kwargs: Any) -> None:
        """Log consciousness event (custom level for Helix)"""
        self.logger.log(self.CONSCIOUSNESS, self._format_message(message, kwargs))

    def exception(self, message: str, **kwargs: Any) -> None:
        """Log exception with traceback"""
        self.logger.exception(self._format_message(message, kwargs))

    def _format_message(self, message: str, extra: Dict[str, Any]) -> str:
        """Format message with extra context"""
        if not extra:
            return message

        # Add extra context
        context_parts = [f"{k}={v}" for k, v in extra.items()]
        context = " ".join(context_parts)

        return f"{message} [{context}]"

    def set_level(self, level: int) -> None:
        """Set logging level"""
        self.logger.setLevel(level)


# ============================================================================
# Global logger instance
# ============================================================================

_global_logger: Optional[HelixLogger] = None


def get_logger(
    name: str = "helix",
    level: int = logging.INFO,
    use_colors: bool = True,
    use_icons: bool = True,
    log_file: Optional[str] = None,
) -> HelixLogger:
    """
    Get or create a Helix logger instance

    Args:
        name: Logger name
        level: Logging level
        use_colors: Enable colored output
        use_icons: Enable emoji icons
        log_file: Optional file path for logging

    Returns:
        HelixLogger instance
    """
    return HelixLogger(
        name=name,
        level=level,
        use_colors=use_colors,
        use_icons=use_icons,
        log_file=log_file,
    )


def configure(
    level: int = logging.INFO,
    use_colors: bool = True,
    use_icons: bool = True,
    log_file: Optional[str] = None,
) -> HelixLogger:
    """
    Configure the global Helix logger

    Args:
        level: Logging level
        use_colors: Enable colored output
        use_icons: Enable emoji icons
        log_file: Optional file path for logging

    Returns:
        Configured global logger
    """
    global _global_logger
    _global_logger = get_logger(
        name="helix",
        level=level,
        use_colors=use_colors,
        use_icons=use_icons,
        log_file=log_file,
    )
    return _global_logger


def _ensure_global_logger() -> HelixLogger:
    """Ensure global logger exists"""
    global _global_logger
    if _global_logger is None:
        _global_logger = configure()
    return _global_logger


# ============================================================================
# Convenience functions (use global logger)
# ============================================================================

def debug(message: str, **kwargs: Any) -> None:
    """Log debug message using global logger"""
    _ensure_global_logger().debug(message, **kwargs)


def info(message: str, **kwargs: Any) -> None:
    """Log info message using global logger"""
    _ensure_global_logger().info(message, **kwargs)


def warning(message: str, **kwargs: Any) -> None:
    """Log warning message using global logger"""
    _ensure_global_logger().warning(message, **kwargs)


def error(message: str, **kwargs: Any) -> None:
    """Log error message using global logger"""
    _ensure_global_logger().error(message, **kwargs)


def critical(message: str, **kwargs: Any) -> None:
    """Log critical message using global logger"""
    _ensure_global_logger().critical(message, **kwargs)


def success(message: str, **kwargs: Any) -> None:
    """Log success message using global logger"""
    _ensure_global_logger().success(message, **kwargs)


def consciousness(message: str, **kwargs: Any) -> None:
    """Log consciousness event using global logger"""
    _ensure_global_logger().consciousness(message, **kwargs)
