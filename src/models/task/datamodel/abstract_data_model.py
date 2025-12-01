from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from models.enums.action_type import ActionType
from models.model_validation import ModelValidation
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
  data_items: list[
    MapWithFloatValueDataItem | StringDataItem | FloatValueMatrixDataItem | StringListDataItem] = Field()

  def model_post_init(self, __context):
    self._data_map = {item.data_name: item for item in self.data_items}

  @classmethod
  @abstractmethod
  def create(cls):
    pass

  @abstractmethod
  def validate_model_with_text_response(self) -> ModelValidation:
    pass

  @abstractmethod
  def get_model_summary(self) -> str:
    pass

  def update_data(self, data_item_name: str, key: str, value, key2=None):
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

  # todo create exceptions and refactor
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

  def get_resource_descriptions(self) -> str:
    descriptions = ""
    for item in self._data_map.values():
      descriptions += f"{item.data_name}: {item.description}\n"
    return descriptions

  def get_resource_action_examples(self) -> str:
    examples = ""
    for item in self._data_map.values():
      examples += f"{item.action_examples}\n"
    return examples

  @staticmethod
  def _get_empty_validation_rules(data_items: AbstractDataItem, msg) -> list[
                                                                          str] | None:
    rules = []

    for item in data_items.data.keys():
      if not data_items.data[item]:
        rules.append(f"{msg}  {item}")

    return rules
