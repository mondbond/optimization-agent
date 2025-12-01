import boto3
from langchain_aws import ChatBedrockConverse

from llm.abstract_llm_provider import AbstractLlmProvider
from models.exceptions.model_not_supported import ModelNotSupportedError
from src.utils.logger import logger


class BedrockLlmProvider(AbstractLlmProvider):
  """
  LLM Provider for AWS Bedrock models.
  """

  SUPPORTED_MODELS = [
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "us.anthropic.claude-opus-4-20250514-v1:0",
    "us.amazon.nova-premier-v1:0",
  ]

  SOURCE_NAME = "bedrock"

  def get_client(self, model: str, temperature: float):
    if model not in self.SUPPORTED_MODELS:
      raise ModelNotSupportedError(
        f"Model '{model}' is not supported by Bedrock Provider. Supported models for {self.SOURCE_NAME}: {self.SUPPORTED_MODELS}")

    session = boto3.Session()
    credentials = session.get_credentials().get_frozen_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    aws_session_token = credentials.token

    logger.info(
      f"Provide Bedrock client with model: {model} and temperature {temperature}")

    return ChatBedrockConverse(
        model_id=model,
        region_name="us-east-1",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        temperature=temperature
    )

  def get_source_name(self) -> str:
    return self.SOURCE_NAME
