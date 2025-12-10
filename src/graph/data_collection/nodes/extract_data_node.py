from graph.data_collection.state.data_collection_state import \
  DataPopulationState
from models.enums.action_type import ActionType
from models.structured_output.action_extractors import ExtractionActionList
from services.llm_services.extract_actions_service import \
  ExtractActionTaskService
from src.utils.logger import logger


def extract_data(state: DataPopulationState):
  """
  First step of data collection subgraph process.
  Extract data collection actions from the conversation history and optimization data model.

  It breaks the flow instantly if user requests to delete all data or no actions were extracted.
  Otherwise, it routes to the next step of data model population.
  """
  action_list: ExtractionActionList = ExtractActionTaskService.invoke(
      state['history'], state['optimization_data_model'],
      state.get('optimization_data_model').already_existed_entities(),
      max_turns=1)

  if len(action_list.tasks) == 0:
    state['model_validation'].add_prompt_missed_data_instructions(
        ["No actions were extracted from the user input. Tell him to be more specific if the conversation history is not chatting."])
    return {
      'route': 'validation',
      'model_validation': state['model_validation'],
      'data_collection_actions': action_list
    }
  elif __is_user_wants_to_delete_all_data(action_list):
    state['model_validation'].add_prompt_instructions(
        ["All data has been deleted by user's request. Starting over."])
    return {
      'route': 'answer',
      'model_validation': state['model_validation'],
      'is_need_to_delete_all_data': True,
    }
  else:
    logger.info(f"Extracted actions: {action_list.tasks}")

    return {
      'route': 'next',
      'data_collection_actions': action_list
    }


def __is_user_wants_to_delete_all_data(action_list: ExtractionActionList):
  for extracted_action in action_list.tasks:
    if extracted_action.action == ActionType.DELETE_ALL:
      logger.info("User requested to delete all data.")
      return True
  return False
