from fastapi import FastAPI
from src.models.rest.user_message import UserMessage
from src.graph.optimizator.optimization_agent import optimization_agent

web_app = FastAPI(title="Optimizer-agent", debug=True)


# todo init file to initiazte common resouces

# todo  router include


# todo mifdleve

# response moodel


# todo basemodel dict


# todo. pydantic - model config def as an example

@web_app.post("/chat")
async def chat_endpoint(request: UserMessage) -> dict:

  config = {'thread_id': 'default_thread'}
  response = await optimization_agent.run({request.message}, config)

  return {"reply": response['agent_message']}

if __name__ == "__main__":
  import uvicorn


  # swagger: http://localhost:8000/docs
  # fastapis standart uicorn under the hood

  uvicorn.run(web_app, host="localhost", port=8000)
