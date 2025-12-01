from enum import Enum


class LlmPurpose(Enum):
  """
  Enumeration of purposes for LLM needed for application.
  """

  DEFAULT = "DEFAULT"
  REASONING = "REASONING"
  SUMMARY = "SUMMARY"
