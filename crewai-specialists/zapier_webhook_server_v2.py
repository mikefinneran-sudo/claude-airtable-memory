#!/usr/bin/env python3
"""
WalterSignal Zapier Webhook Server v2 - With Real CrewAI Integration
FastAPI server that receives webhooks from Zapier and triggers real CrewAI specialists

Usage:
    python zapier_webhook_server_v2.py

Endpoints:
    POST /webhook/research - Trigger research crew (real execution)
    POST /webhook/lead-enrichment - Enrich lead data (uses research crew)
    GET /health - Health check
"""

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import uvicorn
import os
from datetime import datetime
import json
from pathlib import Path
import sys

# Add CrewAI to path
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

app = FastAPI(
    title="WalterSignal CrewAI Webhook Server v2",
    description="Zapier integration with real CrewAI specialists",
    version="2.0.0"
)

# Security - API Key authentication
API_KEY = os.getenv("ZAPIER_API_KEY", "waltersignal-dev-key-12345")

def verify_api_key(x_api_key: str = Header(None)):
    """Verify API key from header"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


# LLM Configuration
def get_llm(model_name="llama3.1:70b"):
    """Get LLM instance for CrewAI agents"""
    return Ollama(
        model=model_name,
        base_url="http://localhost:11434",
        timeout=300
    )


# Request Models
class ResearchRequest(BaseModel):
    """Request model for research crew"""
    topic: str = Field(..., description="Research topic or query")
    depth: Optional[str] = Field("standard", description="Research depth: quick, standard, deep")
    output_format: Optional[str] = Field("markdown", description="Output format: markdown, json")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata from Zapier")


class LeadEnrichmentRequest(BaseModel):
    """Request model for lead enrichment"""
    company_name: str = Field(..., description="Company name to enrich")
    website: Optional[str] = Field(None, description="Company website")
    industry: Optional[str] = Field(None, description="Industry sector")
    fields_to_enrich: Optional[List[str]] = Field(
        default_factory=lambda: ["company_info", "decision_makers", "pain_points", "tech_stack"],
        description="Data points to enrich"
    )
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata from Zapier")


# Response Models
class WebhookResponse(BaseModel):
    """Standard webhook response"""
    success: bool
    crew_type: str
    execution_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str
    execution_time_seconds: Optional[float] = None


# CrewAI Functions
def create_research_crew(topic: str, depth: str = "standard"):
    """
    Create a research crew for a given topic
    Simplified version - single agent for speed
    """

    # Determine detail level based on depth
    detail_instruction = {
        "quick": "Provide a concise 2-3 paragraph summary with 3-5 key points.",
        "standard": "Provide a comprehensive analysis with 5-10 key findings and sources.",
        "deep": "Conduct deep research with extensive analysis, 10-15 key findings, and detailed sources."
    }.get(depth, "Provide a comprehensive analysis.")

    # Create research agent
    researcher = Agent(
        role="Research Specialist",
        goal=f"Research and analyze: {topic}",
        backstory=f"""You are an expert researcher with deep knowledge across multiple domains.
        You excel at gathering accurate information, analyzing data, and presenting clear insights.
        You always cite sources and provide actionable recommendations.""",
        llm=get_llm("llama3.1:70b"),
        verbose=True,
        allow_delegation=False
    )

    # Create research task
    research_task = Task(
        description=f"""
        Research the following topic thoroughly: {topic}

        {detail_instruction}

        Your research should include:
        1. Overview and context
        2. Key findings and insights
        3. Trends and patterns
        4. Actionable recommendations
        5. Sources and references

        Format your response as a structured report.
        """,
        agent=researcher,
        expected_output=f"A detailed research report on {topic} with findings, insights, and recommendations."
    )

    # Create crew
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True
    )

    return crew


def create_lead_enrichment_crew(company_name: str, website: str = None, industry: str = None):
    """
    Create a crew to enrich lead data
    Uses research capabilities to find company information
    """

    # Build research query
    query_parts = [f"Company: {company_name}"]
    if website:
        query_parts.append(f"Website: {website}")
    if industry:
        query_parts.append(f"Industry: {industry}")

    research_query = " | ".join(query_parts)

    # Create lead enrichment agent
    enrichment_agent = Agent(
        role="Lead Intelligence Specialist",
        goal=f"Gather comprehensive intelligence about {company_name}",
        backstory="""You are an expert at B2B lead research and company intelligence.
        You excel at finding key decision makers, understanding company challenges,
        identifying technology stacks, and uncovering business opportunities.
        You always provide accurate, actionable intelligence.""",
        llm=get_llm("llama3.1:70b"),
        verbose=True,
        allow_delegation=False
    )

    # Create enrichment task
    enrichment_task = Task(
        description=f"""
        Gather comprehensive intelligence about this company:
        {research_query}

        Research and provide the following information:

        1. **Company Information**
           - Full company name and description
           - Employee count estimate
           - Revenue estimate (if publicly available)
           - Headquarters location
           - Year founded

        2. **Decision Makers**
           - CEO/Founder name and background
           - Key executives (CTO, VP Sales, etc.)
           - LinkedIn profiles (if available)

        3. **Pain Points & Challenges**
           - Industry challenges they likely face
           - Business problems based on their market
           - Growth opportunities

        4. **Technology Stack**
           - Known technologies they use
           - CRM, marketing tools, etc.
           - Development stack (if tech company)

        5. **Business Intelligence**
           - Recent news or announcements
           - Funding status
           - Competitive positioning

        Format your response as structured JSON-like data that can be easily parsed.
        """,
        agent=enrichment_agent,
        expected_output=f"Comprehensive intelligence report about {company_name} with all requested data points."
    )

    # Create crew
    crew = Crew(
        agents=[enrichment_agent],
        tasks=[enrichment_task],
        process=Process.sequential,
        verbose=True
    )

    return crew


# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "WalterSignal CrewAI Webhook Server v2",
        "version": "2.0.0",
        "real_crews": True,
        "timestamp": datetime.now().isoformat(),
        "available_endpoints": [
            "/webhook/research",
            "/webhook/lead-enrichment"
        ]
    }


# Webhook Endpoints
@app.post("/webhook/research", response_model=WebhookResponse)
async def research_webhook(
    request: ResearchRequest,
    x_api_key: str = Header(None)
):
    """
    Trigger REAL research crew from Zapier

    Example Zapier webhook data:
    {
        "topic": "AI consulting market in Chicago",
        "depth": "deep",
        "output_format": "markdown"
    }
    """
    verify_api_key(x_api_key)

    execution_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    start_time = datetime.now()

    try:
        print(f"\n{'='*80}")
        print(f"🔬 EXECUTING REAL RESEARCH CREW")
        print(f"{'='*80}")
        print(f"Topic: {request.topic}")
        print(f"Depth: {request.depth}")
        print(f"Execution ID: {execution_id}")
        print(f"{'='*80}\n")

        # Create and execute real research crew
        crew = create_research_crew(request.topic, request.depth)
        crew_result = crew.kickoff()

        execution_time = (datetime.now() - start_time).total_seconds()

        print(f"\n{'='*80}")
        print(f"✅ RESEARCH COMPLETE")
        print(f"Execution time: {execution_time:.2f}s")
        print(f"{'='*80}\n")

        # Format result
        result = {
            "topic": request.topic,
            "depth": request.depth,
            "findings": str(crew_result),
            "summary": f"Completed {request.depth} research on: {request.topic}",
            "execution_id": execution_id,
            "model_used": "llama3.1:70b"
        }

        return WebhookResponse(
            success=True,
            crew_type="research",
            execution_id=execution_id,
            status="completed",
            result=result,
            timestamp=datetime.now().isoformat(),
            execution_time_seconds=execution_time
        )

    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        print(f"\n❌ ERROR: {str(e)}\n")

        return WebhookResponse(
            success=False,
            crew_type="research",
            execution_id=execution_id,
            status="failed",
            error=str(e),
            timestamp=datetime.now().isoformat(),
            execution_time_seconds=execution_time
        )


@app.post("/webhook/lead-enrichment", response_model=WebhookResponse)
async def lead_enrichment_webhook(
    request: LeadEnrichmentRequest,
    x_api_key: str = Header(None)
):
    """
    Enrich lead data using REAL research crew

    Example Zapier webhook data:
    {
        "company_name": "Acme Corp",
        "website": "https://acme.com",
        "industry": "Manufacturing",
        "fields_to_enrich": ["company_info", "decision_makers", "pain_points"]
    }
    """
    verify_api_key(x_api_key)

    execution_id = f"enrich_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    start_time = datetime.now()

    try:
        print(f"\n{'='*80}")
        print(f"💼 EXECUTING REAL LEAD ENRICHMENT CREW")
        print(f"{'='*80}")
        print(f"Company: {request.company_name}")
        print(f"Website: {request.website}")
        print(f"Industry: {request.industry}")
        print(f"Execution ID: {execution_id}")
        print(f"{'='*80}\n")

        # Create and execute real lead enrichment crew
        crew = create_lead_enrichment_crew(
            request.company_name,
            request.website,
            request.industry
        )
        crew_result = crew.kickoff()

        execution_time = (datetime.now() - start_time).total_seconds()

        print(f"\n{'='*80}")
        print(f"✅ LEAD ENRICHMENT COMPLETE")
        print(f"Execution time: {execution_time:.2f}s")
        print(f"{'='*80}\n")

        # Format enriched data
        enriched_data = {
            "company_name": request.company_name,
            "website": request.website,
            "industry": request.industry,
            "enrichment_report": str(crew_result),
            "execution_id": execution_id,
            "model_used": "llama3.1:70b",
            "fields_requested": request.fields_to_enrich,
            "last_updated": datetime.now().isoformat()
        }

        return WebhookResponse(
            success=True,
            crew_type="lead_enrichment",
            execution_id=execution_id,
            status="completed",
            result=enriched_data,
            timestamp=datetime.now().isoformat(),
            execution_time_seconds=execution_time
        )

    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        print(f"\n❌ ERROR: {str(e)}\n")

        return WebhookResponse(
            success=False,
            crew_type="lead_enrichment",
            execution_id=execution_id,
            status="failed",
            error=str(e),
            timestamp=datetime.now().isoformat(),
            execution_time_seconds=execution_time
        )


if __name__ == "__main__":
    # Check for API key
    if API_KEY == "waltersignal-dev-key-12345":
        print("⚠️  WARNING: Using default API key. Set ZAPIER_API_KEY environment variable in production!")

    print("🚀 Starting WalterSignal Zapier Webhook Server v2...")
    print("📍 Version: 2.0.0 (Real CrewAI Integration)")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print(f"🔗 Server will run on: http://0.0.0.0:8001")
    print(f"📚 API Docs: http://0.0.0.0:8001/docs")
    print(f"🤖 LLM: llama3.1:70b @ 192.168.68.88:11434")
    print()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
