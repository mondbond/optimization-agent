from abc import ABC, abstractmethod

from src.graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState


# todo reomove
class AbstractLlmTaskService(ABC):

  @staticmethod
  @abstractmethod
  async def invoke(self, *args, **kwargs) -> OptimizatorAgentState:
    pass
