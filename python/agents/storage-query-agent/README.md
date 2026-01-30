# 💾🖥️ Storage Query Conversation Agent

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-ADK-4285F4.svg)](https://github.com/google/adk-python)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

A conversational agent that answers questions by querying storage systems and computer servers. This agent demonstrates how to build an intelligent assistant that can access and retrieve information from various storage backends.

## Overview

The Storage Query Agent is designed to help users find information stored across multiple storage systems and computer servers. It provides a natural language interface for querying:

- File systems and directories
- Server information and metrics
- Storage usage and capacity
- File content and metadata

The agent uses custom tools to interact with storage systems and provides informative responses based on the retrieved data.

## Features

- **Natural Language Queries**: Ask questions in plain English about your storage and servers
- **Multiple Storage Backends**: Query file systems, server metrics, and storage information
- **Intelligent Responses**: Get contextual answers with relevant details from your storage systems
- **Conversational Interface**: Engage in multi-turn conversations about your data

## Getting Started

### Prerequisites

- Python 3.10+
- Git, for cloning the repository
- Access to either:
  - Google AI Studio API key (quickest way to get started), or
  - Google Cloud Project with Vertex AI enabled

### Installation

1. Clone the repository:

```bash
git clone https://github.com/google/adk-samples.git
cd adk-samples/python/agents/storage-query-agent
```

2. Install [uv](https://docs.astral.sh/uv/getting-started/installation) (used to manage dependencies):

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (uncomment below line)
# powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> [!NOTE]
> You may need to restart or open a new terminal after installing `uv`.

3. Configure environment variables (via `.env` file):

There are two different ways to call Gemini models:

- Calling the Gemini API directly using an API key created via Google AI Studio.
- Calling Gemini models through Vertex AI APIs on Google Cloud.

> [!TIP] 
> An API key from Google AI Studio is the quickest way to get started.
> 
> Existing Google Cloud users may want to use Vertex AI.

<details open>
<summary>Gemini API Key</summary> 

Get an API Key from Google AI Studio: https://aistudio.google.com/apikey

Create a `.env` file by running the following (replace `<your_api_key_here>` with your API key):

```sh
echo "GOOGLE_API_KEY=<your_api_key_here>" >> .env \
&& echo "GOOGLE_GENAI_USE_VERTEXAI=FALSE" >> .env
```

</details>

<details>
<summary>Vertex AI</summary>

To use Vertex AI, you will need to [create a Google Cloud project](https://developers.google.com/workspace/guides/create-project) and [enable Vertex AI](https://cloud.google.com/vertex-ai/docs/start/cloud-environment).

Authenticate and enable Vertex AI API:

```bash
gcloud auth login
# Replace <your_project_id> with your project ID
gcloud config set project <your_project_id>
gcloud services enable aiplatform.googleapis.com
```

Create a `.env` file by running the following (replace `<your_project_id>` with your project ID):
```sh
echo "GOOGLE_GENAI_USE_VERTEXAI=TRUE" >> .env \
&& echo "GOOGLE_CLOUD_PROJECT=<your_project_id>" >> .env \
&& echo "GOOGLE_CLOUD_LOCATION=us-central1" >> .env
```

</details>

4. (Optional) Configure storage paths in your `.env` file:

```sh
echo "STORAGE_BASE_PATH=/path/to/your/storage" >> .env
```

Now you are ready to run the agent!

## Running the Agent

### Local Deployment

Run the agent in interactive mode:

```bash
uv run storage_query_agent/agent.py
```

The agent will start and you can ask questions like:

- "What files are in the /home directory?"
- "How much storage space is available?"
- "Show me the contents of config.txt"
- "What servers are currently running?"

## Example Usage

```
User: What files are in the current directory?
Agent: Let me check the current directory for you...
[Uses list_files tool]
Agent: The current directory contains the following files:
- agent.py
- tools.py
- __init__.py
- README.md

User: How much disk space is available?
Agent: I'll check the storage capacity for you...
[Uses get_storage_info tool]
Agent: Current storage status:
- Total: 500 GB
- Used: 320 GB (64%)
- Available: 180 GB (36%)
```

## Architecture

The agent is built using:

- **Google ADK**: Agent Development Kit for orchestration
- **Custom Tools**: Python functions for storage and server queries
  - `list_files`: List files in a directory
  - `read_file_content`: Read file contents
  - `get_storage_info`: Get storage capacity and usage
  - `get_server_info`: Get server metrics and information

## Customization

You can customize the agent by:

1. **Adding new storage backends**: Extend the tools to support databases, cloud storage, etc.
2. **Modifying the system instruction**: Update the agent's behavior in `agent.py`
3. **Adding new tools**: Create additional tools in `tools.py` for specific storage operations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE file](LICENSE) for details.
