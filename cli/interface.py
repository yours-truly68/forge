# cli/interface.py
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.status import Status
from rich.theme import Theme
from cli.auth import save_credential, dispatch_task, poll_run_status

theme = Theme({
    "brand": "bold #D97706",         # Warm Claude amber
    "agent": "bold #3B82F6",         # Blue status
    "success": "bold #10B981",       # Emerald green
    "error": "bold #EF4444",         # High-contrast red
    "subtle": "#6B7280",             # Dimmed gray
    "border": "#4B5563"              # Slate gray
})

console = Console(theme=theme)

def render_banner():
    """Renders the master console logo and connection status."""
    banner_text = Text.from_markup("🔨 FORGE : DECOUPLED AGENT SANDBOX\n[subtle]System online & listening[/subtle]", justify="center", style="bold")
    console.print(Panel(
        banner_text,
        title="[brand]FORGE SHELL[/brand]", border_style="brand", padding=(1, 5)
    ))

def run_onboarding_wizard():
    """Renders the step-by-step setup configuration console panel."""
    console.print(Panel(
        Text("🛡️  FORGE SECURITY CREDENTIAL MANAGER\n\nNo active keys detected. Let's configure your model provider.", justify="center"),
        title="[brand]Onboarding[/brand]", border_style="border"
    ))

    console.print("\n[bold]Choose your model provider configuration:[/bold]")
    console.print("  [brand]1)[/brand] OpenAI\n  [brand]2)[/brand] Groq Cloud\n  [brand]3)[/brand] Vercel AI Gateway\n  [brand]4)[/brand] Local (Ollama / Passthrough)")
    
    choice = Prompt.ask("\nSelect Option", choices=["1", "2", "3", "4"], default="1")
    if choice == "4":
        console.print("\n[success]✔ Local mode configured.[/success]\n")
        return

    provider_map = {
        "1": ("OPENAI_API_KEY", "OpenAI API Key"),
        "2": ("GROQ_API_KEY", "Groq Cloud API Key"),
        "3": ("VERCEL_API_KEY", "Vercel API Key")
    }
    
    env_var, name = provider_map[choice]
    key_val = Prompt.ask(f"\nEnter your [brand]{name}[/brand]", password=True)
    if not key_val:
        console.print("[error]❌ Key value cannot be blank.[/error]")
        sys.exit(1)

    save_credential(env_var, key_val)
    
    if choice == "3":
        gateway = Prompt.ask("Enter your [brand]VERCEL_BASE_URL[/brand]").strip()
        save_credential("VERCEL_GATEWAY_URL", gateway)

    console.print("\n[success]✔ Config updated! Key saved to .env.[/success]\n")

def dispatch_with_spinner(task: str, model: str):
    """Wraps the task dispatch and live polling inside a clean Claude-style loading spinner."""
    event_id = dispatch_task(task, model)
    
    if not event_id:
        console.print("[error]✖ Transmission failed. Is your main.py server running?[/error]")
        return

    # Active status loader block
    with Status("[bold]Agent initiated... awaiting first reasoning cycle[/bold]", spinner="dots", console=console) as status:
        
        # This function updates the spinner label live based on what the background engine is doing!
        def update_spinner(run_status: str):
            if run_status == "Running":
                status.update("[bold]Agent executing thinking turns and terminal tools...[/bold]")
            elif run_status == "Completed":
                status.update("[success]Finalizing workflow details...[/success]")
                
        # Block the CLI and poll until complete
        final_run_data = poll_run_status(event_id, update_spinner)
        
    # Spinner clears completely! Display beautiful final success blocks
    final_status = final_run_data.get("status")
    
    if final_status == "Completed":
        console.print("\n[success]✔ Task executed and completed successfully![/success]")
        console.print("[subtle]Changes successfully applied to local sandbox filesystem.[/subtle]")
    else:
        console.print(f"\n[error]✖ Run finished with status: {final_status}[/error]")
        console.print("[subtle]Check http://localhost:8288/runs to trace the failure.[/subtle]")