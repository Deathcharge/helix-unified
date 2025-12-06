# Helix Unified API Examples

Example scripts showing how to interact with the Helix Unified API.

## Quick Start

```bash
# Install dependencies
pip install requests python-dotenv

# Set your API URL
export HELIX_API_URL="http://localhost:8000"
# Or for production:
export HELIX_API_URL="https://helix-backend-api.up.railway.app"

# Run examples
python examples/01_health_check.py
python examples/02_auth_flow.py
python examples/03_chat_completion.py
```

## Examples

1. **01_health_check.py** - Check API health and status
2. **02_auth_flow.py** - Register, login, get user info
3. **03_chat_completion.py** - Use multi-LLM chat API
4. **04_subscription_flow.py** - Manage subscriptions
5. **05_agent_interaction.py** - Interact with consciousness agents
6. **06_webhooks.py** - Set up Zapier webhooks
7. **07_consciousness_metrics.py** - Query UCF metrics

## Environment Variables

Create a `.env` file in this directory:

```bash
# API Configuration
HELIX_API_URL=http://localhost:8000
HELIX_API_KEY=your-api-key-here

# For testing subscriptions
STRIPE_TEST_CARD=4242424242424242

# For LLM routing
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...
```

## Testing Against Production

```bash
# Set production URL
export HELIX_API_URL="https://helix-backend-api.up.railway.app"

# Run tests
python examples/01_health_check.py
```

## Need Help?

- API Documentation: `/docs` endpoint (FastAPI auto-generated)
- Deployment Guide: `../DEPLOYMENT_GUIDE.md`
- Quick Start: `../QUICK_START.md`
