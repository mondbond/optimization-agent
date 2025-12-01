
class ModelNotSupportedError(RuntimeError):
    """Exception raised when a requested model is not supported."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.message = f"The model '{self.model_name}' is not supported."
        super().__init__(self.message)
