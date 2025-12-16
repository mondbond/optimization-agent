import json

from models.task.datamodel.blend_data_model import BlendDataModel


class BlendingTaskOptimisationMcpAdapter:
  """
  Adapter to convert transportation task data model to specific optimisation MCP-compatible dictionary
  and to format the solver output into a human-readable answer.

  As soon as at the stage of calculation optimisation task is already defined by conversation flow
  - no need to involve LLM here.
  """

  @staticmethod
  def to_mcp_dict(blending_nodel : BlendDataModel) -> dict:
    return {
      "task": {
        "material_to_cost": blending_nodel._data_map[BlendDataModel.MATERIAL_TO_COST].data,
        "composition_constraint": blending_nodel._data_map[
          BlendDataModel.PRODUCTS_COMPOSITIONS].data,
        "materials_to_composition": blending_nodel._data_map[
          BlendDataModel.MATERIAL_TO_COMPOSITIONS_COST].data,
        "objective_function": blending_nodel._data_map[BlendDataModel.OBJECTIVE_FUNCTION].data
      }
    }

  @staticmethod
  def result_to_answer(solver_output: tuple) -> str:
    data = json.loads(solver_output[0])
    lines = []
    lines.append("Blending Plan:")
    for material, amount in data["material_to_amount"].items():
      lines.append(f"  {material}: {amount} units")
    lines.append(f"Total Cost: {data['total_cost']}")
    return "\n".join(lines)

