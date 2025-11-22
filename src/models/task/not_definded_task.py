from src.models.task.abstract_optimization_task import AbstractOptimizationTask
from src.models.enums.optimization_type import OptimizationType


class NotDefinedOptimizationTask(AbstractOptimizationTask):

  @classmethod
  def description(cls):
    return "This optimization type need to be choosen when it is not possible to clearly detect optimization goal. In this case, no specific optimization will be applied."

  @classmethod
  def get_type(cls):
    return OptimizationType.NONE

  def get_steps(self):
    return None
