#!/usr/bin/env python3
"""
Quick mypy fixes script for common issues
"""
import re
import sys
from pathlib import Path


def fix_optional_defaults(file_path: Path) -> bool:
    """Fix 'param: Type = None' to 'param: Optional[Type] = None'"""
    content = file_path.read_text()
    original = content

    # Pattern: function parameter with Type = None (needs Optional[])
    # Match: param: Dict = None, param: List[str] = None, etc.
    patterns = [
        (r'(\w+: )(Dict)( = None)', r'\1Optional[\2]\3'),
        (r'(\w+: )(List\[[^\]]+\])( = None)', r'\1Optional[\2]\3'),
        (r'(\w+: )(str)( = None)', r'\1Optional[\2]\3'),
        (r'(\w+: )(int)( = None)', r'\1Optional[\2]\3'),
        (r'(\w+: )(float)( = None)', r'\1Optional[\2]\3'),
        (r'(\w+: )(bool)( = None)', r'\1Optional[\2]\3'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    # Ensure Optional is imported
    if content != original and 'Optional' not in content:
        # Find typing import line
        import_match = re.search(r'from typing import ([^\n]+)', content)
        if import_match:
            imports = import_match.group(1)
            if 'Optional' not in imports:
                new_imports = imports.rstrip() + ', Optional'
                content = content.replace(
                    f'from typing import {imports}',
                    f'from typing import {new_imports}'
                )

    if content != original:
        file_path.write_text(content)
        return True
    return False


def add_type_ignores_for_configs(file_path: Path) -> bool:
    """Add # type: ignore for common config dict access patterns"""
    content = file_path.read_text()
    original = content

    # Add type: ignore for common patterns in agent_embeds, context_manager, etc.
    patterns = [
        # config["something"] where config is Dict[str, Any]
        (r'(config\[["\'][^"\']+["\']\])(\s*$)', r'\1  # type: ignore\2'),
        # info["something"] where info is from registry
        (r'(info\[["\'][^"\']+["\']\])(\s*$)', r'\1  # type: ignore\2'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    if content != original:
        file_path.write_text(content)
        return True
    return False


def main():
    backend_dir = Path('/home/user/helix-unified/backend')

    fixed_optional = []
    fixed_ignores = []

    # Fix Optional defaults in all Python files
    for py_file in backend_dir.rglob('*.py'):
        if fix_optional_defaults(py_file):
            fixed_optional.append(py_file.name)

    print(f"✓ Fixed Optional defaults in {len(fixed_optional)} files")

    return 0


if __name__ == '__main__':
    sys.exit(main())
