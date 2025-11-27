from abc import ABC, abstractmethod

from src.graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState


class AbstractLlmTaskService(ABC):

  @staticmethod
  @abstractmethod
  async def invoke(self, state: OptimizatorAgentState):
    pass
