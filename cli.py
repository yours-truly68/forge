import os
import sys
import httpx
from dotenv import set_key

API_URL = "http://127.0.0.1:8000/api/inngest"

def ensure_any_api_key():
    """
    Scans the environment for any valid credential key setup.
    If completely blank, prompts the user to choose their target 
    provider and writes the corresponding key into the .env file.
    """
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    
    if not os.path.exists(env_path):
        with open(env_path, "w") as f:
            pass
    

    keys_to_check = ["GROQ_API_KEY", "VERCEL_API_KEY", "OPENAI_API_KEY"]
    active_keys=  {k: os.getenv(k,"") for k in keys_to_check}
    
    
# Read the physical file if env variables haven't been exported yet
    with open(env_path, "r") as f:
        for line in f:
            for k in keys_to_check:
                if line.startswith(k) and not active_keys[k]:
                    # CRITICAL FIX: Add [1] to isolate the string value from the split list 
                    # before applying string manipulation methods.
                    active_keys[k] = line.split("=")[1].strip().strip('"').strip("'")
                    
                    
    if any(active_keys.values()):
        return
    
    # 2. If completely dark, run the initialization onboarding wizard
    print("🛡️  [Forge Credentials Interceptor]")
    print("No active environment keys detected for OpenAI, Groq, or Vercel.")
    print("Select your target provider setup configuration:")
    print("1) OpenAI")
    print("2) Groq Cloud")
    print("3) Vercel AI Gateway")
    print("4) Running completely locally (Ollama / Passthrough)")
    
    choice = input("Select Option [1-4]: ").strip()
    
    if choice == "4":
        print("✅ Local mode selected. Assuming Ollama is active on port 11434.\n")
        return
        
    provider_map = {
        "1": ("OPENAI_API_KEY", "OpenAI API Key"),
        "2": ("GROQ_API_KEY", "Groq Cloud API Key"),
        "3": ("VERCEL_API_KEY", "Vercel API Key")
    }
    
    if choice not in provider_map:
        print("❌ Invalid target selected. Powering down.")
        sys.exit(1)
        
    env_variable, display_name = provider_map[choice]
    provided_key = input(f"Please enter your {display_name} securely: ").strip()
    
    if not provided_key:
        print("❌ Error: Key cannot be empty.")
        sys.exit(1)
        
    # If Vercel was chosen, also grab their Gateway Endpoint routing string
    if choice == "3":
        gateway_url = input("Please enter your VERCEL_GATEWAY_URL: ").strip()
        set_key(env_path, "VERCEL_GATEWAY_URL", gateway_url)
        os.environ["VERCEL_GATEWAY_URL"] = gateway_url

    # Save target parameters straight to disk configurations
    set_key(env_path, env_variable, provided_key)
    os.environ[env_variable] = provided_key
    print(f"✅ {display_name} successfully committed to your local .env configuration!\n")

def run_cli_session():
    """Manages the interactive command terminal interface prompt loop."""
    print("==================================================")
    print("   🔨 FORGE: Multi-Provider Coding Agent CLI      ")
    print("==================================================")
    print("Enter 'exit' or 'quit' at any prompt to close.\n")
    
    ensure_any_api_key()
    
    while True:
        try:
            
            task = input(
                "\n===========================================\n\n"
                "Forge 🤖 ❯ Enter task description: ").strip()
            "\n\n============================================\n"
            if not task:
                continue
            if task.lower() in ["exit", "quit"]:
                print("👋 Exiting Forge core harness assembly. Goodbye!")
                break
                
            print("\n💡 Model Naming Examples:")
            print(" - OpenAI: gpt-4o-mini, gpt-4o")
            print(" - Groq:   groq/llama-3.3-70b-specdec")
            print(" - Vercel: vercel/claude-3-5-sonnet")
            print(" - Local:  local-llama3")
            
            model_choice = input("Forge 🤖 ❯ Select model target [default: gpt-4o-mini]: ").strip()
            if not model_choice:
                model_choice = "gpt-4o-mini"
                
            print("\n🚀 Dispatching task event token to background execution queues...")
            
            payload = {
                "name": "agent/run.task",
                "data": {
                    "task": task,
                    "model_name": model_choice
                }
            }
            
            with httpx.Client() as client:
                response = client.post(API_URL, json=payload)
                
            if response.status_code in [200, 201]:
                print("✅ Task scheduled perfectly! Watch progress in your Inngest dev console.\n")
            else:
                print(f"❌ Failed to communicate with engine backend queue: {response.status_code}\n")
                
        except KeyboardInterrupt:
            print("\n👋 Session interrupted. Exiting.")
            break
        except Exception as e:
            print(f"❌ Network transmission failure encountered: {str(e)}\n")

if __name__ == "__main__":
    run_cli_session()