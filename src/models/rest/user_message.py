from pydantic import BaseModel, Field

class UserMessage(BaseModel):
    message: str = Field(
        ...,
        description="The message content sent by the user. Cannot be null."
    )
