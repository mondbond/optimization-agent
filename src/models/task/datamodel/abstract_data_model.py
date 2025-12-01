from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from models.enums.action_type import ActionType
from models.model_validation import ModelValidationInstructions
from models.structured_output.data_extraction_task import DataExtractionAction
from models.task.datamodel.dataitem.data_item import AbstractDataItem
from models.task.datamodel.dataitem.float_value_matrix_data_item import \
  FloatValueMatrixDataItem
from models.task.datamodel.dataitem.map_data_item import \
  MapWithFloatValueDataItem
from models.task.datamodel.dataitem.string_data_item import StringDataItem
from models.task.datamodel.dataitem.string_list_data_item import \
  StringListDataItem


class AbstractDataModel(ABC, BaseModel):
  """
  Abstract class for data model handlers in optimization tasks.
  Each data model handler must implement methods to create instances,
  validate the model with text responses, and provide a summary of the model.
  It helps to manage and validate data extracted from user inputs for optimization tasks.

  AbstractDataModel is responsible for common logic between different data models.
  """

  data_items: list[
    MapWithFloatValueDataItem | StringDataItem | FloatValueMatrixDataItem | StringListDataItem] = Field()

  def model_post_init(self, __context):
    self._data_map = {item.data_name: item for item in self.data_items}

  @classmethod
  @abstractmethod
  def create(cls):
    """
    Factory method to create an instance of the data model with predefined data items.
    :return: instance of a DomainModel
    """
    pass

  @abstractmethod
  def validate_model_with_instruction(self) -> ModelValidationInstructions:
    """
    Validates the data model and returns instructions for any necessary corrections.
    :return: ModelValidationInstructions object containing validation instructions for LLM.
    """
    pass

  @abstractmethod
  def get_model_summary(self) -> str:
    """
    Provides a summary of the current state of the data model.
    It's needed for confirming state with the user.
    :return: string summary of the data model.
    """
    pass

  @abstractmethod
  def to_mcp_dict(self) -> dict:
    """
    Converts the data model into a dictionary format suitable for MCP solver input.
    Need to refactor to Adapter pattern in case multiple mcp suporters are added.
    :return: map of data model suitable for MCP solver input.
    """
    pass

  @abstractmethod
  def already_existed_entities(self) -> str:
    """
    Provides a string representation of already existing entities in the data model.
    Goal is to make LLM aware of what entities are already present to avoid user's mistypes.
    :return: string representation of already existing entities.
    """
    pass

  def update_data(self, data_item_name: str, key: str, value, key2=None):
    """
    Updates the data item in the model with the provided key(s) and value.
    :param data_item_name:
    :param key:
    :param value:
    :param key2:
    :return:
    """
    if key2:
      self._data_map[data_item_name].update(
          key1=key,
          key2=key2,
          value=value
      )
    else:
      self._data_map[data_item_name].update(
          key1=key,
          value=value
      )

  def update_with_action(self, action: DataExtractionAction):
    # if not action.key1:
    #   return

    if action.action == ActionType.UPDATE:
      if action.key2:
        self._data_map[action.resource].update(
            key1=action.key1,
            key2=action.key2,
            value=action.value
        )
      else:
        self._data_map[action.resource].update(
            key1=action.key1,
            value=action.value)

    if action.action == ActionType.REMOVE:
      if action.key2:
        if action.key1 in self._data_map[action.resource].data:
          if action.key2 in self._data_map[action.resource].data[action.key1]:
            del self._data_map[action.resource].data[action.key1][action.key2]
      else:
        if action.key1 in self._data_map[action.resource].data:
          del self._data_map[action.resource].data[action.key1]

  def get_prompt_resource_descriptions(self) -> str:
    """
    Provides descriptions of all data resources in the model for prompt generation.
    Directly affects the quality of data extraction from user inputs.
    :return: string containing descriptions of all data resources.
    """

    descriptions = ""
    for item in self._data_map.values():
      descriptions += f"{item.data_name}: {item.description}\n"
    return descriptions

  def get_prompt_resource_action_examples(self) -> str:
    """
    Provides action examples for all data resources in the model for prompt generation.
    Directly affects the quality of data extraction from user inputs.
    :return: string containing action examples for all data resources.
    """

    examples = ""
    for item in self._data_map.values():
      examples += f"{item.action_examples}\n"
    return examples

  @staticmethod
  def _get_empty_validation_instructions(data_items: AbstractDataItem, msg) -> list[
                                                                          str] | None:
    """
    Common validation logic to check for empty data items in the model. Refactor it to a separate validator class if needed in future.
    :param data_items:
    :param msg:
    :return:
    """
    instructions = []

    for item in data_items.data.keys():
      if not data_items.data[item]:
        instructions.append(f"{msg}  {item}")

    return instructions
