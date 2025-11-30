from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

class MatrixDataItem(BaseModel):

  data : dict[str, dict[str, int]] = Field()
  data_name : str = Field()
  data_type : str = Field()
  description : str = Field()
  action_examples : str = Field()

  def update(self, key1 = None, key2 = None, value = None):
    self.data[key1] = value

    if key2:
      self.data[key1][key2] = value

  @property
  def data(self) -> dict:
    return self.data

  @property
  def name(self):
    return self.data_name

  @property
  def description(self):
    return self.description

  @property
  def action_examples(self):
    return self.action_examples



