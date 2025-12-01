from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from models.enums.action_type import ActionType
from models.enums.optimization_type import OptimizationType
from models.model_validation import ModelValidationInstructions
from models.structured_output.action_extractors import ExtractionActionList
from services.data_action_executor import DataModelPopulationService
from services.llm_services.data_collection_service import \
  RespondUserWithErrorsService
from services.llm_services.extract_actions_service import \
  ExtractActionTaskService
from utils.constants import REGISTERED_TASKS
from src.utils.logger import logger


def data_collection_node(state: OptimizatorAgentState):
  if state.get('confirmation_stage'):
    state['confirmation_stage'] = None
    return {
      'route': 'next',
    }

  history_deep_focus = 1
  if is_task_just_defined(state):
    state['optimization_data_model'] = get_data_model(
        state['optimization_task_type'])
    return {
      'route': 'answer',
      'agent_message': "Great! Let's start collecting the necessary data for your optimization task.",
      'optimization_data_model': state['optimization_data_model'],
      'optimization_task_type': state['optimization_task_type']
    }

  action_list: ExtractionActionList = ExtractActionTaskService.invoke(
      state['history'], state['optimization_data_model'], state.get('optimization_data_model').already_existed_entities(),
      max_turns=history_deep_focus)

  logger.info(f"Extracted actions: {action_list.tasks}")

  if is_user_wants_to_delete_all_data(action_list):
    clear_task_related_data(state)
    return {
      'route': 'answer',
      'agent_message': "All data has been deleted. Let's start over.",
      'optimization_data_model': state['optimization_data_model'],
      'optimization_task_type': state['optimization_task_type']
    }

  instructions: ModelValidationInstructions = populate_and_validate_data_model(state,
                                                                                    action_list)
  if instructions.is_valid:
    return {
      'route': 'answer',
      'agent_message': 'Data collection completed successfully. Are you ready to proceed to optimization?' +
                       state['optimization_data_model'].get_model_summary(),
      'confirmation_stage': True,
      'optimization_data_model': state['optimization_data_model'],
      'optimization_task_type': state['optimization_task_type']
    }
  else:
    return {
      'route': 'answer',
      'agent_message': RespondUserWithErrorsService.invoke(state['history'],
                                                           instructions),
      'optimization_data_model': state['optimization_data_model'],
      'optimization_task_type': state['optimization_task_type']
    }


def populate_and_validate_data_model(state,
    action_list: ExtractionActionList) -> ModelValidationInstructions:
  validation_rules_during_population: ModelValidationInstructions = DataModelPopulationService.execute(
    action_list, state[
        'optimization_data_model'])

  if not validation_rules_during_population.is_valid:
    logger.info("Data model population resulted in validation errors.")
    return validation_rules_during_population

  model_validation_rules: ModelValidationInstructions = (state['optimization_data_model']
                                                         .validate_model_with_instruction())
  if not model_validation_rules.is_valid:
    logger.info("Data model validation after population resulted in errors.")
    return model_validation_rules

  return ModelValidationInstructions.valid()


def clear_task_related_data(state):
  state['optimization_data_model'] = None
  state['optimization_task_type'] = None


def is_task_just_defined(state):
  return not state.get('optimization_data_model')


def get_data_model(type: OptimizationType):
  for task in REGISTERED_TASKS:
    if task.get_type().value == type.value:
      return task.get_optimization_data_model()

  raise Exception("Failed to get data model for task type: "
                  f"{type.value}")


def is_user_wants_to_delete_all_data(action_list: ExtractionActionList):
  for action in action_list.tasks:
    if action == ActionType.DELETE_ALL:
      logger.info("User requested to delete all data.")
      return True
  return False
