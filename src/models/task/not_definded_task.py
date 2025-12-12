from models.exceptions.agent_failed_exception import AgentFailedException
from src.models.enums.optimization_type import OptimizationType
from src.models.task.abstract_optimization_task import AbstractOptimizationTask


class NotDefinedOptimizationTask(AbstractOptimizationTask):

  @staticmethod
  def prompt_description():
    return "need to be selected when nothing ele fit or several optimization types can be possible at the same time from users conversation"

  @staticmethod
  def get_type():
    return OptimizationType.NONE

  @staticmethod
  def get_optimization_data_model():
    raise AgentFailedException("Empty type has no task implementation and can not be selected")
