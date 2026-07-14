
# Stateless Coding Agent Platform

A modular, highly resilient backend architecture designed for driving autonomous AI coding agents. This platform leverages a strict separation of concerns, ensuring that agent profiles remain entirely stateless, while the execution harness controls security guardrails, hardware connectivity, and LLM communication.

---

## 🏗️ Architecture Overview

The system is split into independent micro-modules to ensure complete horizontal scalability. If you need to switch LLM providers, add tools, or create multi-agent verification chains, you only modify the specific module responsible for that domain.

```text
coding_agent/
│
├── config.py         # Centralized environment configurations & guardrail definitions
├── main.py           # Application Factory entry point (FastAPI + Inngest integration)
│
├── agents/
│   ├── __init__.py
│   └── registry.py   # Pure configuration definitions of stateless agent personas
│
├── harness/
│   ├── __init__.py
│   ├── client.py     # Provider-agnostic LLM network communication wrapper
│   ├── engine.py     # Stateless single-step reasoning loop processor
│   └── queue.py      # Stateful, durable background worker queue (Inngest workflows)
│
└── tools/
    ├── __init__.py
    └── terminal.py   # System-level hardware execution interfaces & tool schemas

```

---

## 🧩 Core Modules & Components

### 1. Configuration Layer (`config.py`)

Acts as the **Single Source of Truth** for the execution workspace. It safely loads credentials from local environments and anchors the runtime boundaries via an explicit execution command whitelist to prevent rogue actions.

### 2. Hardware Interface Layer (`tools/terminal.py`)

Acts as the physical hands of the agent on the local keyboard. It wraps Python's `subprocess` utility to cleanly route terminal commands, convert binary byte streams into readable text strings, and enforce the security whitelist interceptor before commands hit the host machine.

### 3. Stateless Registry Layer (`agents/registry.py`)

Maintains pure data configurations of who the agent is (personas/instructions). It contains zero runtime state or memory. It exposes a `compile_agent_prompt` function that dynamically injects real-time workspace directories and whitelisted parameters straight into the prompt sequence.

### 4. Network Client Layer (`harness/client.py`)

Provides a provider-agnostic wrapper around the LLM client infrastructure. It separates the native SDK syntax from the engine loop, automatically mounting functional JSON tool schemas onto every outbound payload block.

### 5. Reasoning Engine Layer (`harness/engine.py`)

The stateless processing unit that drives individual execution steps. It accepts an agent persona and an isolated slice of context history, extracts the predicted thoughts, and deserializes flat JSON strings from the LLM back into workable Python dictionary configurations.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have [uv](https://github.com/astral-sh/uv) installed on your host system.

### 1. Project Initialization & Setup

Clone or navigate to your project directory and synchronize the virtual runtime environment:

```bash
# Verify dependencies are aligned matching the lockfile
uv sync

```

### 2. Configure Environment Variables

Create a `.env` configuration file in the absolute root folder:

```env
OPENAI_API_KEY="your-secret-openai-api-key"
ENVIRONMENT="sandbox-v1"

```

### 3. Running the Server Assembly

Launch the FastAPI development environment using the Application Factory assembly:

```bash
uv run uvicorn main:app --reload

```

---

## 🔒 Security Guardrails

* **Whitelisted Subprocesses:** The application checks the primary keyword of all agent tool actions against a strict array constraint defined inside `config.py`.
* **Execution Timeouts:** Terminal tasks are throttled with a maximum timeout threshold of 20 seconds per operation to prevent zombie processes and infinite runtime execution loops.

```
