from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from models.enums.optimization_type import OptimizationType
from services.adapters.blending_task_optimisation_mcp_adapter import \
  BlendingTaskOptimisationMcpAdapter
from services.adapters.transportation_task_optimisation_mcp_adapter import \
  TransportationTaskOptimisationMcpAdapter
from src.services.mcp_service import optimisation_mcp_service
from src.utils.logger import logger


async def solve_node(state: OptimizatorAgentState):
  """
  Node to solve the optimization task based on the collected data.
  It determines the type of optimization task and invokes the appropriate service to perform the optimization.
  """

  result = None
  if state['optimization_task_type'].name == OptimizationType.TRANSPORTATION.name:
    input_data = TransportationTaskOptimisationMcpAdapter.to_mcp_dict(
        state.get('optimization_data_model'))

    solver_output = await optimisation_mcp_service.calculate_transportation(
      input_data)

    result = TransportationTaskOptimisationMcpAdapter.result_to_answer(
      solver_output)

  else:
    input_data = BlendingTaskOptimisationMcpAdapter.to_mcp_dict(
        state.get('optimization_data_model'))


    solver_output = await optimisation_mcp_service.calculate_blending(input_data)
    logger.warning(result)

    result = BlendingTaskOptimisationMcpAdapter.result_to_answer(
        solver_output)

  return {
    'agent_message': str(result),
    'optimization_data_model': None,
    'optimization_task_type': None
  }
