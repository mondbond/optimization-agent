

from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from models.enums.optimization_type import OptimizationType
from models.model_validation import ModelValidationInstructions
from models.structured_output.action_extractors import ExtractionActionList
from models.task.datamodel.abstract_data_model import AbstractDataModel


class DataPopulationState(TypedDict):
  route: str | None

  # conversation related
  history: list[AnyMessage] = []

  data_collection_actions : ExtractionActionList

  model_validation: ModelValidationInstructions

  user_message: str

  agent_message: str | None

  optimization_data_model: AbstractDataModel | None

  is_need_to_delete_all_data: bool | None
