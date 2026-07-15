from openai import OpenAI
from config import settings
from tools.terminal import BASH_TOOL_SCHEMA

class LLMHarnessClient:
    """
    Dynamic Multi-Provider Network Diplomat.
    Routes execution payloads seamlessly to OpenAI, Groq, Vercel AI Gateway,
    or local Ollama instances based strictly on the model name keyword target.
    """
    
    def _get_provider_client(self, model_name: str) -> tuple[OpenAI, str]:
        """
        Evaluates the model name string target to return the correctly configured 
        SDK client instance along with its validated authentication security key.
        """
        # harness/client.py (Update the local route branch)

        # 1. Local Ollama Mapping Route
        if model_name.startswith("local-") or model_name in ["llama3", "mistral", "phi3"]:
            # local_url = os.getenv("{OLLAMA_BASE_URL", "http://localhost:11434/v1")
            local_url = settings.OLLAMA_BASE_URL or "http://localhost:1143/v1"
            # CRITICAL FIX: Strip off the local- prefix so Ollama gets the exact model tag
            target_model = model_name.replace("local-", "")
            return OpenAI(base_url=local_url, api_key="ollama-passthrough"), target_model
            
        # 2. Groq Cloud Engine Mapping Route
        elif model_name.startswith("groq/") or "llama-3" in model_name or "mixtral" in model_name:
            # groq_key = os.getenv("GROQ_API_KEY", "")
            groq_key = settings.GROQ_API_KEY or ""
            # base_url=os.getenv("GROQ_BASE_URL","https://api.groq.com/openai/v1"),
            base_url = settings.GROQ_BASE_URL or "https://api/groq.com/openai/v1"
            target_model = model_name.replace("groq/", "")
            
            return OpenAI(
                base_url=base_url,
                api_key=groq_key
            ), target_model

        # 3.  NEW: Vercel AI Gateway Route
        elif model_name.startswith("vercel/"):
            # vercel_key = os.getenv("VERCEL_API_KEY", "")
            vercel_key = settings.VERCEL_API_KEY or ""
            # gateway_url = os.getenv("VERCEL_BASE_URL", "")
            gateway_url = settings.VERCEL_BASE_URL or ""            
            target_model = model_name.replace("vercel/", "")
            return OpenAI(
                base_url=gateway_url,
                api_key=vercel_key
            ), target_model
            
        # 4. Default OpenAI Cloud Route System
        else:
            return OpenAI(api_key=settings.OPENAI_API_KEY), model_name

    def call_brain(self, model_name: str, messages: list, temperature: float = 0.1):
        """Resolves the appropriate model gateway dynamically and executes inference."""
        client, resolved_model = self._get_provider_client(model_name)
        
        response = client.chat.completions.create(
            model=resolved_model,
            messages=messages,
            temperature=temperature,
            tools=[BASH_TOOL_SCHEMA],
            tool_choice="auto"
        )
        return response.choices[0].message