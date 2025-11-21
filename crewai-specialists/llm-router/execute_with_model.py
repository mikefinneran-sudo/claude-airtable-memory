#!/usr/bin/env python3
"""
Direct model execution - Claude does the routing
Usage: python execute_with_model.py <model_name> "Your task here"
"""

import sys
import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Task

# Load API keys
load_dotenv()

from model_configs import MODELS, is_local_model

def execute_task(model_name: str, task_description: str) -> dict:
    """
    Execute a task with the specified model (skips classification)
    Claude has already decided which model to use
    """

    model_config = MODELS.get(model_name)
    if not model_config:
        return {
            "error": f"Model {model_name} not found",
            "available_models": list(MODELS.keys())
        }

    is_local = is_local_model(model_name)
    provider = model_config.get("provider", "ollama")

    print(f"\n🚀 Executing with {model_name}")
    if is_local:
        print(f"   📍 Local (DGX) - FREE")
        print(f"   Size: {model_config.get('size_gb', 'N/A')} GB | Params: {model_config.get('params', 'N/A')}")
    else:
        print(f"   ☁️  Commercial ({provider.upper()}) - PAID")
        print(f"   Cost: ${model_config.get('cost_per_1m_in', 0)}/1M in, ${model_config.get('cost_per_1m_out', 0)}/1M out")
    print(f"   Speed: {model_config['speed']} | Quality: {model_config['quality']}")
    print(f"   Why: {model_config['when_to_use']}\n")

    # Create worker agent with selected model
    worker_agent = Agent(
        role="Task Executor",
        goal=f"Complete the task using {model_name}",
        backstory=f"""You are powered by {model_name}, a {model_config['params']} parameter model.
        Your specialization: {model_config['specialization']}.
        You excel at: {', '.join(model_config['capabilities'])}.""",
        llm=model_config["llm"],
        verbose=True
    )

    # Create execution task
    execution_task = Task(
        description=task_description,
        agent=worker_agent,
        expected_output="A complete answer to the user's task"
    )

    # Execute with Crew
    crew = Crew(
        agents=[worker_agent],
        tasks=[execution_task],
        verbose=True
    )

    result = crew.kickoff()

    # Calculate cost for commercial models
    cost_usd = 0.0
    if not is_local:
        # Rough token estimation
        input_tokens = len(task_description.split()) * 1.3
        output_tokens = len(str(result).split()) * 1.3
        cost_in = (input_tokens / 1_000_000) * model_config.get("cost_per_1m_in", 0)
        cost_out = (output_tokens / 1_000_000) * model_config.get("cost_per_1m_out", 0)
        cost_usd = cost_in + cost_out

    return {
        "selected_model": model_name,
        "model_params": model_config.get("params", "N/A"),
        "model_size_gb": model_config.get("size_gb", "N/A"),
        "is_local": is_local,
        "provider": provider,
        "cost_usd": cost_usd,
        "result": str(result)
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python execute_with_model.py <model_name> 'Your task here'")
        print("\nAvailable models:")
        for model in MODELS.keys():
            if not MODELS[model].get("deprecated", False):
                print(f"  - {model}")
        sys.exit(1)

    model_name = sys.argv[1]
    task = " ".join(sys.argv[2:])

    print(f"\n📝 Task: {task}")

    result = execute_task(model_name, task)

    if "error" in result:
        print(f"\n❌ ERROR: {result['error']}")
        sys.exit(1)

    print(f"\n{'='*80}")
    print("✅ RESULT")
    print('='*80)
    print(f"\n🤖 Model: {result['selected_model']}")
    print(f"📍 Type: {'LOCAL (FREE)' if result['is_local'] else 'COMMERCIAL (PAID)'}")
    print(f"💰 Cost: ${result['cost_usd']:.6f}")
    print(f"\n📄 Output:\n{result['result']}\n")
