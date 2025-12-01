from enum import Enum


class OptimizationType(Enum):
  """
  Enum representing different types of optimization tasks.
  """

  TRANSPORTATION = "TRANSPORTATION"
  BLENDING = "BLENDING"
  NONE = "NONE"
