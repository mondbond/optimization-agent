
class AgentFailedException(RuntimeError):
    """Exception raised when agent broke or runtme execution in a place it shouldn't."""

    def __init__(self, message: str = "The agent has failed to complete its task."):
        super().__init__(message)
