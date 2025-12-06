

from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from models.enums.optimization_type import OptimizationType
from models.task.datamodel.abstract_data_model import AbstractDataModel


class DataCollectionState(TypedDict):
  route: str | None

  # conversation related
  history: list[AnyMessage] = []

  user_message: str

  agent_message: str | None

  optimization_data_model: AbstractDataModel | None
