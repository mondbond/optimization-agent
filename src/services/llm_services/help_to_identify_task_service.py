from langchain_core.messages import AnyMessage
from langchain_core.prompts import ChatPromptTemplate

from models.task.abstract_optimization_task import AbstractOptimizationTask
from services.task_descriptors_service import TaskDescriptorService
from src.llm.llm_provider import get_llm
from src.services.history_limitation_service import HistoryLimitationService
from src.utils.prompt_manager import prompt_manager


class TaskTypeIdentificationHelpAnswerService:
  """
  LLM Service for chatting with user in case the optimization task is not yet defined.
  Service generate the message for chatting and specifying detail questions to help user define the optimization task.
  """

  @staticmethod
  def invoke(history: list[AnyMessage]):
    task_descriptions = TaskDescriptorService.get_task_descriptions_for_prompt()

    history = HistoryLimitationService.dialog_turn_limiter(history,
                                                           max_turns=10)
    help_answer_prompt = prompt_manager['task_identification_help']

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
      ("human", help_answer_prompt)
    ])

    chain = prompt | llm
    answer = chain.invoke({
      "history": history,
      "optimization_task_descriptions": task_descriptions
    })

    return answer.content

  def extract_existing_task_descriptions(self,
      registered_tasks: list[AbstractOptimizationTask]) -> str:
    messages = []
    for task in registered_tasks:
      msg = f"Type: {task.get_type().value}, Description: {task.prompt_description()} \n"
      messages.append(msg)
    task_descriptions = "".join(messages)
    return task_descriptions
