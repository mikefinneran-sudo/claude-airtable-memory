# Clay.com + CrewAI Specialists Integration Plan
**WalterSignal Agentic Automation Architecture**

**Created:** 2025-11-13
**Status:** Planning Phase
**Priority:** High - Strategic Capability Enhancement

---

## Executive Summary

This plan outlines the integration of Clay.com's programmable data engine with WalterSignal's CrewAI specialist agents to create an advanced agentic GTM automation system. The integration transforms Clay tables from passive data stores into active orchestration layers for multi-agent AI workflows.

### Strategic Value

1. **Data Orchestration Hub**: Clay becomes the central nervous system for all CrewAI specialist operations
2. **100+ Data Sources**: Instant access to enrichment providers without individual API integrations
3. **State Management**: Clay tables manage task queues, agent state, and results persistence
4. **GTM Automation**: End-to-end workflows from lead sourcing to AI-powered outreach
5. **Cost Efficiency**: Waterfall enrichments maximize data quality while minimizing API costs

---

## Part 1: Architecture Overview

### The Agentic Orchestration Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAY TABLE (State Manager)                │
│  ┌────────────┬──────────────┬────────────┬───────────────┐ │
│  │ Task Queue │ Data Context │ Agent Jobs │ Results Store │ │
│  └────────────┴──────────────┴────────────┴───────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ▲         │
                           │         │
                    ┌──────┴─────────▼──────┐
                    │   WEBHOOK BRIDGE      │
                    │   (Update via Dedupe) │
                    └──────▲─────────┬──────┘
                           │         │
                           │         ▼
┌──────────────────────────┴──────────────────────────────────┐
│              CREWAI SPECIALIST FRAMEWORK (DGX)              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ LLM Router (25 models) → Specialist Crews          │   │
│  │  • Design Crew    • Research Crew                   │   │
│  │  • Marketing Crew • Data Crew                       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Core Integration Patterns

**Pattern 1: Clay → CrewAI (Task Provisioning)**
- Clay table identifies tasks (e.g., "Enrich 500 leads")
- Webhook or scheduled script triggers CrewAI specialists
- Agents receive pre-enriched context from Clay

**Pattern 2: CrewAI → Clay (Results Persistence)**
- CrewAI agents complete tasks (research, content, analysis)
- POST results back to Clay via webhook URL
- Auto-dedupe feature merges results into existing rows

**Pattern 3: Bi-Directional Loop (Full Orchestration)**
- Clay provisions tasks with rich context
- CrewAI executes complex multi-agent workflows
- Results update Clay tables, triggering downstream actions
- CRM/outreach tools consume final enriched data

---

## Part 2: Specialist-Specific Use Cases

### Use Case 1: Marketing Crew + Clay Lead Engine

**Objective:** Automated B2B lead sourcing, enrichment, and hyper-personalized outreach

**Clay Table Architecture:**
```
Table: "Lead_Generation_Master"
Columns:
1. company_domain (Text, Unique Key)
2. company_name (Find Companies)
3. industry (Auto-enriched)
4. headcount (Auto-enriched)
5. technologies_used (Auto-enriched)
6. icp_score (Formula: ICP matching logic)
7. decision_makers (Find People → Write to "People" table)
8. crew_task_status (Select: new, pending, complete)
9. personalization_brief (CrewAI result)
10. outreach_sequence (CrewAI result)
```

**CrewAI Marketing Crew Workflow:**
1. **Data Analyst Agent**: Reviews enriched company data, identifies key insights
2. **Research Agent**: Uses Perplexity MCP to find recent company news/launches
3. **Copywriter Agent**: Generates personalized outreach angles
4. **Campaign Manager Agent**: Creates multi-touch sequence (email, LinkedIn, ads)

**Integration Flow:**
1. Clay finds companies matching ICP criteria
2. Waterfall enrichments add firmographics, tech stack, contacts
3. Filtered view shows `icp_score > 8 AND crew_task_status == 'new'`
4. Python script POSTs filtered rows to CrewAI API endpoint
5. Marketing crew processes each company (parallel execution)
6. Results POST back to Clay webhook with `company_domain` as unique key
7. Auto-dedupe merges personalization into existing rows
8. Final column pushes to HubSpot/Outreach.io (Only run if complete == true)

