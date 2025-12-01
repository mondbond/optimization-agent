from abc import ABC, abstractmethod

from models.task.datamodel.abstract_data_model import AbstractDataModel
from src.models.enums.optimization_type import OptimizationType


class AbstractOptimizationTask(ABC):
  """
  Abstract class for optimization task types.
  Each optimization task type must implement methods to provide its description,
  type, and associated data model.
  It helps to iterate through registered tasks, extract their description for prompt injection.
  """

  @staticmethod
  @abstractmethod
  def description() -> str:
    """
    Provides a description of the optimization task type for later use in prompt injection.
    :return: description string
    """
    pass

  @staticmethod
  @abstractmethod
  def get_type() -> OptimizationType:
    """
    Returns the optimization type enum value associated with this task fot iterative match of the type.
    :return: OptimizationType enum value
    """
    pass

  @staticmethod
  @abstractmethod
  def get_optimization_data_model():
    """
    Returns the instance of data model handler class associated with this optimization task type.
    :return: Data model hendler
    """
    pass
