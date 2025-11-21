#!/usr/bin/env python3
"""
Level 2 Example: Go-To-Market Strategy Crew using Agent Templates

Demonstrates how to:
1. Import agents from the template library
2. Customize templates with specific inputs
3. Combine multiple template agents into a crew
4. Reuse templates across different projects
"""
from crewai import Agent, Task, Crew, Process
from pathlib import Path
import yaml

# Load agent templates
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

def load_agent_templates():
    """Load all agent templates from library"""
    with open(TEMPLATES_DIR / "agent_library.yaml", 'r') as f:
        return yaml.safe_load(f)

def create_agent_from_template(template_name, templates, custom_inputs=None):
    """
    Create an Agent from a template with custom inputs

    Args:
        template_name: Name of template in agent_library.yaml
        templates: Loaded templates dictionary
        custom_inputs: Dict of {placeholder: value} to interpolate

    Returns:
        Agent instance
    """
    if template_name not in templates:
        raise ValueError(f"Template '{template_name}' not found in library")

    template = templates[template_name].copy()

    # Interpolate custom inputs if provided
    if custom_inputs:
        for key in ['role', 'goal', 'backstory']:
            if key in template:
                for placeholder, value in custom_inputs.items():
                    template[key] = template[key].replace(f'{{{placeholder}}}', str(value))

    return Agent(
        role=template['role'],
        goal=template['goal'],
        backstory=template['backstory'],
        verbose=template.get('verbose', True),
        allow_delegation=template.get('allow_delegation', False)
    )

