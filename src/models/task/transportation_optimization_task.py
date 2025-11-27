from models.task.datamodel.abstract_data_model import AbstractDataModel
from models.task.datamodel.transportation_data_model import \
  TransportationDataModel
from src.models.task.abstract_optimization_task import AbstractOptimizationTask
from src.models.enums.optimization_type import OptimizationType


class TransportationOptimizationTask(AbstractOptimizationTask):

  @classmethod
  def description(cls):
    return "This optimization type need to be choosen when you can clearly detect entities that supply and entities that can consume from suppliers."

  @classmethod
  def get_type(cls):
    return OptimizationType.TRANSPORTATION

  @staticmethod
  def get_optimization_data_model() -> AbstractDataModel:
    return TransportationDataModel.create()
