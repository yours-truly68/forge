import subprocess
from config import settings


def run_bash_command(command: str) -> str:
    """
    Safely executes bash terminal commands locally and intercepts the output.
    """
    #Primary command
    primary_command = command.strip().split()[0] if command.strip() else ""
    
    if primary_command not in settings.ALLOWED_COMMANDS:
        return f"Security Error: Command execution denied. '{primary_command}' is not whitelisted."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=20
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\nError:\n {result.stderr}"
            
        return output if output.strip() else "Command executed successfully (no output)."
    
    except subprocess.TimeoutExpired:
        return "Error: Command execution timed out after 20 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"
    
    
BASH_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "run_bash_command",
        "description": (
            "Execute a command in the local bash shell workspace. "
            "CRITICAL: When writing multi-line code or text containing parentheses () or brackets [] to a file, "
            "never use raw echo. ALWAYS use a heredoc template with single-quotes around EOF to prevent shell "
            "syntax errors. Example:\n"
            "cat << 'EOF' > filename.py\n"
            "def add(a, b):\n"
            "    return a + b\n"
            "EOF"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The exact bash command to execute."
                }
            },
            "required": ["command"]
        }
    }
}
    