from typing import Any

from pydantic import BaseModel, Field

from models.exceptions.chat_error_exception import DataPopulationError
from models.task.datamodel.dataitem.data_item import AbstractDataItem


class StringDataItem(AbstractDataItem):
  """
  Represents a data item that holds a string value.
  """

  STRING_CLASS: str = "StringDataItem"

  data: str = Field(default='')
  data_name: str = Field()
  description: str = Field()
  action_examples: str = Field()

  def update(self, key1=None, key2=None, value=None):
    if not value:
      raise DataPopulationError(f"Value for {self.data_name} cannot be None.")

    self.data = str(value)
