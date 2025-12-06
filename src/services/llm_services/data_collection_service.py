from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

from llm.llm_provider import get_llm
from models.model_validation import ModelValidationInstructions
from models.task.datamodel.transportation_data_model import \
  TransportationDataModel
from services.history_limitation_service import HistoryLimitationService
from src.utils.prompt_manager import prompt_manager
from utils.settings import settings


class RespondUserWithErrorsService:
  """
  LLM Service to form the message to user with identified errors in the data model or next steps in order to fulfill the data.
  """

  @staticmethod
  def invoke(history, model_validation: ModelValidationInstructions):
    history = HistoryLimitationService.dialog_turn_limiter(history,
                                                           max_turns=settings.HISTORY_CONTEXT_MULTIPLIER * 3)
    help_answer_prompt = prompt_manager['data_collecting']

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
      ("human", help_answer_prompt)
    ])

    validation_rules = model_validation.rules_for_prompt
    if validation_rules is None:
      validation_rules = model_validation.rules_for_injections

    chain = prompt | llm
    answer = chain.invoke({
      "history": history,
      "validation_rules": validation_rules
    })

    return answer.content


if __name__ == "__main__":
  hist = [
    HumanMessage("I have been in Paris last summer.")
  ]

  model = TransportationDataModel()

  model.update_data(TransportationDataModel.SUPPLIER_AVAILABILITY, "A", 100)
  model.update_data(TransportationDataModel.SUPPLIER_AVAILABILITY,
                    "Ice Cream Factory", None)

  model.update_data(TransportationDataModel.CONSUMER_NEEDS, "X", None)
  model.update_data(TransportationDataModel.CONSUMER_NEEDS, "Y", None)

  model.update_data(TransportationDataModel.SUPPLIER_TO_CONSUMER, key="A",
                    key2="X", value=4)

  validation = model.validate_model_with_instruction()

  print(validation.is_valid)
  print(validation.rules_for_prompt)
  print(validation.rules_for_injections)

  result = RespondUserWithErrorsService.invoke(hist, validation)

  print(result)
