

class ModelValidationInstructions:
  """
  ModelValidation holds the instructions for the model llm to validate and speak with user about issues in the model.
  """

  def __init__(self, rules_for_prompt : list[str] | None, rules_for_injections: list[str] | None):
    self._rules_for_prompt = rules_for_prompt
    self._rules_for_injections = rules_for_injections


  @property
  def rules_for_prompt(self) -> list[str]:
    return self._rules_for_prompt

  @property
  def rules_for_injections(self) -> list[str]:
    return self._rules_for_injections

  @property
  def is_valid(self) -> bool:
    if self._rules_for_prompt is None and self._rules_for_injections is None:
      return True

    return False

  def append_instructions(self, instructions: list[str]):
    self._rules_for_prompt.extend(instructions)

  @staticmethod
  def valid():
    return ModelValidationInstructions(None, None)