---

### Use Case 2: Design Crew + Clay Website Audit Pipeline

**Objective:** Automated website design audits and improvement recommendations

**Clay Table Architecture:**
```
Table: "Website_Audit_Queue"
Columns:
1. website_url (Text, Unique Key)
2. company_name (Enrich from domain)
3. industry (Auto-enriched)
4. screenshot_url (Puppeteer MCP capture)
5. lighthouse_score (HTTP API to PageSpeed)
6. accessibility_score (HTTP API)
7. competitor_urls (Claygent research)
8. crew_task_status (Select: new, in_progress, complete)
9. visual_analysis (Visual Analyst Agent result)
10. ui_recommendations (UI Designer Agent result)
11. brand_assessment (Brand Designer Agent result)
12. implementation_plan (Project Manager Agent result)
```

**CrewAI Design Crew Workflow:**
1. **Visual Content Analyst**: Analyzes screenshots, competitors, identifies issues
2. **Web UI Designer**: Creates UI/UX recommendations
3. **Graphic Brand Designer**: Develops brand asset specifications
4. **Business Ops Manager**: Synthesizes into actionable project plan

**Integration Flow:**
1. New website URLs added to Clay table (webhook from lead capture)
2. Auto-update enrichments run: screenshot, Lighthouse, competitor research
3. Once enriched, `crew_task_status` set to 'pending'
4. Scheduled Python script finds pending rows
5. For each row, triggers Design Crew with context (screenshot URL, scores, competitor data)
6. Design crew executes full analysis (4 agents, sequential process)
7. Each agent result POSTs back via webhook with `website_url` as unique key
8. Auto-dedupe merges all 4 agent outputs into single row
9. Final status: 'complete' triggers email report to prospect

---

### Use Case 3: Research Crew + Clay Competitive Intel System

**Objective:** Automated competitive intelligence gathering and analysis

**Clay Table Architecture:**
```
Table: "Competitive_Intelligence"
Columns:
1. competitor_domain (Text, Unique Key)
2. competitor_name (Find Company)
3. recent_funding (Crunchbase enrichment)
4. product_launches (Claygent: "Find recent launches")
5. job_postings (Claygent: "Check job boards")
6. tech_stack_changes (BuiltWith enrichment)
7. social_sentiment (Claygent: Reddit/Twitter scan)
8. crew_task_status (Select)
9. strategic_analysis (Research Organizer Elite result)
10. threat_assessment (Research result)
11. opportunity_insights (Research result)
```

**CrewAI Research Crew Workflow:**
1. **Research Manager**: Orchestrates multi-source intelligence gathering
2. **Market Analyst**: Analyzes competitive positioning, pricing
3. **Product Analyst**: Reverse-engineers product strategy from signals
4. **Strategic Advisor**: Synthesizes into actionable intel brief

**Integration Flow:**
1. Clay monitors competitor domains (weekly auto-refresh)
2. Enrichments detect changes (new funding, product launch, job posting surge)
3. Change detection triggers `crew_task_status = 'pending'`
4. Research crew pulls comprehensive context from Clay row
5. Perplexity MCP performs deep-dive research on detected changes
6. Multi-agent analysis produces strategic brief
7. Results POST back to Clay, triggering Slack notification to exec team

---

### Use Case 4: Data Crew + Clay TAM Sourcing Engine

**Objective:** Total Addressable Market (TAM) identification and territory planning

**Clay Table Architecture:**
```
Table: "TAM_Master_Database"
Columns:
1. account_id (Text, Unique Key)
2. company_name (Find Companies: filters for ICP)
3. industry_segment (Auto-enriched)
4. annual_revenue (Auto-enriched)
5. employee_count (Auto-enriched)
6. decision_maker_count (Find People count)
7. tech_fit_score (Formula: tech stack alignment)
8. geographic_segment (Formula: territory assignment)
9. crew_task_status (Select)
10. account_profile (Data Crew AI summary)
11. territory_assignment (Data Crew result)
12. priority_tier (Data Crew scoring: Tier 1/2/3)
```

