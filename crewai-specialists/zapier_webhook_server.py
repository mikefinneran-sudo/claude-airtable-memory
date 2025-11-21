#!/usr/bin/env python3
"""
WalterSignal Zapier Webhook Server
FastAPI server that receives webhooks from Zapier and triggers CrewAI specialists

Usage:
    python zapier_webhook_server.py

Endpoints:
    POST /webhook/research - Trigger research crew
    POST /webhook/design - Trigger design crew
    POST /webhook/lead-enrichment - Enrich lead data
    GET /health - Health check
"""

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uvicorn
import os
from datetime import datetime
import json
from pathlib import Path
import sys

# Add crews to path
CREWS_DIR = Path(__file__).parent / "crews"
sys.path.insert(0, str(CREWS_DIR))

app = FastAPI(
    title="WalterSignal CrewAI Webhook Server",
    description="Zapier integration for CrewAI specialists",
    version="1.0.0"
)

# Security - API Key authentication
API_KEY = os.getenv("ZAPIER_API_KEY", "waltersignal-dev-key-12345")  # Change in production!

def verify_api_key(x_api_key: str = Header(None)):
    """Verify API key from header"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


# Request Models
class ResearchRequest(BaseModel):
    """Request model for research crew"""
    topic: str = Field(..., description="Research topic or query")
    depth: Optional[str] = Field("standard", description="Research depth: quick, standard, deep")
    output_format: Optional[str] = Field("markdown", description="Output format: markdown, json, pdf")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata from Zapier")


class DesignRequest(BaseModel):
    """Request model for design crew"""
    task_type: str = Field(..., description="Design task: logo, brand, ui")
    company_name: Optional[str] = Field(None, description="Company name")
    description: str = Field(..., description="Design requirements")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata from Zapier")


class LeadEnrichmentRequest(BaseModel):
    """Request model for lead enrichment"""
    company_name: str = Field(..., description="Company name to enrich")
    website: Optional[str] = Field(None, description="Company website")
    industry: Optional[str] = Field(None, description="Industry sector")
    fields_to_enrich: Optional[list] = Field(
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


# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "WalterSignal CrewAI Webhook Server",
        "timestamp": datetime.utcnow().isoformat(),
        "available_endpoints": [
            "/webhook/research",
            "/webhook/design",
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
    Trigger research crew from Zapier

    Example Zapier webhook data:
    {
        "topic": "AI consulting market in Chicago",
        "depth": "deep",
        "output_format": "markdown"
    }
    """
    verify_api_key(x_api_key)

    execution_id = f"research_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    start_time = datetime.utcnow()

    try:
        # TODO: Import and execute actual research crew
        # For now, returning mock response
        result = {
            "topic": request.topic,
            "depth": request.depth,
            "findings": "Research crew execution placeholder",
            "sources": [],
            "summary": f"Researched: {request.topic}",
            "output_file": f"/outputs/{execution_id}.md"
        }

        execution_time = (datetime.utcnow() - start_time).total_seconds()

        return WebhookResponse(
            success=True,
            crew_type="research",
            execution_id=execution_id,
            status="completed",
            result=result,
            timestamp=datetime.utcnow().isoformat(),
            execution_time_seconds=execution_time
        )

    except Exception as e:
        return WebhookResponse(
            success=False,
            crew_type="research",
            execution_id=execution_id,
            status="failed",
            error=str(e),
            timestamp=datetime.utcnow().isoformat()
        )


@app.post("/webhook/design", response_model=WebhookResponse)
async def design_webhook(
    request: DesignRequest,
    x_api_key: str = Header(None)
):
    """
    Trigger design crew from Zapier

    Example Zapier webhook data:
    {
        "task_type": "logo",
        "company_name": "TechCorp",
        "description": "Modern tech company needs minimalist logo"
    }
    """
    verify_api_key(x_api_key)

    execution_id = f"design_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    start_time = datetime.utcnow()

    try:
        # TODO: Import and execute actual design crew
        result = {
            "task_type": request.task_type,
            "company_name": request.company_name,
            "description": request.description,
            "status": "Design crew execution placeholder",
            "output_files": []
        }

        execution_time = (datetime.utcnow() - start_time).total_seconds()

        return WebhookResponse(
            success=True,
            crew_type="design",
            execution_id=execution_id,
            status="completed",
            result=result,
            timestamp=datetime.utcnow().isoformat(),
            execution_time_seconds=execution_time
        )

    except Exception as e:
        return WebhookResponse(
            success=False,
            crew_type="design",
            execution_id=execution_id,
            status="failed",
            error=str(e),
            timestamp=datetime.utcnow().isoformat()
        )


@app.post("/webhook/lead-enrichment", response_model=WebhookResponse)
async def lead_enrichment_webhook(
    request: LeadEnrichmentRequest,
    x_api_key: str = Header(None)
):
    """
    Enrich lead data using research crew

    Example Zapier webhook data:
    {
        "company_name": "Acme Corp",
        "website": "https://acme.com",
        "industry": "Manufacturing",
        "fields_to_enrich": ["company_info", "decision_makers", "pain_points"]
    }
    """
    verify_api_key(x_api_key)

    execution_id = f"enrich_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    start_time = datetime.utcnow()

    try:
        # TODO: Import and execute lead enrichment crew
        # This would use research_organizer_elite crew
        enriched_data = {
            "company_name": request.company_name,
            "website": request.website,
            "industry": request.industry,
            "enriched_fields": {
                "company_info": {
                    "description": "Lead enrichment placeholder",
                    "employee_count": "Unknown",
                    "revenue": "Unknown",
                    "headquarters": "Unknown"
                },
                "decision_makers": [
                    {
                        "name": "Placeholder",
                        "title": "CEO",
                        "linkedin": None
                    }
                ],
                "pain_points": [
                    "Identified pain points would appear here"
                ],
                "tech_stack": [
                    "Technology stack would be listed here"
                ]
            },
            "confidence_score": 0.0,
            "last_updated": datetime.utcnow().isoformat()
        }

        execution_time = (datetime.utcnow() - start_time).total_seconds()

        return WebhookResponse(
            success=True,
            crew_type="lead_enrichment",
            execution_id=execution_id,
            status="completed",
            result=enriched_data,
            timestamp=datetime.utcnow().isoformat(),
            execution_time_seconds=execution_time
        )

    except Exception as e:
        return WebhookResponse(
            success=False,
            crew_type="lead_enrichment",
            execution_id=execution_id,
            status="failed",
            error=str(e),
            timestamp=datetime.utcnow().isoformat()
        )


# Generic webhook receiver (for testing)
@app.post("/webhook/generic")
async def generic_webhook(
    request: Request,
    x_api_key: str = Header(None)
):
    """
    Generic webhook receiver for testing
    Accepts any JSON payload and logs it
    """
    verify_api_key(x_api_key)

    body = await request.json()

    return {
        "success": True,
        "message": "Webhook received",
        "received_data": body,
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    # Check for API key
    if API_KEY == "waltersignal-dev-key-12345":
        print("⚠️  WARNING: Using default API key. Set ZAPIER_API_KEY environment variable in production!")

    print("🚀 Starting WalterSignal Zapier Webhook Server...")
    print(f"📍 API Key: {API_KEY[:10]}...")
    print(f"🔗 Server will run on: http://0.0.0.0:8001")
    print(f"📚 API Docs: http://0.0.0.0:8001/docs")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
