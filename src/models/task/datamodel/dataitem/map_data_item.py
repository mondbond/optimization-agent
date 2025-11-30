from models.exceptions.chat_error_exception import ChatErrorException
from models.task.datamodel.dataitem.data_item import AbstractDataItem
from pydantic import BaseModel, Field
from typing import Any, Dict


class MapWithFloatValueDataItem(BaseModel):

  MAP_WITH_FLOAT : str = "MAP_WITH_FLOAT"

  data: Any = Field(default={})
  data_name : str = Field()
  description : str = Field()
  action_examples : str = Field()

  def update(self, key1=None, key2=None, value=None):

    if not value:
      value = 0.0

    try:
      self.data[key1] = float(value)
    except Exception:
      raise ChatErrorException(
          f"Value for {self.data_name} {key1} must be a float number."
      )
