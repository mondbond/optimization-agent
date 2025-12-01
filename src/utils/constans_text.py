from llm.bedrock_provider import BedrockLlmProvider
from llm.ollama_provider import OllamaLlmProvider

REGISTERED_LLM_PROVIDERS = [
  BedrockLlmProvider(), OllamaLlmProvider()
]
