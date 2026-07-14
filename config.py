import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str=os.getenv("OPENAI_API_KEY")
    VERCEL_BASE_URL: str=os.getenv("VERCEL_BASE_URL")
    GROQ_API_KEY:str =os.getenv("GROQ_API_KEY")
    ENVIRONMENT: str ="sandbox-v1"
    PROJECT_ROOT: str = os.getcwd()
    ALLOWED_COMMANDS: list[str] = [
    "ls",
    "pwd",
    "cd",
    "cat",
    "find",
    "grep",
    "tree",

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
        env_file=".env"


settings = Settings()
