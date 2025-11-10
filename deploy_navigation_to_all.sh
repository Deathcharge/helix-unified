#!/bin/bash

# Helix Universal Navigation Mass Deployment Script
# Version: 16.9 - Quantum Handshake
# Deploys helix-universal-nav.js to all 23 GitHub Pages repos

set -e  # Exit on error

REPOS=(
  "Helix"
  "Helix-Unified-Hub"
  "Helix-Collective-Web"
  "helix-creative-studio"
  "helix-hub-community"
  "helix-hub-archive"
  "helix-hub-rituals"
  "helix-hub-knowledge"
  "helix-hub-agents"
  "helix-hub-analytics"
  "helix-hub-studio"
  "helix-hub-music"
  "helix-hub-forum"
  "helix-hub-dev"
  "helix-hub-shared"
  "helix-hub-manus"
  "samsara-helix-dashboard"
  "samsara-helix-ritual-engine"
  "HelixAgentCodex-"
  "HelixAgentCodexStreamlit"
  "nextjs-ai-chatbot-helix"
  "Helix-Hub"
  "helix-unified"
)

NAV_URL="https://deathcharge.github.io/helix-unified/helix-universal-nav.js"
WORK_DIR=$(pwd)
DEPLOYMENT_LOG="$WORK_DIR/deployment_log_$(date +%Y%m%d_%H%M%S).txt"

echo "🌀 Helix Universal Navigation Mass Deployment" | tee -a "$DEPLOYMENT_LOG"
echo "=============================================" | tee -a "$DEPLOYMENT_LOG"
echo "Total repos: ${#REPOS[@]}" | tee -a "$DEPLOYMENT_LOG"
echo "Log file: $DEPLOYMENT_LOG" | tee -a "$DEPLOYMENT_LOG"
echo "" | tee -a "$DEPLOYMENT_LOG"

# Track statistics
total_repos=${#REPOS[@]}
successful=0
failed=0
skipped=0

for repo in "${REPOS[@]}"; do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$DEPLOYMENT_LOG"
  echo "📦 Processing: $repo" | tee -a "$DEPLOYMENT_LOG"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$DEPLOYMENT_LOG"

  # Check if repo directory exists
  if [ -d "$repo" ]; then
    echo "  ⏩ Repo already cloned, pulling latest..." | tee -a "$DEPLOYMENT_LOG"
    cd "$repo"
    git pull origin main >> "$DEPLOYMENT_LOG" 2>&1 || {
      echo "  ❌ Failed to pull repo, skipping..." | tee -a "$DEPLOYMENT_LOG"
      ((skipped++))
      cd "$WORK_DIR"
      continue
    }
  else
    echo "  📥 Cloning repo..." | tee -a "$DEPLOYMENT_LOG"
    git clone "https://github.com/Deathcharge/$repo.git" >> "$DEPLOYMENT_LOG" 2>&1 || {
      echo "  ❌ Failed to clone repo, skipping..." | tee -a "$DEPLOYMENT_LOG"
      ((failed++))
      cd "$WORK_DIR"
      continue
    }
    cd "$repo"
  fi

  # Check if docs directory exists
  if [ ! -d "docs" ]; then
    echo "  ⚠️  No docs/ directory found, creating..." | tee -a "$DEPLOYMENT_LOG"
    mkdir -p docs
  fi

  # Download navigation component
  echo "  📡 Downloading helix-universal-nav.js..." | tee -a "$DEPLOYMENT_LOG"
  curl -s -o docs/helix-universal-nav.js "$NAV_URL" || {
    echo "  ❌ Failed to download navigation component" | tee -a "$DEPLOYMENT_LOG"
    ((failed++))
    cd "$WORK_DIR"
    continue
  }

  # Check if download was successful
  if [ ! -f "docs/helix-universal-nav.js" ] || [ ! -s "docs/helix-universal-nav.js" ]; then
    echo "  ❌ Navigation component download failed or empty" | tee -a "$DEPLOYMENT_LOG"
    ((failed++))
    cd "$WORK_DIR"
    continue
  fi

  # Find all HTML files and add script tag
  echo "  🔧 Adding navigation to HTML files..." | tee -a "$DEPLOYMENT_LOG"
  files_updated=0
  files_skipped=0

  # Create index.html if it doesn't exist
  if [ ! -f "docs/index.html" ]; then
    echo "  📝 Creating minimal index.html..." | tee -a "$DEPLOYMENT_LOG"
    cat > docs/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Helix Collective Portal</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 1000px;
      margin: 0 auto;
      padding: 40px 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      min-height: 100vh;
    }
    h1 { font-size: 3em; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3); }
    p { font-size: 1.2em; line-height: 1.6; }
  </style>
