from typing import Any

from pydantic import BaseModel, Field

from models.exceptions.chat_error_exception import DataPopulationError
from models.task.datamodel.dataitem.data_item import AbstractDataItem
from typing import Any, Dict


class FloatValueMatrixDataItem(AbstractDataItem):
  """
  Represents a data item that holds a matrix of float values.
  The matrix is structured as a nested dictionary, where the first-level keys
  represent row identifiers and the second-level keys represent column identifiers.
  Each value in the matrix is a float number.
  """

  MATRIX_FLOAT_CLASS: str = "FloatValueMatrixDataItem"

  data: Dict[str, Dict[str, float]] = Field(default={})
  data_name: str = Field()
  description: str = Field()
  action_examples: str = Field()

  def update(self, key1=None, key2=None, value=None):
    if not key1:
      raise DataPopulationError(f"Problem with updating data {self.data_name}")

    if not key2:
      raise DataPopulationError(
          f"Problem with updating data {self.data_name} with {key1}")

    value_to_insert = None
    try:
      if not value:
        value = 0.0
      value_to_insert = float(value)
    except Exception:
      raise DataPopulationError(
          f"Value for {self.data_name}  {key1}  {key2} must be a float number.")

    if key1 not in self.data:
      self.data[key1] = {}

    self.data[key1][key2] = value_to_insert
