# test_engine.py
from agents.registry import CODE_EXECUTOR
from harness.engine import compute_agent_step

print("--- Simulating a Single Engine Compute Turn ---")

# Mocking an input user prompt task
mock_history = [{"role": "user", "content": "List the files in the current folder."}]

# Run a single calculation cycle step
step_output = compute_agent_step(
    agent=CODE_EXECUTOR, 
    history=mock_history, 
    model_name="gpt-4o"
)

print("\n[Engine Extracted Thoughts]:")
print(step_output["raw_message"]["content"])

print("\n[Engine Extracted Tool Calls Map]:")
print(step_output["tool_calls"])