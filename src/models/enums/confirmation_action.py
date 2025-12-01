from enum import Enum


class Confirmation(Enum):
  """
  Enum representing confirmation actions by user on already validated model.
  """

  CONFIRMED = "CONFIRMED"
  REJECTED = "REJECTED"
