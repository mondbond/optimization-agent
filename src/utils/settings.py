from pydantic_settings import BaseSettings, SettingsConfigDict
from src.utils.logger import logger

class Settings(BaseSettings):


  # todo  move to init
  # LOCAL LLM
  LOCAL_OLLAMA_URL : str = "http://localhost:11434"

  # OPERATIONAL_CONSTANTS
  HISTORY_CONTEXT_MULTIPLIER : int = 1

  # LANGSMITH
  LANGSMITH_TRACING : str = "true"
  LANGSMITH_ENDPOINT : str = "https://api.smith.langchain.com"
  LANGSMITH_API_KEY : str = "none"
  LANGSMITH_PROJECT : str = "default"

  # MCP
  OPTIMIZATION_MCP_URL : str = "http://localhost"
  OPTIMIZATION_MCP_PORT : str = "8777"

  model_config = SettingsConfigDict(env_file=".env")

  def model_post_init(self, __context):
    logger.info(f"LOCAL_OLLAMA_URL = {self.LOCAL_OLLAMA_URL}")
    logger.info(f"HISTORY_CONTEXT_MULTIPLIER = {self.HISTORY_CONTEXT_MULTIPLIER}")
    logger.info(f"LANGSMITH_TRACING = {self.LANGSMITH_TRACING}")
    return super().model_post_init(__context)

settings = Settings()
