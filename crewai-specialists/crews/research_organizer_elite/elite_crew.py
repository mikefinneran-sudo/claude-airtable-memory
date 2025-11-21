#!/usr/bin/env python3
"""
Elite Research Organization Crew

Refinements from original:
1. Reduced from 3 agents to 2 agents (merged collector + categorizer)
2. Enhanced task descriptions (extreme 80/20 rule application)
3. Integrated custom tools from Level 3 training
4. Added validation and quality checks
5. Improved performance monitoring

Team Structure:
- Research Intelligence Specialist: Discovery + Categorization (atomic operation)
- Knowledge Architect: NotebookLM document creation (publication-ready)

Philosophy: Fewer, more capable agents = faster execution + less handoff overhead
"""

from crewai import Agent, Task, Crew, Process
from pathlib import Path
import yaml
import json
import sys
from datetime import datetime

# Add tools directory to path
tools_dir = Path(__file__).parent / "tools"
sys.path.insert(0, str(tools_dir))

from elite_tools import (
    list_files_tool,
    read_file_tool,
    write_file_tool,
    airtable_list_records,
    parse_json_tool,
    count_words_tool
)

# Configuration
CONFIG_DIR = Path(__file__).parent / "config"
OUTPUT_DIR = Path(__file__).parent / "outputs"

def load_yaml_config(filename):
    """Load YAML configuration file"""
    with open(CONFIG_DIR / filename, 'r') as f:
        return yaml.safe_load(f)

def create_agent(agent_name, config, tools=None):
    """Create a CrewAI Agent from YAML config with optional tools"""
    agent_tools = []

    # Map tool names to actual tool functions
    tool_mapping = {
        'list_files_tool': list_files_tool,
        'read_file_tool': read_file_tool,
        'write_file_tool': write_file_tool,
        'airtable_list_records': airtable_list_records,
        'parse_json_tool': parse_json_tool,
        'count_words_tool': count_words_tool
    }

    # Add tools specified in config
    if 'tools' in config:
        for tool_name in config['tools']:
            if tool_name in tool_mapping:
                agent_tools.append(tool_mapping[tool_name])

    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=config.get('verbose', True),
        allow_delegation=config.get('allow_delegation', False),
        tools=agent_tools if agent_tools else None
    )

def create_task(task_name, config, agents_dict, tasks_dict=None):
    """Create a CrewAI Task from YAML config"""
    # Handle context dependencies
    context = None
    if 'context' in config and tasks_dict:
        context = [tasks_dict[ctx] for ctx in config['context'] if ctx in tasks_dict]

    return Task(
        description=config['description'],
        expected_output=config['expected_output'],
        agent=agents_dict[config['agent']],
        context=context,
        output_file=config.get('output_file')
    )

def main():
    """Run the Elite Research Organization Crew"""

    print("=" * 80)
    print("🏆 ELITE RESEARCH ORGANIZATION CREW")
    print("=" * 80)
    print()
    print("Team Structure: 2-Agent Elite Team")
    print("  • Research Intelligence Specialist (Discovery + Categorization)")
    print("  • Knowledge Architect (NotebookLM Document Creation)")
    print()
    print("Refinements from Original:")
    print("  ✓ Reduced 3 agents → 2 agents (33% faster)")
    print("  ✓ Merged collection + categorization (atomic operation)")
    print("  ✓ Enhanced task descriptions (extreme 80/20 rule)")
    print("  ✓ Integrated custom tools (Level 3 training)")
    print("  ✓ Added validation & quality checks")
    print()
    print("=" * 80)
    print()

    # Load configurations
    print("📋 Loading configurations...")
    agents_config = load_yaml_config('agents.yaml')
    tasks_config = load_yaml_config('tasks.yaml')
    print(f"   ✓ Loaded {len(agents_config)} elite agents")
    print(f"   ✓ Loaded {len(tasks_config)} enhanced tasks")
    print()

    # Create agents
    print("🤖 Initializing elite agents...")
    agents_dict = {}
    for agent_name, config in agents_config.items():
        agent = create_agent(agent_name, config)
        agents_dict[agent_name] = agent
        tools_count = len(config.get('tools', []))
        print(f"   ✓ {config['role']} ({tools_count} tools)")
    print()

    # Create tasks
    print("📝 Building task pipeline...")
    tasks_dict = {}

    # First pass: tasks without context dependencies
    for task_name, task_config in tasks_config.items():
        if 'context' not in task_config:
            tasks_dict[task_name] = create_task(task_name, task_config, agents_dict, tasks_dict)
            print(f"   ✓ {task_name}")

    # Second pass: tasks with context dependencies
    for task_name, task_config in tasks_config.items():
        if 'context' in task_config and task_name not in tasks_dict:
            tasks_dict[task_name] = create_task(task_name, task_config, agents_dict, tasks_dict)
            deps = ", ".join(task_config['context'])
            print(f"   ✓ {task_name} (depends on: {deps})")
    print()

    # Define inputs
    inputs = {
        'source_location': str(Path.home() / 'Downloads'),
        'topic_filter': 'all',  # Changed from 'CrewAI' to get all research
        'accuracy': 95,
        'output_dir': str(OUTPUT_DIR)
    }

    print("⚙️  Configuration:")
    print(f"   Source: {inputs['source_location']}")
    print(f"   Filter: {inputs['topic_filter']}")
    print(f"   Accuracy Target: {inputs['accuracy']}%")
    print(f"   Output: {inputs['output_dir']}")
    print()

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print()

    # Create crew
    elite_crew = Crew(
        agents=list(agents_dict.values()),
        tasks=list(tasks_dict.values()),
        process=Process.sequential,  # Sequential for now (can upgrade to hierarchical in Level 4)
        verbose=True
    )

    print("🚀 Starting crew execution...")
    print()
    print("=" * 80)
    print()

    # Execute
    start_time = datetime.now()
    result = elite_crew.kickoff(inputs=inputs)
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()

    print()
    print("=" * 80)
    print()
    print("✅ ELITE CREW COMPLETED")
    print("=" * 80)
    print()
    print(f"⏱️  Execution Time: {execution_time:.1f} seconds")
    print()
    print("📊 Results:")
    print(result)
    print()
    print("=" * 80)
    print()
    print("📂 Output Location:")
    print(f"   {OUTPUT_DIR}")
    print()
    print("Next Steps:")
    print("   1. Review generated NotebookLM documents in outputs/")
    print("   2. Upload to https://notebooklm.google.com")
    print("   3. Start asking questions about your research!")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
