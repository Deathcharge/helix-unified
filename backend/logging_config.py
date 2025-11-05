# Helix Collective v15.2+ - Centralized Logging Configuration
# Features: Log rotation, structured logging, multiple handlers

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
import json

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

def setup_logging(
    log_dir: str = "Shadow/manus_archive",
    log_level: str = "INFO",
    enable_rotation: bool = True
):
    """
    Configure centralized logging with rotation for Helix Collective.
    
    Args:
        log_dir: Directory for log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        enable_rotation: Enable log rotation (recommended for production)
    
    Returns:
        Configured logger instance
    """
    # Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # ========================================================================
    # CONSOLE HANDLER (for development/debugging)
    # ========================================================================
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # ========================================================================
    # FILE HANDLER WITH ROTATION (operations log)
    # ========================================================================
    if enable_rotation:
        # Rotate daily, keep 30 days
        operations_handler = logging.handlers.TimedRotatingFileHandler(
            filename=log_path / "operations.log",
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
    else:
        # Simple file handler (no rotation)
        operations_handler = logging.FileHandler(
            filename=log_path / "operations.log",
            encoding='utf-8'
        )
    
    operations_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)-20s | %(funcName)-20s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    operations_handler.setFormatter(file_formatter)
    logger.addHandler(operations_handler)
    
    # ========================================================================
    # ERROR HANDLER WITH ROTATION (errors only)
    # ========================================================================
    if enable_rotation:
        # Rotate by size (10MB), keep 5 files
        error_handler = logging.handlers.RotatingFileHandler(
            filename=log_path / "errors.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
    else:
        error_handler = logging.FileHandler(
            filename=log_path / "errors.log",
            encoding='utf-8'
        )
    
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    logger.addHandler(error_handler)
    
    # ========================================================================
    # JSON HANDLER (for structured logs)
    # ========================================================================
    json_handler = JSONFileHandler(
        filename=log_path / "structured.jsonl",
        max_bytes=50*1024*1024,  # 50MB
        backup_count=3
    )
    json_handler.setLevel(logging.INFO)
    logger.addHandler(json_handler)
    
    logger.info("✅ Logging system initialized with rotation")
    logger.info(f"📁 Log directory: {log_path.absolute()}")
    logger.info(f"📊 Log level: {log_level}")
    logger.info(f"🔄 Rotation enabled: {enable_rotation}")
    
    return logger


# ============================================================================
# JSON FILE HANDLER (for structured logging)
# ============================================================================

class JSONFileHandler(logging.Handler):
    """
    Custom handler that writes logs as JSON lines (JSONL format).
    Includes automatic rotation by file size.
    """
    
    def __init__(self, filename, max_bytes=50*1024*1024, backup_count=3):
        """
        Initialize JSON file handler.
        
        Args:
            filename: Path to log file
            max_bytes: Maximum file size before rotation (default 50MB)
            backup_count: Number of backup files to keep
        """
        super().__init__()
        self.filename = Path(filename)
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.filename.parent.mkdir(parents=True, exist_ok=True)
    
    def emit(self, record):
        """Emit a log record as JSON."""
        try:
            # Check if rotation is needed
            if self.filename.exists() and self.filename.stat().st_size > self.max_bytes:
                self.rotate()
            
            # Create JSON log entry
            log_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "level": record.levelname,
                "logger": record.name,
                "function": record.funcName,
                "line": record.lineno,
                "message": record.getMessage(),
            }
            
            # Add exception info if present
            if record.exc_info:
                log_entry["exception"] = self.format(record)
            
            # Add extra fields if present
            if hasattr(record, 'extra'):
                log_entry.update(record.extra)
            
            # Write to file (append mode)
            with open(self.filename, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        
        except Exception as e:
            self.handleError(record)
    
    def rotate(self):
        """Rotate log files."""
        # Delete oldest backup if exists
        oldest = self.filename.with_suffix(f'.log.{self.backup_count}')
        if oldest.exists():
            oldest.unlink()
        
        # Rotate existing backups
        for i in range(self.backup_count - 1, 0, -1):
            old_file = self.filename.with_suffix(f'.log.{i}')
            new_file = self.filename.with_suffix(f'.log.{i+1}')
            if old_file.exists():
                old_file.rename(new_file)
        
        # Rotate current file to .1
        if self.filename.exists():
            self.filename.rename(self.filename.with_suffix('.log.1'))


# ============================================================================
# AGENT-SPECIFIC LOGGERS
# ============================================================================

def get_agent_logger(agent_name: str):
    """
    Get a logger for a specific agent.
    
    Args:
        agent_name: Name of the agent (e.g., "Manus", "Claude", "Kavach")
    
    Returns:
        Logger instance for the agent
    """
    return logging.getLogger(f"helix.agent.{agent_name.lower()}")


def get_module_logger(module_name: str):
    """
    Get a logger for a specific module.
    
    Args:
        module_name: Name of the module (e.g., "ritual_engine", "ucf_protocol")
    
    Returns:
        Logger instance for the module
    """
    return logging.getLogger(f"helix.module.{module_name}")


# ============================================================================
# LOG CLEANUP UTILITY
# ============================================================================

def cleanup_old_logs(log_dir: str = "Shadow/manus_archive", days: int = 30):
    """
    Clean up log files older than specified days.
    
    Args:
        log_dir: Directory containing log files
        days: Delete files older than this many days
    """
    log_path = Path(log_dir)
    if not log_path.exists():
        return
    
    import time
    cutoff_time = time.time() - (days * 86400)
    deleted_count = 0
    
    for log_file in log_path.glob("*.log*"):
        if log_file.stat().st_mtime < cutoff_time:
            log_file.unlink()
            deleted_count += 1
    
    if deleted_count > 0:
        logger = logging.getLogger()
        logger.info(f"🗑️ Cleaned up {deleted_count} old log files (>{days} days)")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Initialize logging
    logger = setup_logging(log_level="DEBUG")
    
    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Test agent-specific logger
    manus_logger = get_agent_logger("Manus")
    manus_logger.info("Manus operational executor initialized")
    
    # Test module-specific logger
    ritual_logger = get_module_logger("ritual_engine")
    ritual_logger.info("Z-88 ritual cycle initiated")
    
    print("\n✅ Logging test complete. Check Shadow/manus_archive/ for log files:")
    print("  - operations.log (all logs with rotation)")
    print("  - errors.log (errors only with rotation)")
    print("  - structured.jsonl (JSON format for parsing)")

