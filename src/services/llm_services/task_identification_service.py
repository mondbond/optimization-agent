from langchain_core.messages import AnyMessage
from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_provider import get_llm
from src.models.structured_output.optimization_task_resolver import \
  OptimizationTaskResolver
from src.services.history_limitation_service import HistoryLimitationService
from src.services.task_descriptors_service import TaskDescriptorService
from src.utils.prompt_manager import prompt_manager


class TaskExtractionService:
  """
  LLM Service to extract the optimization task type from user messages.
  """

  @staticmethod
  def invoke(history: list[AnyMessage]):
    task_descriptions = TaskDescriptorService.get_task_descriptions_for_prompt()

    history = HistoryLimitationService.dialog_turn_limiter(history,
                                                           max_turns=10)

    prompt_text = prompt_manager.get_prompt('optimization_task_resolver')

    llm = get_llm().with_structured_output(OptimizationTaskResolver)

    prompt = ChatPromptTemplate.from_messages([
      ("human", prompt_text)
    ])

    chain = prompt | llm
    task_resolver: OptimizationTaskResolver = chain.invoke({
      "history": history,
      "optimization_task_descriptions": task_descriptions
    })

    return task_resolver.type
