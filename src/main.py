from fastapi import FastAPI
from src.models.rest.user_message import UserMessage
from src.graph.optimizator.optimization_agent import optimization_agent
import uvicorn

web_app = FastAPI(title="Optimizer agent", debug=True)

@web_app.post("/chat")
async def chat_endpoint(request: UserMessage) -> dict:
  """
  Chat endpoint to interact with the optimization agent.
  :param request: request containing user's message
  :return: dictionary with agent's reply
  """

  config = {'thread_id': 'default_thread'}
  response = await optimization_agent.run({request.message}, config)

  return {"reply": response['agent_message']}

if __name__ == "__main__":
  uvicorn.run(web_app, host="localhost", port=8000)
