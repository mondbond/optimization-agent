from pydantic_settings import BaseSettings, SettingsConfigDict
from src.utils.logger import logger

class Settings(BaseSettings):


  # LOCAL LLM
  LOCAL_OLLAMA_URL : str = "http://localhost:11434"

  # LLM
  # DEFAULT_LLM_SOURCE_MODEL : str = "ollama/mistral:instruct"
  DEFAULT_LLM_SOURCE_MODEL : str = "bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
  SUMMARY_LLM_SOURCE_MODEL : str = "ollama/mistral:instruct"
  REASONING_LLM_SOURCE_MODEL : str = "ollama/mistral:instruct"

  # OPERATIONAL_CONSTANTS
  """
  Multiplier to increase the amount of historical context to send to the LLM.
  For example, if set to 2, it will send twice the amount of historical context defined in the system.
  """
  HISTORY_CONTEXT_MULTIPLIER : int = 1

  # LANGSMITH
  LANGSMITH_TRACING : str = "false"
  LANGSMITH_ENDPOINT : str = "https://api.smith.langchain.com"
  LANGSMITH_API_KEY : str = "none"
  LANGSMITH_PROJECT : str = "default"

  # MCP
  OPTIMIZATION_MCP_URL : str = "http://localhost"
  OPTIMIZATION_MCP_PORT : str = "8777"

  model_config = SettingsConfigDict(env_file=".env")

  def model_post_init(self, __context):
    logger.info(f"LOCAL_OLLAMA_URL = {self.LOCAL_OLLAMA_URL}")

    logger.info(f"DEFAULT_LLM_SOURCE_MODEL = {self.DEFAULT_LLM_SOURCE_MODEL}")
    logger.info(f"SUMMARY_LLM_SOURCE_MODEL = {self.SUMMARY_LLM_SOURCE_MODEL}")
    logger.info(f"REASONING_LLM_SOURCE_MODEL = {self.REASONING_LLM_SOURCE_MODEL}")


    logger.info(f"HISTORY_CONTEXT_MULTIPLIER = {self.HISTORY_CONTEXT_MULTIPLIER}")
    logger.info(f"LANGSMITH_TRACING = {self.LANGSMITH_TRACING}")
    return super().model_post_init(__context)

settings = Settings()
