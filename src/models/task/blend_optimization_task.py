from models.task.datamodel.blend_data_model import BlendDataModel
from src.models.enums.optimization_type import OptimizationType
from src.models.task.abstract_optimization_task import AbstractOptimizationTask


class BlendOptimizationTask(AbstractOptimizationTask):
  """
  Optimization task type for blending optimization problems.
  """

  @staticmethod
  def prompt_description():
    return "This need to be selected when components or ingredients like entities can be detected and the goal is to create a new product by mixing them in certain proportions only."

  @staticmethod
  def get_type():
    return OptimizationType.BLENDING

  @staticmethod
  def get_optimization_data_model():
    return BlendDataModel.create()