**CrewAI Data Crew Workflow:**
1. **Data Engineer Agent**: Validates and cleans enrichment data
2. **Analytics Agent**: Calculates propensity scores, segmentation
3. **Territory Planner Agent**: Assigns accounts to sales territories
4. **Reporting Agent**: Generates executive TAM dashboard data

**Integration Flow:**
1. Clay sources 50,000 companies matching broad ICP criteria
2. Waterfall enrichments maximize data completeness (revenue, headcount, tech)
3. Conditional runs prevent expensive enrichments on non-ICP accounts
4. Data crew processes in batches of 1,000 (managed via filtered views)
5. Segmentation, scoring, and territory logic applied
6. Results update Clay table via webhook
7. Final sync to CRM: Only run if `priority_tier == 'Tier 1'`

---

## Part 3: Technical Implementation

### Phase 1: Foundation Setup (Week 1-2)

**1.1 Clay Account Configuration**
- [ ] Provision Clay workspace (Starter plan minimum for Google Sheets sync)
- [ ] Create workbook structure for specialist teams
- [ ] Configure Auto-dedupe on all master tables
- [ ] Set up webhook endpoints for each specialist crew

**1.2 CrewAI-Clay Bridge Development**
- [ ] Create `clay_integration.py` module in `/crewai-specialists/integrations/`
- [ ] Implement webhook POST functions with retry logic
- [ ] Build "Update via Dedupe" pattern handler
- [ ] Create task queue polling scripts

**1.3 Knowledge Base Transfer**
- [ ] Copy Clay.com guide to DGX: `/training/knowledge-base/`
- [ ] Create specialist-specific Clay workflow templates
- [ ] Document field mapping schemas for each crew

### Phase 2: Pilot Integration (Week 3-4)

**2.1 Marketing Crew Pilot**
- [ ] Build "Lead_Generation_Master" table in Clay
- [ ] Configure Find Companies source (50 test companies)
- [ ] Set up waterfall enrichments (email, LinkedIn, firmographics)
- [ ] Connect Marketing crew to process 10 test leads
- [ ] Validate webhook round-trip (Clay → Crew → Clay)

**2.2 Design Crew Pilot**
- [ ] Build "Website_Audit_Queue" table
- [ ] Integrate Puppeteer MCP for screenshot capture
- [ ] Connect Lighthouse API for performance scoring
- [ ] Test Design crew with 5 website audits
- [ ] Verify multi-agent results merge correctly

**2.3 Error Handling & Monitoring**
- [ ] Implement Clay "Errored Rows" view monitoring
- [ ] Create Slack alerts for crew failures
- [ ] Build retry queue for failed webhook POSTs
- [ ] Set up cost tracking dashboard (Clay credits + LLM tokens)

### Phase 3: Advanced Patterns (Week 5-6)

**3.1 Multi-Table Orchestration**
- [ ] Implement "Companies" → "People" relational pattern
- [ ] Use "Write to Table" for task spawning
- [ ] Create lookup patterns for cross-table enrichment
- [ ] Build aggregation views for reporting

**3.2 Conditional Logic & Gating**
- [ ] Implement "Only run if" conditional chains
- [ ] Create checkbox columns for manual review gates
- [ ] Build ICP scoring formulas with Clayscript
- [ ] Set up filtered views for batch processing

**3.3 CRM Integration**
- [ ] Configure HubSpot "Clay-owned" custom fields
- [ ] Implement sandbox testing workflow
- [ ] Create controlled batch update scripts
- [ ] Set up data ownership governance rules

### Phase 4: Production Scale (Week 7-8)

**4.1 High-Volume Workflows**
- [ ] Implement "Passthrough Table" pattern for real-time webhooks
- [ ] Configure automated row deletion for processed tasks
- [ ] Build monitoring for 50k row limit management
- [ ] Optimize enrichment costs with own API keys

