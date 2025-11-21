#!/usr/bin/env python3
"""
Level 1 Training: Research Organization Crew (YAML-based)

Learning Objectives:
1. Load agents and tasks from YAML configs
2. Apply 80/20 rule (focus on task descriptions)
3. Use sequential process for linear pipeline
4. Understand input interpolation with {placeholders}

Usage:
    python3 crew.py
"""
from crewai import Agent, Task, Crew, Process
from pathlib import Path
import yaml
import json
from datetime import datetime

# Load YAML configurations
CONFIG_DIR = Path(__file__).parent / "config"

def load_yaml_config(filename):
    """Load YAML configuration file"""
    with open(CONFIG_DIR / filename, 'r') as f:
        return yaml.safe_load(f)

# Load agents and tasks from YAML
agents_config = load_yaml_config('agents.yaml')
tasks_config = load_yaml_config('tasks.yaml')

# Create Agent objects from YAML
def create_agent(agent_name, config):
    """Create a CrewAI Agent from YAML config"""
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=config.get('verbose', True),
        allow_delegation=config.get('allow_delegation', False)
    )

# Create Task objects from YAML
def create_task(task_name, config, agents_dict):
    """Create a CrewAI Task from YAML config"""
    return Task(
        description=config['description'],
        expected_output=config['expected_output'],
        agent=agents_dict[config['agent']],
        context=[tasks_dict[ctx] for ctx in config.get('context', [])] if 'context' in config else None,
        output_file=config.get('output_file')
    )

# Initialize agents
agents_dict = {
    name: create_agent(name, config)
    for name, config in agents_config.items()
}

# Initialize tasks (need to build this after agents are created)
tasks_dict = {}
for task_name, task_config in tasks_config.items():
    # For tasks with context dependencies, we'll handle them in second pass
    if 'context' not in task_config:
        tasks_dict[task_name] = create_task(task_name, task_config, agents_dict)

# Second pass: Create tasks with context dependencies
for task_name, task_config in tasks_config.items():
    if 'context' in task_config and task_name not in tasks_dict:
        tasks_dict[task_name] = create_task(task_name, task_config, agents_dict)

# Create the Crew
research_crew = Crew(
    agents=list(agents_dict.values()),
    tasks=list(tasks_dict.values()),
    process=Process.sequential,  # Linear pipeline: collect → categorize → format
    verbose=True
)

def main():
    """Run the research organization crew"""
    print("=" * 80)
    print("🎓 LEVEL 1 TRAINING: YAML-Based Research Organization Crew")
    print("=" * 80)
    print()
    print("Learning Focus: 80/20 Rule - Notice how task descriptions are detailed")
    print("                while agent definitions are simple and role-focused")
    print()
    print("=" * 80)
    print()

    # Define inputs for placeholder interpolation
    inputs = {
        'source_type': 'local markdown files',
        'source_location': str(Path.home() / 'Downloads'),
        'topic_filter': 'CrewAI',
        'accuracy': 95,
        'output_dir': str(Path(__file__).parent / 'outputs')
    }

    print(f"📂 Source: {inputs['source_location']}")
    print(f"🏷️  Filter: {inputs['topic_filter']}")
    print(f"🎯 Target Accuracy: {inputs['accuracy']}%")
    print(f"📝 Output: {inputs['output_dir']}")
    print()
    print("=" * 80)
    print()

    # Ensure output directory exists
    Path(inputs['output_dir']).mkdir(parents=True, exist_ok=True)

    # Run the crew
    result = research_crew.kickoff(inputs=inputs)

    print()
    print("=" * 80)
    print("✅ CREW COMPLETED")
    print("=" * 80)
    print()
    print("📊 Result Summary:")
    print(result)
    print()
    print("=" * 80)
    print()
    print("🎓 Training Takeaways:")
    print("   1. YAML configs make agents/tasks reusable and maintainable")
    print("   2. 80/20 rule: Detailed task descriptions drive quality output")
    print("   3. Sequential process = Simple, predictable pipeline")
    print("   4. Input interpolation with {placeholders} makes crews flexible")
    print()
    print("Next Level: Custom tools with @tool decorator")
    print("=" * 80)

if __name__ == "__main__":
    main()
