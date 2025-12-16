from langchain.messages import AnyMessage
from typing_extensions import TypedDict
from models.model_validation import ConversationInstructions
from models.structured_output.action_extractors import ExtractionActionList
from models.task.datamodel.abstract_data_model import AbstractDataModel


class DataPopulationState(TypedDict):
  """
  State information for data population in a conversation-driven data collection process.
  1. route: Optional route identifier for the data collection process.
  2. history: List of messages exchanged in the conversation.
  3. data_collection_actions: List of extraction actions to be performed on data model.
  4. model_validation: Instructions for validataion to inject in answering prompt after data caollection graph execution.
  5. user_message: The latest message from the user.
  7. optimization_data_model: The data model used for optimization tasks.
  It will be populated during Data Collection phase.
  8. is_need_to_delete_all_data: Flag indicating whether all data needs to be deleted.

  """

  route: str | None

  history: list[AnyMessage] = []

  data_collection_actions: ExtractionActionList

  model_validation: ConversationInstructions

  user_message: str

  optimization_data_model: AbstractDataModel | None

  is_need_to_delete_all_data: bool | None
