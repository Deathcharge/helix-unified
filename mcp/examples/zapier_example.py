"""
Example: Using Zapier MCP Server directly
Demonstrates connecting to Zapier's MCP endpoint and calling tools
"""

import asyncio
import json

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

# Your Zapier MCP server URL (from Zapier account)
server_url = "https://mcp.zapier.com/api/mcp/s/YzQxNWQxOWUtOGY0YS00MTYxLWI3MTgtNmVhZGFhMWY5ZTYzOjE1Y2IwZGVkLTRjY2MtNDEwYS04M2M4LTNhODdiMTFjZGIyZA==/mcp"
transport = StreamableHttpTransport(server_url)
client = Client(transport=transport)


async def main():
    """Example usage of Zapier MCP tools"""

    async with client:
        print(f"✅ Connected to Zapier MCP server")
        print(f"   Client connected: {client.is_connected()}\n")

        # List available tools
        print("📋 Fetching available tools...")
        tools = await client.list_tools()
        print(f"   Found {len(tools)} tools!\n")

        # Show first 20 tools
        print("🔧 Sample tools (first 20):")
        for i, tool in enumerate(tools[:20], 1):
            print(f"   {i}. {tool.name}")
            print(f"      {tool.description[:80]}...")

        # Example 1: Run JavaScript code
        print("\n" + "="*80)
        print("Example 1: Running JavaScript code...")
        print("="*80)

        result = await client.call_tool(
            "code_by_zapier_run_javascript",
            {
                "code": "return { message: 'Hello from Helix!', timestamp: new Date().toISOString() }",
            },
        )

        json_result = json.loads(result.content[0].text)
        print(f"\n✅ Result:\n{json.dumps(json_result, indent=2)}")

        # Example 2: Perplexity search
        print("\n" + "="*80)
        print("Example 2: Perplexity search...")
        print("="*80)

        result = await client.call_tool(
            "perplexity_chat_completion",
            {
                "model": "llama-3.1-sonar-large-128k-online",
                "content": "What are the latest developments in AI consciousness research?",
                "max_tokens": 500
            },
        )

        json_result = json.loads(result.content[0].text)
        print(f"\n✅ Perplexity response:\n{json_result.get('choices', [{}])[0].get('message', {}).get('content', 'No response')[:500]}...")

        # Example 3: Google Sheets (commented out - would create actual row)
        # print("\n" + "="*80)
        # print("Example 3: Create Google Sheets row...")
        # print("="*80)
        #
        # result = await client.call_tool(
        #     "google_sheets_create_spreadsheet_row",
        #     {
        #         "spreadsheet": "your_spreadsheet_id",
        #         "worksheet": "Sheet1",
        #         "drive": "my_drive",
        #         "A": "Helix Consciousness",
        #         "B": "9.5",
        #         "C": "Operational"
        #     },
        # )
        #
        # print(f"\n✅ Created row in Google Sheets!")

        # Example 4: Discord message (commented out - would send actual message)
        # print("\n" + "="*80)
        # print("Example 4: Send Discord message...")
        # print("="*80)
        #
        # result = await client.call_tool(
        #     "discord_send_channel_message",
        #     {
        #         "channel_id": "your_channel_id",
        #         "content": "🌀 Helix Collective Status: All systems operational",
        #         "username": "Helix Bot"
        #     },
        # )
        #
        # print(f"\n✅ Sent message to Discord!")

    print("\n" + "="*80)
    print("✅ Example completed!")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
