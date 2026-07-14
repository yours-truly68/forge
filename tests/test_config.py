import os 
from config import settings



print("----Harness Config Test----")
print(f"Project Root Detected: {settings.PROJECT_ROOT}")
print(f"Allowed Commands: {settings.ALLOWED_COMMANDS}")

if settings.OPENAI_API_KEY:
    print("✅ API Key loaded successfully from .env!")
else:
    print("❌ API Key is missing! Check your .env file setup.")