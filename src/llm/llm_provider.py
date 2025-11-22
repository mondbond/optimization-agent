from src.utils.settings import settings
from langchain_ollama import ChatOllama
from src.utils.logger import logger

def local_ollama_client(temperature=0):
  return ChatOllama(base_url=settings.LOCAL_OLLAMA_URL, model="mistral:instruct", verbose=True, temperature=temperature)

def get_llm(temperature=0, source = 'default'):
  if "default" in source:
    logger.info("llm_provider: using ollama client")
    return local_ollama_client(temperature)

