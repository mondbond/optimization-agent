from models.task.datamodel.blend_data_model import BlendDataModel
from src.models.enums.optimization_type import OptimizationType
from src.models.task.abstract_optimization_task import AbstractOptimizationTask


class BlendOptimizationTask(AbstractOptimizationTask):
  """
  Optimization task type for blending optimization problems.
  """

  @staticmethod
  def prompt_description():
    return "This optimization type need to be selected when you can clearly detect entities that mixing/blending together can produce a new entities/products"

  @staticmethod
  def get_type():
    return OptimizationType.BLENDING

  @staticmethod
  def get_optimization_data_model():
    return BlendDataModel.create()
