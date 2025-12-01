from models.exceptions.agent_failed_exception import AgentFailedException
from src.models.enums.optimization_type import OptimizationType
from src.models.task.abstract_optimization_task import AbstractOptimizationTask


class NotDefinedOptimizationTask(AbstractOptimizationTask):

  @staticmethod
  def prompt_description():
    return "This optimization type need to be choosen when it is not possible to clearly detect optimization goal. In this case, no specific optimization will be applied."

  @staticmethod
  def get_type():
    return OptimizationType.NONE

  @staticmethod
  def get_optimization_data_model():
    raise AgentFailedException("Empty type has no task implementation and can not be choosen")
