from abc import ABC, abstractmethod
from src.models.enums.optimization_type import OptimizationType
from utils.constans_text import SUB_CLASS_IMPLEMENTATION_ERROR_MSG


class AbstractOptimizationTask(ABC):

    @classmethod
    def description(cls) -> str:
      raise NotImplementedError(SUB_CLASS_IMPLEMENTATION_ERROR_MSG)

    @classmethod
    def get_type(cls) -> OptimizationType:
      raise NotImplementedError(SUB_CLASS_IMPLEMENTATION_ERROR_MSG)

    @abstractmethod
    def get_steps(cls) -> list:
      raise NotImplementedError(SUB_CLASS_IMPLEMENTATION_ERROR_MSG)
