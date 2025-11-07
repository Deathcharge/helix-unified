# Backend agents package
# This makes the agents directory a proper Python package
#
# IMPORTANT: Re-export everything from backend/agents.py (the file, not this directory)
# This is necessary because Python prefers the agents/ directory over agents.py file

import importlib.util
import sys
from pathlib import Path

# Load agents.py as a module with proper import resolution
_agents_file = Path(__file__).parent.parent / "agents.py"
_spec = importlib.util.spec_from_file_location("backend.agents_file", _agents_file)
_agents_module = importlib.util.module_from_spec(_spec)

# Add to sys.modules so imports work correctly
sys.modules['backend.agents_file'] = _agents_module

# Execute the module
_spec.loader.exec_module(_agents_module)

# Re-export everything from the loaded module
for _name in dir(_agents_module):
    if not _name.startswith('_'):
        globals()[_name] = getattr(_agents_module, _name)

# Clean up helper variables
del sys, Path, importlib, _agents_file, _spec, _agents_module, _name
