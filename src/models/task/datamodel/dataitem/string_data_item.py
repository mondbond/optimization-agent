from models.exceptions.chat_error_exception import ChatErrorException
from models.task.datamodel.dataitem.data_item import AbstractDataItem
from pydantic import BaseModel, Field
from typing import Any

class StringDataItem(BaseModel):

  STRING_CLASS : str = "StringDataItem"

  data: Any = Field(default='')
  data_name : str = Field()
  description : str = Field()
  action_examples : str = Field()
  # def __init__(self, data_name: str, description: str, action_examples: str):
  #   super().__init__(data="",
  #                    name=data_name,
  #                    description=description,
  #                    action_examples=action_examples)


  def update(self, key1=None, key2=None, value=None):
    if not value:
      raise ChatErrorException(f"Value for {self.data_name} cannot be None.")

    self.data = str(value)
