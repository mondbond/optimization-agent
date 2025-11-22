from models.task.blend_optimization_task import BlendOptimizationTask
from models.task.abstract_optimization_task import AbstractOptimizationTask
from models.task.not_definded_task import NotDefinedOptimizationTask
from models.task.transportation_optimization_task import \
  TransportationOptimizationTask
from services.task_descriptors_service import TaskDescriptorService
from src.graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from src.services.llm_services.abstract_llm_task_service import \
  AbstractLlmTaskService
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage
from langchain_core.prompts import ChatPromptTemplate

from src.graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from src.llm.llm_provider import get_llm
from src.services.history_limitation_service import HistoryLimitationService
from src.utils.prompt_manager import prompt_manager
from src.models.structured_output.optimization_task_resolver import \
  OptimizationTaskResolver
from src.services.task_descriptors_service import TaskDescriptorService


class TaskIdentificationService(AbstractLlmTaskService):

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
