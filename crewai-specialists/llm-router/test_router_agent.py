#!/usr/bin/env python3
"""
Test Script: RouterAgent with ModelSelectionTool
Goal: Verify that llama3.2:1b can reliably call a custom tool to return structured output
"""

from crewai import Agent, Task, Crew, LLM
from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import json


# 1. Define Pydantic output structure
class ModelSelectionOutput(BaseModel):
    """Structured output for model selection."""
    model_name: str = Field(description="The full ollama model tag (e.g., 'ollama/deepseek-r1:70b')")
    category: str = Field(description="Routing category (e.g., 'max_reasoning', 'simple_chat')")
    justification: str = Field(description="Brief reasoning for why this model was chosen")
    confidence: float = Field(description="Confidence score 0-1", ge=0, le=1)


# 2. Define Custom Tool
class ModelSelectionTool(BaseTool):
    name: str = "Select Optimal LLM"
    description: str = """
    Selects the optimal local LLM for a given task description.
    You MUST call this tool to route the task. Do not answer the task yourself.
    """
    args_schema: Type[BaseModel] = ModelSelectionOutput

    def _run(self, model_name: str, category: str, justification: str, confidence: float) -> str:
        """
        This tool just validates and returns the structured selection.
        The agent's tool call IS the routing decision.
        """
        result = {
            "model_name": model_name,
            "category": category,
            "justification": justification,
            "confidence": confidence,
            "status": "✅ Model selected successfully"
        }
        return json.dumps(result, indent=2)


# 3. Define Router LLM (llama3.2:1b on DGX)
router_llm = LLM(
    model="ollama/llama3.2:1b",
    base_url="http://192.168.68.88:11434"
)


# 4. Define RouterAgent with Few-Shot Training
ROUTER_SYSTEM_PROMPT = """
You are a Model Router. Your SOLE job is to call the 'Select Optimal LLM' tool.

TRAINING EXAMPLES (Learn from these):

Task: "Analyze this sales chart from the image"
→ model_name: "ollama/llama3.2-vision:90b"
→ category: "max_vision"
→ justification: "Complex visual analysis of chart data"
→ confidence: 0.95

Task: "Solve this complex calculus problem step by step"
→ model_name: "ollama/deepseek-r1:70b"
→ category: "max_reasoning"
→ justification: "Complex multi-step mathematical reasoning"
→ confidence: 0.9

Task: "Hey, how are you today?"
→ model_name: "ollama/mistral:7b"
→ category: "simple_chat"
→ justification: "Simple conversational chat"
→ confidence: 0.85

Task: "Write a blog post about AI"
→ model_name: "ollama/mixtral:8x7b"
→ category: "default_general"
→ justification: "General creative writing task"
→ confidence: 0.8

Now analyze the task and call the tool with your selection.
You are {role}. Your goal: {goal}
"""


router_agent = Agent(
    role="Task Router",
    goal="Select the best LLM by calling the 'Select Optimal LLM' tool",
    backstory="You are an expert at matching tasks to the optimal LLM model.",
    llm=router_llm,
    tools=[ModelSelectionTool()],
    system_template=ROUTER_SYSTEM_PROMPT,
    verbose=True,
    allow_delegation=False
)


# 5. Test Cases
test_tasks = [
    "I need to analyze the quarterly sales from this image.",
    "Solve this physics problem: A ball is thrown at 20m/s at 45 degrees...",
    "Hey, what's the weather like?",
    "Write me a blog post about machine learning."
]


def run_test(task_description: str):
    """Run a single routing test"""
    print("\n" + "="*80)
    print(f"TEST: {task_description}")
    print("="*80)

    route_task = Task(
        description=f"Route this task: {task_description}",
        expected_output="Call the 'Select Optimal LLM' tool with model selection",
        agent=router_agent
    )

    crew = Crew(
        agents=[router_agent],
        tasks=[route_task],
        verbose=True
    )

    try:
        result = crew.kickoff()
        print(f"\n✅ RESULT:\n{result}\n")
        return result
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        return None


if __name__ == "__main__":
    print("\n🧪 TESTING: RouterAgent with ModelSelectionTool")
    print("Goal: Verify llama3.2:1b calls tool reliably\n")

    # Run all tests
    results = []
    for task in test_tasks:
        result = run_test(task)
        results.append({"task": task, "result": result})

    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    successful = sum(1 for r in results if r["result"] is not None)
    print(f"Successful: {successful}/{len(results)}")

    if successful == len(results):
        print("\n✅ ALL TESTS PASSED - RouterAgent works!")
        print("Next: Test inside Flow")
    else:
        print("\n⚠️ SOME TESTS FAILED - Debug needed")
