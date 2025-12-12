from models.task.datamodel.abstract_data_model import AbstractDataModel
from models.task.datamodel.transportation_data_model import \
  TransportationDataModel
from src.models.enums.optimization_type import OptimizationType
from src.models.task.abstract_optimization_task import AbstractOptimizationTask


class TransportationOptimizationTask(AbstractOptimizationTask):

  @staticmethod
  def prompt_description():
    return "Need to be selected when related when entities that supply and consume something and relation between them are detected. And the goal is to optimize relation between them only"

  @staticmethod
  def get_type():
    return OptimizationType.TRANSPORTATION

  @staticmethod
  def get_optimization_data_model():
    return TransportationDataModel.create()
