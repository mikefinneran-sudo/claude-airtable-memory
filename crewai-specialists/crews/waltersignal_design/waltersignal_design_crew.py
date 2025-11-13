#!/usr/bin/env python3
"""
WalterSignal Website Design Enhancement Crew

This crew analyzes and enhances the WalterSignal.io website design.
Team: visual_content_analyst + web_ui_designer + graphic_brand_designer + business_operations_manager
"""

import sys
import yaml
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM

# Load configurations
config_dir = Path(__file__).parent.parent.parent / "config"

with open(config_dir / "models.yaml") as f:
    models_config = yaml.safe_load(f)

with open(config_dir / "agents.yaml") as f:
    agents_config = yaml.safe_load(f)

def get_llm(model_type="general"):
    """Get LLM instance for specified model type"""
    base_url = models_config["ollama"]["base_url"]
    model_name = models_config["models"][model_type]["name"]
    timeout = models_config["ollama"]["timeout"]
    return LLM(model=f'ollama/{model_name}', base_url=base_url)

# Create specialized agents from config
visual_analyst = Agent(
    role=agents_config["visual_content_analyst"]["role"],
    goal=agents_config["visual_content_analyst"]["goal"],
    backstory=agents_config["visual_content_analyst"]["backstory"],
    llm=get_llm("vision"),  # Uses Vision 90B
    verbose=True,
    allow_delegation=False
)

ui_designer = Agent(
    role=agents_config["web_ui_designer"]["role"],
    goal=agents_config["web_ui_designer"]["goal"],
    backstory=agents_config["web_ui_designer"]["backstory"],
    llm=get_llm("general"),  # Uses Llama3 70B
    verbose=True,
    allow_delegation=False
)

brand_designer = Agent(
    role=agents_config["graphic_brand_designer"]["role"],
    goal=agents_config["graphic_brand_designer"]["goal"],
    backstory=agents_config["graphic_brand_designer"]["backstory"],
    llm=get_llm("general"),  # Uses Llama3 70B
    verbose=True,
    allow_delegation=False
)

project_manager = Agent(
    role=agents_config["business_operations_manager"]["role"],
    goal=agents_config["business_operations_manager"]["goal"],
    backstory=agents_config["business_operations_manager"]["backstory"],
    llm=get_llm("reasoning"),  # Uses DeepSeek R1 70B
    verbose=True,
    allow_delegation=True
)

# Define tasks using 80/20 rule (detailed task descriptions)
task1_analyze_current = Task(
    description="""
    Analyze the current WalterSignal.io website design thoroughly.
    
    **Website URL**: https://waltersignal.io
    
    **Required Analysis**:
    1. **Visual Assessment**
       - Overall design aesthetics and professionalism
       - Color scheme effectiveness
       - Typography choices and readability
       - Spacing, layout, and visual hierarchy
       - Mobile responsiveness
    
    2. **User Experience (UX)**
       - Navigation clarity and ease
       - Call-to-action (CTA) visibility and effectiveness
       - Content organization and flow
       - Loading speed and performance
       - Accessibility issues
    
    3. **Brand Consistency**
       - Logo placement and sizing
       - Brand colors vs website colors
       - Visual identity coherence
       - Professional vs casual tone
    
    4. **Competitive Comparison**
       - How does it compare to competitors in the AI/automation space?
       - What are industry standards for similar products?
       - What makes it stand out or blend in?
    
    **Quality Standards**:
    - Provide specific examples for each issue found
    - Use screenshots or specific page references
    - Rate each area on a scale of 1-10
    - Prioritize issues by impact (high/medium/low)
    
    **Output Format**:
    Structured markdown report with:
    - Executive summary (3-5 key findings)
    - Detailed analysis by category
    - Priority ranking of issues
    - Screenshots/visual references where applicable
    """,
    expected_output="Comprehensive visual analysis report with prioritized findings and ratings",
    agent=visual_analyst
)

task2_design_recommendations = Task(
    description="""
    Based on the visual analysis, create detailed UI/UX design recommendations for WalterSignal.io.
    
    **Context**: You will receive the visual analysis report from the previous task.
    
    **Required Deliverables**:
    1. **Layout & Structure Recommendations**
       - Homepage layout redesign (wireframe description)
       - Navigation structure improvements
       - Content hierarchy recommendations
       - Mobile-first responsive design approach
    
    2. **Visual Design System**
       - Color palette refinement (primary, secondary, accent colors)
       - Typography system (headings, body, code blocks)
       - Spacing and grid system
       - Component design patterns (buttons, cards, forms)
    
    3. **User Experience Enhancements**
       - Improved user journey from landing to conversion
       - CTA optimization (placement, wording, design)
       - Micro-interactions and animations
       - Loading states and error handling
    
    4. **Technical Implementation**
       - Framework recommendations (React, Next.js, Tailwind, etc)
       - Performance optimization strategies
       - Accessibility (WCAG 2.1) compliance checklist
       - SEO best practices integration
    
    **Quality Standards**:
    - Every recommendation must have a "why" (business/UX rationale)
    - Include before/after comparisons conceptually
    - Prioritize by implementation effort vs impact
    - Ensure consistency with WalterSignal brand identity
    
    **Output Format**:
    Detailed design specification document with:
    - Wireframe descriptions for key pages
    - Design system specifications
    - Implementation roadmap (quick wins vs long-term)
    - Success metrics for each recommendation
    """,
    expected_output="Complete UI/UX design specification with prioritized recommendations and implementation roadmap",
    agent=ui_designer
)

