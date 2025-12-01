from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

#  todo delete
def get_mcp_config():
  mcp_config = {
    "servers": [
      {
        "name": "mond_mcp",
        "transport": "streamable-http",
        "url": "http://mond_mcp:8887",
        "description": (
          "This server provides tools to get stock price changes and fundamental properties. "
          "Available tools:\n"
          "1. get_ticker_price_change(ticker: str) -> dict: Get price change for a ticker in percents for the last trading day.\n"
          "2. get_ticker_fundamental(ticker: str, fund_property: str) -> dict: Get fundamental property for a ticker. "
          "Available properties include marketCap, trailingPE, forwardPE, priceToBook, beta, dividendYield, earningsPerShare."
        )
      }
    ]
  }
  return mcp_config




mcp_url = "http://0.0.0.0:8777/mcp"


mcp_client = None

# http://mond_mcp:8887/mcp
if mcp_url is not None and mcp_url != "":
  mcp_client = MultiServerMCPClient(
      {
        "optimizator_mcp": {
          "transport": "streamable_http",
          "url": mcp_url,
        }
      }
  )



if __name__ == "__main__":
  async def main():
    config = get_mcp_config()
    tools = await mcp_client.get_tools()
    print(tools)

  asyncio.run(main())
