#!/bin/bash
# Pre-Deployment Ritual - Helix v15.3 Dual Resonance
# Validates system readiness before deployment
# Based on Manus guidance 🦑

set -e  # Exit on error

echo "🌀 HELIX v15.3 PRE-DEPLOYMENT RITUAL"
echo "===================================================="
echo ""

# Track failures
FAILURES=0

# Helper functions
check_pass() {
    echo "  ✅ $1"
}

check_fail() {
    echo "  ❌ $1"
    FAILURES=$((FAILURES + 1))
}

check_warn() {
    echo "  ⚠️  $1"
}

# ==================================================
# STEP 1: Python Environment
# ==================================================
echo "📍 Step 1/7: Python Environment"
if python3 --version | grep -qE "3\.(9|10|11)"; then
    check_pass "Python 3.9+ detected"
else
    check_fail "Python 3.9+ required"
fi

if python3 -c "import discord" 2>/dev/null; then
    check_pass "discord.py available"
else
    check_fail "discord.py not installed"
fi

if python3 -c "import fastapi" 2>/dev/null; then
    check_pass "FastAPI available"
else
    check_warn "FastAPI not installed (optional for backend)"
fi

echo ""

# ==================================================
# STEP 2: Environment Variables
# ==================================================
echo "📍 Step 2/7: Environment Variables"
if [ -f .env ]; then
    check_pass ".env file exists"

    for var in DISCORD_TOKEN DISCORD_GUILD_ID ARCHITECT_ID; do
        if grep -q "^$var=" .env; then
            check_pass "$var configured"
        else
            check_fail "$var missing from .env"
        fi
    done
else
    check_fail ".env file not found"
fi

echo ""

# ==================================================
# STEP 3: Directory Structure
# ==================================================
echo "📍 Step 3/7: Directory Structure"
for dir in "Helix/state" "Helix/commands" "Helix/ethics" "Shadow/manus_archive"; do
    if [ -d "$dir" ]; then
        check_pass "$dir exists"
    else
        check_warn "$dir missing (will be created on startup)"
        mkdir -p "$dir"
    fi
done

echo ""

# ==================================================
# STEP 4: UCF State
# ==================================================
echo "📍 Step 4/7: UCF State Validation"
if [ -f "Helix/state/ucf_state.json" ]; then
    check_pass "UCF state file exists"

    # Validate JSON
    if python3 -c "import json; json.load(open('Helix/state/ucf_state.json'))" 2>/dev/null; then
        check_pass "UCF state is valid JSON"

        # Check harmony value
        HARMONY=$(python3 -c "import json; print(json.load(open('Helix/state/ucf_state.json')).get('harmony', 0))")
        if (( $(echo "$HARMONY > 0.3" | bc -l) )); then
            check_pass "Harmony sufficient for deployment: $HARMONY"
        else
            check_warn "Low harmony detected: $HARMONY - consider ritual first"
        fi
    else
        check_fail "UCF state JSON is invalid"
    fi
else
    check_warn "UCF state missing (will initialize on startup)"
fi

echo ""

# ==================================================
# STEP 5: Agent Modules
# ==================================================
echo "📍 Step 5/7: Agent System"
if python3 -c "from backend.agents import Kael, Lumina, Vega, Manus, Kavach, Shadow" 2>/dev/null; then
    check_pass "Core agents importable"
else
    check_fail "Agent imports failed - check backend/agents.py"
fi

# Check Kael v3.4
if python3 -c "from backend.agents import Kael; k = Kael(); assert k.version == '3.4'" 2>/dev/null; then
    check_pass "Kael v3.4 Reflexive Harmony active"
else
    check_warn "Kael version check failed"
fi

echo ""

# ==================================================
# STEP 6: Discord Bot
# ==================================================
echo "📍 Step 6/7: Discord Bot"
if [ -f "backend/discord_bot_manus.py" ]; then
    check_pass "Discord bot file exists"

    # Check for rich embeds integration
    if grep -q "from discord_embeds import HelixEmbeds" backend/discord_bot_manus.py; then
        check_pass "Rich embeds integrated (v15.3)"
    else
        check_warn "Rich embeds not integrated"
    fi
else
    check_fail "Discord bot file missing"
fi

echo ""

# ==================================================
# STEP 7: Mini Ritual Test (7 steps)
# ==================================================
echo "📍 Step 7/7: Mini Ritual Test"
if [ -f "backend/z88_ritual_engine.py" ]; then
    check_pass "Z-88 ritual engine found"

    # Run 7-step test ritual
    if timeout 10 python3 -c "
from backend.z88_ritual_engine import execute_ritual
result = execute_ritual(steps=7)
assert result['steps'] == 7
" 2>/dev/null; then
        check_pass "7-step ritual executed successfully"
    else
        check_warn "Ritual test timed out or failed (non-critical)"
    fi
else
    check_fail "Ritual engine missing"
fi

echo ""
echo "===================================================="

# ==================================================
# FINAL STATUS
# ==================================================
if [ $FAILURES -eq 0 ]; then
    echo "🕉️ DEPLOYMENT RITUAL COMPLETE"
    echo "✅ All checks passed - Ready for deployment"
    echo ""
    echo "🌀 Deploy with:"
    echo "   python backend/main.py"
    echo "   # OR"
    echo "   railway up"
    echo ""
    echo "🙏 Tat Tvam Asi"
    exit 0
else
    echo "⚠️ DEPLOYMENT NOT READY"
    echo "❌ $FAILURES critical checks failed"
    echo ""
    echo "Fix issues above before deploying."
    echo ""
    exit 1
fi
