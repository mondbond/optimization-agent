from pydantic import BaseModel, Field

from models.enums.action_type import ActionType
from models.structured_output.data_extraction_task import DataExtractionAction


class ExtractionActionList(BaseModel):
  tasks: list[DataExtractionAction]
