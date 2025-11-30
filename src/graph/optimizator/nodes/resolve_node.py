from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from models.enums.optimization_type import OptimizationType

from src.services.mcp_service import optimisation_mcp_service


async def resolve_node(state : OptimizatorAgentState):
    # todo error handling

    result = None
    if state['optimization_task_type'] == OptimizationType.TRANSPORTATION:
      result = await optimisation_mcp_service.calculate_transportation(state.get('optimization_data_model').to_mcp_dict())
    else:
      result = await optimisation_mcp_service.calculate_blending(state.get('optimization_data_model').to_mcp_dict())


    return {
        'agent_message' : str(result)
    }
