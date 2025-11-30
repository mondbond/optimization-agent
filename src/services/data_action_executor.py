from models.exceptions.chat_error_exception import ChatErrorException
from models.model_validation import ModelValidation
from models.structured_output.action_extractors import ExtractionActionList
from models.task.datamodel.abstract_data_model import AbstractDataModel


class DataActionExecutor:

    @staticmethod
    def execute(action_list : ExtractionActionList, model : AbstractDataModel) -> ModelValidation:
      try:
        for action in action_list.tasks:
            model.update_with_action(action)
      except ChatErrorException as e:
        return ModelValidation(rules_for_prompt=[e.get_rule()], rules_for_injections=None)

      return ModelValidation(rules_for_injections=None, rules_for_prompt=None)
