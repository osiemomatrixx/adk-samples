#!/usr/bin/env python3
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

"""Demo script to showcase the Storage Query Agent capabilities."""

import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from storage_query_agent.tools import (
    get_server_info,
    get_storage_info,
    list_files,
    read_file_content,
)


def main():
    """Run the demo."""
    print("\n" + "=" * 70)
    print("  💾🖥️  Storage Query Agent Demo")
    print("=" * 70 + "\n")

    # Set environment variable for demo
    os.environ["STORAGE_BASE_PATH"] = os.getcwd()

    demos = [
        {
            "title": "📋 Listing Files in Current Directory",
            "function": list_files,
            "args": ["."],
        },
        {
            "title": "💾 Getting Storage Information",
            "function": get_storage_info,
            "args": ["/"],
        },
        {
            "title": "🖥️ Getting Server Information",
            "function": get_server_info,
            "args": [],
        },
    ]

    for i, demo in enumerate(demos, 1):
        print(f"\n{i}. {demo['title']}")
        print("-" * 70)
        result = demo["function"](*demo["args"])
        print(result)

    print("\n" + "=" * 70)
    print("  ✅ Demo Completed!")
    print("=" * 70 + "\n")

    print("💡 Tip: You can interact with this agent conversationally by running:")
    print("   uv run storage_query_agent/agent.py")
    print("\nOr using:")
    print("   python3 -m storage_query_agent.agent")
    print()


if __name__ == "__main__":
    main()