**4.2 Agentic Frameworks**
- [ ] Full CrewAI orchestration loop for each specialist team
- [ ] Scheduled polling scripts (cron on DGX)
- [ ] Priority queue management (Tier 1 → Tier 2 → Tier 3)
- [ ] Results aggregation and executive dashboards

**4.3 Documentation & Training**
- [ ] Create runbooks for each specialist workflow
- [ ] Document troubleshooting procedures
- [ ] Build cost optimization guidelines
- [ ] Train team on Clay + CrewAI operations

---

## Part 4: Technical Reference

### Clay-CrewAI Bridge Code Structure

```python
# /crewai-specialists/integrations/clay_integration.py

import requests
import time
from typing import Dict, List, Optional
import logging

class ClayBridge:
    """Integration layer between CrewAI specialists and Clay tables"""

    def __init__(self, table_webhook_url: str, unique_key_field: str):
        """
        Initialize Clay table connection

        Args:
            table_webhook_url: Clay table's webhook endpoint
            unique_key_field: Field name for auto-dedupe (e.g., 'email', 'task_id')
        """
        self.webhook_url = table_webhook_url
        self.unique_key = unique_key_field
        self.logger = logging.getLogger(__name__)

    def push_results(self, data: Dict, retry_count: int = 3) -> bool:
        """
        Push CrewAI results back to Clay table using Update via Dedupe pattern

        Args:
            data: Dictionary with unique_key + result fields
            retry_count: Number of retry attempts

        Returns:
            bool: Success status
        """
        if self.unique_key not in data:
            raise ValueError(f"Data must contain unique key field: {self.unique_key}")

        for attempt in range(retry_count):
            try:
                response = requests.post(
                    self.webhook_url,
                    json=data,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )

                if response.status_code == 200:
                    self.logger.info(f"Successfully pushed results for {data[self.unique_key]}")
                    return True
                else:
                    self.logger.warning(f"Attempt {attempt + 1} failed: {response.status_code}")

            except Exception as e:
                self.logger.error(f"Error on attempt {attempt + 1}: {e}")

            time.sleep(2 ** attempt)  # Exponential backoff

        return False

    def fetch_pending_tasks(self, export_url: str) -> List[Dict]:
        """
        Fetch tasks with status='pending' from Clay table CSV export

        Args:
            export_url: Clay table CSV export URL

        Returns:
            List of task dictionaries
        """
        # Implementation: Parse CSV, filter for pending tasks
        pass

    def update_task_status(self, task_id: str, status: str, results: Optional[Dict] = None):
        """
        Update task status in Clay table

        Args:
            task_id: Unique task identifier
            status: New status (pending, in_progress, complete, error)
            results: Optional results payload
        """
        payload = {
            self.unique_key: task_id,
            "crew_task_status": status
        }

        if results:
            payload.update(results)

        return self.push_results(payload)


# Example Usage with Marketing Crew
from crews.marketing_crew import create_marketing_crew

def process_clay_lead(lead_data: Dict, clay_bridge: ClayBridge):
    """Process a single lead from Clay table with Marketing Crew"""

    # Extract lead context
    company = lead_data.get('company_name')
    domain = lead_data.get('company_domain')
    industry = lead_data.get('industry')
    tech_stack = lead_data.get('technologies_used')

    # Mark as in_progress
    clay_bridge.update_task_status(domain, 'in_progress')

    try:
        # Create crew with lead context
        crew = create_marketing_crew(
            task_description=f"""
            Create hyper-personalized outreach for {company} ({industry}).
            Tech stack: {tech_stack}
            Domain: {domain}

            Generate:
            1. Personalization brief (key insights, pain points)
            2. 3-email sequence (cold → value → ask)
            3. LinkedIn connection message
            """,
            expected_output="Complete outreach package with personalization"
        )

        # Execute crew
        result = crew.kickoff()

        # Parse results (assuming structured output)
        results_payload = {
            domain: domain,  # Unique key
            'personalization_brief': result.personalization_brief,
            'email_sequence': result.email_sequence,
            'linkedin_message': result.linkedin_message,
            'crew_task_status': 'complete'
        }

        # Push back to Clay
        clay_bridge.push_results(results_payload)

    except Exception as e:
        # Mark as error
        clay_bridge.update_task_status(domain, 'error', {'error_message': str(e)})
        raise
```

