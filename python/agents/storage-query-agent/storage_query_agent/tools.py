# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Custom tools for querying storage systems and computer servers."""

import os
import platform
import shutil


def list_files(directory_path: str = ".") -> str:
    """
    List files and directories in the specified path.

    Args:
        directory_path: The directory path to list. Defaults to current directory.

    Returns:
        A formatted string containing the list of files and directories.
    """
    try:
        base_path = os.path.abspath(os.getenv("STORAGE_BASE_PATH", "/home"))

        # Convert relative path to absolute using base path
        if not os.path.isabs(directory_path):
            if directory_path == ".":
                full_path = base_path
            else:
                full_path = os.path.join(base_path, directory_path.lstrip("/"))
        else:
            full_path = directory_path

        # Security: Ensure the path is within allowed boundaries
        full_path = os.path.abspath(full_path)

        # Verify the resolved path is still within base_path
        if not full_path.startswith(base_path):
            return (
                f"Error: Access denied. Path '{directory_path}' is outside "
                "the allowed directory."
            )

        if not os.path.exists(full_path):
            return f"Error: Path '{directory_path}' does not exist."

        if not os.path.isdir(full_path):
            return f"Error: '{directory_path}' is not a directory."

        items = os.listdir(full_path)

        if not items:
            return f"The directory '{directory_path}' is empty."

        files = []
        directories = []

        for item in sorted(items):
            item_path = os.path.join(full_path, item)
            if os.path.isdir(item_path):
                directories.append(f"📁 {item}/")
            else:
                # Get file size
                size = os.path.getsize(item_path)
                size_str = format_size(size)
                files.append(f"📄 {item} ({size_str})")

        result = f"Contents of '{directory_path}':\n\n"
        if directories:
            result += "Directories:\n"
            result += "\n".join(directories) + "\n\n"
        if files:
            result += "Files:\n"
            result += "\n".join(files)

        return result
    except PermissionError:
        return f"Error: Permission denied to access '{directory_path}'."
    except Exception as e:
        return f"Error listing directory: {str(e)}"


def read_file_content(file_path: str, max_lines: int = 50) -> str:
    """
    Read and return the contents of a file.

    Args:
        file_path: Path to the file to read.
        max_lines: Maximum number of lines to return (default: 50).

    Returns:
        The file contents or an error message.
    """
    try:
        base_path = os.path.abspath(os.getenv("STORAGE_BASE_PATH", "/home"))

        # Convert relative path to absolute using base path
        if not os.path.isabs(file_path):
            full_path = os.path.join(base_path, file_path.lstrip("/"))
        else:
            full_path = file_path

        # Security: Ensure the path is within allowed boundaries
        full_path = os.path.abspath(full_path)

        # Verify the resolved path is still within base_path
        if not full_path.startswith(base_path):
            return (
                f"Error: Access denied. Path '{file_path}' is outside "
                "the allowed directory."
            )

        if not os.path.exists(full_path):
            return f"Error: File '{file_path}' does not exist."

        if not os.path.isfile(full_path):
            return f"Error: '{file_path}' is not a file."

        # Check file size
        file_size = os.path.getsize(full_path)
        if file_size > 1024 * 1024:  # 1MB limit
            return (
                f"Error: File is too large ({format_size(file_size)}). "
                "Maximum supported size is 1MB."
            )

        # Read file line by line for better memory efficiency
        lines = []
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line)

        # Count total lines
        total_lines = 0
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            for _ in f:
                total_lines += 1

        if total_lines > max_lines:
            content = "".join(lines)
            result = f"File: {file_path}\n"
            result += f"Size: {format_size(file_size)}\n"
            result += f"Showing first {max_lines} of {total_lines} lines:\n\n"
            result += content
            result += f"\n\n... ({total_lines - max_lines} more lines not shown)"
        else:
            content = "".join(lines)
            result = f"File: {file_path}\n"
            result += f"Size: {format_size(file_size)}\n"
            result += f"Lines: {total_lines}\n\n"
            result += content

        return result
    except PermissionError:
        return f"Error: Permission denied to read '{file_path}'."
    except UnicodeDecodeError:
        return f"Error: File '{file_path}' is not a text file or uses an unsupported encoding."
    except Exception as e:
        return f"Error reading file: {str(e)}"


def get_storage_info(path: str = "/") -> str:
    """
    Get storage capacity and usage information for a given path.

    Args:
        path: The path to check storage information for. Defaults to root.

    Returns:
        Storage information including total, used, and available space.
    """
    try:
        if not os.path.exists(path):
            path = "/"

        usage = shutil.disk_usage(path)

        total = usage.total
        used = usage.used
        free = usage.free

        percent_used = (used / total) * 100 if total > 0 else 0

        result = f"Storage Information for '{path}':\n\n"
        result += f"Total Space: {format_size(total)}\n"
        result += f"Used Space: {format_size(used)} ({percent_used:.1f}%)\n"
        result += f"Available Space: {format_size(free)} ({100 - percent_used:.1f}%)\n"

        return result
    except Exception as e:
        return f"Error getting storage information: {str(e)}"


def get_server_info() -> str:
    """
    Get information about the current server/computer.

    Returns:
        Server information including OS, hostname, and other metrics.
    """
    try:
        result = "Server Information:\n\n"
        result += f"Operating System: {platform.system()} {platform.release()}\n"
        result += f"Platform: {platform.platform()}\n"
        result += f"Hostname: {platform.node()}\n"
        result += f"Processor: {platform.processor()}\n"
        result += f"Architecture: {platform.machine()}\n"
        result += f"Python Version: {platform.python_version()}\n"

        return result
    except Exception as e:
        return f"Error getting server information: {str(e)}"


def format_size(bytes_size: int) -> str:
    """
    Format byte size to human-readable string.

    Args:
        bytes_size: Size in bytes.

    Returns:
        Human-readable size string (e.g., "1.5 GB").
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"