task3_brand_assets = Task(
    description="""
    Create brand and visual asset recommendations to enhance WalterSignal.io's visual identity.
    
    **Context**: You will receive both the visual analysis and UI/UX recommendations.
    
    **Required Deliverables**:
    1. **Visual Identity Refinement**
       - Logo variations needed (light/dark backgrounds, small/large sizes)
       - Brand color palette with hex codes and usage guidelines
       - Typography pairing recommendations
       - Iconography style and library recommendations
    
    2. **Marketing Collateral Design Concepts**
       - Hero section graphics/imagery
       - Feature illustrations or icons
       - Social media graphics templates
       - Email signature and marketing email designs
       - Presentation deck template (Gamma.app compatible)
    
    3. **Visual Content Strategy**
       - Photography style guidelines (if using photos)
       - Illustration style (flat, isometric, 3D, etc)
       - Data visualization approach
       - Infographic templates for complex concepts
    
    4. **Implementation Assets List**
       - Favicon and app icons
       - Open Graph images for social sharing
       - Loading animations or brand loaders
       - Error page designs (404, 500, etc)
    
    **Quality Standards**:
    - Align with modern AI/tech industry aesthetics
    - Ensure scalability across all media
    - Consider accessibility (color contrast, readability)
    - Provide mood boards or references for each concept
    
    **Output Format**:
    Brand asset specification document with:
    - Visual style guide outline
    - Asset creation priority list
    - Design tool recommendations (Figma, Gamma, etc)
    - Timeline estimates for asset creation
    """,
    expected_output="Complete brand and visual asset specification with creation roadmap",
    agent=brand_designer
)

task4_project_plan = Task(
    description="""
    Synthesize all design recommendations into an actionable implementation plan for WalterSignal.io.
    
    **Context**: You will receive:
    - Visual analysis report
    - UI/UX design recommendations
    - Brand asset specifications
    
    **Required Deliverables**:
    1. **Executive Summary**
       - Top 5 design improvements with highest impact
       - Estimated timeline and resource requirements
       - Expected business outcomes (conversion, engagement, brand perception)
       - Budget considerations if external resources needed
    
    2. **Phased Implementation Roadmap**
       - **Phase 1 (Quick Wins - Week 1-2)**: Immediate improvements
       - **Phase 2 (Core Redesign - Week 3-6)**: Major UI/UX changes
       - **Phase 3 (Brand Assets - Week 7-10)**: Visual identity enhancement
       - **Phase 4 (Polish & Optimize - Week 11-12)**: Final touches
    
    3. **Resource Allocation**
       - Designer hours needed per phase
       - Developer hours needed per phase
       - External contractor needs (if any)
       - Tool/software requirements
    
    4. **Success Metrics & KPIs**
       - User engagement metrics (bounce rate, time on site)
       - Conversion metrics (CTA clicks, sign-ups)
       - Brand perception (professional appearance rating)
       - Technical metrics (load time, accessibility score)
    
    5. **Risk Assessment**
       - Potential challenges and mitigation strategies
       - Stakeholder review and approval process
       - Rollback plan if redesign underperforms
    
    **Quality Standards**:
    - Realistic timelines based on typical web projects
    - Clear ownership for each task
    - Measurable success criteria
    - Contingency planning for delays
    
    **Output Format**:
    Professional project plan with:
    - Gantt chart or timeline visualization (text description)
    - Task breakdown with dependencies
    - Budget estimate (if applicable)
    - Next steps and immediate action items
    """,
    expected_output="Complete implementation project plan with timeline, resources, and success metrics",
    agent=project_manager
)

# Create the crew
waltersignal_design_crew = Crew(
    agents=[visual_analyst, ui_designer, brand_designer, project_manager],
    tasks=[task1_analyze_current, task2_design_recommendations, task3_brand_assets, task4_project_plan],
    process=Process.sequential,  # Each task builds on previous
    verbose=True
)

def create_waltersignal_design_crew(task_description=None, expected_output=None, agent_id=None, use_manager=False):
    """Factory function to create a fresh instance of the crew

    For training mode: pass task_description, expected_output, and agent_id
    For normal execution: call without parameters to use default tasks
    """
    # Map agent IDs to agent instances
    agent_map = {
        "visual_content_analyst": visual_analyst,
        "web_ui_designer": ui_designer,
        "graphic_brand_designer": brand_designer,
        "business_operations_manager": project_manager
    }

    # If task_description provided, create a custom task for training
    if task_description and agent_id:
        agent = agent_map.get(agent_id, visual_analyst)
        custom_task = Task(
            description=task_description,
            expected_output=expected_output or "A complete, professional deliverable addressing the task requirements",
            agent=agent
        )
        tasks = [custom_task]
    else:
        # Use default tasks for normal execution
        tasks = [task1_analyze_current, task2_design_recommendations, task3_brand_assets, task4_project_plan]

    return Crew(
        agents=[visual_analyst, ui_designer, brand_designer, project_manager],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🎨 WALTERSIGNAL.IO DESIGN ENHANCEMENT CREW")
    print("="*80)
    print("\nTeam:")
    print("  1. Visual Content Analyst (Vision 90B) - Current design analysis")
    print("  2. Web UI Designer (Llama3 70B) - UI/UX recommendations")
    print("  3. Graphic Brand Designer (Llama3 70B) - Brand asset creation")
    print("  4. Business Operations Manager (DeepSeek R1 70B) - Project coordination")
    print("\n" + "="*80)
    print("Starting design enhancement process...\n")
    
    # Execute the crew
    result = waltersignal_design_crew.kickoff()
    
    # Save output
    output_dir = Path(__file__).parent.parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "waltersignal_design_enhancement_plan.md"
    with open(output_file, 'w') as f:
        f.write(str(result))
    
    print("\n" + "="*80)
    print(f"✅ Design enhancement plan complete!")
    print(f"📄 Saved to: {output_file}")
    print("="*80 + "\n")