### Scheduled Task Polling Script

```python
# /crewai-specialists/scripts/clay_task_processor.py

import os
import sys
from pathlib import Path
import time
import logging

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integrations.clay_integration import ClayBridge
from crews.marketing_crew import create_marketing_crew

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
CLAY_WEBHOOK_URL = os.getenv('CLAY_MARKETING_WEBHOOK_URL')
CLAY_EXPORT_URL = os.getenv('CLAY_MARKETING_EXPORT_URL')
BATCH_SIZE = 10
POLL_INTERVAL = 300  # 5 minutes

def main():
    """Main polling loop for Clay task processing"""

    clay_bridge = ClayBridge(
        table_webhook_url=CLAY_WEBHOOK_URL,
        unique_key_field='company_domain'
    )

    logger.info("🚀 Clay task processor started")

    while True:
        try:
            # Fetch pending tasks from Clay
            pending_tasks = clay_bridge.fetch_pending_tasks(CLAY_EXPORT_URL)

            if not pending_tasks:
                logger.info("No pending tasks, sleeping...")
                time.sleep(POLL_INTERVAL)
                continue

            logger.info(f"📋 Found {len(pending_tasks)} pending tasks")

            # Process in batches
            for i in range(0, len(pending_tasks), BATCH_SIZE):
                batch = pending_tasks[i:i + BATCH_SIZE]

                logger.info(f"Processing batch {i // BATCH_SIZE + 1}")

                for task in batch:
                    try:
                        process_clay_lead(task, clay_bridge)
                    except Exception as e:
                        logger.error(f"Failed to process {task['company_domain']}: {e}")

                # Rate limiting between batches
                time.sleep(10)

        except KeyboardInterrupt:
            logger.info("👋 Shutting down gracefully")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    main()
```

### Cron Setup on DGX

```bash
# Add to crontab on DGX server
# Run Clay task processor every 5 minutes
*/5 * * * * /home/mikefinneran/crewai-specialists/venv/bin/python /home/mikefinneran/crewai-specialists/scripts/clay_task_processor.py >> /home/mikefinneran/crewai-specialists/logs/clay-processor.log 2>&1
```

---

## Part 5: Cost & Performance Optimization

### Clay Credit Management

**Best Practices:**
1. **Disable Auto-Update by Default**: Prevent accidental mass enrichments
2. **Use Own API Keys**: Connect direct to providers (50-70% cheaper than Clay credits)
3. **Conditional Gating**: Only run expensive enrichments on qualified rows
4. **Batch Processing**: Use filtered views to control enrichment volume
5. **Test on Samples**: Always test on 10 rows before running on 1,000+

**Estimated Costs (per 1,000 leads):**
- Clay credits (waterfall email + LinkedIn enrichment): ~$150-200
- Own API keys (Prospeo + Phantombuster): ~$50-75
- CrewAI LLM costs (local Ollama): $0 (compute only)
- CrewAI commercial models (GPT-4o for final polish): ~$20-30

**Total per-lead cost:** $0.20-0.30 (fully enriched + AI personalization)

### LLM Router Optimization

**Strategy:** Use Clay data to intelligently route to appropriate LLM

```python
# Example: Route based on task complexity
def route_enrichment_task(clay_row):
    """Route to optimal LLM based on Clay data richness"""

    data_completeness = calculate_completeness(clay_row)

    if data_completeness > 80:
        # Rich context → use faster local model
        return "llama3.1:70b"
    elif data_completeness > 50:
        # Medium context → use balanced model
        return "mixtral:8x7b"
    else:
        # Sparse data → use reasoning model to infer
        return "deepseek-r1:70b"
```

### Performance Metrics

