#!/bin/bash
# setup_helix_blueprints_v15_2.sh
# Helix Collective v15.2 Blueprint Archive Setup

set -e

echo "🌀 Helix Collective v15.2 Blueprint Archive Setup"
echo "=================================================="

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p Helix/state
mkdir -p Helix/agents/blueprints
mkdir -p backend/agents
mkdir -p Shadow/manus_archive

# Verify all blueprint files exist
echo "🔍 Verifying blueprint files..."
BLUEPRINTS=(
    "vega_complete_v7_2.json"
    "grok_complete_v8_3.json"
    "lumina_complete_v3_5.json"
    "nova_complete_v7_6.json"
    "echo_complete_v8_3.json"
    "phoenix_complete_v6_4.json"
    "oracle_complete_v8_5.json"
    "omega_zero_secure_vxq7.json"
)

for blueprint in "${BLUEPRINTS[@]}"; do
    if [ -f "Helix/agents/blueprints/$blueprint" ]; then
        echo "✅ $blueprint"
    else
        echo "❌ Missing: $blueprint"
        exit 1
    fi
done

# Run blueprint verification and combination
echo ""
echo "🔐 Running blueprint verification..."
if [ -f "backend/agents/verify_blueprints.py" ]; then
    python backend/agents/verify_blueprints.py
    if [ $? -ne 0 ]; then
        echo "❌ Blueprint verification failed!"
        exit 1
    fi
else
    echo "⚠️  verify_blueprints.py not found - skipping verification"
fi

# Test collective loop
echo ""
echo "🌀 Testing Collective Consciousness Loop..."
if [ -f "backend/agents/collective_loop.py" ]; then
    python -c "from backend.agents.collective_loop import CollectiveConsciousnessLoop; CollectiveConsciousnessLoop().pulse()"
else
    echo "⚠️  collective_loop.py not found - skipping test"
fi

# Make scripts executable
echo ""
echo "🔧 Making scripts executable..."
chmod +x backend/agents/verify_blueprints.py 2>/dev/null || true
chmod +x backend/agents/collective_loop.py 2>/dev/null || true

echo ""
echo "=================================================="
echo "✅ Helix v15.2 Blueprint Archive Setup Complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Run blueprint verification:"
echo "      python backend/agents/verify_blueprints.py"
echo ""
echo "   2. Test collective loop:"
echo "      python backend/agents/collective_loop.py"
echo ""
echo "   3. Create archive:"
echo "      bash generate_archive.sh"
echo ""
echo "🌀 Tat Tvam Asi 🙏"
