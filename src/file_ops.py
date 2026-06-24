"""File Operations Module.

This module provides utilities for file automation
including batch renaming, file conversion, and directory operations.
"""

import os
import shutil
import glob
from pathlib import Path
from typing import Any


class FileOperations:
    """Handles file and directory operations."""

    def __init__(self, base_path: str = "."):
        """Initialize FileOperations.

        Args:
            base_path: Base directory path.
        """
        self.base_path = base_path

    def list_files(
        self,
        pattern: str = "*",
        recursive: bool = False
    ) -> list[str]:
        """List files matching a pattern.

        Args:
            pattern: Glob pattern.
            recursive: Search recursively.

        Returns:
            List of file paths.
        """
        if recursive:
            return glob.glob(f"{self.base_path}/**/{pattern}", recursive=True)
        return glob.glob(f"{self.base_path}/{pattern}")

    def batch_rename(
        self,
        directory: str,
        pattern: str,
        replacement: str
    ) -> list[tuple[str, str]]:
        """Batch rename files.

        Args:
            directory: Directory containing files.
            pattern: Pattern to match.
            replacement: Replacement string.

        Returns:
            List of (old, new) rename pairs.
        """
        files = glob.glob(f"{directory}/{pattern}")
        renames = []

        for filepath in files:
            filename = os.path.basename(filepath)
            new_filename = filename.replace(pattern.replace("*", ""), replacement)
            new_filepath = os.path.join(directory, new_filename)

            os.rename(filepath, new_filepath)
            renames.append((filepath, new_filepath))

        return renames

    def copy_files(
        self,
        source: str,
        destination: str,
        pattern: str = "*"
    ) -> list[str]:
        """Copy files matching pattern.

        Args:
            source: Source directory.
            destination: Destination directory.
            pattern: File pattern.

        Returns:
            List of copied files.
        """
        files = glob.glob(f"{source}/{pattern}")
        copied = []

        os.makedirs(destination, exist_ok=True)

        for filepath in files:
            filename = os.path.basename(filepath)
            dest_path = os.path.join(destination, filename)
            shutil.copy2(filepath, dest_path)
            copied.append(dest_path)

        return copied

    def move_files(
        self,
        source: str,
        destination: str,
        pattern: str = "*"
    ) -> list[str]:
        """Move files matching pattern.

        Args:
            source: Source directory.
            destination: Destination directory.
            pattern: File pattern.

        Returns:
            List of moved files.
        """
        files = glob.glob(f"{source}/{pattern}")
        moved = []

        os.makedirs(destination, exist_ok=True)

        for filepath in files:
            filename = os.path.basename(filepath)
            dest_path = os.path.join(destination, filename)
            shutil.move(filepath, dest_path)
            moved.append(dest_path)

        return moved

    def create_directory_structure(
        self,
        base: str,
        structure: dict[str, Any]
    ) -> None:
        """Create directory structure from dict.

        Args:
            base: Base directory.
            structure: Dict defining structure.
        """
        os.makedirs(base, exist_ok=True)

        for name, content in structure.items():
            path = os.path.join(base, name)
            if isinstance(content, dict):
                self.create_directory_structure(path, content)
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as f:
                    f.write(str(content))

    def get_file_stats(self, filepath: str) -> dict[str, Any]:
        """Get file statistics.

        Args:
            filepath: Path to file.

        Returns:
            File statistics.
        """
        stat = os.stat(filepath)
        return {
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "accessed": stat.st_atime,
            "is_file": os.path.isfile(filepath),
            "is_dir": os.path.isdir(filepath)
        }


def cleanup_empty_directories(root: str) -> int:
    """Remove empty directories recursively.

    Args:
        root: Root directory to start from.

    Returns:
        Number of directories removed.
    """
    removed = 0
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        if not dirnames and not filenames:
            os.rmdir(dirpath)
            removed += 1
    return removed
