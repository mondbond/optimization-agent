from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

from models.enums.action_type import ActionType
from models.model_validation import ModelValidation
from models.structured_output.data_extraction_task import DataExtractionAction
from models.task.datamodel.data_item import DataItem


class AbstractDataModel(ABC, BaseModel):
  data_items: list[DataItem] = Field()

  def model_post_init(self, __context):
    self._data_map = {item.name : item for item in self.data_items}

  @classmethod
  @abstractmethod
  def create(cls):
    raise NotImplementedError

  @abstractmethod
  def validate_model_with_text_response(self) -> ModelValidation:
    raise NotImplementedError

  @abstractmethod
  def get_model_summary(self) -> str:
    raise NotImplementedError

  def update_data(self, data_item_name : str, key: str, value : float, key2=None):
    self._data_map[data_item_name].update(
        key1 = key,
        value=value
    )

  def update_with_action(self, action : DataExtractionAction):
    if not action.key1:
      return

    if action.action == ActionType.UPDATE:
      if action.key2:
        self._data_map[action.resource].update(
            key1 = action.key1,
            key2 = action.key2,
            value=action.value
        )
      else:
        self._data_map[action.resource].update(
            key1 = action.key1,
            value=action.value)

    if action.action == ActionType.REMOVE:
      if action.key2:
        if action.key1 in self._data_map[action.resource].data:
          if action.key2 in self._data_map[action.resource].data[action.key1]:
            del self._data_map[action.resource].data[action.key1][action.key2]
      else:
        if action.key1 in self._data_map[action.resource].data:
          del self._data_map[action.resource].data[action.key1]

  def get_resource_descriptions(self) -> str:
    descriptions = ""
    for item in self._data_map.values():
      descriptions += f"{item.name}: {item.description}\n"
    return descriptions

  def get_resource_action_examples(self) -> str:
    examples = ""
    for item in self._data_map.values():
      examples += f"{item.action_examples}\n"
    return examples

  @staticmethod
  def _get_empty_validation_rules(data_items: DataItem, msg) -> list[
                                                                          str] | None:
    rules = []

    for item in data_items.data.keys():
      if not data_items.data[item]:
        rules.append(f"{msg}  {item}")

    return rules


