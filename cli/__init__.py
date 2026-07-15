import httpx
from rich.panel import Panel
from rich.prompt import Prompt

from cli.auth import get_stored_keys
from cli.interface import (
    console,
    dispatch_with_spinner,
    render_banner,
    run_onboarding_wizard,
)


def ask_multiline_task() -> str:
    """
    Collects task input from the terminal.
    - If it's a standard single line, it submits immediately on Enter.
    - If a line ends with a backslash '\\', it continues on the next line.
    """
    console.print(
        "\n[brand]forge[/brand] [agent]🤖[/agent] [subtle](Enter task. End with '\\' for multi-line)[/subtle]:"
    )

    lines = []
    while True:
        try:
            line = input()
            # If the line ends with a backslash, strip it and prepare for more lines
            if line.endswith("\\"):
                lines.append(line[:-1])  # Store line without the backslash
                continue

            # Otherwise, append this final line and break
            lines.append(line)
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt

    return "\n".join(lines).strip()


def curate_user_prompt(raw_prompt: str) -> str:
    """
    Passes the user's raw input to a fast local model to expand it into
    an explicit, detailed, and tool-friendly execution plan.
    """
    system_instruction = (
        "You are an expert Prompt Engineer for AI Coding Agents. Your job is to take a raw, "
        "short user prompt and expand it into a highly explicit, step-by-step instruction set.\n"
        "CRITICAL: If the user is asking for a simple utility action (like deleting a file, "
        "removing a directory, checking status, or cleaning up), DO NOT over-engineer it. Just "
        "provide the direct, safe shell execution steps (e.g., standard rm or rmdir commands).\n"
        "Only use multi-line heredocs (cat << 'EOF') if the user explicitly asks to write source code code "
        "or create complex multi-line program scripts. Respond ONLY with the expanded prompt."
    )

    try:
        # Use your running Ollama instance to curate the prompt instantly
        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:latest",
                "prompt": f"{system_instruction}\n\nRaw user prompt to expand: {raw_prompt}",
                "stream": False,
            },
            timeout=8.0,
        )
        if response.status_code == 200:
            curated_prompt = response.json().get("response", "").strip()
            if curated_prompt:
                print(curated_prompt)
                return curated_prompt
    except Exception as e:
        # If Ollama is offline, gracefully fall back to the raw prompt
        print(e)
        pass

    return raw_prompt


def is_strictly_coding_task(prompt_text: str) -> bool:
    """
    Uses an ultra-fast local LLM check to ensure the user is only asking for coding,
    debugging, setup, testing, or file structure creation.
    """
    system_instruction = (
        "You are a strict task classifier. Your job is to determine if a prompt is a "
        "software engineering task (writing code, debugging, git, creating project files/directories, "
        "installing packages, running scripts, tests, etc.) or not.\n"
        "Respond with ONLY the word 'TRUE' if it is a coding/development task, "
        "and ONLY the word 'FALSE' if it is general conversation, math, story writing, philosophy, or unrelated to coding."
    )

    try:
        # Query Ollama locally (or OpenAI depending on what's active)
        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:latest",
                "prompt": f"{system_instruction}\n\nTask to classify: {prompt_text}",
                "stream": False,
            },
            timeout=5.0,
        )
        if response.status_code == 200:
            result = response.json().get("response", "").strip().upper()
            return "TRUE" in result
    except Exception:
        # Fallback rule-based filter if local model isn't running
        coding_keywords = [
            "code",
            "create",
            "file",
            "folder",
            "git",
            "run",
            "python",
            "js",
            "ts",
            "directory",
            "script",
            "mkdir",
            "write",
        ]
        return any(word in prompt_text.lower() for word in coding_keywords)

    return True


def run_cli_session():
    """Core terminal execution loop."""
    render_banner()

    # Pre-flight credential verification
    # if not any(get_stored_keys().values())
    run_onboarding_wizard()

    while True:
        try:
            # Calls the smart multi-line collector
            task = ask_multiline_task()

            if not task:
                continue
            if task.lower() in ["exit", "quit", "e", "q"]:
                console.print(
                    "\n[subtle]👋 Shutdown signal received. Exiting Forge shell.[/subtle]"
                )
                break

            # 🛡️ THE GUARDRAIL: Pre-flight domain verification
            if not is_strictly_coding_task(task):
                console.print("\n")
                console.print(
                    Panel(
                        "[error]⛔ ACCESS DENIED: NON-DEVELOPMENT PROMPT DETECTED[/error]\n\n"
                        "Forge is optimized exclusively for software engineering tasks.\n"
                        "Please prompt me with tasks like writing code, debugging, package installation, or directory updates.",
                        title="[brand]Domain Guardrail[/brand]",
                        border_style="error",
                    )
                )
                continue

            # 🪄 THE CURATOR: Expand the prompt before dispatching
            console.print(
                "[subtle]🪄 Curating and optimizing your prompt for the agent...[/subtle]"
            )
            curated_task = curate_user_prompt(task)
            console.print(f"[subtle]Curated Prompt: {curated_task}[/subtle]\n\n")

            console.print(
                "[subtle]💡 e.g., gpt-4o-mini | groq/llama-3.3-70b-specdec | local-llama3.2:latest[/subtle]"
            )
            model = (
                Prompt.ask(
                    "[brand]model[/brand] [subtle](default: vercel/gpt-4o-mini)[/subtle]"
                ).strip()
                or "vercel/gpt-4o-mini"
            )
            
            # Dispatch the beautifully optimized curated task instead of the raw one!
            dispatch_with_spinner(curated_task, model)

        except KeyboardInterrupt:
            console.print(
                "\n\n[subtle]👋 Keyboard interrupt detected. Exiting.[/subtle]"
            )
            break


if __name__ == "__main__":
    run_cli_session()
