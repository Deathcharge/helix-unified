# Backend agents package
# This makes the agents directory a proper Python package
#
# IMPORTANT: Re-export everything from backend/agents.py (the file, not this directory)
# This is necessary because Python prefers the agents/ directory over agents.py file

import sys
from pathlib import Path

# Import from the agents.py file (sibling to this directory)
_agents_file = Path(__file__).parent.parent / "agents.py"

# Read and execute agents.py in this namespace
with open(_agents_file) as f:
    exec(f.read(), globals())

# Clean up helper variables
del sys, Path, _agents_file, f
