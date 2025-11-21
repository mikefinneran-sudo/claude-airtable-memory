#!/usr/bin/env python3
"""
Custom tools for Research Organization Crew
Integrates with Gemini Deep Research, Perplexity API, and NotebookLM
"""
import sys
from pathlib import Path
from crewai_tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import json

# Add parent directory for vaultwarden access
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from vaultwarden_client import get_api_key


class GeminiResearchInput(BaseModel):
    """Input for Gemini Deep Research tool"""
    topic: str = Field(..., description="Research topic or question for Gemini Deep Research")
    depth: str = Field(default="comprehensive", description="Research depth: quick, comprehensive, or deep")


class GeminiDeepResearchTool(BaseTool):
    name: str = "Gemini Deep Research"
    description: str = """
    Conduct deep research using Gemini Deep Research.
    Returns comprehensive research report with citations and analysis.
    """
    args_schema: Type[BaseModel] = GeminiResearchInput
    
    def _run(self, topic: str, depth: str = "comprehensive") -> str:
        """Run Gemini Deep Research and return results"""
        try:
            api_key = get_api_key("Google")
            
            # Gemini API endpoint
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-thinking-exp:generateContent"
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # Construct prompt for deep research
            research_prompt = f"""
            Conduct comprehensive research on: {topic}
            
            Provide:
            1. Executive Summary
            2. Key Findings (numbered list)
            3. Detailed Analysis with sections
            4. Source recommendations (URLs to authoritative sources)
            5. Related topics for further research
            6. Confidence assessment
            
            Format as structured markdown with clear headings.
            """
            
            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": research_prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.4,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 8192
                }
            }
            
            response = requests.post(f"{url}?key={api_key}", headers=headers, json=data, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract research content
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            return json.dumps({
                "topic": topic,
                "depth": depth,
                "research": content,
                "model": "gemini-2.0-flash-thinking-exp",
                "tokens_used": result.get('usageMetadata', {})
            }, indent=2)
            
        except Exception as e:
            return f"Error running Gemini Deep Research: {str(e)}"


class PerplexitySearchInput(BaseModel):
    """Input for Perplexity search tool"""
    query: str = Field(..., description="Research question or topic to search")
    search_type: str = Field(default="comprehensive", 
                             description="Search type: quick, comprehensive, or academic")


class PerplexitySearchTool(BaseTool):
    name: str = "Search Perplexity AI"
    description: str = """
    Search Perplexity AI for research insights and citations.
    Returns AI-generated answers with source citations.
    """
    args_schema: Type[BaseModel] = PerplexitySearchInput
    
    def _run(self, query: str, search_type: str = "comprehensive") -> str:
        """Search Perplexity and return results"""
        try:
            api_key = get_api_key("Perplexity")
            
            # Perplexity API endpoint
            url = "https://api.perplexity.ai/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Map search type to model
            model_map = {
                "quick": "llama-3.1-sonar-small-128k-online",
                "comprehensive": "llama-3.1-sonar-large-128k-online",
                "academic": "llama-3.1-sonar-huge-128k-online"
            }
            
            data = {
                "model": model_map.get(search_type, "llama-3.1-sonar-large-128k-online"),
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a research assistant. Provide detailed answers with citations."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "temperature": 0.2,
                "return_citations": True,
                "return_images": False
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract answer and citations
            answer = result['choices'][0]['message']['content']
            citations = result.get('citations', [])
            
            return json.dumps({
                "query": query,
                "answer": answer,
                "citations": citations,
                "model": data["model"]
            }, indent=2)
            
        except Exception as e:
            return f"Error searching Perplexity: {str(e)}"


class MarkdownFormatterInput(BaseModel):
    """Input for markdown formatter tool"""
    content: dict = Field(..., description="Research content to format (from Gemini or Perplexity)")
    topic: str = Field(..., description="Research topic name")


class MarkdownFormatterTool(BaseTool):
    name: str = "Format for NotebookLM"
    description: str = """
    Format research content into NotebookLM-optimized markdown.
    Adds proper structure, citations, and metadata.
    """
    args_schema: Type[BaseModel] = MarkdownFormatterInput
    
    def _run(self, content: dict, topic: str) -> str:
        """Format research into NotebookLM markdown"""
        try:
            from datetime import datetime
            
            # Extract sources
            gemini_content = content.get('gemini', '')
            perplexity_content = content.get('perplexity', '')
            
            # Build markdown
            markdown = f"""---
title: "{topic}"
sources: ["Gemini Deep Research", "Perplexity AI"]
created: "{datetime.now().isoformat()}"
---

# {topic}

## Executive Summary

{gemini_content.split('Executive Summary')[1].split('#')[0] if 'Executive Summary' in gemini_content else 'Research summary...'}

## Key Findings

### From Gemini Deep Research

{gemini_content.split('Key Findings')[1].split('#')[0] if 'Key Findings' in gemini_content else ''}

### From Perplexity AI

{perplexity_content}

## Detailed Analysis

{gemini_content}

## Sources

### Perplexity Citations

"""
            
            # Add Perplexity citations
            if 'citations' in content:
                for i, citation in enumerate(content['citations'], 1):
                    markdown += f"{i}. [{citation.get('title', 'Source')}]({citation.get('url', '')})\n"
            
            return markdown
            
        except Exception as e:
            return f"Error formatting markdown: {str(e)}"


# Export tools for crew use
all_tools = [
    GeminiDeepResearchTool(),
    PerplexitySearchTool(),
    MarkdownFormatterTool()
]
