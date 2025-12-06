class DataPopulationError(RuntimeError):
  """
  Custom exception for data population related errors.
  Raised when there is an issue during the understanding of user's input data.
  get_rule intent is to provide to the answer prompt to formulate a better response.
  """

  def __init__(self, message: str):
    super().__init__(message)
    self.message = message

  def __str__(self):
    return f"ChatErrorException: {self.message}"

  def get_instruction(self):
    return ("Something wrong happen during understanding of user's input data."
            "Ask user to explain more clearly. Problem is ") + self.message
