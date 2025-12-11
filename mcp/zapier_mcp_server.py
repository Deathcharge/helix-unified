#!/usr/bin/env python3
"""
Zapier MCP Server Integration
Provides access to 300+ Zapier integrations via MCP
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool


class ZapierMCPServer:
    """
    MCP server that wraps Zapier's MCP endpoint.

    Provides access to 300+ integrations including:
    - Google Suite (Sheets, Docs, Calendar, Drive)
    - Notion (Pages, Databases, Blocks)
    - Discord, Slack, Gmail
    - ChatGPT, Perplexity, Claude, Grok
    - Airtable, HubSpot, ClickUp, Asana
    - And many more!
    """

    def __init__(self):
        self.server = Server("helix-zapier")

        # Zapier MCP server URL from environment or config
        self.zapier_url = os.getenv(
            "ZAPIER_MCP_URL",
            "https://mcp.zapier.com/api/mcp/s/YzQxNWQxOWUtOGY0YS00MTYxLWI3MTgtNmVhZGFhMWY5ZTYzOjE1Y2IwZGVkLTRjY2MtNDEwYS04M2M4LTNhODdiMTFjZGIyZA==/mcp"
        )

        # Initialize Zapier client
        self.transport = StreamableHttpTransport(self.zapier_url)
        self.zapier_client = Client(transport=self.transport)

        # Cache for Zapier tools
        self.zapier_tools: List[Any] = []

        self.register_tools()

    async def fetch_zapier_tools(self):
        """Fetch available tools from Zapier MCP server"""
        async with self.zapier_client:
            self.zapier_tools = await self.zapier_client.list_tools()

    def register_tools(self):
        """Register dynamic tools based on Zapier capabilities"""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List all available Zapier tools"""

            # Fetch tools from Zapier if not cached
            if not self.zapier_tools:
                await self.fetch_zapier_tools()

            # Convert Zapier tools to MCP tools
            tools = []

            # Add a few high-priority tools with custom descriptions
            priority_tools = {
                "google_sheets_create_spreadsheet_row": "Create new rows in Google Sheets",
                "notion_create_page": "Create pages in Notion",
                "discord_send_channel_message": "Send messages to Discord channels",
                "slack_send_channel_message": "Post messages to Slack channels",
                "gmail_send_email": "Send emails via Gmail",
                "code_by_zapier_run_python": "Execute Python code (advanced)",
                "code_by_zapier_run_javascript": "Execute JavaScript code (advanced)",
                "perplexity_chat_completion": "Query Perplexity AI",
                "chatgpt_openai_conversation": "Chat with ChatGPT",
                "google_drive_upload_file": "Upload files to Google Drive",
                "airtable_create_record": "Create records in Airtable",
            }

            for tool in self.zapier_tools:
                # Build input schema from parameters
                properties = {}
                required = []

                if hasattr(tool, 'params') and tool.params:
                    for param in tool.params:
                        properties[param] = {
                            "type": "string",
                            "description": f"Parameter: {param}"
                        }
                        required.append(param)

                tools.append(Tool(
                    name=tool.name,
                    description=priority_tools.get(tool.name, tool.description),
                    inputSchema={
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                ))

            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Execute a Zapier tool"""

            try:
                # Connect to Zapier and execute tool
                async with self.zapier_client:
                    result = await self.zapier_client.call_tool(name, arguments)

                    # Extract text content from result
                    if hasattr(result, 'content') and len(result.content) > 0:
                        text_content = result.content[0].text

                        # Try to parse as JSON for pretty formatting
                        try:
                            json_result = json.loads(text_content)
                            formatted = json.dumps(json_result, indent=2)
                            return [TextContent(
                                type="text",
                                text=f"✅ {name} executed successfully:\n\n{formatted}"
                            )]
                        except json.JSONDecodeError:
                            return [TextContent(
                                type="text",
                                text=f"✅ {name} executed successfully:\n\n{text_content}"
                            )]
                    else:
                        return [TextContent(
                            type="text",
                            text=f"✅ {name} executed successfully (no output)"
                        )]

            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"❌ Error executing {name}: {str(e)}"
                )]

    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main():
    """Main entry point"""
    server = ZapierMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
