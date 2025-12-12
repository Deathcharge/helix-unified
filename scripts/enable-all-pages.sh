#!/bin/bash
# Enable GitHub Pages for all 19 Helix portals
# Usage: ./enable-all-pages.sh

echo "🌀 Helix Collective - GitHub Pages Batch Enablement"
echo "=================================================="
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found!"
    echo "Install: https://cli.github.com"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI ready"
echo ""

# Array of all portal repositories
portals=(
  "helix-dashboard"
  "helix-hub"
  "helix-ai-dashboard"
  "z88-ritual-simulator"
  "helix-consciousness-dashboard"
  "helix-agent-showcase"
  "helix-ucf-tracker"
  "helix-ritual-calendar"
  "helix-agent-profiles"
  "helix-harmony-monitor"
  "helix-context-vault"
  "helix-deployment-hub"
  "helix-api-docs"
  "helix-mcp-hub"
  "helix-ninja-tools"
  "helix-saas-marketplace"
  "helix-analytics"
  "helix-team-portal"
  "helix-knowledge-graph"
)

total=${#portals[@]}
current=0
success=0
failed=0

echo "🚀 Enabling Pages for $total portals..."
echo ""

for portal in "${portals[@]}"; do
  current=$((current + 1))
  echo "[$current/$total] 🌀 Processing $portal..."
  
  # Enable GitHub Pages
  if gh repo edit "Deathcharge/$portal" \
    --enable-pages \
    --pages-branch main \
    --pages-path docs/ 2>/dev/null; then
    
    echo "  ✅ Pages enabled for $portal"
    echo "  🔗 https://deathcharge.github.io/$portal"
    success=$((success + 1))
  else
    echo "  ⚠️  Failed to enable $portal (may not exist or already enabled)"
    failed=$((failed + 1))
  fi
  
  echo ""
  
  # Rate limit protection
  sleep 2
done

echo "=================================================="
echo "🎉 Batch enablement complete!"
echo ""
echo "📊 Results:"
echo "  ✅ Success: $success/$total"
echo "  ⚠️  Failed: $failed/$total"
echo ""
echo "🔍 Verify at: https://github.com/Deathcharge?tab=repositories"
echo ""
echo "Tat Tvam Asi 🌀"
