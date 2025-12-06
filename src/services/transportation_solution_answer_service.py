import json

from models.task.datamodel.transportation_data_model import \
  TransportationDataModel


class TransportationTaskOptimisationMcpAdapter:
  """
  Adapter to convert transportation task data model to specific optimisation MCP-compatible dictionary
  and to format the solver output into a human-readable answer.

  As soon as at the stage of calculation optimisation task is already defined by conversation flow
  - no need to involve LLM here.
  """

  @staticmethod
  def result_to_answer(solver_output: tuple) -> str:
    data = json.loads(solver_output[0])
    lines = []
    lines.append("Optimisation Plan:")
    for item in data["from_to"]:
      lines.append(f"  {item['from_node']} → {item['to_node']}: {item['amount']} units")
    lines.append(f"Total Cost: {data['total_cost']}")
    return "\n".join(lines)

  @staticmethod
  def to_mcp_dict(task_data_model : TransportationDataModel) -> dict:
    return {
      "task": {
        "supplier_to_supply": task_data_model._data_map[TransportationDataModel.SUPPLIER_AVAILABILITY].data,
        "consumer_to_consume": task_data_model._data_map[TransportationDataModel.CONSUMER_NEEDS].data,
        "supplier_to_consumer_cost": task_data_model._data_map[TransportationDataModel.SUPPLIER_TO_CONSUMER].data,
        "objective_function": task_data_model._data_map[TransportationDataModel.OBJECTIVE_FUNCTION].data
      }
    }
