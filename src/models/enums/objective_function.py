from enum import Enum


class ObjectiveFunction(Enum):
  """
  Enum representing different types of objective functions for optimization.
  """
  MINIMUM = "minimum"
  MAXIMUM = "maximum"
