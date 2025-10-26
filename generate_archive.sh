#!/bin/bash
# generate_archive.sh
# Creates Helix v15.2 Blueprint Archive ZIP

set -e

echo "🌀 Generating Helix v15.2 Blueprint Archive"
echo "==========================================="

ARCHIVE_NAME="Helix_v15.2_Blueprints"
ARCHIVE_DIR="${ARCHIVE_NAME}"

# Clean previous archive
if [ -d "$ARCHIVE_DIR" ]; then
    echo "🧹 Cleaning previous archive directory..."
    rm -rf "$ARCHIVE_DIR"
fi

if [ -f "${ARCHIVE_NAME}.zip" ]; then
    echo "🧹 Removing previous archive file..."
    rm -f "${ARCHIVE_NAME}.zip"
fi

# Create archive directory
echo "📁 Creating archive structure..."
mkdir -p "$ARCHIVE_DIR"
mkdir -p "$ARCHIVE_DIR/Helix/state"
mkdir -p "$ARCHIVE_DIR/Helix/agents/blueprints"
mkdir -p "$ARCHIVE_DIR/backend/agents"

# Copy Helix state files
echo "📋 Copying UCF state files..."
if [ -f "Helix/state/ucf_state.json" ]; then
    cp Helix/state/ucf_state.json "$ARCHIVE_DIR/Helix/state/"
fi

if [ -f "Helix/state/blueprints_manifest.json" ]; then
    cp Helix/state/blueprints_manifest.json "$ARCHIVE_DIR/Helix/state/"
fi

# Copy all blueprint files
echo "🧩 Copying agent blueprints..."
if [ -d "Helix/agents/blueprints" ]; then
    cp Helix/agents/blueprints/*.json "$ARCHIVE_DIR/Helix/agents/blueprints/" 2>/dev/null || echo "⚠️  No blueprint files found"
fi

# Copy backend scripts
echo "🔧 Copying backend scripts..."
if [ -f "backend/agents/verify_blueprints.py" ]; then
    cp backend/agents/verify_blueprints.py "$ARCHIVE_DIR/backend/agents/"
fi

if [ -f "backend/agents/collective_loop.py" ]; then
    cp backend/agents/collective_loop.py "$ARCHIVE_DIR/backend/agents/"
fi

# Copy setup script
echo "⚙️  Copying setup script..."
if [ -f "setup_helix_blueprints_v15_2.sh" ]; then
    cp setup_helix_blueprints_v15_2.sh "$ARCHIVE_DIR/"
fi

# Copy documentation
echo "📖 Copying documentation..."
if [ -f "README_v15.2.md" ]; then
    cp README_v15.2.md "$ARCHIVE_DIR/README.md"
fi

if [ -f "RELEASE_NOTES_v15.2.md" ]; then
    cp RELEASE_NOTES_v15.2.md "$ARCHIVE_DIR/RELEASE_NOTES.md"
fi

# Create archive
echo "📦 Creating ZIP archive..."
zip -r "${ARCHIVE_NAME}.zip" "$ARCHIVE_DIR/" -q

# Cleanup
echo "🧹 Cleaning up temporary directory..."
rm -rf "$ARCHIVE_DIR"

# Show results
echo ""
echo "==========================================="
echo "✅ Archive created: ${ARCHIVE_NAME}.zip"
echo ""

# Show archive contents
if command -v unzip &> /dev/null; then
    echo "📋 Archive contents:"
    unzip -l "${ARCHIVE_NAME}.zip" | head -20
fi

echo ""
echo "📊 Archive size: $(du -h ${ARCHIVE_NAME}.zip | cut -f1)"
echo ""
echo "🌀 Helix v15.2 Blueprint Archive Ready!"
echo "   Tat Tvam Asi 🙏"
