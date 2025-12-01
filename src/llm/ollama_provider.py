from langchain_ollama import ChatOllama

from llm.abstract_llm_provider import AbstractLlmProvider
from models.exceptions.model_not_supported import ModelNotSupportedError
from src.utils.settings import settings
from src.utils.logger import logger


class OllamaLlmProvider(AbstractLlmProvider):
  """
  LLM Provider for Ollama models.
  """

  SUPPORTED_MODELS = [
    "mistral:instruct",
  ]

  SOURCE_NAME = "ollama"

  def get_client(self, model: str, temperature: int):
    if model not in self.SUPPORTED_MODELS:
      raise ModelNotSupportedError(
        f"Model '{model}' is not supported by Ollama Provider. Supported models for f{self.SOURCE_NAME}: {self.SUPPORTED_MODELS}")

    logger.info(
      f"Provide Ollama client with model: {model} and temperature {temperature}")
    return ChatOllama(base_url=settings.LOCAL_OLLAMA_URL, model=model,
                      verbose=True, temperature=temperature)

  def get_source_name(self) -> str:
    return self.SOURCE_NAME
