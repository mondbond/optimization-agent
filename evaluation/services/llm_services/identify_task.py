import yaml
import pytest
from langchain_core.messages import HumanMessage, AIMessage
from pathlib import Path
from services.llm_services.task_identification_service import TaskIdentificationService

def load_test_cases():

  # todo wtf
  here = Path(__file__).resolve()
  base = here.parent.parent.parent

  case_file = base / "resources" / "task_classification" / "task_classification.yaml"

  with open(case_file, 'r') as file:
      return yaml.safe_load(file)

test_cases = load_test_cases()

@pytest.mark.evaluation
@pytest.mark.parametrize(
    "test_case",
    test_cases,
    ids=[tc["name"] for tc in test_cases]
)
def test_identify_task_service(test_case):
  history = convert_history(test_case['history'])
  expected_intent = test_case['expected_optimization_task_type']

  identified_intent = TaskIdentificationService.invoke(history)

  assert identified_intent.value == expected_intent


def convert_history(history_data):
  history = []
  for msg in history_data:
    if msg["role"] == "human":
      history.append(HumanMessage(content=msg["content"]))
    else:
      history.append(AIMessage(content=msg["content"]))

  return history
