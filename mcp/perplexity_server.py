#!/usr/bin/env python3
"""
Perplexity MCP Server
Provides Model Context Protocol tools for Perplexity API access
"""

import asyncio
import json
import sys
from typing import Any, Dict, List
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# Add parent directory to path for imports
sys.path.insert(0, '/app')
from backend.integrations.perplexity_api import get_perplexity


class PerplexityMCPServer:
    """MCP server exposing Perplexity API functionality"""

    def __init__(self):
        self.server = Server("perplexity-search")
        self.perplexity = get_perplexity()

        # Register tools
        self.register_tools()

    def register_tools(self):
        """Register all Perplexity tools"""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="search_web",
                    description=(
                        "Search the web using Perplexity's sonar model with citations. "
                        "Returns AI-generated answer with sources."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query or question"
                            },
                            "model": {
                                "type": "string",
                                "description": "Model to use",
                                "enum": ["sonar-small", "sonar-large", "sonar-huge"],
                                "default": "sonar-large"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="ask_llama_70b",
                    description="Ask Meta's Llama 3.1 70B model (offline, no search)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Prompt for the model"
                            },
                            "temperature": {
                                "type": "number",
                                "description": "Sampling temperature (0-1)",
                                "default": 0.7
                            }
                        },
                        "required": ["prompt"]
                    }
                ),
                Tool(
                    name="ask_sonar_large",
                    description=(
                        "Ask Perplexity's Sonar Large model with web search. "
                        "Best for current events and factual queries."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Question or prompt"
                            }
                        },
                        "required": ["prompt"]
                    }
                ),
                Tool(
                    name="compare_llms",
                    description=(
                        "Compare responses from multiple LLMs (Llama 8B, 70B, Sonar). "
                        "Useful for evaluating different perspectives."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Prompt to send to all models"
                            },
                            "models": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Models to compare",
                                "default": ["sonar-small", "llama-8b", "llama-70b"]
                            }
                        },
                        "required": ["prompt"]
                    }
                ),
                Tool(
                    name="research_topic",
                    description=(
                        "Deep research on a topic using Sonar Huge (most capable). "
                        "Returns comprehensive answer with citations."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Research topic or question"
                            },
                            "max_tokens": {
                                "type": "integer",
                                "description": "Maximum response length",
                                "default": 2048
                            }
                        },
                        "required": ["topic"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls"""

            if name == "search_web":
                result = await self.perplexity.search_query(
                    query=arguments["query"],
                    model=arguments.get("model", "sonar-large")
                )

                content = result["choices"][0]["message"]["content"]
                citations = result.get("citations", [])

                response = f"{content}\n\n"
                if citations:
                    response += "**Sources:**\n"
                    for i, citation in enumerate(citations, 1):
                        response += f"{i}. {citation}\n"

                return [TextContent(type="text", text=response)]

            elif name == "ask_llama_70b":
                result = await self.perplexity.chat_completion(
                    messages=[{"role": "user", "content": arguments["prompt"]}],
                    model="llama-70b",
                    temperature=arguments.get("temperature", 0.7),
                    search=False
                )

                content = result["choices"][0]["message"]["content"]
                usage = result.get("usage", {})

                response = f"{content}\n\n*Tokens: {usage.get('total_tokens', 0)}*"
                return [TextContent(type="text", text=response)]

            elif name == "ask_sonar_large":
                result = await self.perplexity.search_query(
                    query=arguments["prompt"],
                    model="sonar-large"
                )

                content = result["choices"][0]["message"]["content"]
                citations = result.get("citations", [])

                response = f"{content}\n\n"
                if citations:
                    response += "**Sources:**\n"
                    for citation in citations:
                        response += f"- {citation}\n"

                return [TextContent(type="text", text=response)]

            elif name == "compare_llms":
                results = await self.perplexity.multi_llm_comparison(
                    prompt=arguments["prompt"],
                    models=arguments.get("models")
                )

                response = "**Multi-LLM Comparison:**\n\n"
                for model, data in results.items():
                    response += f"### {model}\n"
                    if "error" in data:
                        response += f"ERROR: {data['error']}\n\n"
                    else:
                        response += f"{data['content']}\n"
                        response += f"*Tokens: {data['usage'].get('total_tokens', 0)}*\n\n"

                return [TextContent(type="text", text=response)]

            elif name == "research_topic":
                result = await self.perplexity.search_query(
                    query=arguments["topic"],
                    model="sonar-huge",
                    max_tokens=arguments.get("max_tokens", 2048)
                )

                content = result["choices"][0]["message"]["content"]
                citations = result.get("citations", [])

                response = f"# Research: {arguments['topic']}\n\n{content}\n\n"
                if citations:
                    response += "## Citations\n"
                    for i, citation in enumerate(citations, 1):
                        response += f"{i}. {citation}\n"

                return [TextContent(type="text", text=response)]

            else:
                raise ValueError(f"Unknown tool: {name}")

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
    server = PerplexityMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
