from agents.registry import CODE_EXECUTOR, compile_agent_prompt

print(f"--- Testing Agent Profile: {CODE_EXECUTOR.name} ---")
compiled_prompt = compile_agent_prompt(CODE_EXECUTOR)
print(compiled_prompt)