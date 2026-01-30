#!/usr/bin/env python3
"""Security test for storage query agent tools."""

import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from storage_query_agent.tools import list_files, read_file_content  # noqa: E402


def test_path_traversal():
    """Test that path traversal attacks are blocked."""
    print("🔒 Testing Security - Path Traversal Protection")
    print("=" * 70)

    # Set a restricted base path
    os.environ["STORAGE_BASE_PATH"] = "/home/runner/work/adk-samples/adk-samples/python"

    test_cases = [
        ("../../../etc", "Path traversal with relative path (list_files)"),
        (
            "../../../../../../etc/passwd",
            "Path traversal to /etc/passwd (read_file_content)",
        ),
        ("/etc/passwd", "Absolute path to /etc/passwd (read_file_content)"),
        ("/etc", "Absolute path to /etc (list_files)"),
    ]

    print("\n1. Testing list_files with path traversal attempts:")
    print("-" * 70)
    for path, description in test_cases[::2]:
        print(f"\nTest: {description}")
        print(f"Input: '{path}'")
        result = list_files(path)
        if "Access denied" in result or "outside the allowed directory" in result:
            print("✅ BLOCKED: " + result.split("\n")[0])
        else:
            print(f"❌ FAILED: Path traversal not blocked!\n{result[:100]}")

    print("\n\n2. Testing read_file_content with path traversal attempts:")
    print("-" * 70)
    for path, description in test_cases[1::2]:
        print(f"\nTest: {description}")
        print(f"Input: '{path}'")
        result = read_file_content(path)
        if "Access denied" in result or "outside the allowed directory" in result:
            print("✅ BLOCKED: " + result.split("\n")[0])
        else:
            print(f"❌ FAILED: Path traversal not blocked!\n{result[:100]}")

    print("\n\n3. Testing valid paths within allowed directory:")
    print("-" * 70)
    result = list_files("agents/storage-query-agent")
    if "Access denied" not in result:
        print("✅ Valid path works correctly")
    else:
        print(f"❌ Valid path incorrectly blocked: {result}")

    print("\n" + "=" * 70)
    print("🎉 Security tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    test_path_traversal()
