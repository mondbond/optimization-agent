from models.task.datamodel.abstract_data_model import AbstractDataModel
from models.task.datamodel.transportation_data_model import \
  TransportationDataModel
from src.models.enums.optimization_type import OptimizationType
from src.models.task.abstract_optimization_task import AbstractOptimizationTask


class TransportationOptimizationTask(AbstractOptimizationTask):

  @staticmethod
  def prompt_description():
    return "This optimization type need to be selected when users clearly tal about you can clearly detect entities that supply and consume something, and relation between them."

  @staticmethod
  def get_type():
    return OptimizationType.TRANSPORTATION

  @staticmethod
  def get_optimization_data_model():
    return TransportationDataModel.create()
