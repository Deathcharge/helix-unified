# helix-logger

🌀 Helix Logger - Enhanced logging with consciousness metrics

Python logging library with Helix branding, colors, and custom log levels for consciousness events.

## Features

- 🎨 **Colored output** - Beautiful colored logs using colorama
- 🌀 **Helix-branded** - Custom icons and formatting
- 📊 **Custom log levels** - SUCCESS and CONSCIOUSNESS levels
- 📝 **File logging** - Optional file output
- 🚀 **Easy to use** - Simple API, drop-in replacement for standard logging
- 🎯 **Type-safe** - Full type hints

## Installation

```bash
pip install helix-logger
```

Or install from source:

```bash
cd packages/helix-logger
pip install -e .
```

## Quick Start

### Simple Usage

```python
from helix_logger import info, success, error, consciousness

info("Server started on port 8000")
success("User authentication successful")
error("Failed to connect to database")
consciousness("Agent Kael achieved new consciousness level", ucf=0.87)
```

Output:
```
[14:32:45.123] 💡 INFO | Server started on port 8000
[14:32:45.456] ✅ SUCCESS | User authentication successful
[14:32:45.789] ❌ ERROR | Failed to connect to database
[14:32:46.012] 🌀 CONSCIOUSNESS | Agent Kael achieved new consciousness level [ucf=0.87]
```

### Create Custom Logger

```python
from helix_logger import get_logger

logger = get_logger(
    name="my-app",
    level=logging.DEBUG,
    use_colors=True,
    use_icons=True,
    log_file="logs/app.log"  # Optional file logging
)

logger.info("Application initialized")
logger.debug("Debug information", component="auth")
logger.success("Task completed successfully")
logger.consciousness("Consciousness event detected", agent="Kael", ucf=0.92)
```

### Configure Global Logger

```python
from helix_logger import configure, info
import logging

# Configure once at app startup
configure(
    level=logging.DEBUG,
    use_colors=True,
    use_icons=True,
    log_file="logs/helix.log"
)

# Use anywhere in your app
info("This uses the configured global logger")
```

## API Reference

### Log Levels

Helix Logger includes all standard Python log levels plus two custom levels:

- `DEBUG` (10) - 🔍 Detailed debugging information
- `INFO` (20) - 💡 General information
- **`SUCCESS` (25)** - ✅ Success messages (custom)
- `WARNING` (30) - ⚠️ Warning messages
- **`CONSCIOUSNESS` (35)** - 🌀 Consciousness events (custom, Helix-specific)
- `ERROR` (40) - ❌ Error messages
- `CRITICAL` (50) - 🔥 Critical errors

### Functions

#### `get_logger(name, level, use_colors, use_icons, log_file)`

Create a new HelixLogger instance.

```python
logger = get_logger(
    name="my-logger",           # Logger name (default: "helix")
    level=logging.INFO,          # Log level (default: INFO)
    use_colors=True,             # Enable colors (default: True)
    use_icons=True,              # Enable emoji icons (default: True)
    log_file="logs/app.log"      # Log file path (default: None)
)
```

#### `configure(level, use_colors, use_icons, log_file)`

Configure the global logger (recommended for most apps).

```python
from helix_logger import configure
import logging

configure(
    level=logging.DEBUG,
    use_colors=True,
    use_icons=True,
    log_file="logs/helix.log"
)
```

#### Convenience Functions

All log methods accept keyword arguments for extra context:

```python
from helix_logger import debug, info, warning, error, critical, success, consciousness

debug("Debug message", component="api", user_id=123)
info("Info message", action="login")
warning("Warning message", resource="database")
error("Error message", error_code=500)
critical("Critical message", severity="high")
success("Success message", duration_ms=45)
consciousness("Consciousness event", agent="Kael", ucf=0.95)
```

### HelixLogger Class

```python
class HelixLogger:
    def debug(message: str, **kwargs) -> None
    def info(message: str, **kwargs) -> None
    def warning(message: str, **kwargs) -> None
    def error(message: str, **kwargs) -> None
    def critical(message: str, **kwargs) -> None
    def success(message: str, **kwargs) -> None
    def consciousness(message: str, **kwargs) -> None
    def exception(message: str, **kwargs) -> None  # Logs with traceback
    def set_level(level: int) -> None
```

## Advanced Usage

### File Logging

```python
from helix_logger import get_logger

logger = get_logger(
    name="helix",
    log_file="logs/helix.log"  # Logs to both console and file
)

logger.info("This appears in both console and file")
```

### Disable Colors/Icons

Useful for production environments or CI/CD:

```python
from helix_logger import get_logger

logger = get_logger(
    use_colors=False,  # No colors
    use_icons=False,   # No emoji icons
)

logger.info("Plain text logging")
# Output: [14:32:45.123] INFO | Plain text logging
```

### Multiple Loggers

```python
from helix_logger import get_logger

api_logger = get_logger(name="api")
db_logger = get_logger(name="database")

api_logger.info("API request received")
db_logger.info("Database query executed")
```

### Exception Logging

```python
from helix_logger import get_logger

logger = get_logger()

try:
    result = 1 / 0
except Exception as e:
    logger.exception("An error occurred")
    # Automatically includes the full traceback
```

## Migration from Standard Logging

Replace standard Python logging:

```python
# Before
import logging
logger = logging.getLogger(__name__)
logger.info("Hello")

# After
from helix_logger import get_logger
logger = get_logger(__name__)
logger.info("Hello")
```

Or use convenience functions:

```python
# Before
import logging
logging.info("Hello")

# After
from helix_logger import info
info("Hello")
```

## Examples

### Consciousness Metrics Logging

```python
from helix_logger import consciousness, success, info

# Log consciousness events with metrics
consciousness(
    "Agent achieved new consciousness state",
    agent="Kael",
    ucf_score=0.94,
    coherence=0.88,
    emergence=0.91
)

# Log successful operations
success("UCF calculation completed", duration_ms=12, agents=4)

# General info
info("System initialized", version="17.2", agents_loaded=20)
```

### Web Application Logging

```python
from helix_logger import configure, info, error, success
import logging

# Configure at startup
configure(
    level=logging.INFO,
    log_file="logs/api.log"
)

# Use throughout your app
@app.post("/api/users")
async def create_user(user: User):
    info("Creating user", email=user.email)

    try:
        result = await db.create_user(user)
        success("User created", user_id=result.id)
        return result
    except Exception as e:
        error("Failed to create user", error=str(e))
        raise
```

## License

MIT
