from abc import ABC, abstractmethod
from typing import Any, Dict

from pydantic import BaseModel, Field


class AbstractDataItem(ABC, BaseModel):
  # data: Any = Field(default=None)
  data_name: str = Field()
  description: str = Field()
  action_examples: str = Field()

  @abstractmethod
  def update(self, key1=None, key2=None, value=None):
    pass
