from models.task.not_definded_task import NotDefinedOptimizationTask
from models.task.blend_optimization_task import BlendOptimizationTask
from models.task.transportation_optimization_task import \
  TransportationOptimizationTask
from utils.constants import REGISTERED_TASKS


class TaskDescriptorService:


  @classmethod
  def get_task_descriptions_for_prompt(cls):

    messages = []
    for task in REGISTERED_TASKS:
      msg = f"Type: {task.get_type().value}, Description: {task.description()} \n"
      messages.append(msg)
    task_descriptions = "".join(messages)
    return task_descriptions
