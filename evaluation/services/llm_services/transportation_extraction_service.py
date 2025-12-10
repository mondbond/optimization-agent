import yaml
import pytest
from langchain_core.messages import HumanMessage, AIMessage
from pathlib import Path

from models.enums.action_type import ActionType
from models.structured_output.action_extractors import ExtractionActionList
from models.task.transportation_optimization_task import \
  TransportationOptimizationTask
from services.llm_services.extract_actions_service import ExtractActionTaskService

def load_test_cases():
  here = Path(__file__).resolve()
  base = here.parent.parent.parent
  case_file = base / "resources" / "task_extraction" / "transportation_action_extraction.yml"
  with open(case_file, 'r') as file:
    return yaml.safe_load(file)

test_cases = load_test_cases()

@pytest.mark.evaluation
@pytest.mark.parametrize(
    "test_case",
    test_cases,
    ids=[tc["name"] for tc in test_cases]
)
def test_extract_action_task_service(test_case):
  history = convert_history(test_case['history'])
  already_existed_entities = test_case.get('already_existed_entities', "")
  expected_actions = test_case['expected_actions']

  data_model = TransportationOptimizationTask.get_optimization_data_model()

  result: ExtractionActionList = ExtractActionTaskService.invoke(
      history=history,
      data_model=data_model,
      already_existed_entities=already_existed_entities,
      max_turns=2
  )

  result_actions = [action.dict() for action in result.tasks]

  assert len(result_actions) == len(expected_actions), f"Number of actions mismatch: expected {len(expected_actions)}, got {len(result_actions)}"

  for idx, (actual, expected) in enumerate(zip(result_actions, expected_actions)):
    for key in expected:
      validate_property(actual.get(key), expected.get(str(key)), key)
    for key in actual:
      assert key in expected, f"Action {idx} has unexpected property '{key}'"

def convert_history(history_data):
  history = []
  for msg in history_data:
    if msg["role"] == "user":
      history.append(HumanMessage(content=msg["content"]))
    else:
      history.append(AIMessage(content=msg["content"]))
  return history


def validate_property(actual, expected, property_name: str):
  if not expected:
    return True

  if isinstance(actual, ActionType):
    actual = actual.name

  assert actual == expected, f"Action property '{property_name}' mismatch: expected '{expected}', got '{actual}'"
