from pydantic import BaseModel, Field

from models.enums.action_type import ActionType


class DataExtractionAction(BaseModel):

  action : ActionType = Field(...,
                       description= "Action that required to be specified. Possible values is REMOVE, UPDATE, DELETE_ALL only"
                       )

  resource: str = Field(
                      description="Resource that need to be modified. One of resource names already named"
                      )

  key1: str = Field(description="Name of the object or resource that should be extracted from users message")

  key2: str = Field(description="Second name to use only if the modifiable resource has a matrix type")

  value: str = Field(description="Actual value to be added. It can be float, int or string depending on the resource type")
