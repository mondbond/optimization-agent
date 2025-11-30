from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from models.enums.confirmation_action import Confirmation
from models.structured_output.confirmation import ConfirmationAction
from services.llm_services.confirmation_service import DataConfirmationService


def repeat_node(state : OptimizatorAgentState):

    confirmation : Confirmation = DataConfirmationService.invoke(state['history'])

    if confirmation == Confirmation.REJECTED:

      return {
        'route' : 'answer',
        'agent_message' : 'How would you like to change the provided data for optimization? Please specify.',
        'confirmation_stage' : False,
      }
    else:
      return {
        'route' : 'next',
      }

