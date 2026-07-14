from pydantic import BaseModel
from config import settings

class AgentPersona(BaseModel):
    """
    A pure configuration blueprint for a stateless agent persona.
    Contains no memory, history, or execution code.
    """
    name:str
    base_instructions :str

CODE_EXECUTOR = AgentPersona(
    name="Code_Executor",
    base_instructions=(
        """
        You are an AUTONOMOUS SOFTWARE ENGINEERING ENGINE. Your job is to write, modify, and execute code to fulfill the user's requests.
        You have direct access to a BASH TERMINAL tool. Always check the output of your commands to verify success
        """
    )
)

def compile_agent_prompt(agent: AgentPersona) -> str:
    """
    Takes a stateless agent persona and dynamically binds the active
    global system context and security rules into its final system prompt.
    """
    global_context = (
        f"\n\n[CRITICAL OPERATING BOUNDARIES]"
        f"\nYour Root Workspace: {settings.PROJECT_ROOT}"
        f"\nAllowed Terminal Commands: {settings.ALLOWED_COMMANDS}"
        f"\nGuardrail: You must never attempt to execute commands outside of the allowed list."
    )
    return f"Role: {agent.name}\nInstructions: {agent.base_instructions}{global_context}"