#!/bin/bash

# Helix Collective Dashboard Deployment Script
# Creates PR for dashboard integration

echo "🌀 Helix Collective Dashboard Deployment Script"
echo "============================================="

# Check if we're on the correct branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "feature/helix-collective-dashboard-integration" ]; then
    echo "❌ Error: Not on the correct branch"
    echo "Current branch: $CURRENT_BRANCH"
    echo "Expected: feature/helix-collective-dashboard-integration"
    exit 1
fi

echo "✅ On correct branch: $CURRENT_BRANCH"

# Check git status
echo "📊 Git Status:"
git status

# Show commits on this branch
echo "📝 Commits on this branch:"
git log --oneline main..HEAD

echo ""
echo "🚀 Ready to push and create PR!"
echo ""
echo "To complete deployment:"
echo "1. Push the branch:"
echo "   git push origin feature/helix-collective-dashboard-integration"
echo ""
echo "2. Create PR on GitHub with:"
echo "   - Title: 🎯 SuperNinja: Add Helix Collective Agents Dashboard"
echo "   - Description: Multi-agent consciousness dashboard with real-time metrics"
echo ""
echo "3. Dashboard files created:"
echo "   - frontend/helix-collective-agents/index.html"
echo "   - frontend/helix-collective-agents/styles.css"
echo ""
echo "4. Features included:"
echo "   - Agent registry with live status"
echo "   - Consciousness stream simulation"
echo "   - UCF metrics monitoring"
echo "   - Responsive cosmic design"
echo "   - Real-time system updates"