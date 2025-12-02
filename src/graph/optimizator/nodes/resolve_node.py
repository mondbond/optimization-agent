from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from models.enums.optimization_type import OptimizationType
from services.transportation_solution_answer_service import \
  TransportationSolutionAnswerService
from src.services.mcp_service import optimisation_mcp_service


async def solve_node(state : OptimizatorAgentState):
    # todo error handling

    result = None
    if state['optimization_task_type'].name == OptimizationType.TRANSPORTATION.name:
      solver_ouput = await optimisation_mcp_service.calculate_transportation(state.get('optimization_data_model').to_mcp_dict())

      result = TransportationSolutionAnswerService.get_transportation_solution_answer(solver_ouput)

    else:
      result = await optimisation_mcp_service.calculate_blending(state.get('optimization_data_model').to_mcp_dict())


    return {
      'agent_message' : str(result),
      'optimization_data_model': None,
      'optimization_task_type': None
    }
