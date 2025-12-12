from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from models.enums.optimization_type import OptimizationType
from models.exceptions.agent_failed_exception import AgentFailedException
from models.structured_output.optimization_task_resolver import \
  OptimizationTaskResolver
from models.task.abstract_optimization_task import AbstractOptimizationTask
from services.llm_services.help_to_identify_task_service import \
  TaskTypeIdentificationHelpAnswerService
from services.llm_services.task_identification_service import \
  TaskExtractionService
from utils.constants import REGISTERED_TASKS
from src.utils.logger import logger


def task_intent_node(state: OptimizatorAgentState):
  """
  Node to identify the optimization task type from user input.
  It uses a task extraction service to analyze the conversation history and determine the task type.
  If the task type is already defined in the state, it routes to the next node.
  If the task type cannot be identified, it generates a help answer to assist the user.
  """

  if is_task_type_already_defined(state):
    return {
      "route": "next",
    }

  history = state.get('history')
  task_resolver: OptimizationTaskResolver = TaskExtractionService.invoke(history)


  if is_failed_to_identify_task_type(task_resolver):
    agent_help_answer = TaskTypeIdentificationHelpAnswerService.invoke(history, task_resolver.question)

    return {
      "route": "answer",
      "agent_message": agent_help_answer
    }

  task = identify_task_intent(task_resolver.type)

  return {
    "route": "next",
    "optimization_task_type": task.get_type(),
    "agent_message": f"Ok, your optimization task is {task.get_type().value}."
  }


def is_failed_to_identify_task_type(task_resolver: OptimizationTaskResolver):
  return task_resolver.type == OptimizationType.NONE or task_resolver.confident_score < 8


def is_task_type_already_defined(state):
  return state.get('optimization_task_type')


def identify_task_intent(intent: OptimizationType) -> AbstractOptimizationTask:
  for task in REGISTERED_TASKS:
    if task.get_type().value == intent.value:
      logger.info(f"Identified task intent: {intent.value}")
      return task

  raise AgentFailedException(f"Failed to identify task intent: {intent.value}")
