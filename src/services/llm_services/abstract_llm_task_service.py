from abc import ABC, abstractmethod

from src.graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState


class AbstractLlmTaskService(ABC):

  @abstractmethod
  async def invokde(self, state: OptimizatorAgentState):
    pass
