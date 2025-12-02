"""
📁 Web OS File System
REST API for file operations with sandbox security
Supports: list, read, write, delete, create files/folders
"""

import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)

# ============================================================================
# FILE SYSTEM MODELS
# ============================================================================


@dataclass
class FileInfo:
    """File information"""

    name: str
    type: str  # 'file' | 'folder'
    path: str
    size: int
    created: str
    modified: str
    readable: bool = True
    writable: bool = True


class FileSystemManager:
    """Secure file system manager for Web OS"""

    def __init__(self, root_dir: str = '/home/helix'):
        self.root_dir = root_dir
        self.max_file_size = 10 * 1024 * 1024  # 10MB

        # Create root if needed
        Path(self.root_dir).mkdir(parents=True, exist_ok=True)

        # Create sample structure
        self._create_sample_structure()

    def _create_sample_structure(self):
        """Create sample file structure"""
        # Create directories
        for dir_name in ['projects', 'documents', 'scripts', 'data']:
            dir_path = os.path.join(self.root_dir, dir_name)
            Path(dir_path).mkdir(parents=True, exist_ok=True)

        # Create sample files
        sample_files = {
            'README.md': '# Helix Web OS\n\nBrowser-based operating system with file explorer, terminal, and code editor.',
            'projects/sample.py': '#!/usr/bin/env python\n# Sample project\nprint("Hello from Helix!")',
            'documents/notes.txt': 'Quick notes and ideas',
            'scripts/backup.sh': '#!/bin/bash\n# Backup script',
        }

        for file_path, content in sample_files.items():
            full_path = os.path.join(self.root_dir, file_path)
            if not os.path.exists(full_path):
                Path(full_path).parent.mkdir(parents=True, exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write(content)

    def _validate_path(self, path: str) -> tuple[bool, str]:
        """Validate path is within sandbox"""
        # Resolve to absolute path
        if path.startswith('/'):
            abs_path = path
        else:
            abs_path = os.path.join(self.root_dir, path)

        abs_path = os.path.abspath(abs_path)

        # Check if within root
        if not abs_path.startswith(self.root_dir):
            return False, f'Access denied: {path}'

        return True, ''

    def list_directory(self, path: str = '') -> tuple[bool, List[FileInfo] | str]:
        """List directory contents"""
        if not path:
            path = self.root_dir

        valid, error = self._validate_path(path)
        if not valid:
            return False, error

        if not path.startswith('/'):
            path = os.path.join(self.root_dir, path)

        abs_path = os.path.abspath(path)

        try:
            if not os.path.exists(abs_path):
                return False, f'Path not found: {path}'

            if not os.path.isdir(abs_path):
                return False, f'Not a directory: {path}'

            files: List[FileInfo] = []

            for item in sorted(os.listdir(abs_path)):
                item_path = os.path.join(abs_path, item)

                try:
                    stat = os.stat(item_path)
                    is_dir = os.path.isdir(item_path)

                    file_info = FileInfo(
                        name=item,
                        type='folder' if is_dir else 'file',
                        path=os.path.relpath(item_path, self.root_dir),
                        size=stat.st_size if not is_dir else 0,
                        created=datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        readable=os.access(item_path, os.R_OK),
                        writable=os.access(item_path, os.W_OK),
                    )
                    files.append(file_info)
                except Exception as e:
                    logger.warning(f"Error reading file info: {e}")
                    continue

            return True, files

        except Exception as e:
            return False, f'Error listing directory: {str(e)}'

    def read_file(self, path: str) -> tuple[bool, str | bytes]:
        """Read file contents"""
        valid, error = self._validate_path(path)
        if not valid:
            return False, error

        if not path.startswith('/'):
            path = os.path.join(self.root_dir, path)

        abs_path = os.path.abspath(path)

        try:
            if not os.path.exists(abs_path):
                return False, f'File not found: {path}'

            if os.path.isdir(abs_path):
                return False, f'Is a directory: {path}'

            # Check file size
            file_size = os.path.getsize(abs_path)
            if file_size > self.max_file_size:
                return False, f'File too large (max {self.max_file_size / 1024 / 1024}MB)'

            # Try reading as text first
            try:
                with open(abs_path, 'r', encoding='utf-8') as f:
                    return True, f.read()
            except UnicodeDecodeError:
                # Read as binary and return base64
                with open(abs_path, 'rb') as f:
                    import base64

                    return True, base64.b64encode(f.read()).decode()

        except Exception as e:
            return False, f'Error reading file: {str(e)}'

    def write_file(self, path: str, content: str) -> tuple[bool, str]:
        """Write file contents"""
        valid, error = self._validate_path(path)
        if not valid:
            return False, error

        if not path.startswith('/'):
            path = os.path.join(self.root_dir, path)

        abs_path = os.path.abspath(path)

        try:
            # Create parent directories if needed
            Path(abs_path).parent.mkdir(parents=True, exist_ok=True)

            # Check size
            if len(content) > self.max_file_size:
                return False, f'Content too large'  # noqa

            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True, f'File written: {path}'

        except Exception as e:
            return False, f'Error writing file: {str(e)}'

    def delete_file(self, path: str) -> tuple[bool, str]:
        """Delete file"""
        valid, error = self._validate_path(path)
        if not valid:
            return False, error

        if not path.startswith('/'):
            path = os.path.join(self.root_dir, path)

        abs_path = os.path.abspath(path)

        try:
            if not os.path.exists(abs_path):
                return False, f'Path not found: {path}'

            if os.path.isdir(abs_path):
                return False, f'Use folder deletion endpoint for directories'  # noqa

            os.remove(abs_path)
            return True, f'File deleted: {path}'

        except Exception as e:
            return False, f'Error deleting file: {str(e)}'

    def delete_folder(self, path: str) -> tuple[bool, str]:
        """Delete folder recursively"""
        valid, error = self._validate_path(path)
        if not valid:
            return False, error

        if not path.startswith('/'):
            path = os.path.join(self.root_dir, path)

        abs_path = os.path.abspath(path)

        try:
            if not os.path.exists(abs_path):
                return False, f'Path not found: {path}'

            if not os.path.isdir(abs_path):
                return False, f'Not a directory: {path}'

            import shutil

            shutil.rmtree(abs_path)
            return True, f'Folder deleted: {path}'

        except Exception as e:
            return False, f'Error deleting folder: {str(e)}'

    def create_folder(self, path: str) -> tuple[bool, str]:
        """Create folder"""
        valid, error = self._validate_path(path)
        if not valid:
            return False, error

        if not path.startswith('/'):
            path = os.path.join(self.root_dir, path)

        abs_path = os.path.abspath(path)

        try:
            if os.path.exists(abs_path):
                return False, f'Already exists: {path}'

            Path(abs_path).mkdir(parents=True, exist_ok=True)
            return True, f'Folder created: {path}'

        except Exception as e:
            return False, f'Error creating folder: {str(e)}'

    def get_file_info(self, path: str) -> tuple[bool, FileInfo | str]:
        """Get file information"""
        valid, error = self._validate_path(path)
        if not valid:
            return False, error

        if not path.startswith('/'):
            path = os.path.join(self.root_dir, path)

        abs_path = os.path.abspath(path)

        try:
            if not os.path.exists(abs_path):
                return False, f'Path not found: {path}'

            stat = os.stat(abs_path)
            is_dir = os.path.isdir(abs_path)

            file_info = FileInfo(
                name=os.path.basename(abs_path),
                type='folder' if is_dir else 'file',
                path=os.path.relpath(abs_path, self.root_dir),
                size=stat.st_size if not is_dir else 0,
                created=datetime.fromtimestamp(stat.st_ctime).isoformat(),
                modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                readable=os.access(abs_path, os.R_OK),
                writable=os.access(abs_path, os.W_OK),
            )

            return True, file_info

        except Exception as e:
            return False, f'Error getting file info: {str(e)}'


# ============================================================================
# FASTAPI INTEGRATION
# ============================================================================


router = APIRouter(prefix='/api/web-os/files', tags=['Web OS Files'])

# Global file manager
file_manager = FileSystemManager()


@router.get('/list')
async def list_files(path: str = Query('')):
    """List directory contents"""
    success, result = file_manager.list_directory(path)

    if not success:
        raise HTTPException(status_code=400, detail=result)

    return {
        'path': path or file_manager.root_dir,
        'files': [
            {
                'name': f.name,
                'type': f.type,
                'path': f.path,
                'size': f.size,
                'created': f.created,
                'modified': f.modified,
            }
            for f in result
        ],
    }


@router.get('/read')
async def read_file(path: str = Query(...)):
    """Read file contents"""
    success, result = file_manager.read_file(path)

    if not success:
        raise HTTPException(status_code=400, detail=result)

    return {'path': path, 'content': result}


@router.post('/write')
async def write_file(path: str = Query(...), content: str = ''):
    """Write file contents"""
    success, result = file_manager.write_file(path, content)

    if not success:
        raise HTTPException(status_code=400, detail=result)

    return {'path': path, 'message': result}


@router.delete('/file')
async def delete_file(path: str = Query(...)):
    """Delete file"""
    success, result = file_manager.delete_file(path)

    if not success:
        raise HTTPException(status_code=400, detail=result)

    return {'message': result}


@router.delete('/folder')
async def delete_folder(path: str = Query(...)):
    """Delete folder"""
    success, result = file_manager.delete_folder(path)

    if not success:
        raise HTTPException(status_code=400, detail=result)

    return {'message': result}


@router.post('/folder')
async def create_folder(path: str = Query(...)):
    """Create folder"""
    success, result = file_manager.create_folder(path)

    if not success:
        raise HTTPException(status_code=400, detail=result)

    return {'message': result}


@router.get('/info')
async def get_file_info(path: str = Query(...)):
    """Get file information"""
    success, result = file_manager.get_file_info(path)

    if not success:
        raise HTTPException(status_code=400, detail=result)

    return {
        'name': result.name,
        'type': result.type,
        'path': result.path,
        'size': result.size,
        'created': result.created,
        'modified': result.modified,
        'readable': result.readable,
        'writable': result.writable,
    }


__all__ = ['router', 'FileSystemManager', 'FileInfo']
