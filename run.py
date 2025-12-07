#!/usr/bin/env python3
"""
🌀 Helix Collective v15.5 — Master Entry Point
run.py — Single launcher that fixes import resolution

This script ensures the project root is in Python's path before
launching the FastAPI application via uvicorn.

Author: Andrew John Ward (Architect)
Version: 15.5.0
"""

import os
import sys
from pathlib import Path

# Add project root to Python path for proper import resolution
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print(f"🌀 Helix Collective v15.5 - Master Entry Point")
print(f"📁 Project root: {project_root}")
print(f"🐍 Python version: {sys.version}")
print(f"🔧 Python path: {sys.path[:3]}...")

# Import and run uvicorn
if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Get port from Railway environment or default to 8000
    port = int(os.getenv("PORT", 8000))

    print(f"🚀 Starting Helix Collective v15.5 on port {port}")
    print(f"🌐 Binding to 0.0.0.0:{port} (Railway/Docker compatible)")

    # Launch FastAPI application
    # CRITICAL: Must bind to 0.0.0.0 for Railway/Docker
    # Uses string module path to avoid premature imports
    uvicorn.run(
        "backend.main:app",  # Module string path
        host="0.0.0.0",      # CRITICAL for Railway/Docker
        port=port,           # Uses Railway's dynamic PORT
        log_level="info",
        access_log=True,
        reload=False         # Disable reload in production
    )
