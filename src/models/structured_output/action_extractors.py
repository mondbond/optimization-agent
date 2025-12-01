from pydantic import BaseModel

from models.structured_output.data_extraction_task import DataExtractionAction


class ExtractionActionList(BaseModel):
  """
  Represents a list of data extraction actions to be performed.
  """

  tasks: list[DataExtractionAction]
