# cli/auth.py
import os
import time
import httpx
from dotenv import set_key

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
API_URL = "http://127.0.0.1:8288/e/mock_key"
DEV_SERVER_API = "http://localhost:8288/v1"

def get_stored_keys() -> dict:
    """Reads keys from the local environment and falls back to the .env file."""
    keys = {"OPENAI_API_KEY": "", "GROQ_API_KEY": "", "VERCEL_API_KEY": ""}
    for key in keys:
        keys[key] = os.getenv(key, "")
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            for line in f:
                parts = line.strip().split("=", 1)
                if len(parts) == 2 and parts[0] in keys and not keys[parts[0]]:
                    keys[parts[0]] = parts[1].strip().strip('"').strip("'")
    return keys

def save_credential(key_name: str, value: str):
    """Writes a secure parameter permanently to the local configuration."""
    set_key(ENV_PATH, key_name, value)
    os.environ[key_name] = value

def dispatch_task(task: str, model: str) -> str | None:
    """
    Sends the event payload to the Inngest queue.
    Returns the unique Inngest Event ID if successful.
    """
    payload = {
        "name": "agent/run.task",
        "data": {"task": task, "model_name": model}
    }
    try:
        with httpx.Client() as client:
            response = client.post(API_URL, json=payload)
        if response.status_code in [200, 201]:
            # Inngest returns: {"ids": ["01HX..."], "status": 200}
            return response.json().get("ids", [None])[0]
    except Exception:
        pass
    return None

def poll_run_status(event_id: str, on_update_callback) -> dict:
    """
    Polls the local Inngest Dev Server until the workflow completes or fails.
    Invokes the callback with step statuses to keep the UI live.
    """
    url = f"{DEV_SERVER_API}/events/{event_id}/runs"
    
    while True:
        try:
            with httpx.Client() as client:
                response = client.get(url)
                
            if response.status_code == 200:
                runs_data = response.json().get("data", [])
                if runs_data:
                    run = runs_data[0]
                    status = run.get("status") # "Running", "Completed", "Failed", "Cancelled"
                    
                    # Send update to UI callback
                    on_update_callback(status)
                    
                    if status in ["Completed", "Failed", "Cancelled"]:
                        return run
        except Exception:
            pass
        time.sleep(1.0)