from fastapi import FastAPI
from src.models.rest.user_message import UserMessage
from src.graph.optimizator.optimization_agent import optimization_agent

web_app = FastAPI(title="Optimizer-agent", debug=True)

@web_app.post("/chat")
async def chat_endpoint(request: UserMessage) -> dict:

  response = optimization_agent.run({request.message})

  return {"reply": response['agent_message']}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(web_app, host="localhost", port=8000)
