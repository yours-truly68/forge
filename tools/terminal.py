import subprocess
from config import settings

def run_bash_command(command: str) -> str:
    """
    Safely executes bash terminal commands locally and intercepts the output.
    """
    # Block dangerous or hidden redirects that throw away output
    if "> /dev/null" in command:
        # Strip out the silent redirect so we can actually capture what happened
        command = command.replace("> /dev/null", "").strip()

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
        
        # 🛡️ THE FIX: If the exit code is not 0, the command failed!
        if result.returncode != 0:
            error_msg = f"Execution Failed (Exit Code {result.returncode})."
            if result.stderr:
                error_msg += f"\nShell Error:\n{result.stderr.strip()}"
            elif result.stdout:
                error_msg += f"\nShell Output:\n{result.stdout.strip()}"
            return error_msg

        output = result.stdout
        return output if output.strip() else "Command executed successfully (no output)."
    
    except subprocess.TimeoutExpired:
        return "Error: Command execution timed out after 20 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"


# --- STRICTLY ENFORCED SCHEMA ---
BASH_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "run_bash_command",
        "description": (
            "Execute a standard local bash command to create files, run python tests, or check directory statuses. "
            "To write a file, write a clean 'cat' command with a single-quoted heredoc delimiter to prevent "
            "syntax errors. Never redirect command outputs to /dev/null."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The exact bash command to execute (e.g., 'cat << 'EOF' > add.py\\ndef add(a,b):\\n    return a+b\\nEOF' or 'python3 add.py')."
                }
            },
            "required": ["command"]
        }
    }
}