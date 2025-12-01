from models.exceptions.model_not_supported import ModelNotSupportedError
from utils.constans_text import REGISTERED_LLM_PROVIDERS


class LlmProviderFactory:
  """
  Factory class to get the appropriate LLM provider based on the provider name.
  """

  @staticmethod
  def get_provider(provider_name: str):
    for provider in REGISTERED_LLM_PROVIDERS:
      if provider.get_source_name() == provider_name:
        return provider

    raise ModelNotSupportedError(
      f"LLM Provider '{provider_name}' is not registered.")
