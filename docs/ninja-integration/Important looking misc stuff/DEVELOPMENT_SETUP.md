# Development Setup Guide

## Quick Start

Get the Helix Unified system running locally in under 10 minutes with this comprehensive setup guide.

## Prerequisites

### Required Software
- **Python 3.11+** - Main runtime environment
- **Node.js 18+** - For frontend development
- **Git** - Version control
- **Discord Bot Token** - Create at [Discord Developer Portal](https://discord.com/developers/applications)

### Discord Bot Setup
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Enable these Privileged Gateway Intents:
   - **MESSAGE CONTENT INTENT** - Required for message processing
   - **SERVER MEMBERS INTENT** - Required for user information
5. Generate bot token (keep it secure!)
6. Go to "OAuth2" → "URL Generator" and select:
   - `bot`
   - `applications.commands`
7. Under Bot Permissions, select:
   - Send Messages
   - Read Message History
   - Connect
   - Speak
   - Use Voice Activity
   - Read Messages/View Channels
   - Embed Links
   - Attach Files
8. Use the generated URL to invite the bot to your server

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/Deathcharge/helix-unified.git
cd helix-unified
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit the environment file
nano .env  # or use your preferred editor
```

### 4. Required Environment Variables
Edit `.env` file with your values:

```env
# Discord Configuration
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CLIENT_ID=your_client_id
DISCORD_GUILD_ID=your_test_guild_id

# API Configuration
API_HOST=127.0.0.1
API_PORT=8000
API_SECRET_KEY=your_secret_key_here

# LLM Configuration
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# TTS Configuration
GOOGLE_CLOUD_TTS_KEY_PATH=path/to/google-cloud-key.json
GOOGLE_CLOUD_PROJECT_ID=your_project_id

# Database Configuration
DATABASE_URL=sqlite:///helix_unified.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/helix_unified.log
```

### 5. Database Setup
```bash
# Run database migrations
python -m migrations.migrate
```

### 6. Start the Development Server
```bash
# Start the FastAPI backend
python main.py

# In a new terminal, start the Discord bot
python agent_bot.py
```

## Project Structure

```
helix-unified/
├── main.py                 # FastAPI application entry point
├── agent_bot.py            # Discord bot implementation
├── voice_patrol_system.py  # Voice system functionality
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── utils/                 # Utility modules
│   ├── logging_config.py  # Logging configuration
│   ├── error_handlers.py  # Error handling system
│   └── rate_limiter.py    # Rate limiting
├── monitoring/            # Performance monitoring
│   └── performance_dashboard.py
├── migrations/           # Database migrations
│   ├── __init__.py
│   └── versions/
├── tests/                # Test suite
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_voice_patrol.py
└── docs/                 # Documentation
    ├── DEVELOPMENT_SETUP.md
    ├── ENVIRONMENT_VARIABLES.md
    └── API_DOCUMENTATION.md
```

## Development Workflow

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Code Quality
```bash
# Format code with black
black .

# Lint with flake8
flake8 .

# Type checking with mypy
mypy .
```

### Database Operations
```bash
# Check migration status
python -c "from migrations import migration_manager; print(migration_manager.get_status())"

# Create new migration
python -c "
from migrations import Migration
import os

# Create new migration file
migration_name = input('Migration name: ')
version = input('Version (e.g., 002): ')
description = input('Description: ')

template = f'''
from migrations import Migration
import sqlite3

class Migration{version}(Migration):
    def __init__(self):
        super().__init__(
            version='{version}',
            description='{description}'
        )
    
    def up(self, db_connection):
        cursor = db_connection.cursor()
        # Add your migration SQL here
        pass
    
    def down(self, db_connection):
        cursor = db_connection.cursor()
        # Add your rollback SQL here
        pass
'''

with open(f'migrations/versions/migration_{version}.py', 'w') as f:
    f.write(template)

print(f'Created migration_{version}.py')
"
```

## Common Development Tasks

### Adding a New Discord Command
1. Open `agent_bot.py`
2. Add command handler in `handle_command` method
3. Test with your bot in Discord

### Adding API Endpoints
1. Open `main.py`
2. Create new router or add to existing router
3. Add appropriate rate limiting
4. Write tests in `tests/`

### Monitoring Performance
```bash
# Access performance dashboard
curl http://localhost:8000/metrics

# View recent system metrics
curl http://localhost:8000/api/v1/system/metrics
```

## Troubleshooting

### Common Issues

**Bot doesn't respond to commands:**
- Check Discord token is correct
- Verify bot has proper permissions
- Check console for error messages
- Ensure intents are enabled in Discord Developer Portal

**Voice features not working:**
- Verify Google Cloud TTS credentials
- Check bot has voice permissions
- Ensure FFmpeg is installed

**API endpoints returning 500 errors:**
- Check environment variables are set
- Review logs in `logs/helix_unified.log`
- Run tests to identify issues

**Database connection errors:**
- Run migrations: `python -m migrations.migrate`
- Check DATABASE_URL in `.env`
- Verify write permissions

### Debug Mode
Enable debug logging:
```env
LOG_LEVEL=DEBUG
```

Or temporarily in code:
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## Performance Tips

### Development Environment
- Use SQLite for local development
- Enable debug mode for detailed logs
- Run with limited agent count for testing

### Production Considerations
- Use PostgreSQL for production
- Configure proper logging rotation
- Set up monitoring and alerts
- Use environment-specific configurations

## Contributing

### Code Standards
- Follow PEP 8 for Python code
- Use type hints where possible
- Write tests for new features
- Update documentation

### Submitting Changes
1. Create feature branch: `git checkout -b feature-name`
2. Make changes and test thoroughly
3. Update documentation if needed
4. Submit pull request

## Getting Help

### Resources
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Cloud TTS Documentation](https://cloud.google.com/text-to-speech/docs)

### Support Channels
- Check the GitHub Issues page
- Review the troubleshooting section
- Check logs for detailed error information

## Next Steps

After completing setup:
1. ✅ Test basic Discord commands
2. ✅ Verify API endpoints work
3. ✅ Test voice functionality
4. ✅ Run the test suite
5. ✅ Review performance metrics
6. ✅ Configure production settings

You're now ready to start developing with the Helix Unified system! 🚀