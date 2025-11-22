from pydantic_settings import BaseSettings, SettingsConfigDict
from src.utils.logger import logger

class Settings(BaseSettings):
  LOCAL_OLLAMA_URL : str = "http://localhost:11434"
  LANGSMITH_TRACING : str = "true"
  LANGSMITH_ENDPOINT : str = "https://api.smith.langchain.com"
  LANGSMITH_API_KEY : str = "none"
  LANGSMITH_PROJECT : str = "default"

  model_config = SettingsConfigDict(env_file=".env")

  def model_post_init(self, __context):
    logger.info(f"LOCAL_OLLAMA_URL = {self.LOCAL_OLLAMA_URL}")
    return super().model_post_init(__context)

settings = Settings()
