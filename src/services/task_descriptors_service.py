from utils.constants import REGISTERED_TASKS


class TaskDescriptorService:
  """
  Goal of this service is to collect descriptions for all registered tasks in the system.
  This is used to inform LLMs about the available tasks.
  """

  @classmethod
  def get_task_descriptions_for_prompt(cls):
    messages = []
    for task in REGISTERED_TASKS:
      msg = f"Type: {task.get_type().value} \nDescription: {task.description()} \n"
      messages.append(msg)
    task_descriptions = "".join(messages)
    return task_descriptions
