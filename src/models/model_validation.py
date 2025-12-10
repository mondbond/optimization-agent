class ConversationInstructions:
  """
  Stack for collecting all instructions for answer to a user prompt.
  It contains:

    - prompt_instructions.
    General instructions to be added to the prompt before answering.
    It can relate to style, format, tone of the answer, etc.
    Example:
    Tell to the user that all needed data has been collected and you are ready to provide the final answer.


    - prompt_missed_data_instructions.
    Instructions about missing data to be added to the prompt before answering.
    They are stored separately for a quick check on data model completeness via is_valid property.
    Example:
    The following data is missing: <list of missing data>.


    - after_answer_injections.
    Instructions to be injected after the answer of LLM is generated.
    Used to pregenerated text that should be added after the LLM answer in order
    to provide some information that is not needed to be processed by LLM in order to save the token count.
  """

  def __init__(self):
    self.__prompt_instructions = []
    self.__prompt_missed_data_instructions = []
    self.__after_answer_injections = []

  @staticmethod
  def create_empty():
    return ConversationInstructions()


  def merge_with(self, model_validation: 'ConversationInstructions'):
    self.__prompt_missed_data_instructions.extend(model_validation.missed_data)
    self.__after_answer_injections.extend(
      model_validation.after_answer_injections)
    self.__prompt_instructions.extend(model_validation.prompt_instructions)

  @property
  def all_instructions(self) -> list[str]:
    return self.__prompt_instructions + self.__prompt_missed_data_instructions

  @property
  def missed_data(self) -> list[str]:
    return self.__prompt_missed_data_instructions

  @property
  def after_answer_injections(self) -> list[str]:
    return self.__after_answer_injections

  @property
  def prompt_instructions(self) -> list[str]:
    return self.__prompt_instructions

  @property
  def is_data_model_comlete(self) -> bool:
    if self.__prompt_missed_data_instructions is None or len(
        self.__prompt_missed_data_instructions) == 0:
      return True

    return False

  def add_after_answer_injections(self, injections: list[str]):
    self.__after_answer_injections.extend(injections)

  def add_prompt_instructions(self, orders: list[str]):
    self.__prompt_instructions.extend(orders)

  def add_prompt_missed_data_instructions(self, instructions: list[str]):
    self.__prompt_missed_data_instructions.extend(instructions)
