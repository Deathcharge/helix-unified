"""
📁 Async File I/O Service
Non-blocking file operations for better performance
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import aiofiles
from loguru import logger


class AsyncFileService:
    """Async file operations service"""
    
    @staticmethod
    async def read_text(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
        """
        Read text file asynchronously.
        
        Args:
            file_path: Path to file
            encoding: File encoding (default: utf-8)
            
        Returns:
            File content as string
            
        Example:
            >>> content = await AsyncFileService.read_text("config.txt")
        """
        try:
            async with aiofiles.open(file_path, "r", encoding=encoding) as f:
                content = await f.read()
            logger.debug(f"📖 Read file: {file_path}")
            return content
        except FileNotFoundError:
            logger.error(f"❌ File not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"❌ Error reading file {file_path}: {e}")
            raise
    
    @staticmethod
    async def write_text(
        file_path: Union[str, Path],
        content: str,
        encoding: str = "utf-8",
        create_dirs: bool = True
    ) -> None:
        """
        Write text file asynchronously.
        
        Args:
            file_path: Path to file
            content: Content to write
            encoding: File encoding (default: utf-8)
            create_dirs: Create parent directories if they don't exist
            
        Example:
            >>> await AsyncFileService.write_text("output.txt", "Hello World")
        """
        try:
            # Create parent directories if needed
            if create_dirs:
                Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(file_path, "w", encoding=encoding) as f:
                await f.write(content)
            logger.debug(f"✍️ Wrote file: {file_path}")
        except Exception as e:
            logger.error(f"❌ Error writing file {file_path}: {e}")
            raise
    
    @staticmethod
    async def read_json(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Read JSON file asynchronously.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Parsed JSON data as dictionary
            
        Example:
            >>> data = await AsyncFileService.read_json("config.json")
        """
        try:
            content = await AsyncFileService.read_text(file_path)
            data = json.loads(content)
            logger.debug(f"📖 Read JSON: {file_path}")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON in {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error reading JSON {file_path}: {e}")
            raise
    
    @staticmethod
    async def write_json(
        file_path: Union[str, Path],
        data: Dict[str, Any],
        indent: int = 2,
        create_dirs: bool = True
    ) -> None:
        """
        Write JSON file asynchronously.
        
        Args:
            file_path: Path to JSON file
            data: Data to write
            indent: JSON indentation (default: 2)
            create_dirs: Create parent directories if they don't exist
            
        Example:
            >>> await AsyncFileService.write_json("data.json", {"key": "value"})
        """
        try:
            content = json.dumps(data, indent=indent, ensure_ascii=False)
            await AsyncFileService.write_text(file_path, content, create_dirs=create_dirs)
            logger.debug(f"✍️ Wrote JSON: {file_path}")
        except Exception as e:
            logger.error(f"❌ Error writing JSON {file_path}: {e}")
            raise
    
    @staticmethod
    async def append_text(
        file_path: Union[str, Path],
        content: str,
        encoding: str = "utf-8",
        create_dirs: bool = True
    ) -> None:
        """
        Append to text file asynchronously.
        
        Args:
            file_path: Path to file
            content: Content to append
            encoding: File encoding (default: utf-8)
            create_dirs: Create parent directories if they don't exist
            
        Example:
            >>> await AsyncFileService.append_text("log.txt", "New log entry\\n")
        """
        try:
            if create_dirs:
                Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(file_path, "a", encoding=encoding) as f:
                await f.write(content)
            logger.debug(f"➕ Appended to file: {file_path}")
        except Exception as e:
            logger.error(f"❌ Error appending to file {file_path}: {e}")
            raise
    
    @staticmethod
    async def read_lines(
        file_path: Union[str, Path],
        encoding: str = "utf-8"
    ) -> List[str]:
        """
        Read file lines asynchronously.
        
        Args:
            file_path: Path to file
            encoding: File encoding (default: utf-8)
            
        Returns:
            List of lines
            
        Example:
            >>> lines = await AsyncFileService.read_lines("data.txt")
        """
        try:
            async with aiofiles.open(file_path, "r", encoding=encoding) as f:
                lines = await f.readlines()
            logger.debug(f"📖 Read {len(lines)} lines from: {file_path}")
            return lines
        except Exception as e:
            logger.error(f"❌ Error reading lines from {file_path}: {e}")
            raise
    
    @staticmethod
    async def file_exists(file_path: Union[str, Path]) -> bool:
        """
        Check if file exists asynchronously.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file exists
            
        Example:
            >>> exists = await AsyncFileService.file_exists("config.json")
        """
        return Path(file_path).exists()
    
    @staticmethod
    async def delete_file(file_path: Union[str, Path]) -> None:
        """
        Delete file asynchronously.
        
        Args:
            file_path: Path to file
            
        Example:
            >>> await AsyncFileService.delete_file("temp.txt")
        """
        try:
            if await AsyncFileService.file_exists(file_path):
                os.remove(file_path)
                logger.debug(f"🗑️ Deleted file: {file_path}")
            else:
                logger.warning(f"⚠️ File not found for deletion: {file_path}")
        except Exception as e:
            logger.error(f"❌ Error deleting file {file_path}: {e}")
            raise
    
    @staticmethod
    async def copy_file(
        source: Union[str, Path],
        destination: Union[str, Path],
        create_dirs: bool = True
    ) -> None:
        """
        Copy file asynchronously.
        
        Args:
            source: Source file path
            destination: Destination file path
            create_dirs: Create parent directories if they don't exist
            
        Example:
            >>> await AsyncFileService.copy_file("source.txt", "dest.txt")
        """
        try:
            content = await AsyncFileService.read_text(source)
            await AsyncFileService.write_text(destination, content, create_dirs=create_dirs)
            logger.debug(f"📋 Copied file: {source} → {destination}")
        except Exception as e:
            logger.error(f"❌ Error copying file {source} to {destination}: {e}")
            raise
    
    @staticmethod
    async def get_file_size(file_path: Union[str, Path]) -> int:
        """
        Get file size in bytes asynchronously.
        
        Args:
            file_path: Path to file
            
        Returns:
            File size in bytes
            
        Example:
            >>> size = await AsyncFileService.get_file_size("data.json")
        """
        try:
            return Path(file_path).stat().st_size
        except Exception as e:
            logger.error(f"❌ Error getting file size {file_path}: {e}")
            raise


# Convenience functions
async def read_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Convenience function to read JSON file"""
    return await AsyncFileService.read_json(file_path)


async def write_json_file(
    file_path: Union[str, Path],
    data: Dict[str, Any],
    indent: int = 2
) -> None:
    """Convenience function to write JSON file"""
    await AsyncFileService.write_json(file_path, data, indent)


async def read_text_file(file_path: Union[str, Path]) -> str:
    """Convenience function to read text file"""
    return await AsyncFileService.read_text(file_path)


async def write_text_file(file_path: Union[str, Path], content: str) -> None:
    """Convenience function to write text file"""
    await AsyncFileService.write_text(file_path, content)


# Export
__all__ = [
    "AsyncFileService",
    "read_json_file",
    "write_json_file",
    "read_text_file",
    "write_text_file"
]
