from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

from llm.llm_provider import get_llm
from models.structured_output.action_extractors import ExtractionActionList
from models.structured_output.confirmation import ConfirmationAction
from models.structured_output.data_extraction_task import DataExtractionAction
from models.task.datamodel.abstract_data_model import AbstractDataModel
from services.history_limitation_service import HistoryLimitationService
from services.llm_services.abstract_llm_task_service import \
  AbstractLlmTaskService
from src.utils.prompt_manager import prompt_manager
from utils.settings import settings


class DataConfirmationService(AbstractLlmTaskService):

  @staticmethod
  def invoke(history) -> ExtractionActionList:
    history = HistoryLimitationService.dialog_turn_limiter(history, max_turns=settings.HISTORY_CONTEXT_MULTIPLIER * 1)
    confirmation_prompt = prompt_manager.get_prompt('confirmation')


    llm = get_llm().with_structured_output(ConfirmationAction)

    prompt = ChatPromptTemplate.from_messages([
      ("human", confirmation_prompt)
    ])

    chain = prompt | llm
    extraction_task : ConfirmationAction = chain.invoke({
      "history": history,
    })

    return extraction_task.action
