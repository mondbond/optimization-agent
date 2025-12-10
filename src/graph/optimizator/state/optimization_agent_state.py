from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from models.enums.optimization_type import OptimizationType
from models.task.datamodel.abstract_data_model import AbstractDataModel

class OptimizatorAgentState(TypedDict):
  """
  State structure for the optimization agent.
  It holds information about the conversation history, user and agent messages,
  confirmation stage, optimization task type, and the associated data model.
  1. route: str | None - The current route in the agent's workflow.
  2. history: list[AnyMessage] - The conversation history between the user and the agent.
  3. user_message: str - The latest message from the user.
  4. agent_message: str | None - The latest message from the agent.
  5. confirmation_stage: bool | None - Indicates if the agent is in the confirmation stage.
  6. optimization_task_type: OptimizationType | None - The type of optimization task being handled.
  7. optimization_data_model: AbstractDataModel | None - The data model associated with the optimization task.
  """

  route: str | None

  history: Annotated[list[AnyMessage], operator.add] = []

  user_message: str

  agent_message: str | None

  confirmation_stage: bool | None

  optimization_task_type: OptimizationType | None

  optimization_data_model: AbstractDataModel | None
