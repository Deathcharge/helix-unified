#!/bin/bash
# Command Module Audit Script
# Checks which command modules are loaded vs available

echo "🔍 Helix Command Module Audit"
echo "=============================="
echo ""

# Find all command modules
echo "📁 Available command modules:"
find backend/commands -name "*.py" -type f ! -name "__init__.py" ! -name "helpers.py" | while read file; do
    module=$(basename "$file" .py)
    count=$(grep -c "@commands.command" "$file" || echo "0")
    echo "  • $module ($count commands)"
done

echo ""
echo "✅ Loaded in discord_bot_manus.py:"
grep -o "commands\.[a-z_]*" backend/discord_bot_manus.py | sort -u | while read module; do
    module_name=$(echo "$module" | cut -d'.' -f2)
    echo "  • $module_name"
done

echo ""
echo "❌ NOT loaded (orphaned modules):"

# Check each module file
for file in backend/commands/*.py; do
    module=$(basename "$file" .py)

    # Skip __init__ and helpers
    if [[ "$module" == "__init__" ]] || [[ "$module" == "helpers" ]]; then
        continue
    fi

    # Check if loaded
    if ! grep -q "commands\.$module" backend/discord_bot_manus.py; then
        count=$(grep -c "@commands.command" "$file" || echo "0")
        echo "  • $module ($count commands missing)"
    fi
done

echo ""
echo "💡 To enable missing modules, run:"
echo "   python3 scripts/enable_missing_commands.py"
