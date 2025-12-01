from models.exceptions.chat_error_exception import DataPopulationError
from models.model_validation import ModelValidationInstructions
from models.structured_output.action_extractors import ExtractionActionList


class DataModelPopulationService:
  """
    Service responsible for executing data population actions on the optimization data model.
    In case of data population errors, it captures the exception and returns a ModelValidation
    object containing the relevant instructions for prompt generation.
  """

  @staticmethod
  def execute(action_list: ExtractionActionList, model) -> ModelValidationInstructions:
    try:
      for action in action_list.tasks:
        model.update_with_action(action)
    except DataPopulationError as e:
      return ModelValidationInstructions(rules_for_prompt=[e.get_rule()],
                                         rules_for_injections=None)

    return ModelValidationInstructions(rules_for_injections=None, rules_for_prompt=None)
