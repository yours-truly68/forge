# Forge: Decoupled Agent Sandbox (The Complete Guide)

## Part 1: Deep-Dive Architecture Explanation

To understand why Forge is built this way, you have to understand the fundamental limitation of traditional AI agents: **The Stateless HTTP Timeout Problem.**

Most simple agent frameworks run their execution loop inside a standard, synchronous HTTP request. This approach is highly fragile. If you ask an agent to scan directories, write code, run tests, and debug errors, the entire loop can easily take 2 to 5 minutes. Traditional web servers (like FastAPI, Uvicorn, or Nginx) are configured to terminate connections that remain idle for more than 30 to 60 seconds. If a timeout occurs, or if your Wi-Fi blinks, the server thread crashes. The agent loses its entire history, and any tokens you paid for up to that point are completely wasted.

Forge completely solves this by decoupling the **User Interface** from the **Execution Engine** using a **Durable Event-Driven Architecture**.

### 1. The CLI Client (`forge` wrapper)

The command-line interface acts as a lightweight, interactive, non-blocking client.

* It accepts your task prompt.
* It runs a **local pre-flight security check** using a fast local LLM to ensure the prompt is strictly about coding.
* Instead of running the task itself, it submits a fire-and-forget event payload containing the task to your FastAPI backend and **immediately frees up the shell**.
* It then enters a lightweight **polling loop**, checking the status of the run via HTTP every second. This keeps the CLI responsive and allows it to show a continuous, animated status spinner while the heavy lifting happens elsewhere.

### 2. The Orchestrator (Inngest)

Once the FastAPI backend receives the event, it hands it off to **Inngest**, a durable execution engine.

* Inngest runs your Python code as a series of isolated, checkpointed steps using `await context.step.run()`.
* Every time your agent makes an LLM reasoning call or runs a whitelisted shell command, Inngest **checkpoints and freezes the state** in its database.
* If your local server restarts, crashes, or loses power, Inngest does not lose the state. Once the server is back online, Inngest checks its execution log, finds the last successfully completed step, and **resumes the agent from that exact microsecond** without wasting duplicate API tokens.

### 3. The Secure Terminal Executor

When the agent decides to execute a bash command (like compiling a file or running tests), the request goes through a secure middleware guardrail.

* The command is parsed, and the primary command (e.g., `git`, `python`, `mkdir`) is checked against a strict, deterministic whitelist in your `Settings` config.
* If the command is not explicitly allowed, execution is blocked, and a security warning is returned to the agent's context, protecting your host operating system from destructive or hallucinated commands.

---

## Part 2: Installation & Workspace Setup

This setup guide configures **Forge** to run globally on your system, allowing you to use the `forge` command inside any workspace or directory on your Mac.

### Step 1: Install System Dependencies

Forge relies on **`uv`** (a lightning-fast Python package manager) and **Ollama** (to run your local pre-flight classifier model offline).

1. **Install `uv**` (if you haven't already):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

```


2. **Install and Run Ollama**:
* Download Ollama from [ollama.com](https://ollama.com/).
* Open your terminal and pull the lightweight `llama3.2` model used for fast pre-flight classification:
```bash
ollama pull llama3.2:latest

```





### Step 2: Configure Your Local Workspace

1. Navigate to your project directory:
```bash
cd /Users/mohammadrazim/Desktop/Projects/coding-agent

```


2. Sync and lock your Python virtual environment dependencies:
```bash
uv sync

```



### Step 3: Install Forge Globally on Your Machine

Forge uses **Hatchling** as its modern build backend to package your project natively. To install the CLI globally so you can trigger it from anywhere:

```bash
uv tool install . --force

```

*(This compiles the `cli` package, provisions an isolated global virtual environment, and links the global executable binary `forge` to your system's `$PATH`.)*

---

## Part 3: Running and Configuring Forge

### 1. Launching the Backend Servers

Because Forge is a decoupled system, your backend queue and Inngest engine must be running in the background to process dispatched tasks.

* **Start your FastAPI application** (which hosts your agent runner endpoints):
```bash
uvicorn main:app --reload --port 8000

```


* **Start the Inngest Dev Server** (which manages your background step queues and state logging):
```bash
inngest-cli dev

```


*(You can inspect your live agent runs, variable histories, and step waterfall timelines visually by opening **`http://localhost:8288`** in your browser.)*

### 2. Launching the CLI

Open a brand new terminal window, navigate to **any folder** on your computer where you want to perform coding tasks, and simply type:

```bash
forge

```

---

## Part 4: Step-by-Step Usage Guide

### Scenario A: Running a Valid Coding Task

1. When prompted, enter a software development task:
```text
forge 🤖 ❯ (Enter your task): Create a new directory named 'calculator_app', add a python script that multiplies two numbers inside it, and verify it exists.

```


2. Choose your model (press Enter to default to `gpt-4o-mini`, or type `local-llama3.2:latest` to run completely offline).
3. The CLI will transition to an active thinking spinner while the background queue securely runs `mkdir`, writing files, and inspecting paths.
4. Once completed, the spinner disappears and is replaced with a green success panel:
```text
✔ Task executed and completed successfully!

```



### Scenario B: Testing the Domain Guardrail

1. Try prompting the agent with a non-development or general conversational task:
```text
forge 🤖 ❯ (Enter your task): Write a romantic story about a programmer.

```


2. The local `llama3.2` model runs a lightning-fast pre-flight check on the prompt string.
3. The prompt is instantly blocked before it ever hits Inngest or your paid API endpoints:
```text
⛔ ACCESS DENIED: NON-DEVELOPMENT PROMPT DETECTED

Forge is optimized exclusively for software engineering tasks.
Please prompt me with tasks like writing code, debugging, package installation, or directory updates.

```