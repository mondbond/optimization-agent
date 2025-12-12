from pydantic import BaseModel, Field

from models.enums.optimization_type import OptimizationType


class OptimizationTaskResolver(BaseModel):
  """
  Represents an optimization task to be resolved.
  """

  type: OptimizationType = Field(...,
                                 description="Type of the optimization task to be resolved.")

  confident_score: int = Field(...,
                                 description="Score that represent how confident you are in a selected optimization type.")

  question: str = Field(...,
                                 description="What question would you ask the user to be more confident in your answer?")

