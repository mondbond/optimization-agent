from graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from models.enums.optimization_type import OptimizationType
from models.exceptions.agent_failed_exception import AgentFailedException
from services.llm_services.help_to_identify_task_service import \
  HelpToIdentifyTaskService
from services.llm_services.task_identification_service import \
  TaskIdentificationService
from utils.constants import REGISTERED_TASKS
from src.utils.logger import logger


def task_intent_node(state: OptimizatorAgentState):
  if state.get('optimization_task_type'):
    return {
      "route": "next",
    }

  history = state.get('history')
  intent: OptimizationType = TaskIdentificationService.invoke(history)

  if intent == OptimizationType.NONE:
    help_answer = HelpToIdentifyTaskService.invoke(history)

    return {
      "route": "answer",
      "agent_message": help_answer
    }

  for task in REGISTERED_TASKS:
    if task.get_type().value == intent.value:
      logger.info(f"Identified task intent: {intent.value}")
      answer = f"Ok, your optimization task is {task.get_type().value}."

      return {
        "route": "next",
        "optimization_task_type": task.get_type(),
        "agent_message": answer
      }

  raise AgentFailedException("Task intent identification failed")
