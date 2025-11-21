#!/usr/bin/env python3
"""
WalterSignal Zapier Webhook Server v3 - With Hybrid LLM Router Integration
FastAPI server that receives webhooks from Zapier and uses the working LLM router

Usage:
    python zapier_webhook_server_v3.py

Endpoints:
    POST /webhook/research - Research using LLM router
    POST /webhook/lead-enrichment - Enrich lead data using LLM router
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
import subprocess

# LLM router will be called via subprocess (no imports needed)

app = FastAPI(
    title="WalterSignal CrewAI Webhook Server v3",
    description="Zapier integration with Hybrid LLM Router",
    version="3.0.0"
)

# Security - API Key authentication
API_KEY = os.getenv("ZAPIER_API_KEY", "waltersignal-dev-key-12345")

def verify_api_key(x_api_key: str = Header(None)):
    """Verify API key from header"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


# Request Models
class ResearchRequest(BaseModel):
    """Request model for research"""
    topic: str = Field(..., description="Research topic or query")
    depth: Optional[str] = Field("standard", description="Research depth: quick, standard, deep")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class LeadEnrichmentRequest(BaseModel):
    """Request model for lead enrichment"""
    company_name: str = Field(..., description="Company name to enrich")
    website: Optional[str] = Field(None, description="Company website")
    industry: Optional[str] = Field(None, description="Industry sector")
    fields_to_enrich: Optional[List[str]] = Field(
        default_factory=lambda: ["company_info", "decision_makers", "pain_points", "tech_stack"]
    )
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


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


def execute_with_llm(model_name: str, prompt: str) -> Dict[str, Any]:
    """
    Execute task using LLM router
    Calls the working execute_with_model.py script
    """
    router_dir = Path(__file__).parent / "llm-router"
    venv_python = Path(__file__).parent / "venv" / "bin" / "python"

    cmd = [
        str(venv_python),
        str(router_dir / "execute_with_model.py"),
        model_name,
        prompt
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=str(Path(__file__).parent)
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": f"LLM execution failed: {result.stderr}"
            }

        # Extract the answer from output
        output = result.stdout

        # Find the "Final Output:" section
        if "📄 Output:" in output:
            answer = output.split("📄 Output:")[1].strip()
            # Remove trailing trace batch info
            if "╭─" in answer:
                answer = answer.split("╭─")[0].strip()
        else:
            answer = output

        return {
            "success": True,
            "answer": answer,
            "raw_output": output
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "LLM execution timed out after 5 minutes"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"LLM execution error: {str(e)}"
        }


def select_model_for_task(task_type: str, complexity: str = "standard") -> str:
    """
    Select optimal model for the task
    Uses the same logic as the hybrid LLM router
    """
    if task_type == "research":
        if complexity == "quick":
            return "mistral:7b"  # Fast, simple
        elif complexity == "deep":
            return "deepseek-r1:70b"  # Max reasoning
        else:
            return "mixtral:8x7b"  # Balanced

    elif task_type == "lead_enrichment":
        return "mixtral:8x7b"  # Good for structured data extraction

    else:
        return "mistral:7b"  # Default to fastest


# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "WalterSignal CrewAI Webhook Server v3",
        "version": "3.0.0",
        "integration": "Hybrid LLM Router",
        "models_available": 25,
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
    Trigger research using LLM router

    Example:
    {
        "topic": "AI consulting market in Chicago",
        "depth": "deep"
    }
    """
    verify_api_key(x_api_key)

    execution_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    start_time = datetime.now()

    try:
        print(f"\n{'='*80}")
        print(f"🔬 RESEARCH REQUEST")
        print(f"{'='*80}")
        print(f"Topic: {request.topic}")
        print(f"Depth: {request.depth}")
        print(f"Execution ID: {execution_id}")

        # Select model based on depth
        model = select_model_for_task("research", request.depth)
        print(f"Selected Model: {model}")
        print(f"{'='*80}\n")

        # Build research prompt
        detail_level = {
            "quick": "Provide a concise 2-3 paragraph summary.",
            "standard": "Provide a comprehensive 5-paragraph analysis with key findings.",
            "deep": "Conduct deep research with extensive analysis, 10+ key findings, and sources."
        }.get(request.depth, "Provide a comprehensive analysis.")

        prompt = f"""Research the following topic: {request.topic}

