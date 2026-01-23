#!/usr/bin/env python3
"""
Perplexity Pro MCP Server
Provides research capabilities using Perplexity's AI search API
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Initialize Perplexity API client
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

class PerplexityMCP:
    def __init__(self):
        self.app = Server("perplexity-research")
        self.setup_handlers()

    def setup_handlers(self):
        """Register MCP tool handlers"""

        @self.app.list_tools()
        async def list_tools() -> List[Tool]:
            """List available Perplexity research tools"""
            return [
                Tool(
                    name="perplexity_search",
                    description=(
                        "Search the web using Perplexity Pro for comprehensive research. "
                        "Returns AI-generated answers with citations and sources. "
                        "Best for: market research, competitive analysis, fact-finding, "
                        "technical research, current events."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The research query or question to search for"
                            },
                            "search_domain_filter": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional: Filter results to specific domains (e.g., ['bloomberg.com', 'techcrunch.com'])"
                            },
                            "search_recency_filter": {
                                "type": "string",
                                "enum": ["month", "week", "day", "hour"],
                                "description": "Optional: Filter results by recency"
                            },
                            "model": {
                                "type": "string",
                                "enum": [
                                    "llama-3.1-sonar-small-128k-online",
                                    "llama-3.1-sonar-large-128k-online",
                                    "llama-3.1-sonar-huge-128k-online"
                                ],
                                "description": "Model to use (default: sonar-large)",
                                "default": "llama-3.1-sonar-large-128k-online"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="perplexity_deep_research",
                    description=(
                        "Perform deep research on a topic with follow-up questions. "
                        "Iteratively explores a topic to gather comprehensive information. "
                        "Best for: market sizing, company analysis, industry deep-dives, "
                        "strategic research."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "The main topic to research deeply"
                            },
                            "focus_areas": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Specific aspects to focus on (e.g., ['market size', 'competitors', 'trends'])"
                            },
                            "depth": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 5,
                                "default": 3,
                                "description": "How deep to research (1=surface, 5=exhaustive)"
                            }
                        },
                        "required": ["topic"]
                    }
                ),
                Tool(
                    name="perplexity_compare",
                    description=(
                        "Compare two or more entities (companies, products, technologies, etc.) "
                        "using Perplexity research. Returns structured comparison."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "entities": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "description": "List of entities to compare (e.g., ['CapIQ', 'PitchBook', 'WalterSignal'])"
                            },
                            "comparison_criteria": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "What to compare (e.g., ['pricing', 'features', 'market share'])"
                            }
                        },
                        "required": ["entities"]
                    }
                )
            ]

        @self.app.call_tool()
        async def call_tool(name: str, arguments: Any) -> List[TextContent | ImageContent | EmbeddedResource]:
            """Handle tool calls"""

            if name == "perplexity_search":
                return await self.perplexity_search(
                    query=arguments["query"],
                    domain_filter=arguments.get("search_domain_filter"),
                    recency_filter=arguments.get("search_recency_filter"),
                    model=arguments.get("model", "llama-3.1-sonar-large-128k-online")
                )

            elif name == "perplexity_deep_research":
                return await self.perplexity_deep_research(
                    topic=arguments["topic"],
                    focus_areas=arguments.get("focus_areas", []),
                    depth=arguments.get("depth", 3)
                )

            elif name == "perplexity_compare":
                return await self.perplexity_compare(
                    entities=arguments["entities"],
                    criteria=arguments.get("comparison_criteria", [])
                )

            else:
                raise ValueError(f"Unknown tool: {name}")

    async def perplexity_search(
        self,
        query: str,
        domain_filter: Optional[List[str]] = None,
        recency_filter: Optional[str] = None,
        model: str = "llama-3.1-sonar-large-128k-online"
    ) -> List[TextContent]:
        """Perform Perplexity search"""

        if not PERPLEXITY_API_KEY:
            return [TextContent(
                type="text",
                text="Error: PERPLEXITY_API_KEY environment variable not set. Please add your API key."
            )]

        # Build request payload
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful research assistant. Provide comprehensive, well-cited answers with sources."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "max_tokens": 4000,
            "temperature": 0.2,
            "top_p": 0.9,
            "return_citations": True,
            "return_images": False,
            "search_domain_filter": domain_filter or [],
        }

        if recency_filter:
            payload["search_recency_filter"] = recency_filter

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    PERPLEXITY_API_URL,
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    timeout=60.0
                )
                response.raise_for_status()

                result = response.json()
                content = result["choices"][0]["message"]["content"]
                citations = result.get("citations", [])

                # Format response with citations
                formatted_response = f"# Research Results\n\n{content}\n\n"

                if citations:
                    formatted_response += "## Sources\n\n"
                    for i, citation in enumerate(citations, 1):
                        formatted_response += f"{i}. {citation}\n"

                return [TextContent(type="text", text=formatted_response)]

        except httpx.HTTPError as e:
            return [TextContent(
                type="text",
                text=f"Error calling Perplexity API: {str(e)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Unexpected error: {str(e)}"
            )]

    async def perplexity_deep_research(
        self,
        topic: str,
        focus_areas: List[str],
        depth: int = 3
    ) -> List[TextContent]:
        """Perform deep iterative research on a topic"""

        results = []

        # Initial broad search
        results.append(f"# Deep Research: {topic}\n\n")

        initial_query = f"Provide a comprehensive overview of {topic}"
        if focus_areas:
            initial_query += f", focusing on: {', '.join(focus_areas)}"

        overview = await self.perplexity_search(initial_query)
        results.append(overview[0].text)

        # Follow-up questions based on depth
        if depth >= 2 and focus_areas:
            for area in focus_areas[:depth]:
                results.append(f"\n## Deep Dive: {area}\n\n")
                follow_up_query = f"Detailed analysis of {area} in the context of {topic}"
                follow_up = await self.perplexity_search(follow_up_query)
                results.append(follow_up[0].text)

        combined_result = "\n".join(results)
        return [TextContent(type="text", text=combined_result)]

    async def perplexity_compare(
        self,
        entities: List[str],
        criteria: List[str]
    ) -> List[TextContent]:
        """Compare multiple entities"""

        entities_str = " vs. ".join(entities)
        query = f"Create a detailed comparison of {entities_str}"

        if criteria:
            query += f" focusing on: {', '.join(criteria)}"

        query += ". Provide a structured comparison table or detailed analysis."

        return await self.perplexity_search(query)

    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(
                read_stream,
                write_stream,
                self.app.create_initialization_options()
            )

async def main():
    """Main entry point"""
    server = PerplexityMCP()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
