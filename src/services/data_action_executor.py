from models.structured_output.action_extractors import ExtractionActionList
from models.task.datamodel.abstract_data_model import AbstractDataModel


class DataActionExecutor:

    @staticmethod
    def execute(action_list : ExtractionActionList, model : AbstractDataModel):
        for action in action_list.tasks:
            model.update_with_action(action)
