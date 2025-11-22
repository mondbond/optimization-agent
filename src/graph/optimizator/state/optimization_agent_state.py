from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from models.enums.optimization_type import OptimizationType


class OptimizatorAgentState(TypedDict):
  route: str | None

  history: Annotated[list[AnyMessage], operator.add] = []

  optimization_task_type: OptimizationType | None

  user_message: str

  agent_message: str | None
