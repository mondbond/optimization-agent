from graph.data_collection.state.data_collection_state import \
  DataPopulationState
from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from models.enums.optimization_type import OptimizationType
from models.exceptions.agent_failed_exception import AgentFailedException
from models.model_validation import ConversationInstructions
from services.llm_services.data_collection_service import \
  RespondUserWithErrorsService
from utils.constants import REGISTERED_TASKS
from src.graph.data_collection.data_collection_agent import data_collection_agent


def data_collection_orhestrator(state: OptimizatorAgentState):
  """
  Orchestrator node for data collection process in optimization agent.
  It manages the flow of data collection, validation, and user confirmation in scope of data collection subgraph.
  """

  if state.get('confirmation_stage'):
    state['confirmation_stage'] = None
    return {
      'route': 'next',
    }

  action_history_parse_deep = 1
  model_validation = ConversationInstructions.create_empty()

  if __is_task_just_defined(state):
    action_history_parse_deep = 3
    state['optimization_data_model'] = __get_data_model(
        state['optimization_task_type'])
    model_validation.add_prompt_instructions([f"User has just defined the optimization task type. {state['optimization_task_type'].value}"])

  data_collection_state : DataPopulationState = data_collection_agent.run(state['history'], state['optimization_data_model'], model_validation)

  if data_collection_state.get('model_validation').is_data_model_comlete:
    state['confirmation_stage'] = True
    data_collection_state['model_validation'].add_prompt_instructions(['Ask user to confirm the collected data before proceeding to optimization.'])
    data_collection_state['model_validation'].add_after_answer_injections([state['optimization_data_model'].get_model_summary()])

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


def __is_task_just_defined(state):
  return not state.get('optimization_data_model')


def __get_data_model(type: OptimizationType):
  for task in REGISTERED_TASKS:
    if task.get_type().value == type.value:
      return task.get_optimization_data_model()

  raise AgentFailedException("Failed to get data model for task type: "
                  f"{type.value}")
