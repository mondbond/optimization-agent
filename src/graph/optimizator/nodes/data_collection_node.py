from langchain_core.messages import HumanMessage, AIMessage

from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from models.enums.action_type import ActionType
from models.model_validation import ModelValidation
from models.structured_output.action_extractors import ExtractionActionList
from models.task.datamodel.transportation_data_model import \
  TransportationDataModel
from services.data_action_executor import DataActionExecutor
from services.llm_services.data_collection_service import DataCollectionService
from services.llm_services.extract_actions_service import \
  ExtractActionTaskService
from services.llm_services.task_identification_service import \
  TaskIdentificationService
from utils.constants import REGISTERED_TASKS


def data_collection_node(state: OptimizatorAgentState):
  # todo rewrite with get
  if state.get('confirmation_stage'):
    state['confirmation_stage'] = None
    return {
      'route' : 'next',
    }


  history_deep_focus = 1
  if not state.get('optimization_data_model'):
    for task in REGISTERED_TASKS:
      if task.get_type().value == state.get('optimization_task_type').value:
        state['optimization_data_model'] = task.get_optimization_data_model()

        return {
          'route' : 'answer',
          'agent_message' : "Great! Let's start collecting the necessary data for your optimization task.",
          'optimization_data_model' : state['optimization_data_model'],
          'optimization_task_type' : state['optimization_task_type']
        }


  action_list : ExtractionActionList = ExtractActionTaskService.invoke(state['history'], state['optimization_data_model'], max_turns=history_deep_focus)
  print("Extracted actions: {}", action_list)

  for action in action_list.tasks:
    if action == ActionType.DELETE_ALL:
      state['optimization_data_model'] = None
      state['optimization_task_type'] = None
      return {
        'route' : 'answer',
        'agent_message' : "All data has been deleted. Let's start over.",
        'optimization_data_model' : state['optimization_data_model'],
        'optimization_task_type' : state['optimization_task_type']
      }

  DataActionExecutor.execute(action_list, state['optimization_data_model'])

  validation : ModelValidation = state['optimization_data_model'].validate_model_with_text_response()
  print("validation: {}", validation)

  if validation.is_valid:
    return {
      'route' : 'answer',
      'agent_message' : 'Data collection completed successfully. Are you ready to proceed to optimization?' + state['optimization_data_model'].get_model_summary(),
      'confirmation_stage' : True,
      'optimization_data_model' : state['optimization_data_model'],
      'optimization_task_type' : state['optimization_task_type']

    }
  else:
    answer = DataCollectionService.invoke(state['history'], validation)

  return {
    'route' : 'answer',
    'agent_message' : answer,
    'optimization_data_model' : state['optimization_data_model'],
    'optimization_task_type' : state['optimization_task_type']
  }


if __name__ == "__main__":
  state = OptimizatorAgentState()

  state['history'] = [
    HumanMessage("I been in Paris last summer."),
    AIMessage("Cool, what about the suppliers?"),
    HumanMessage("SoftServe can supply 400 and Epam can 3243")
  ]

  state["optimization_task_type"] = REGISTERED_TASKS[1].get_type()
  state["optimization_data_model"] = TransportationDataModel()

  result  = data_collection_node(state)

  print(result)
