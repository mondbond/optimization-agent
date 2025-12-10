from llm.abstract_llm_provider import AbstractLlmProvider
from llm.llm_provider_factory import LlmProviderFactory
from models.enums.llm_purpose import LlmPurpose
from src.utils.settings import settings
from functools import lru_cache


@lru_cache(maxsize=34)
def get_llm(purpose: LlmPurpose = LlmPurpose.DEFAULT, temperature=0):
  """
  Get LLM cached clients based on purpose and temperature.

  It parsed the env setting of the model based on structure {provider}/{model}.
  F.e. bedrock/anthropic.claude-3-sonnet-20240229-v1:0

  :param purpose: f.r. DEFAULT, REASONING, SUMMARY
  :param temperature:
  :return: cached LLM client
  """

  provider_model = None

  if purpose == LlmPurpose.DEFAULT:
    provider_model = settings.DEFAULT_LLM_SOURCE_MODEL
  elif purpose == LlmPurpose.REASONING:
    provider_model = settings.SUMMARIZATION_LLM_SOURCE
  elif purpose == LlmPurpose.SUMMARY:
    provider_model = settings.SUMMARY_LLM_SOURCE_MODEL

  provider, model = provider_model.split("/", 1)

  llm_provider: AbstractLlmProvider = LlmProviderFactory.get_provider(provider)

  return llm_provider.get_client(model=model, temperature=temperature)
