```
# Forge: Durable, Multi-Provider Coding Agent Platform

Forge is a production-grade, highly resilient backend engine framework engineered to drive autonomous AI software engineering agents. 

By anchoring the platform on a strict **Separation of Concerns**, the system ensures that AI agent personas remain completely stateless runtime entities, while the surrounding environment layers guarantee robust security guardrails, dynamic multi-provider API routing (OpenAI, Groq, Vercel AI Gateway, and local Ollama), structural data serialization, and fault-tolerant long-term memory.

---

## 🏗️ Architectural Systems Design

Forge isolates layout concerns into modular micro-packages. This decoupled design makes horizontal scaling seamless—allowing you to extend utility toolsets, introduce alternative foundation gateways, or orchestrate complex verification loops without modifying the core inference loop.

```text
forge/
│
├── config.py         # Centralized environment configurations & path scopes
├── main.py           # Application Factory setup (FastAPI + Inngest)
├── cli.py            # Interactive CLI & credential configuration manager
├── pyproject.toml    # Virtual environment rules and dependencies
│
├── agents/
│   ├── __init__.py
│   └── registry.py   # Immutable system parameters of stateless agent personas
│
├── harness/
│   ├── __init__.py
│   ├── client.py     # Provider-agnostic API switchboard & gateway router
│   ├── engine.py     # Stateless single-step inference execution processor
│   └── queue.py      # Stateful, durable background execution orchestrator (Inngest)
│
└── tools/
    ├── __init__.py
    └── terminal.py   # Protected system-level execution utilities & schemas

```

---

## 🧩 Comprehensive Module Breakdown

### 🛡️ 1. The Configuration Layer (`config.py`)

Acts as the global **Single Source of Truth** for system parameters.

* Resolves workspace boundaries using script-relative absolute path processing to prevent environment collision.
* Maintains a rigorous command execution blocklist (`ALLOWED_COMMANDS`) to instantly trap and neutralize unauthorized terminal inputs before they touch the processor.
* Leverages `pydantic-settings` to deliver unified, type-validated app state configurations on initialization.

### 🎭 2. The Stateless Registry Layer (`agents/registry.py`)

Maintains pure data blueprints defining structural agent prompts and instructions.

* **100% Stateless Architecture:** Persona vectors hold absolutely zero active step parameters, system context arrays, or operational token memory slots.
* Employs a text compilation driver (`compile_agent_prompt`) that dynamically flushes current local directory states and operational boundaries into the runtime prompt trace immediately before inference.

### 🔌 3. The Protected Hardware Interface (`tools/terminal.py`)

Serves as the physical hands of the AI agent on the host machine.

* Connects directly with the operating system shell using Python's primitive `subprocess` utility.
* Acts as an inline security interceptor, checking the first keyword token of all incoming agent requests against the global configuration whitelist.
* Intercepts standard streams, cleans output buffers, catches system exceptions, and forces a hard **20-second execution timeout** to prevent zombie loops or interactive prompt blockages.

### 📡 4. The Multi-Provider Gateway Client (`harness/client.py`)

An advanced, provider-agnostic networking diplomat that abstracts vendor configurations away from the loop.

* Dynamically routes structural payload messages to OpenAI, Groq Cloud, Vercel AI Gateway, or local Ollama instances based on simple string prefixes (`groq/`, `vercel/`, `local-`).
* Leverages OpenAI-compatible API layers to maintain a unified method structure while mounting operational function schemas (`tool_choice="auto"`) across all models natively.

### 🧠 5. The Reasoning Engine Layer (`harness/engine.py`)

The stateless processing node responsible for computing single inference turns.

* Compiles historical conversation matrices cleanly, blending current contexts seamlessly with active state variables.
* Extracts structural tool invocations from incoming network raw packets.
* Ensures strict compliance with upstream workflows by utilizing Pydantic's `.model_dump(exclude_none=True)` to convert complex SDK objects into flat, primitive dictionaries suitable for JSON storage.

### 🔄 6. The Durable Orchestration Queue (`harness/queue.py`)

The stateful, fault-tolerant memory engine that manages the continuous Think-Act-Observe cycle.

* Orchestrates durable execution paradigms using Inngest event messaging micro-queues.
* Enforces structural state encapsulation checkpoints (`ctx.step.run`) around inference iterations and shell actions to create historical database markers.
* Eliminates operational losses: If a local server crashes, a network connection fails, or an API threshold drops mid-assignment, the workflow safely restores state metrics from its latest checkpoint without duplicating tokens or repeating completed tasks.

---

## 🚀 Installation & System Activation

### Prerequisites

* Ensure that the [uv package manager](https://github.com/astral-sh/uv) is installed.
* Node.js runtime environment installed (for hosting the Inngest engine monitoring panel).

### 1. Align Virtual Dependencies

Navigate into your workspace application root and map dependencies using your lockfile settings:

```bash
uv sync

```

### 2. Spawn the Core Application Server

Boot up the FastAPI background worker framework out of your local locked execution shell context:

```bash
uv run python -m uvicorn main:app --reload

```

*The host API process will initialize and listen on `http://127.0.0.1:8000`.*

### 3. Ignite the Event Pipeline Gateway

Open a secondary terminal window pane, jump to the root project workspace folder, and initialize the background event router:

```bash
npx inngest-cli@latest dev -u [http://127.0.0.1:8000/api/inngest](http://127.0.0.1:8000/api/inngest)

```

*The central orchestration monitor layout will light up and be visible on `http://localhost:8288`.*

---

## 🕹️ Driving Tasks via the Interactive CLI UI

Forge ships with a powerful, smart terminal environment manager that eliminates the need to compile manual JSON inputs.

Open a third terminal window tab and invoke the CLI:

```bash
uv run python cli.py

```

### Key Management Wizard Onboarding

If your `.env` configuration file is fresh or lacks active API keys, the CLI will run a pre-flight interception sweep. You will be prompted with an onboarding menu to select your provider (OpenAI, Groq, Vercel, or local Ollama) and paste your credentials. The utility will dynamically save them straight into your local workspace setup.

### Directing the Agent

Once authorized, use the console prompts to input assignments and select models by leveraging prefix parameters:

```text
==================================================
   🔨 FORGE: Multi-Provider Coding Agent CLI      
==================================================

Forge 🤖 ❯ Enter task description: Create a text file named forge_rocks.txt
 
💡 Model Naming Examples:
 - OpenAI: gpt-4o-mini, gpt-4o
 - Groq:   groq/llama-3.3-70b-specdec
 - Vercel: vercel/claude-3-5-sonnet
 - Local:  local-llama3

Forge 🤖 ❯ Select model target [default: gpt-4o-mini]: groq/llama-3.3-70b-specdec

🚀 Dispatching task event token to background execution queues...
✅ Task scheduled perfectly! Watch progress in your Inngest dev console.

```

Open your Inngest Dev Dashboard at **`http://localhost:8288/runs`** to watch the waterfall timeline execute code, trigger the whitelisted hardware steps, and record immutable checkpoints in real-time.

```
```
