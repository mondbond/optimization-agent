from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Any

class DataItem(BaseModel):

  data: Any = Field(default=None)
  data_name : str = Field()
  data_type : str = Field()
  value_type : str = Field()
  description : str = Field()
  action_examples : str = Field()

  def update(self, key1 = None, key2 = None, value = None):

    if self.data_type == 'string':
      self.data = str(value)
      return


    if self.data_type == 'map':
      if not value:
        self.data[key1] = 0.0
      else:
        self.data[key1] = float(value)
      return


    if self.data_type == 'matrix':
      if key2:
        if key1 not in self.data:
          self.data[key1] = {}
        if not value:
          self.data[key1][key2] = 0.0
        else:
          self.data[key1] = float(value)
        return

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