**Target KPIs:**
- **Lead Enrichment Throughput**: 1,000 leads/hour
- **CrewAI Processing Time**: 30-60 seconds per lead (4-agent workflow)
- **End-to-End Latency**: < 5 minutes (Clay → Crew → Clay → CRM)
- **Data Accuracy**: > 95% (waterfall enrichment validation)
- **Cost per Qualified Lead**: < $0.50 (enrichment + AI personalization + CRM sync)

---

## Part 6: Success Metrics & ROI

### Quantitative Metrics

**Efficiency Gains:**
- Manual research time per lead: 15-20 minutes
- Automated enrichment + AI: 1-2 minutes
- **Time savings:** 87-93% per lead

**Cost Comparison:**
- SDR fully-loaded cost: $75-100/hour ($18.75-25 per lead @ 4 leads/hour)
- Clay + CrewAI automation: $0.20-0.50 per lead
- **Cost reduction:** 97-98%

**Scale Unlocked:**
- Manual capacity: 30-40 leads/day/SDR
- Automated capacity: 1,000+ leads/day
- **Volume increase:** 25-33x

### Qualitative Metrics

1. **Personalization Depth**: AI can analyze 100+ data points vs. SDR's 5-10
2. **Consistency**: Every lead gets same quality analysis
3. **Speed to Market**: Launch campaigns in hours, not weeks
4. **Sales Focus**: Reps spend time on calls, not research

---

## Part 7: Risk Mitigation

### Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Clay API rate limits | High | Implement rate limiting, use batch processing |
| Webhook failures | Medium | Retry logic, dead letter queue, monitoring alerts |
| Auto-dedupe conflicts | Medium | Enforce unique key validation, test in sandbox |
| Data overwrites in CRM | High | Clay-owned fields only, manual approval gates |
| 50k row table limit | Medium | Passthrough pattern, automated archival |

### Operational Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Unexpected Clay credit spend | High | Disable auto-update, approval workflows, budget alerts |
| Incorrect data enrichment | Medium | Waterfall validation, human spot-checks, error views |
| Agent hallucinations | Medium | Chain-of-thought prompts, validation agents, human review |
| Scaling costs (LLM tokens) | Medium | Hybrid local/commercial routing, batch optimization |

### Compliance Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| GDPR/data privacy violations | High | Data retention policies, consent tracking, EU data residency |
| Email deliverability issues | Medium | Use verified emails only, warm-up sequences |
| Anti-spam regulations | High | Opt-out mechanisms, legitimate interest basis |

---

## Part 8: Next Steps

### Immediate Actions (This Week)

1. **Review & Approve Plan**: Stakeholder sign-off on architecture and scope
2. **Provision Clay Account**: Set up workspace, configure webhooks
3. **Create Pilot Tables**: Build "Lead_Generation_Master" and "Website_Audit_Queue"
4. **Develop Clay Bridge**: Code `clay_integration.py` module
5. **Test Round-Trip**: Validate Clay → Crew → Clay → CRM flow with 10 test records

### Phase 1 Deliverables (Week 1-2)

- [ ] Clay workspace operational with 2 pilot tables
- [ ] Webhook integration tested and validated
- [ ] `clay_integration.py` module production-ready
- [ ] Documentation: setup guide, field mapping schemas
- [ ] Demo: End-to-end automation for 10 test leads

### Long-Term Roadmap

**Q1 2025:**
- Marketing Crew + Lead Engine (1,000 leads/month)
- Design Crew + Website Audit Pipeline (50 audits/month)

**Q2 2025:**
- Research Crew + Competitive Intel (20 competitors monitored)
- Data Crew + TAM Sourcing (50,000 accounts segmented)

**Q3 2025:**
- Multi-crew orchestration (leads → research → outreach → close)
- Advanced agentic patterns (self-healing, dynamic routing)

**Q4 2025:**
- Enterprise scale (100,000+ leads/month)
- White-label offering for clients

---

## Appendix A: Clay Table Schemas

### Marketing: Lead_Generation_Master

