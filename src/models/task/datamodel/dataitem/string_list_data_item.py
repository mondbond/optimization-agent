from models.exceptions.chat_error_exception import ChatErrorException
from models.task.datamodel.dataitem.data_item import AbstractDataItem
from pydantic import BaseModel, Field
from typing import Any


class StringListDataItem(BaseModel):

  STRING_LIST_CLASS : str = "StringListClass"

  data: Any = Field(default=[])
  data_name : str = Field()
  description : str = Field()
  action_examples : str = Field()

  def update(self, key1=None, key2=None, value=None):
    if not value:
      raise ChatErrorException(f"Value for {self.data_name} cannot be None.")

    self.data.append(str(value))
