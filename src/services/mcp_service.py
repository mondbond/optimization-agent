from langchain_mcp_adapters.client import MultiServerMCPClient
from src.utils.settings import settings


class OptimizationMcpService:
  """
  MCP Service for interacting with Multi-Server MCP Client
  """

  def __init__(self, mcp_url: str, port: str = '8887', ):
    self.mcp_url = mcp_url
    self.port = port
    self.mcp_client = MultiServerMCPClient(
        {
          "optimizator_mcp": {
            "transport": "streamable_http",
            "url": mcp_url + f":{port}/mcp",
          }
        }
    )

  async def calculate_transportation(self, transportation_data: dict) -> dict:
    tools = await self.mcp_client.get_tools()

    courutine = tools[0].coroutine(**transportation_data)

    return await courutine

  async def calculate_blending(self, transportation_data: dict) -> dict:
    tools = await self.mcp_client.get_tools()

    courutine = tools[1].coroutine(**transportation_data)

    return await courutine


optimisation_mcp_service = OptimizationMcpService(
  mcp_url=settings.OPTIMIZATION_MCP_URL, port=settings.OPTIMIZATION_MCP_PORT)
