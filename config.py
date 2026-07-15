import os
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Settings(BaseSettings):
    OPENAI_API_KEY: str=os.getenv("OPENAI_API_KEY")
    VERCEL_API_KEY: str=os.getenv("VERCEL_API_KEY")
    VERCEL_BASE_URL: str=os.getenv("VERCEL_BASE_URL")
    GROQ_API_KEY:str =os.getenv("GROQ_API_KEY")
    OLLAMA_BASE_URL:str= os.getenv("OLLAMA_BASE_URL")
    GROQ_BASE_URL:str = os.getenv("GROQ_BASE_URL")
    ENVIRONMENT: str ="sandbox-v1"
    PROJECT_ROOT: str = BASE_DIR
    ALLOWED_COMMANDS: list[str] = [
        "ls",
        "pwd",
        "cd",
        "cat",
        "find",
        "grep",
        "tree",
        
        "rm",
        "rmdir"

        "git",
        "uv",
        "python",
        "pytest",

        "npm",
        "npx",
        "pnpm",
        "yarn",

        "node",

        "mkdir",
        "touch",
        "cp",
        "mv",

        "echo",

        "cargo",
        "go",
        "java",
        "javac",
        "mvn",
        "gradle",

        "pip",
        "pip3",
    ]
    
    class Config:
        # Pass the absolute path straight to the environment loader
        env_file = os.path.join(BASE_DIR, ".env")
        extra = "ignore"  # Gracefully ignore extra fields if present

settings = Settings()
