from langchain_core.messages import AIMessage

from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState


def answer_node(state: OptimizatorAgentState):
  """
  Node to generate the final answer from the agent's message.
  It retrieves the agent's message from the state and formats it into a response structure.
  """
  agent_response = state.get('agent_message')
  state['agent_message'] = None

  return {
    "history": [AIMessage(agent_response)],
  }
