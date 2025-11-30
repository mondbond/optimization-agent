from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState

from src.services.mcp_service import optimisation_mcp_service


async def resolve_node(state : OptimizatorAgentState):
    # todo error handling

    result = await optimisation_mcp_service.calculate_transportation(state.get('optimization_data_model').to_mcp_dict())


    return {
        'agent_message' : str(result)
    }
