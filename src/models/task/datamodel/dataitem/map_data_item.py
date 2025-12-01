from typing import Any

from pydantic import BaseModel, Field

from models.exceptions.chat_error_exception import DataPopulationError


class MapWithFloatValueDataItem(BaseModel):
  """
  Represents a data item that holds a map (dictionary) of float values.
  Each key in the map is associated with a float number.
  """

  MAP_WITH_FLOAT: str = "MAP_WITH_FLOAT"

  data: Any = Field(default={})
  data_name: str = Field()
  description: str = Field()
  action_examples: str = Field()

  def update(self, key1=None, key2=None, value=None):
    if not key1:
      raise DataPopulationError(f"Problem with updating data {self.data_name}")

    if not value:
      value = 0.0

    try:
      self.data[key1] = float(value)
    except Exception:
      raise DataPopulationError(
          f"Value for {self.data_name} {key1} must be a float number."
      )
