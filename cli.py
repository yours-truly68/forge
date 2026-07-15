import os
import httpx
from rich.prompt import Prompt
from rich.panel import Panel
from cli.auth import get_stored_keys
from cli.interface import (
    console, 
    render_banner, 
    run_onboarding_wizard, 
    dispatch_with_spinner
)

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
                "stream": False
            },
            timeout=5.0
        )
        if response.status_code == 200:
            result = response.json().get("response", "").strip().upper()
            return "TRUE" in result
    except Exception:
        # Fallback rule-based filter if local model isn't running
        coding_keywords = ["code", "create", "file", "folder", "git", "run", "python", "js", "ts", "directory", "script", "mkdir", "write"]
        return any(word in prompt_text.lower() for word in coding_keywords)
        
    return True

def run_cli_session():
    """Core terminal execution loop."""
    render_banner()
    
    # Pre-flight credential verification
    if not any(get_stored_keys().values()):
        run_onboarding_wizard()
        
    while True:
        try:
            task = Prompt.ask("\n[brand]forge[/brand] [agent]🤖[/agent] [subtle](Enter your task)[/subtle]").strip()
            if not task:
                continue
            if task.lower() in ["exit", "quit"]:
                console.print("\n[subtle]👋 Shutdown signal received. Exiting Forge shell.[/subtle]")
                break
            
            # 🛡️ THE GUARDRAIL: Pre-flight domain verification
            if not is_strictly_coding_task(task):
                console.print("\n")
                console.print(Panel(
                    "[error]⛔ ACCESS DENIED: NON-DEVELOPMENT PROMPT DETECTED[/error]\n\n"
                    "Forge is optimized exclusively for software engineering tasks.\n"
                    "Please prompt me with tasks like writing code, debugging, package installation, or directory updates.",
                    title="[brand]Domain Guardrail[/brand]", 
                    border_style="error"
                ))
                continue  # Skip to the next prompt cycle without asking for a model or dispatching

            console.print("[subtle]💡 e.g., gpt-4o-mini | groq/llama-3.3-70b-specdec | vercel/claude-3-5-sonnet | local-llama3[/subtle]")
            model = Prompt.ask("[brand]model[/brand] [subtle](default: gpt-4o-mini)[/subtle]").strip() or "gpt-4o-mini"
            
            # Delegates rendering and calling logic to cli/interface
            dispatch_with_spinner(task, model)
                
        except KeyboardInterrupt:
            console.print("\n\n[subtle]👋 Keyboard interrupt detected. Exiting.[/subtle]")
            break

if __name__ == "__main__":
    run_cli_session()