def main():
    """
    Example: Build a Go-To-Market Strategy Crew for a new AI product

    Crew composition:
    - Competitive Intelligence (research competition)
    - Business Strategist (develop GTM strategy)
    - Marketing Copywriter (create messaging)
    - Sales Strategist (build sales playbook)
    """

    print("=" * 80)
    print("🎓 LEVEL 2: Using Agent Templates for GTM Strategy")
    print("=" * 80)
    print()

    # Load templates
    templates = load_agent_templates()
    print(f"✅ Loaded {len(templates)} agent templates from library")
    print()

    # Product context
    product_name = "WalterSignal CrewAI Platform"
    target_market = "Mid-market companies (100-1000 employees)"
    competitors = "LangChain, AutoGen, Microsoft Semantic Kernel"

    print("📊 Product Context:")
    print(f"   Product: {product_name}")
    print(f"   Market: {target_market}")
    print(f"   Competitors: {competitors}")
    print()
    print("=" * 80)
    print()

    # Create agents from templates with custom inputs
    print("🤖 Creating agents from templates...")
    print()

    competitive_intel = create_agent_from_template(
        'competitive_intelligence',
        templates,
        {'competitor': competitors}
    )
    print("✓ Competitive Intelligence Specialist (from template)")

    strategist = create_agent_from_template(
        'business_strategist',
        templates,
        {
            'strategy_type': 'Go-To-Market',
            'company': product_name,
            'objective': 'acquire first 50 customers'
        }
    )
    print("✓ Business Strategy Consultant (from template)")

    copywriter = create_agent_from_template(
        'marketing_copywriter',
        templates,
        {
            'content_type': 'product messaging',
            'desired_action': 'demo signups'
        }
    )
    print("✓ Marketing Copywriter (from template)")

    sales_expert = create_agent_from_template(
        'sales_strategist',
        templates,
        {
            'product': product_name,
            'market': target_market
        }
    )
    print("✓ Sales Strategy Specialist (from template)")

    print()
    print("=" * 80)
    print()

    # Define tasks (detailed descriptions following 80/20 rule)
    print("📋 Defining tasks...")
    print()

    task1 = Task(
        description=f"""
        Conduct comprehensive competitive analysis of: {competitors}

        For each competitor, analyze:
        1. Product features and capabilities
        2. Pricing model and packages
        3. Target market and ideal customer profile
        4. Key differentiators and unique value props
        5. Strengths and weaknesses
        6. Market positioning and messaging

        Identify:
        - Market gaps we can exploit
        - Features we need to match
        - Pricing opportunities
        - Positioning angles competitors haven't claimed

        Provide a SWOT analysis comparing our offering to the competitive landscape.
        """,
        expected_output="""
        A comprehensive competitive analysis report with:
        - Competitor comparison table (features, pricing, positioning)
        - SWOT analysis for {product_name} vs each competitor
        - List of 5-7 market gaps and opportunities
        - Recommended differentiation strategy
        - Pricing range based on competitive analysis
        """.format(product_name=product_name),
        agent=competitive_intel
    )

    task2 = Task(
        description=f"""
        Using the competitive intelligence, develop a complete Go-To-Market strategy
        for {product_name} targeting {target_market}.

        The strategy must include:

        1. Market Positioning:
           - Unique value proposition
           - Key differentiators vs competitors
           - Positioning statement

        2. Target Customer Profile:
           - Ideal customer profile (ICP)
           - Buyer personas (titles, pain points, goals)
           - Customer journey mapping

        3. Channel Strategy:
           - Primary acquisition channels (content, paid, partnerships, etc.)
           - Channel priorities and rationale
           - Resource allocation across channels

        4. Launch Plan:
           - 90-day roadmap with milestones
           - Success metrics and KPIs
           - Budget allocation recommendations

        5. Pricing Strategy:
           - Recommended pricing model (freemium, tiered, usage-based, etc.)
           - Pricing tiers and packaging
           - Rationale based on competitive analysis

        Use strategic frameworks (Business Model Canvas, Porter's Five Forces) where appropriate.
        """,
        expected_output="""
        A complete Go-To-Market strategy document (5-7 pages) with:
        - Executive summary
        - Market positioning and value proposition
        - Target customer profile and personas
        - Multi-channel acquisition strategy
        - 90-day launch roadmap with milestones
        - Pricing strategy and packaging
        - Success metrics and KPIs
        - Next steps and recommendations
        """,
        agent=strategist,
        context=[task1]
    )

    task3 = Task(
        description=f"""
        Create compelling product messaging for {product_name} based on the GTM strategy.

        Deliverables:

        1. Core Messaging:
           - Value proposition (1 sentence)
           - Elevator pitch (2-3 sentences)
           - Key benefit statements (3-5 bullets)

        2. Website Copy:
           - Hero headline and subheadline
           - "How it Works" section (3 steps)
           - "Why Choose Us" section (3-4 differentiators)
           - Customer testimonial template

        3. Sales Collateral:
           - One-pager overview (bullet points for design)
           - Email outreach templates (cold, warm, follow-up)
           - Demo invitation email

        4. Social Proof:
           - Case study outline (problem, solution, results)
           - Success story angles (3-4 ideas)

        Messaging should:
        - Address target audience pain points directly
        - Highlight competitive differentiators
        - Use clear, jargon-free language
        - Include specific value metrics where possible
        - Drive toward demo signup as CTA
        """,
        expected_output="""
        A complete messaging document with:
        - Core value proposition and elevator pitch
        - Website copy (hero, how it works, differentiators)
        - Sales email templates (5 variations)
        - One-pager outline for design
        - Case study structure and success story angles
        - Messaging guidelines for consistency

        All copy should be ready to use without further editing.
        """,
        agent=copywriter,
        context=[task1, task2]
    )

    task4 = Task(
        description=f"""
        Build a sales playbook for {product_name} targeting {target_market}.

        The playbook must include:

        1. Sales Process:
           - Lead qualification criteria (BANT/MEDDIC)
           - Sales stages and exit criteria
           - Average deal cycle and velocity targets

        2. Discovery Framework:
           - Key questions to ask prospects
           - Pain points to uncover
           - Success criteria to understand
           - Decision-making process questions

        3. Demo Best Practices:
           - Pre-demo qualification
           - Demo flow and structure
           - Value-focused features to highlight
           - Objection handling strategies

        4. Objection Handling:
           - Top 10 objections and responses
           - Competitive objections (vs each competitor)
           - Pricing objections and negotiation strategies

        5. Closing Techniques:
           - Trial/pilot program structure
           - Contract negotiation guidelines
           - Pricing discount authority levels

        6. Tools and Resources:
           - CRM setup and workflow
           - Required collateral checklist
           - Sales metrics to track

        The playbook should enable a new sales rep to run effective demos and close
        deals within 30 days of onboarding.
        """,
        expected_output="""
        A complete sales playbook (8-10 pages) with:
        - Sales process diagram and stage definitions
        - Discovery question framework
        - Demo script and best practices
        - Objection handling guide (10+ objections with responses)
        - Closing strategies and trial program structure
        - CRM workflow and required tools
        - Sales metrics dashboard template
        - 30-day new rep onboarding checklist
        """,
        agent=sales_expert,
        context=[task1, task2, task3]
    )

    # Create crew
    gtm_crew = Crew(
        agents=[competitive_intel, strategist, copywriter, sales_expert],
        tasks=[task1, task2, task3, task4],
        process=Process.sequential,
        verbose=True
    )

    print("✅ GTM Strategy Crew created with 4 agents, 4 tasks")
    print()
    print("=" * 80)
    print()
    print("🎓 Key Learnings:")
    print("   1. Agent templates make crew creation faster (reuse vs rebuild)")
    print("   2. Placeholder interpolation customizes templates for specific use cases")
    print("   3. Same templates can be used across multiple crews and projects")
    print("   4. Template library grows over time, becoming an org-wide asset")
    print()
    print("💡 Template Reusability:")
    print("   - competitive_intelligence: Used in product launches, partnerships, M&A")
    print("   - business_strategist: Used in GTM, fundraising, expansion planning")
    print("   - marketing_copywriter: Used in campaigns, websites, sales collateral")
    print("   - sales_strategist: Used in new products, new markets, channel expansion")
    print()
    print("=" * 80)
    print()
    print("To run this crew (requires API keys):")
    print("  python3 gtm_strategy_crew.py")
    print()
    print("Output: Complete GTM strategy with competitive analysis, messaging, playbook")
    print("=" * 80)

if __name__ == "__main__":
    main()
