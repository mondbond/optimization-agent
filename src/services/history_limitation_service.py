from langchain.messages import AnyMessage


class HistoryLimitationService:
  """
  Service to limit the dialog history for LLM prompts with window cut.
  """

  @classmethod
  def dialog_turn_limiter(cls, history: list[AnyMessage], max_turns=10) -> str:
    """
    Method to limit the dialog history for LLM prompts with window cut.
    :return formated dialog history into a proper string representation.
    """
    return cls.represent_dialog_format(history[-max_turns:])

  @classmethod
  def represent_dialog_format(cls, history: list[AnyMessage]) -> str:
    dialog_representation = ""
    for message in history:
      if message.type == "human":
        dialog_representation += f"Human: {message.content}\n"
      elif message.type == "ai":
        dialog_representation += f"AI: {message.content}\n"
    return dialog_representation.strip()
