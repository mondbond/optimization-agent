from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState


def repeat_node(state : OptimizatorAgentState):
    answer = state['optimization_data_model'].get_model_summary()

    return {
        'route' : 'answer',
        'agent_message' : answer
    }
