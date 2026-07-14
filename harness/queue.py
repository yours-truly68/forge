import inngest
from tools.terminal import run_bash_command
from harness.engine import compute_agent_step
from agents.registry import CODE_EXECUTOR

inngest_client = inngest.Inngest(app_id="forge_agent_platform", is_production=False)


@inngest_client.create_function(
    fn_id="run_durable_agent_loop",
    trigger=inngest.TriggerEvent(event="agent/run.task"),
)


async def run_durable_agent_loop(context: inngest.Contextn):
    task_prompt = context.event.data["task"]
    model_name=context.event.data.get("model_name", "gpt-4o")
    
    chat_history = [{"role": "user", "content": task_prompt}]
    
    
    for iteration in range(5):
        
        #Checkpoint LLM reasoning cycle
        
        step_result = await context.step.run(
            f"llm_inference_turn-{iteration}",
            lambda: compute_agent_step(CODE_EXECUTOR, chat_history, model_name)
        )
        
        chat_history.append(step_result["raw_message"])
        
        
        #If the agent doesnt want to run any more tool calls the iteration ends
        if not step_result["tool_calls"]:
            break
        
        
        #Intercept and process tool intentions sequentially
        for tool in step_result["tool_calls"]:
            if tool["name"] == "run_bash_command":
                cmd = tool["arguments"]["command"]
                
                
                tool_output = await context.step.run(
                    f"bash-execution-{iteration}",
                    lambda: run_bash_command(cmd)
                )
                
                chat_history.append({
                    "role": "tool",
                    "tool_call_id": tool["id"],
                    "name": "run_bash_command",
                    "content": tool_output
                })
                        
    return {"status": "finished", "final_history_length": len(chat_history)}