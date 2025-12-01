from enum import Enum


class ActionType(Enum):
  """
  Enum representing different types of actions that can be performed on the data model.
  """

  REMOVE = "REMOVE"
  UPDATE = "UPDATE"
  DELETE_ALL = "DELETE_ALL"
