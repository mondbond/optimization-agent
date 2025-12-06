

class ModelValidationInstructions:
  """
  ModelValidation holds the instructions for the model llm to validate and speak with user about issues in the model.
  """



  def __init__(self):
    self._rules_for_prompt = []
    self._rules_for_injections = []
    self._rules_for_orders = []


  def populate(self, model_validation: 'ModelValidationInstructions'):
    self._rules_for_prompt.extend(model_validation.rules_for_prompt)
    self._rules_for_injections.extend(model_validation.rules_for_injections)
    self._rules_for_orders.extend(model_validation.rules_for_orders)


  @property
  def all_instructions(self) -> list[str]:
    return self._rules_for_orders + self._rules_for_prompt

  @property
  def rules_for_prompt(self) -> list[str]:
    return self._rules_for_prompt

  @property
  def rules_for_injections(self) -> list[str]:
    return self._rules_for_injections

  @property
  def rules_for_orders(self) -> list[str]:
    return self._rules_for_orders

  @property
  def is_valid(self) -> bool:
    if self._rules_for_prompt is None or  len(self._rules_for_prompt) == 0:
      return True

    return False

  def add_injections(self, injections: list[str]):
    self._rules_for_injections.extend(injections)

  def add_orders(self, orders: list[str]):
    self._rules_for_orders.extend(orders)

  def append_instructions(self, instructions: list[str]):
    self._rules_for_prompt.extend(instructions)

  @staticmethod
  def create_valid():
    return ModelValidationInstructions()
