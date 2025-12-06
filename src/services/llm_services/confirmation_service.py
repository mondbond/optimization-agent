from langchain_core.messages import AnyMessage
from langchain_core.prompts import ChatPromptTemplate

from llm.llm_provider import get_llm
from models.enums.confirmation_action import Confirmation
from models.structured_output.confirmation import ConfirmationAction
from services.history_limitation_service import HistoryLimitationService
from src.utils.prompt_manager import prompt_manager
from utils.settings import settings


class DataConfirmationService:
  """
  Service to confirm data with the user.
  """

  @staticmethod
  def invoke(history: list[AnyMessage]) -> Confirmation:
    history = HistoryLimitationService.dialog_turn_limiter(history,
                                                           max_turns=settings.HISTORY_CONTEXT_MULTIPLIER * 1)
    confirmation_prompt = prompt_manager['confirmation']

    llm = get_llm().with_structured_output(ConfirmationAction)

    prompt = ChatPromptTemplate.from_messages([
      ("human", confirmation_prompt)
    ])

    chain = prompt | llm
    extraction_task: ConfirmationAction = chain.invoke({
      "history": history,
    })

    return extraction_task.action
