from pydantic import BaseModel, Field


class UserMessage(BaseModel):
  """
  UserMessage represents a message sent by a user in a REST API context.
  It contains the message content and ensures that it is not null.
  """

  message: str = Field(
      ...,
      description="The message content sent by the user. Cannot be null."
  )
