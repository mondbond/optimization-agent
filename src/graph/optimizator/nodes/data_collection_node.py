from graph.data_collection.state.data_collection_state import \
  DataPopulationState
from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from models.enums.action_type import ActionType
from models.enums.optimization_type import OptimizationType
from models.exceptions.agent_failed_exception import AgentFailedException
from models.exceptions.chat_error_exception import DataPopulationError
from models.model_validation import ModelValidationInstructions
from models.structured_output.action_extractors import ExtractionActionList
from services.data_action_executor import DataModelPopulationService
from services.llm_services.data_collection_service import \
  RespondUserWithErrorsService
from services.llm_services.extract_actions_service import \
  ExtractActionTaskService
from utils.constants import REGISTERED_TASKS
from src.utils.logger import logger
from src.graph.data_collection.data_collection_agent import data_collection_agent


def data_collection_orhestrator(state: OptimizatorAgentState):
  if state.get('confirmation_stage'):
    state['confirmation_stage'] = None
    return {
      'route': 'next',
    }

  action_history_parse_deep = 1
  model_validation = ModelValidationInstructions.create_valid()

  if __is_task_just_defined(state):
    action_history_parse_deep = 3
    state['optimization_data_model'] = __get_data_model(
        state['optimization_task_type'])
    model_validation.add_orders([f"User has just defined the optimization task type. {state['optimization_task_type'].value}"])

  data_collection_state : DataPopulationState = data_collection_agent.run(state['history'], state['optimization_data_model'], model_validation)

  if data_collection_state.get('model_validation').is_valid:
    state['confirmation_stage'] = True
    data_collection_state['model_validation'].add_orders(['Ask user to confirm the collected data before proceeding to optimization.'])
    data_collection_state['model_validation'].add_injections([state['optimization_data_model'].get_model_summary()])

  answer = RespondUserWithErrorsService.invoke(state['history'],
                                               data_collection_state['model_validation'])

  if data_collection_state.get('is_need_to_delete_all_data'):
    return {
      'route': 'answer',
      'agent_message': answer,
      'optimization_data_model': None,
      'optimization_task_type': None
    }

  return {
    'route': 'answer',
    'agent_message': answer,
    'confirmation_stage': state.get('confirmation_stage', False),
    'optimization_data_model': state['optimization_data_model'],
    'optimization_task_type': state['optimization_task_type']
  }




# def data_collection_node(state: OptimizatorAgentState):
#   if state.get('confirmation_stage'):
#     state['confirmation_stage'] = None
#     return {
#       'route': 'next',
#     }
#
#   action_history_parse_deep = 1
#   model_validation = ModelValidationInstructions.create_valid()
#
#   if __is_task_just_defined(state):
#     action_history_parse_deep = 3
#     state['optimization_data_model'] = __get_data_model(
#         state['optimization_task_type'])
#
#     model_validation.append_instructions([f"User has just defined the optimization task type. {state['optimization_task_type'].value}"])
#
#     #
#     # return {
#     #   'route': 'answer',
#     #   'agent_message': "Great! Let's start collecting the necessary data for your optimization task.",
#     #   'optimization_data_model': state['optimization_data_model'],
#     #   'optimization_task_type': state['optimization_task_type']
#     # }
#
#   try:
#     action_list: ExtractionActionList = ExtractActionTaskService.invoke(
#       state['history'], state['optimization_data_model'], state.get('optimization_data_model').already_existed_entities(),
#       max_turns=action_history_parse_deep)
#
#     if len(action_list.tasks) == 0:
#       model_validation.append_instructions(["No actions were extracted from the user input. User don't understand what data is required or speaks not according to optimisation task. Explain him better."])
#   except DataPopulationError as e:
#     logger.error(f"Error during action extraction: {str(e)}")
#     return {
#       'route': 'answer',
#       'agent_message': RespondUserWithErrorsService.invoke(state['history'],
#                                                            ModelValidationInstructions([e.get_instruction()])),
#       'optimization_data_model': state['optimization_data_model'],
#       'optimization_task_type': state['optimization_task_type']
#     }
#
#
#   logger.info(f"Extracted actions: {action_list.tasks}")
#
#   if __is_user_wants_to_delete_all_data(action_list):
#     return {
#       'route': 'answer',
#       'agent_message': "All data has been deleted. Let's start over.",
#       'optimization_data_model': None,
#       'optimization_task_type': None
#     }
#
#   model_validation.populate(__populate_and_validate_data_model(state,
#                                                                action_list))
#   if model_validation.is_valid:
#     return {
#       'route': 'answer',
#       'agent_message': 'Data collection completed successfully. Are you ready to proceed to optimization?' +
#                        state['optimization_data_model'].get_model_summary(),
#       'confirmation_stage': True,
#       'optimization_data_model': state['optimization_data_model'],
#       'optimization_task_type': state['optimization_task_type']
#     }
#   else:
#     return {
#       'route': 'answer',
#       'agent_message': RespondUserWithErrorsService.invoke(state['history'],
#                                                            model_validation),
#       'optimization_data_model': state['optimization_data_model'],
#       'optimization_task_type': state['optimization_task_type']
#     }



  if not validation_rules_during_population.is_valid:
    return validation_rules_during_population

  model_validation_rules: ModelValidationInstructions = (state['optimization_data_model']
                                                         .validate_model_with_instruction())
  if not model_validation_rules.is_valid:
    return model_validation_rules

  return ModelValidationInstructions.create_valid()


def __is_task_just_defined(state):
  return not state.get('optimization_data_model')


def __get_data_model(type: OptimizationType):
  for task in REGISTERED_TASKS:
    if task.get_type().value == type.value:
      return task.get_optimization_data_model()

  raise AgentFailedException("Failed to get data model for task type: "
                  f"{type.value}")
