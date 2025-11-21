#!/usr/bin/env python3
"""
Test Script v3: Force tool execution with function_calling_llm
"""

from crewai import Agent, Task, Crew, LLM
from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import json


class ModelSelectionInput(BaseModel):
    """Input for model selection tool."""
    task_description: str = Field(description="The user's task to route")


class ModelSelectionTool(BaseTool):
    name: str = "select_optimal_llm"  # Shorter name
    description: str = "Select the best LLM model for a task. Input: task_description (string)"
    args_schema: Type[BaseModel] = ModelSelectionInput

    def _run(self, task_description: str) -> str:
        """Mock routing logic"""
        if "image" in task_description.lower() or "chart" in task_description.lower():
            model = "llama3.2-vision:90b"
            category = "max_vision"
        elif "math" in task_description.lower() or "solve" in task_description.lower():
            model = "deepseek-r1:70b"
            category = "max_reasoning"
        else:
            model = "mixtral:8x7b"
            category = "default"

        result = {
            "✅": "TOOL WAS CALLED!",
            "model": model,
            "category": category,
            "task": task_description
        }

        return json.dumps(result, indent=2)


# Try with a LARGER model that's better at tool calling
# llama3.2:1b might be too small for reliable tool use
router_llm = LLM(
    model="ollama/mixtral:8x7b",  # Larger model, better tool calling
    base_url="http://localhost:11434"
)


SIMPLE_PROMPT = """
You have ONE tool: select_optimal_llm

When given a task, you MUST:
1. Call select_optimal_llm with task_description parameter
2. Return ONLY the tool's output

DO NOT describe what you would do. ACTUALLY DO IT.

Task: {input}
"""


router_agent = Agent(
    role="Router",
    goal="Call select_optimal_llm tool for every task",
    backstory="I only call the select_optimal_llm tool. Nothing else.",
    llm=router_llm,
    tools=[ModelSelectionTool()],
    verbose=True,
    allow_delegation=False,
    function_calling_llm=router_llm  # Explicit function calling
)


def run_test():
    print("\n🧪 TEST: Using larger model (mixtral:8x7b) for tool calling\n")

    task = Task(
        description="Analyze this sales chart",
        expected_output="Tool output with model selection",
        agent=router_agent
    )

    crew = Crew(
        agents=[router_agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()

    print("\n" + "="*80)
    print("RESULT:")
    print("="*80)
    print(result)
    print("="*80)

    if "✅" in str(result) and "TOOL WAS CALLED" in str(result):
        print("\n✅ SUCCESS: Tool was actually executed!")
        return True
    else:
        print("\n❌ FAIL: Tool still not called")
        return False


if __name__ == "__main__":
    run_test()
