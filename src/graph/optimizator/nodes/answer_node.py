from langchain_core.messages import AIMessage

from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState


def answer_node(state: OptimizatorAgentState):
  agent_response = state.get('agent_message')
  state['agent_message'] = None

  return {
    "history": [AIMessage(agent_response)],
  }