{detail_level}

Include:
1. Overview and context
2. Key findings
3. Trends and patterns
4. Recommendations

Format your response clearly and concisely."""

        # Execute with LLM router
        llm_result = execute_with_llm(model, prompt)

        execution_time = (datetime.now() - start_time).total_seconds()

        if not llm_result.get("success"):
            raise Exception(llm_result.get("error", "Unknown error"))

        print(f"\n{'='*80}")
        print(f"✅ RESEARCH COMPLETE")
        print(f"Execution time: {execution_time:.2f}s")
        print(f"{'='*80}\n")

        result = {
            "topic": request.topic,
            "depth": request.depth,
            "findings": llm_result.get("answer", ""),
            "model_used": model,
            "execution_id": execution_id,
            "cost_usd": 0.0  # Local models are free
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
    Enrich lead data using LLM router

    Example:
    {
        "company_name": "Acme Corp",
        "website": "https://acme.com",
        "industry": "Manufacturing"
    }
    """
    verify_api_key(x_api_key)

    execution_id = f"enrich_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    start_time = datetime.now()

    try:
        print(f"\n{'='*80}")
        print(f"💼 LEAD ENRICHMENT REQUEST")
        print(f"{'='*80}")
        print(f"Company: {request.company_name}")
        print(f"Website: {request.website}")
        print(f"Industry: {request.industry}")
        print(f"Execution ID: {execution_id}")

        # Select model for lead enrichment
        model = select_model_for_task("lead_enrichment")
        print(f"Selected Model: {model}")
        print(f"{'='*80}\n")

        # Build enrichment prompt
        query_parts = [f"Company: {request.company_name}"]
        if request.website:
            query_parts.append(f"Website: {request.website}")
        if request.industry:
            query_parts.append(f"Industry: {request.industry}")

        prompt = f"""Gather intelligence about this company:
{' | '.join(query_parts)}

Provide the following information in a structured format:

1. COMPANY INFORMATION
   - Full name and description
   - Employee count estimate
   - Revenue estimate
   - Headquarters location
   - Year founded

2. DECISION MAKERS
   - CEO/Founder name
   - Key executives (CTO, VP Sales, etc.)

3. PAIN POINTS & CHALLENGES
   - Industry challenges
   - Business problems
   - Growth opportunities

4. TECHNOLOGY STACK
   - Known technologies
   - CRM, marketing tools
   - Development stack

5. BUSINESS INTELLIGENCE
   - Recent news
   - Funding status
   - Competitive position

Be specific and factual. If information is not available, state "Unknown"."""

        # Execute with LLM router
        llm_result = execute_with_llm(model, prompt)

        execution_time = (datetime.now() - start_time).total_seconds()

        if not llm_result.get("success"):
            raise Exception(llm_result.get("error", "Unknown error"))

        print(f"\n{'='*80}")
        print(f"✅ LEAD ENRICHMENT COMPLETE")
        print(f"Execution time: {execution_time:.2f}s")
        print(f"{'='*80}\n")

        enriched_data = {
            "company_name": request.company_name,
            "website": request.website,
            "industry": request.industry,
            "enrichment_report": llm_result.get("answer", ""),
            "model_used": model,
            "execution_id": execution_id,
            "fields_requested": request.fields_to_enrich,
            "cost_usd": 0.0,  # Local models are free
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
    if API_KEY == "waltersignal-dev-key-12345":
        print("⚠️  WARNING: Using default API key. Set ZAPIER_API_KEY in production!")

    print("🚀 Starting WalterSignal Zapier Webhook Server v3...")
    print("📍 Version: 3.0.0 (Hybrid LLM Router Integration)")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print(f"🔗 Server: http://0.0.0.0:8001")
    print(f"📚 API Docs: http://0.0.0.0:8001/docs")
    print(f"🤖 Models: 25 (20 free local + 5 commercial)")
    print()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
