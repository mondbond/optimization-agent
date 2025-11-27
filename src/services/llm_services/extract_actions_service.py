from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

from llm.llm_provider import get_llm
from models.structured_output.action_extractors import ExtractionActionList
from models.structured_output.data_extraction_task import DataExtractionAction
from models.task.datamodel.abstract_data_model import AbstractDataModel
from services.history_limitation_service import HistoryLimitationService
from services.llm_services.abstract_llm_task_service import \
  AbstractLlmTaskService
from src.utils.prompt_manager import prompt_manager
from utils.settings import settings


class ExtractActionTaskService(AbstractLlmTaskService):

  @staticmethod
  def invoke(history, data_model : AbstractDataModel, max_turns=1) -> ExtractionActionList:
    history = HistoryLimitationService.dialog_turn_limiter(history, max_turns=settings.HISTORY_CONTEXT_MULTIPLIER * 1)
    help_answer_prompt = prompt_manager.get_prompt('task_extraction')

    resource_description = data_model.get_resource_descriptions()
    examples = data_model.get_resource_action_examples()

    llm = get_llm().with_structured_output(ExtractionActionList)

    prompt = ChatPromptTemplate.from_messages([
      ("human", help_answer_prompt)
    ])

    chain = prompt | llm
    extraction_task : ExtractionActionList = chain.invoke({
      "history": history,
      "data_model_description": resource_description,
      "examples" : examples
    })

    return extraction_task



if __name__ == "__main__":
  hist = [
    HumanMessage("SoftServe can produce 400 and Epam can 3243")
  ]
  result  = ExtractActionTaskService.invoke(hist)

  print(result)

