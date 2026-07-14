
# Forge: Durable & Modular Coding Agent Platform

Forge is a production-grade, highly resilient backend engine framework built for orchestrating autonomous AI software engineering agents. 

By anchoring the codebase on a strict **Separation of Concerns**, the system ensures that AI agent profiles remain completely stateless text processing units, while the surrounding Python runtime harness guarantees strict security guardrails, hardware access, data normalization, and fault-tolerant long-term memory.

---

## 🏗️ Architectural Systems Design

Forge divides system logic into independent, isolated micro-modules. This modular approach ensures absolute horizontal scalability—allowing you to scale out toolkits, add alternative model providers, or stitch multi-agent review hierarchies without modifying the core execution loop.

```text
forge/
│
├── config.py         # Centralized environment configurations & path scopes
├── main.py           # Application Factory entry point (FastAPI + Inngest)
├── pyproject.toml    # Virtual environment constraints and dependencies
│
├── agents/
│   ├── __init__.py
│   └── registry.py   # Data blueprints of stateless agent personas
│
├── harness/
│   ├── __init__.py
│   ├── client.py     # Provider-agnostic LLM network diplomat layer
│   ├── engine.py     # Stateless single-step inference & parsing processor
│   └── queue.py      # Stateful, durable execution orchestrator (Inngest)
│
└── tools/
    ├── __init__.py
    └── terminal.py   # Hardware execution interface & JSON tool schemas

```

---

## 🧩 Comprehensive Module Breakdown

### 🛡️ 1. The Configuration Layer (`config.py`)

Acts as the global **Single Source of Truth** for the entire project workspace runtime environment.

* Safely resolves project workspace boundaries dynamically using absolute base directory evaluations.
* Maintains a rigorous security command whitelist array (`ALLOWED_COMMANDS`) to instantly catch and deflect malicious terminal activities before execution.
* Utilizes `pydantic-settings` to deliver fast type-validated app state configurations on server initialization.

### 🔌 2. The Hardware Interface (`tools/terminal.py`)

Serves as the physical hands of the AI agent on the host system keyboard.

* Interfaces natively with the host operating system shell using Python's `subprocess` utility.
* Acts as a critical security proxy, intercepting and cross-checking the primary token keyword of all generated command requests against the global configuration whitelist.
* Intercepts system byte logs, cleans stdout/stderr, handles exceptions, and forces a maximum **20-second timeout threshold** to cleanly block zombie loops or interactive user-input deadlocks.
* Exposes the standardized OpenAPI function call JSON blueprint schema to advertise its capabilities to the LLM backend.

### 🎭 3. The Stateless Registry Layer (`agents/registry.py`)

Maintains pure data blueprints defining individual agent behaviors, parameters, and instructions.

* **100% Stateless Architecture:** Profiles possess absolutely no execution tracking state, context arrays, or token memory allocations.
* Features a dynamic **Prompt Compiler** (`compile_agent_prompt`) that programmatically flushes real-time environment scopes, current system directories, and strict operational boundaries directly into the final system message block right before inference.

### 📡 4. The Network Client Layer (`harness/client.py`)

Serves as an isolated, provider-agnostic abstraction envelope around the LLM provider SDK fabric.

* Completely protects the inner platform engine mechanics from changes to third-party SDK syntaxes.
* Responsible for dynamically mounting tool schemas and assigning execution properties (`tool_choice="auto"`) onto outgoing network call streams.
* Easily customizable to switch endpoints between OpenAI, Anthropic, or local open-source models via Ollama.

### 🧠 5. The Reasoning Engine Layer (`harness/engine.py`)

The stateless calculator that handles processing independent conversation steps.

* Reconstructs the systemic history layout block dynamically by blending compiled system directives smoothly with historical conversation slices.
* Extracts the predicted thoughts out of incoming network payload segments.
* Automatically converts and sanitizes raw, complex Pydantic response objects into clean Python native primitive objects via `.model_dump()` to ensure problem-free upstream serialization.

### 🔄 6. The Durable Orchestration Queue (`harness/queue.py`)

The stateful, fault-tolerant heartbeat that orchestrates the continuous Think-Act-Observe cycle.

* Implements **Durable Execution** using Inngest background event processing loops.
* Uses cryptographic step-level checkpoints (`ctx.step.run`) to permanently write intermediate LLM choices and terminal tool logs into a persistent state ledger.
* Prevents data and monetary loss: If a network timeout, code exception, or server crash happens midway through a complex task, the queue resumes precisely from the last successful step without wasting tokens on recalculating previous states.

---

## 🚀 Step-by-Step Installation & Bootup

### Prerequisites

* Ensure that [uv](https://github.com/astral-sh/uv) is installed.
* Node.js runtime installed (for running the Inngest local dev dashboard).

### 1. Synchronize the Environment

Navigate into your local workspace directory and align the virtual environment states using the lockfile configuration:

```bash
uv sync

```

### 2. Configure Environment Keys

Create a `.env` configuration template in the absolute root folder next to `pyproject.toml`:

```env
OPENAI_API_KEY="your-actual-secret-openai-api-key"
ENVIRONMENT="sandbox-v1"

```

### 3. Initialize the Web Server Framework

Boot up the FastAPI platform server application layer through your locked local project environment:

```bash
uv run python -m uvicorn main:app --reload

```

*The host API endpoint will now be active, scanning, and listening on `http://127.0.0.1:8000`.*

### 4. Ignite the Inngest Developer Workspace

Open a secondary terminal workspace pane, head to the project folder root, and spawn the visual event streaming dashboard pipeline:

```bash
npx inngest-cli@latest dev -u [http://127.0.0.1:8000/api/inngest](http://127.0.0.1:8000/api/inngest)

```

---

## 🕹️ Driving Your First Agent Job Sequence

1. Launch your browser window and navigate to the visual engineering panel layout running at **`http://localhost:8288`**.
2. Click the **Send test event** button in the top-right console dashboard region.
3. Configure the **Event Name** mapping parameter value explicitly to: `agent/run.task`
4. Paste the following structured data payload block inside the JSON input editor, adjusting parameters as desired:

```json
{
  "name": "agent/run.task",
  "data": {
    "task": "Create a new directory named 'forge_output', go inside it, and create a text file named 'success.txt' with the content 'Forge is alive!'.",
    "model_name": "gpt-4o-mini"
  }
}

```

5. Click **Invoke**. Go to the **Runs** tab to watch the execution waterfall graph log steps, execute shell actions, and record immutable checkpoints in real-time.

```