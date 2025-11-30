from pydantic import BaseModel, Field

from models.enums.confirmation_action import Confirmation


class ConfirmationAction(BaseModel):

  action : Confirmation = Field(...,
                              description= "Action that required to be specified. Possible values is CONFIRMED, REJECTED only"
                              )
