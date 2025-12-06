from graph.data_collection.state.data_collection_state import \
  DataPopulationState
from models.exceptions.chat_error_exception import DataPopulationError
from models.model_validation import ModelValidationInstructions
from models.structured_output.action_extractors import ExtractionActionList
from models.task.datamodel.abstract_data_model import AbstractDataModel
from services.data_action_executor import DataModelPopulationService
from src.utils.logger import logger


def data_model_population(state: DataPopulationState):
  try:
   __populate_and_validate_data_model(state['optimization_data_model'], state['data_collection_actions'])
  except DataPopulationError as e:
    logger.error(f"Error during action extraction: {str(e)}")

    state['model_validation'].append_instructions(
        [e.get_instruction()])
    return {
      'route': 'answer',
      'model_validation': state['model_validation'],
    }

  return {
    'route': 'next',
    'optimization_data_model': state['optimization_data_model'],
  }

def __populate_and_validate_data_model(data_model: AbstractDataModel, action_list: ExtractionActionList) -> ModelValidationInstructions:
  validation_rules_during_population: ModelValidationInstructions = DataModelPopulationService.execute(
      action_list, data_model)

  return validation_rules_during_population
