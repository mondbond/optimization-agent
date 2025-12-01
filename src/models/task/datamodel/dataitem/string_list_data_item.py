from typing import Any

from pydantic import BaseModel, Field

from models.exceptions.chat_error_exception import DataPopulationError


class StringListDataItem(BaseModel):
  """
  Represents a data item that holds a list of string values.
  """

  STRING_LIST_CLASS: str = "StringListClass"

  data: Any = Field(default=[])
  data_name: str = Field()
  description: str = Field()
  action_examples: str = Field()

  def update(self, key1=None, key2=None, value=None):
    if not value:
      raise DataPopulationError(f"Value for {self.data_name} cannot be None.")

    self.data.append(str(value))
