# harness/engine.py
import json
from harness.client import LLMHarnessClient
from agents.registry import AgentPersona, compile_agent_prompt

llm_client = LLMHarnessClient()

def compute_agent_step(agent: AgentPersona, history: list, model_name: str) -> dict:
    """
    Executes a single, stateless inference cycle step against the LLM.
    Ensures all outputs are completely converted to primitive types for JSON serialization.
    """
    system_prompt = compile_agent_prompt(agent)
    messages = [{"role": "system", "content": system_prompt}] + history
    
    assistant_msg = llm_client.call_brain(model_name=model_name, messages=messages)
    
    tool_calls_extracted = []
    if assistant_msg.tool_calls:
        for tool in assistant_msg.tool_calls:
            tool_calls_extracted.append({
                "id": tool.id,
                "name": tool.function.name,
                "arguments": json.loads(tool.function.arguments)
            })

    # CRITICAL FIX: Convert the native OpenAI Pydantic model into a primitive dictionary
    
    # so Inngest can seamlessly serialize and checkpoint the step data.
    serializable_message = assistant_msg.model_dump(exclude_none=True)

    return {
        "raw_message": serializable_message,
        "tool_calls": tool_calls_extracted
    }