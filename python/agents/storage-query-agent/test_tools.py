#!/usr/bin/env python3
"""Test script for storage query agent tools."""

import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from storage_query_agent.tools import (  # noqa: E402
    get_server_info,
    get_storage_info,
    list_files,
    read_file_content,
)


def test_list_files():
    """Test the list_files tool."""
    print("=" * 60)
    print("Testing list_files tool")
    print("=" * 60)

    # Test listing current directory
    result = list_files(".")
    print(result)
    print()


def test_read_file_content():
    """Test the read_file_content tool."""
    print("=" * 60)
    print("Testing read_file_content tool")
    print("=" * 60)

    # Test reading README.md
    result = read_file_content(
        "python/agents/storage-query-agent/README.md", max_lines=20
    )
    print(result)
    print()


def test_get_storage_info():
    """Test the get_storage_info tool."""
    print("=" * 60)
    print("Testing get_storage_info tool")
    print("=" * 60)

    result = get_storage_info("/")
    print(result)
    print()


def test_get_server_info():
    """Test the get_server_info tool."""
    print("=" * 60)
    print("Testing get_server_info tool")
    print("=" * 60)

    result = get_server_info()
    print(result)
    print()


if __name__ == "__main__":
    # Set environment variable for testing
    os.environ["STORAGE_BASE_PATH"] = "/home/runner/work/adk-samples/adk-samples"

    print("\n🧪 Running Storage Query Agent Tools Tests\n")

    test_list_files()
    test_read_file_content()
    test_get_storage_info()
    test_get_server_info()

    print("=" * 60)
    print("✅ All tool tests completed!")
    print("=" * 60)
