
class ChatErrorException(RuntimeError):
    """Custom exception for chat-related errors."""

    def __init__(self, message: str):
      super().__init__(message)
      self.message = message

    def __str__(self):
        return f"ChatErrorException: {self.message}"

    def get_rule(self):
        return "Something wrong happen during chat data process. Ask user to explan mpre clearly. Problem is " + self.message
