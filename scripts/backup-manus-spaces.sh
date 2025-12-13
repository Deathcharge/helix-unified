#!/bin/bash
# Backup all Manus Spaces to GitHub
echo "🌀 Backing up Manus Spaces..."
for space in helixcollective samsarahelix nexusdash helixdash helixport helixsync helixstudio; do
  echo "Backing up $space..."
  # Add backup logic here
done
echo "✅ Backup complete"
