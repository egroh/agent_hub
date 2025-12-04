# Agent Hub 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg)](https://fastapi.tiangolo.com/)

**Agent Hub** is a powerful orchestration platform for managing complex tasks with autonomous agents. It bridges the gap between technical power and user accessibility by providing a familiar Kanban interface for monitoring and controlling agent workflows.

![Agent Hub Demo](assets/demo.png)

## Features

- **🧩 Complex Task Orchestration**: Break down high-level objectives into manageable subtasks automatically.
- **📋 Kanban Interface**: Visualize agent progress, dependencies, and status in real-time.
- **🤖 Autonomous Subtasks**: Agents can spawn their own sub-agents to handle specialized work (research, coding, design).
- **🖼️ Multimodal Capabilities**: Integrated support for text generation, code analysis, and image generation.

> [!NOTE]
> **Hackathon Project**: This project was built for the **Hugging Face + Anthropic Smolagents Hackathon** to demonstrate how multi-agent systems can be made accessible to non-technical users.

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Docker & Docker Compose**

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/egroh/agent_hub.git
    cd agent_hub
    ```

2.  **Setup Backend**
    ```bash
    cd backend
    cp .env.example .env
    # Add your API keys to .env
    uv sync
    ```

3.  **Setup Frontend**
    ```bash
    cd ../nextjs-frontend
    cp .env.example .env.local
    pnpm install
    ```

4.  **Run with Docker (Recommended)**
    ```bash
    # From the root directory
    make docker-build
    make docker-start-backend
    make docker-start-frontend
    ```

    Access the app at `http://localhost:3000`.

## Architecture

Agent Hub uses a microservices-inspired architecture:

-   **Frontend**: Next.js 14 with Shadcn UI for a responsive, modern interface.
-   **Backend**: FastAPI for high-performance agent logic and orchestration.
-   **Database**: PostgreSQL for persistent state management.
-   **AI Services**: Integrates with Anthropic (Claude), OpenAI, and Hugging Face for intelligence.

## Demo Mode

You can try the interface without API keys by enabling **Demo Mode**. Set `DEMO_MODE=true` in `backend/.env` and restart the backend. This mocks the AI responses for testing purposes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
