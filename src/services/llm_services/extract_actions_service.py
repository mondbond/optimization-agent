from langchain_core.prompts import ChatPromptTemplate

from llm.llm_provider import get_llm
from models.structured_output.action_extractors import ExtractionActionList
from models.task.datamodel.abstract_data_model import AbstractDataModel
from services.history_limitation_service import HistoryLimitationService
from src.utils.prompt_manager import prompt_manager
from utils.settings import settings


class ExtractActionTaskService:
  """
  LLM Service to extract actions required to fulfill the data model from user message.
  """

  @staticmethod
  def invoke(history, data_model: AbstractDataModel, already_existed_entities : str,
      max_turns=1) -> ExtractionActionList:
    history = HistoryLimitationService.dialog_turn_limiter(history,
                                                           max_turns=2)
    help_answer_prompt = prompt_manager['task_extraction']

    resource_description = data_model.get_prompt_resource_descriptions()
    examples = data_model.get_prompt_resource_action_examples()

    llm = get_llm().with_structured_output(ExtractionActionList)

    prompt = ChatPromptTemplate.from_messages([
      ("human", help_answer_prompt)
    ])

    chain = prompt | llm
    extraction_task: ExtractionActionList = chain.invoke({
      "history": history,
      "data_model_description": resource_description,
      "already_existed_entities": already_existed_entities,
      "examples": examples
    })

    return extraction_task
