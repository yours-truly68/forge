from harness.client import LLMHarnessClient
from agents.registry import CODE_EXECUTOR, compile_agent_prompt

print("--- Initializing LLM Client Wrapper ---")
harness_client = LLMHarnessClient()

# Compile a prompt for testing
system_prompt = compile_agent_prompt(CODE_EXECUTOR)

# Simulate a message history array
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Please create a directory named 'uv_harness_test'."}
]

print("Sending request to LLM Brain...")
response = harness_client.call_brain(model_name="gpt-4o-mini", messages=messages)

print("\n--- LLM Response Received ---")
print(f"Text Content: {response.content}")
print(f"Tool Calls Detected: {response.tool_calls}")