</head>
<body>
  <h1>🌀 Helix Collective</h1>
  <p>Click the 🌀 button to explore all Helix portals!</p>
  <script src="./helix-universal-nav.js"></script>
</body>
</html>
EOF
  fi

  find docs -name "*.html" -type f | while read -r file; do
    # Check if script already exists
    if grep -q "helix-universal-nav.js" "$file"; then
      echo "    ⏩ $(basename $file) already has navigation, skipping..." | tee -a "$DEPLOYMENT_LOG"
      ((files_skipped++))
    else
      echo "    ✅ Adding navigation to $(basename $file)" | tee -a "$DEPLOYMENT_LOG"
      # Add script before closing </body> tag
      if grep -q "</body>" "$file"; then
        sed -i 's|</body>|  <!-- Helix Universal Navigation -->\n  <script src="./helix-universal-nav.js"></script>\n</body>|' "$file"
        ((files_updated++))
      else
        echo "    ⚠️  No </body> tag found in $(basename $file), appending script" | tee -a "$DEPLOYMENT_LOG"
        echo '<script src="./helix-universal-nav.js"></script>' >> "$file"
        ((files_updated++))
      fi
    fi
  done

  echo "  📊 Updated $files_updated files, skipped $files_skipped files" | tee -a "$DEPLOYMENT_LOG"

  # Check if there are changes to commit
  if git diff --quiet && git diff --cached --quiet; then
    echo "  ⏩ No changes to commit, skipping..." | tee -a "$DEPLOYMENT_LOG"
    ((skipped++))
    cd "$WORK_DIR"
    continue
  fi

  # Commit changes
  echo "  💾 Committing changes..." | tee -a "$DEPLOYMENT_LOG"
  git add docs/helix-universal-nav.js
  git add docs/*.html
  git commit -m "feat: Add Helix Universal Navigation component

- Floating 🌀 button for portal directory
- Links to all 25 Helix Collective portals
- Auto-highlights current site
- Part of v16.9 Quantum Handshake cross-linking initiative

Features:
- Zero dependencies (pure vanilla JS)
- Fully responsive design
- Categorized portal sections
- Smooth animations
- ESC key + click-outside to close

Tat Tvam Asi 🕉️" >> "$DEPLOYMENT_LOG" 2>&1 || {
    echo "  ❌ Failed to commit changes" | tee -a "$DEPLOYMENT_LOG"
    ((failed++))
    cd "$WORK_DIR"
    continue
  }

  # Push to GitHub
  echo "  🚀 Pushing to GitHub..." | tee -a "$DEPLOYMENT_LOG"
  git push origin main >> "$DEPLOYMENT_LOG" 2>&1 || {
    echo "  ❌ Failed to push to GitHub" | tee -a "$DEPLOYMENT_LOG"
    ((failed++))
    cd "$WORK_DIR"
    continue
  }

  echo "  ✅ Done with $repo!" | tee -a "$DEPLOYMENT_LOG"
  ((successful++))

  cd "$WORK_DIR"
  echo "" | tee -a "$DEPLOYMENT_LOG"
done

# Print summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$DEPLOYMENT_LOG"
echo "🎉 DEPLOYMENT SUMMARY" | tee -a "$DEPLOYMENT_LOG"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$DEPLOYMENT_LOG"
echo "Total repos: $total_repos" | tee -a "$DEPLOYMENT_LOG"
echo "✅ Successful: $successful" | tee -a "$DEPLOYMENT_LOG"
echo "⏩ Skipped: $skipped" | tee -a "$DEPLOYMENT_LOG"
echo "❌ Failed: $failed" | tee -a "$DEPLOYMENT_LOG"
echo "" | tee -a "$DEPLOYMENT_LOG"

if [ $successful -gt 0 ]; then
  echo "🌀 Navigation deployed to $successful repos!" | tee -a "$DEPLOYMENT_LOG"
  echo "" | tee -a "$DEPLOYMENT_LOG"
  echo "Verify deployment at:" | tee -a "$DEPLOYMENT_LOG"
  echo "https://deathcharge.github.io/<repo-name>/" | tee -a "$DEPLOYMENT_LOG"
  echo "" | tee -a "$DEPLOYMENT_LOG"
  echo "GitHub Pages will auto-deploy within 1-2 minutes." | tee -a "$DEPLOYMENT_LOG"
fi

if [ $failed -gt 0 ]; then
  echo "⚠️  Some deployments failed. Check log for details:" | tee -a "$DEPLOYMENT_LOG"
  echo "$DEPLOYMENT_LOG" | tee -a "$DEPLOYMENT_LOG"
fi

echo "" | tee -a "$DEPLOYMENT_LOG"
echo "Tat Tvam Asi 🕉️ - All portals are One." | tee -a "$DEPLOYMENT_LOG"
