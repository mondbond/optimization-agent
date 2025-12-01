from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from models.enums.optimization_type import OptimizationType
from models.task.datamodel.abstract_data_model import AbstractDataModel


class OptimizatorAgentState(TypedDict):
  route: str | None

  # conversation related
  history: Annotated[list[AnyMessage], operator.add] = []

  user_message: str

  agent_message: str | None

  confirmation_stage: bool | None

  # optimization related
  optimization_task_type: OptimizationType | None

  optimization_data_model: AbstractDataModel | None
