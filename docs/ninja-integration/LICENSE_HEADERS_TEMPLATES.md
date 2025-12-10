# License Header Templates for Helix Discord Bot

## Quick Reference Guide

Use these templates to add license headers to your code files before uploading to GitHub.

---

## Python Files (.py)

### Template 1: Minimal (Recommended for most files)

```python
"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""
```

### Template 2: With AI Collaboration Notice

```python
"""
Helix Unified Discord Bot
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.

Developed in collaboration with AI systems.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for full terms.
"""
```

### Template 3: Detailed (For core/critical files)

```python
"""
Helix Unified Discord Bot - [Module Name]
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.

PROPRIETARY AND CONFIDENTIAL

This file is part of the Helix Collective project and contains proprietary
and confidential information. Unauthorized copying, modification, distribution,
or use of this file, via any medium, is strictly prohibited.

For licensing inquiries: andrew@deathcharge.dev
"""
```

---

## JavaScript/TypeScript Files (.js, .ts)

### Template 1: Minimal

```javascript
/**
 * Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
 * PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
 */
```

### Template 2: With AI Collaboration

```javascript
/**
 * Helix Unified Discord Bot
 * Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
 * 
 * Developed in collaboration with AI systems.
 * PROPRIETARY AND CONFIDENTIAL - See LICENSE file for full terms.
 */
```

---

## Markdown Files (.md)

### Template 1: Minimal

```markdown
<!--
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
-->
```

### Template 2: For Documentation

```markdown
<!--
Helix Unified Discord Bot Documentation
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL
-->
```

---

## HTML Files (.html)

```html
<!--
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
-->
```

---

## CSS Files (.css)

```css
/*
 * Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
 * PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
 */
```

---

## Shell Scripts (.sh)

```bash
#!/bin/bash
#
# Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
# PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
#
```

---

## YAML/TOML Config Files (.yml, .yaml, .toml)

```yaml
# Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
# PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
```

---

## JSON Files (package.json, etc.)

**NOTE:** Don't add headers to `package.json` or `requirements.txt` - these are dependency files.

For other JSON files:
```json
{
  "_comment": "Copyright (c) 2025 Andrew John Ward. All Rights Reserved. PROPRIETARY AND CONFIDENTIAL",
  ...
}
```

---

## Files That DON'T Need Headers

❌ **Skip these files:**
- `package.json`
- `requirements.txt`
- `package-lock.json`
- `.gitignore`
- `.env.example`
- `LICENSE` (it IS the license)
- `README.md` (copyright notice at bottom instead)
- `.dockerignore`
- `Dockerfile` (optional)

---

## Bulk Adding Headers - Python Script

Save this as `add_license_headers.py`:

```python
#!/usr/bin/env python3
"""
Script to add license headers to all code files.
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
"""

import os
from pathlib import Path

PYTHON_HEADER = '''"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""

'''

JS_HEADER = '''/**
 * Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
 * PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
 */

'''

MD_HEADER = '''<!--
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
-->

'''

def add_header_to_file(filepath, header):
    """Add license header to a file if it doesn't already have one."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if header already exists
    if 'Copyright (c) 2025 Andrew John Ward' in content:
        print(f"✓ {filepath} - Already has header")
        return
    
    # Add header
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header + content)
    print(f"✓ {filepath} - Header added")

def process_directory(directory):
    """Process all files in directory."""
    skip_files = {
        'package.json', 'package-lock.json', 'requirements.txt',
        '.gitignore', '.env.example', 'LICENSE', '.dockerignore'
    }
    
    skip_dirs = {
        '__pycache__', 'node_modules', '.git', 'venv', 'env',
        'dist', 'build', '.pytest_cache'
    }
    
    for root, dirs, files in os.walk(directory):
        # Remove skip directories from search
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file in skip_files:
                continue
            
            filepath = Path(root) / file
            
            if file.endswith('.py'):
                add_header_to_file(filepath, PYTHON_HEADER)
            elif file.endswith(('.js', '.ts')):
                add_header_to_file(filepath, JS_HEADER)
            elif file.endswith('.md') and file != 'README.md':
                add_header_to_file(filepath, MD_HEADER)

if __name__ == '__main__':
    print("Adding license headers to all code files...")
    process_directory('.')
    print("\nDone! Review the changes before committing.")
```

**Usage:**
```bash
python add_license_headers.py
```

---

## Manual Addition Guide

### For Each Python File:

1. Open the file
2. Copy the minimal Python header template
3. Paste at the very top of the file (before any imports)
4. Save

### For Each JavaScript/TypeScript File:

1. Open the file
2. Copy the minimal JS header template
3. Paste at the very top of the file
4. Save

### For Each Markdown File:

1. Open the file
2. Copy the minimal MD header template
3. Paste at the very top of the file (before the title)
4. Save

---

## Verification Checklist

After adding headers, verify:

- [ ] All `.py` files have headers (except `__init__.py` if empty)
- [ ] All `.js`/`.ts` files have headers
- [ ] All `.md` documentation files have headers (except README.md)
- [ ] No headers in `package.json`, `requirements.txt`, etc.
- [ ] Headers are at the very top of each file
- [ ] Headers don't break the code (test run everything!)

---

## Example: Before and After

### Before (agent_bot.py):
```python
import discord
from discord.ext import commands

class AgentBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!')
```

### After (agent_bot.py):
```python
"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""

import discord
from discord.ext import commands

class AgentBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!')
```

---

## Pro Tips

1. **Test After Adding**: Run your code after adding headers to ensure nothing broke
2. **Consistent Format**: Use the same template throughout your project
3. **Don't Overdo It**: Minimal headers are professional and sufficient
4. **Update Year**: Change to 2026 next year if still developing
5. **Git Commit**: Commit header additions separately for clean history

---

## Questions?

If you're unsure about a specific file type, use the minimal template format appropriate for that language's comment syntax.

**Remember:** The goal is legal protection, not decoration. Keep headers simple and consistent.