```yaml
table_name: Lead_Generation_Master
auto_dedupe: company_domain
row_limit: 50000

columns:
  - name: company_domain
    type: text
    unique_key: true

  - name: company_name
    type: text
    source: find_companies

  - name: industry
    type: text
    enrichment: apollo_company

  - name: headcount
    type: number
    enrichment: clearbit_company

  - name: annual_revenue
    type: currency
    enrichment: zoominfo_company

  - name: technologies_used
    type: text
    enrichment: builtwith
    only_run_if: "{{headcount}} > 100"

  - name: icp_score
    type: number
    formula: |
      IF(
        ({{headcount}} > 100 && {{annual_revenue}} > 10000000) &&
        ({{industry}}.includes('Software') || {{industry}}.includes('SaaS')),
        10,
        IF({{headcount}} > 50 && {{annual_revenue}} > 5000000, 7, 3)
      )

  - name: decision_makers
    type: text
    source: find_people
    filters:
      job_titles: ["VP", "Director", "Head of", "Chief"]
      departments: ["Marketing", "Sales", "Revenue"]
    write_to_table: Lead_Generation_People

  - name: crew_task_status
    type: select
    options: [new, pending, in_progress, complete, error]
    default: new

  - name: personalization_brief
    type: text
    source: crewai_webhook_result

  - name: email_sequence
    type: text
    source: crewai_webhook_result

  - name: linkedin_message
    type: text
    source: crewai_webhook_result

  - name: hubspot_sync
    type: integration
    destination: hubspot
    action: create_or_update_contact
    only_run_if: "{{crew_task_status}} == 'complete' && {{icp_score}} >= 7"
```

### Design: Website_Audit_Queue

```yaml
table_name: Website_Audit_Queue
auto_dedupe: website_url
row_limit: 10000

columns:
  - name: website_url
    type: url
    unique_key: true

  - name: company_name
    type: text
    enrichment: clearbit_company
    input: "{{website_url}}"

  - name: industry
    type: text
    enrichment: clearbit_company

  - name: screenshot_url
    type: image_from_url
    enrichment: http_api
    endpoint: "puppeteer_screenshot_service"

  - name: lighthouse_score
    type: number
    enrichment: http_api
    endpoint: "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

  - name: accessibility_score
    type: number
    enrichment: http_api
    endpoint: "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

  - name: competitor_urls
    type: text
    enrichment: claygent
    prompt: "Find 3 main competitors for {{company_name}} in {{industry}}"

  - name: crew_task_status
    type: select
    options: [new, pending, in_progress, complete]
    default: new

  - name: visual_analysis
    type: text
    source: crewai_webhook_result

  - name: ui_recommendations
    type: text
    source: crewai_webhook_result

  - name: brand_assessment
    type: text
    source: crewai_webhook_result

  - name: implementation_plan
    type: text
    source: crewai_webhook_result
```

---

## Appendix B: Training Materials Integration

**Clay.com Knowledge Base Location:**
- DGX: `/home/mikefinneran/crewai-specialists/training/knowledge-base/`
- Files to create:
  - `Clay-Complete-Guide.md` (this guide, copied)
  - `Clay-Marketing-Crew-Workflows.md` (specialist templates)
  - `Clay-Design-Crew-Workflows.md`
  - `Clay-Research-Crew-Workflows.md`
  - `Clay-Data-Crew-Workflows.md`

**Training Cases to Add:**
1. **marketing-clay-001**: Lead sourcing + enrichment + AI personalization
2. **design-clay-002**: Website audit + competitive analysis + recommendations
3. **research-clay-003**: Competitive intelligence + threat assessment
4. **data-clay-004**: TAM sourcing + territory planning + segmentation

---

## Document Metadata

**Version:** 1.0
**Last Updated:** 2025-11-13
**Owner:** Mike Finneran
**Stakeholders:** WalterSignal Crew Specialists
**Related Docs:**
- `/training/waltersignal_design_deployment_training.yaml`
- `/training/knowledge-base/Clay.com Tables for Agentic Automation.md`
- `/crews/waltersignal_design/waltersignal_design_crew.py`

**Review Cycle:** Weekly during Phase 1-2, Monthly thereafter
**Next Review:** 2025-11-20
