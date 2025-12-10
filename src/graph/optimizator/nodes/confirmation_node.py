from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from models.enums.confirmation_action import Confirmation
from services.llm_services.confirmation_service import DataConfirmationService


def get_user_confirmation(state: OptimizatorAgentState):
  """
  Node to handle user confirmation for the collected data.
  It uses a confirmation service to analyze the conversation history and determine if the user confirms the data.
  Depending on the confirmation result, it routes to either re-ask for data changes or proceed
  """

  confirmation: Confirmation = DataConfirmationService.invoke(state.get('history'))

  if confirmation == Confirmation.REJECTED:
    return {
      'route': 'answer',
      'agent_message': 'How would you like to change the provided data for optimization? Please specify.',
      'confirmation_stage': False,
    }

  else:
    return {
      'route': 'next',
    }
