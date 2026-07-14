from tools.terminal import run_bash_command


print("--- Testing Whitelisted Command ---")
success_test = run_bash_command("echo 'Hello from the terminal tool!'")
print(f"Result:\n{success_test}\n")

print("--- Testing Security Block Guardrail ---")
blocked_test = run_bash_command("sudo apt-get update")
print(f"Result:\n{blocked_test}")