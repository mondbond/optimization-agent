from pydantic import BaseModel, Field
from models.enums.optimization_type import OptimizationType

class OptimizationTaskResolver(BaseModel):

    type: OptimizationType = Field(..., description="Description of the optimization task to be resolved. Can be only BLENDING choosen")
