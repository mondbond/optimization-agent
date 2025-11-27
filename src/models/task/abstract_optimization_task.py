from abc import ABC, abstractmethod

from models.task.datamodel.abstract_data_model import AbstractDataModel
from src.models.enums.optimization_type import OptimizationType
from utils.constans_text import SUB_CLASS_IMPLEMENTATION_ERROR_MSG


class AbstractOptimizationTask(ABC):

    @classmethod
    def description(cls) -> str:
      raise NotImplementedError(SUB_CLASS_IMPLEMENTATION_ERROR_MSG)

    @classmethod
    def get_type(cls) -> OptimizationType:
      raise NotImplementedError(SUB_CLASS_IMPLEMENTATION_ERROR_MSG)

    @staticmethod
    @abstractmethod
    def get_optimization_data_model() -> AbstractDataModel:
      raise NotImplementedError(SUB_CLASS_IMPLEMENTATION_ERROR_MSG)
