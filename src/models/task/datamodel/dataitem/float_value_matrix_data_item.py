from pydantic import BaseModel

from models.exceptions.chat_error_exception import ChatErrorException
from models.task.datamodel.dataitem.data_item import AbstractDataItem
from pydantic import BaseModel, Field
from typing import Any, Dict

class FloatValueMatrixDataItem(BaseModel):

  MATRIX_FLOAT_CLASS : str = "FloatValueMatrixDataItem"

  data: Any = Field(default={})
  data_name : str = Field()
  description : str = Field()
  action_examples : str = Field()
  # def __init__(self, data_name: str, description: str, action_examples: str):
  #   super().__init__(data={},
  #                    data_name=data_name,
  #                    description=description,
  #                    action_examples=action_examples)

  def update(self, key1=None, key2=None, value=None):
    if not key1:
      raise ChatErrorException(f"Problem with updating data {self.data_name}")

    if not key2:
      raise ChatErrorException(f"Problem with updating data {self.data_name} with {key1}")


    value_to_insert = None
    try:
      if not value:
        value = 0.0
      value_to_insert = float(value)
    except Exception:
      raise ChatErrorException(f"Value for {self.data_name}  {key1}  {key2} must be a float number.")

    if key1 not in self.data:
      self.data[key1] = {}

    self.data[key1][key2] = value_to_insert

