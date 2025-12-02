import json

class TransportationSolutionAnswerService:

  @staticmethod
  def get_transportation_solution_answer(solver_output: int) -> str:
    data = json.loads(solver_output)
    lines = []
    lines.append("Optimisation Plan:")
    for item in data["from_to"]:
      lines.append(f"  {item['from_node']} → {item['to_node']}: {item['amount']} units")
    lines.append(f"Total Cost: {data['total_cost']}")
    return "\n".join(lines)
