from openai import OpenAI
from config import settings
from tools.terminal import BASH_TOOL_SCHEMA

class LLMHarnessClient:
    """
    Handles the direct network connection to LLM provider.
    Isolates the rest of the application from provider-specific SDK syntax.
    """
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.VERCEL_BASE_URL)
        
    def call_brain(self, model_name:str, messages: list, temperature: float = 0.1):
        """
        Sends the compiled context history and tool schemas to the LLM and returns the raw assistant response message.
        """
        
        response = self.client.chat.completions.create(
            model=model_name, 
            messages=messages,
            temperature=temperature,
            tools=[BASH_TOOL_SCHEMA],
            tool_choice="auto"
        )
        
        return response.choices[0].message