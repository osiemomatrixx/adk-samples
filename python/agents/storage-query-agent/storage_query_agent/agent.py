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

"""Storage Query Conversation Agent.

This agent answers questions by querying storage systems and computer servers.
"""

import logging
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent

from .tools import (
    get_server_info,
    get_storage_info,
    list_files,
    read_file_content,
)

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

load_dotenv()

SYSTEM_INSTRUCTION = """You are a helpful storage and server query assistant.

Your role is to help users find information stored on their computer systems and servers.
You have access to tools that can:
- List files and directories
- Read file contents
- Check storage capacity and usage
- Get server information and metrics

When a user asks a question:
1. Determine which tool(s) would be most helpful to answer their question
2. Use the appropriate tool(s) to gather the information
3. Provide a clear, informative response based on the results

Important guidelines:
- Always verify that paths exist before attempting to read files
- Respect file size limits when reading file contents
- Provide helpful error messages if operations fail
- Format your responses in a clear, organized manner
- Use emojis where appropriate to make responses more engaging
- If asked about something outside your capabilities, politely explain what you can help with

Be helpful, informative, and professional in all your interactions.
"""

logger.info("--- 🤖 Creating Storage Query Agent... ---")

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="storage_query_agent",
    description="An agent that can answer questions by querying storage systems and computer servers",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        list_files,
        read_file_content,
        get_storage_info,
        get_server_info,
    ],
)


def main():
    """Run the agent in interactive mode."""
    logger.info("--- 🚀 Starting Storage Query Agent in interactive mode... ---")
    logger.info("--- Type your questions below. Type 'exit' or 'quit' to stop. ---\n")

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            if user_input.lower() in ["exit", "quit", "bye"]:
                logger.info("\n--- 👋 Goodbye! ---")
                break

            if not user_input:
                continue

            logger.info("\n🤖 Agent: ")
            response = root_agent.run(user_input)
            print(response)

        except KeyboardInterrupt:
            logger.info("\n\n--- 👋 Goodbye! ---")
            break
        except Exception as e:
            logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
