from fastapi import FastAPI
import inngest.fast_api
from harness.queue import inngest_client, run_durable_agent_loop
from config import ApprovalSubmit



def create_app() -> FastAPI:
    """
    The Application Factory. Responsible for building, configuring, and initalising the running state of the Forge Platform.
    """
    
    app = FastAPI(
        title = "Forge: Stateless Coding Agent Platform",
        version = "0.1.0"
    )
    
    
    inngest.fast_api.serve(
        app,
        inngest_client,
        [run_durable_agent_loop]
    )
    
    
    return app


app = create_app()

pending_approvals = {}
