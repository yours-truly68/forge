from rich.prompt import Prompt
from cli.auth import get_stored_keys
from cli.interface import (
    console, 
    render_banner, 
    run_onboarding_wizard, 
    dispatch_with_spinner
)

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
                
            console.print("[subtle]💡 e.g., gpt-4o-mini | groq/llama-3.3-70b-specdec | vercel/claude-3-5-sonnet | local-llama3[/subtle]")
            model = Prompt.ask("[brand]model[/brand] [subtle](default: gpt-4o-mini)[/subtle]").strip() or "gpt-4o-mini"
            
            # Delegates rendering and calling logic to cli/interface
            dispatch_with_spinner(task, model)
                
        except KeyboardInterrupt:
            console.print("\n\n[subtle]👋 Keyboard interrupt detected. Exiting.[/subtle]")
            break

if __name__ == "__main__":
    run_cli_session()