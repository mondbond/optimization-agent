from abc import ABC, abstractmethod


class AbstractLlmProvider(ABC):
  """
  Interface for all LLM providers (e.g., Bedrock, Ollama, etc.). They need to provide ot's source
  to be able to match the requested source automatically.
  """

  @abstractmethod
  def get_client(self, model: str, temperature: float):
    pass

  @abstractmethod
  def get_source_name(self) -> str:
    pass
