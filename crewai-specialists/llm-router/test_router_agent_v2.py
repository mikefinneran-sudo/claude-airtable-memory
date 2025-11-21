#!/usr/bin/env python3
"""
Test Script v2: RouterAgent with ModelSelectionTool
Goal: Debug why tool isn't being called
"""

from crewai import Agent, Task, Crew, LLM
from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import json


# 1. Define INPUT schema (what the agent provides to the tool)
class ModelSelectionInput(BaseModel):
    """Input for model selection tool."""
    task_description: str = Field(description="The user's task to route")


# 2. Define Custom Tool
class ModelSelectionTool(BaseTool):
    name: str = "Select Optimal LLM"
    description: str = """
    Use this tool to select the best LLM model for a task.
    Provide the task_description and I will return the optimal model selection.
    """
    args_schema: Type[BaseModel] = ModelSelectionInput

    def _run(self, task_description: str) -> str:
        """
        This is a MOCK tool - it just demonstrates the agent called it.
        In real implementation, this would have routing logic.
        """
        # Mock routing logic (simplified)
        if "image" in task_description.lower() or "chart" in task_description.lower():
            model = "ollama/llama3.2-vision:90b"
            category = "max_vision"
        elif "math" in task_description.lower() or "solve" in task_description.lower():
            model = "ollama/deepseek-r1:70b"
            category = "max_reasoning"
        elif "chat" in task_description.lower() or "weather" in task_description.lower():
            model = "ollama/mistral:7b"
            category = "simple_chat"
        else:
            model = "ollama/mixtral:8x7b"
            category = "default_general"

        result = {
            "model_name": model,
            "category": category,
            "task": task_description,
            "justification": f"Selected {model} for {category} task",
            "status": "✅ Tool was called successfully!"
        }

        return json.dumps(result, indent=2)


# 3. Define Router LLM (llama3.2:1b on DGX)
router_llm = LLM(
    model="ollama/llama3.2:1b",
    base_url="http://localhost:11434"
)


# 4. Define RouterAgent with CLEARER instructions
ROUTER_SYSTEM_PROMPT = """
You are a Model Router. Your job is to USE THE TOOL 'Select Optimal LLM'.

CRITICAL: You MUST call the tool. Do NOT try to answer the task yourself.

To use the tool:
1. Read the task
2. Call 'Select Optimal LLM' tool with task_description parameter
3. Return the tool's output

Example:
User Task: "Analyze this chart"
Your Action: Use 'Select Optimal LLM' tool with task_description="Analyze this chart"

You are {role}. Your goal: {goal}
"""


router_agent = Agent(
    role="Task Router",
    goal="Use the 'Select Optimal LLM' tool to route tasks. Always call the tool.",
    backstory="You route tasks by calling the 'Select Optimal LLM' tool. You never answer tasks directly.",
    llm=router_llm,
    tools=[ModelSelectionTool()],
    system_template=ROUTER_SYSTEM_PROMPT,
    verbose=True,
    allow_delegation=False
)


# 5. Simple test
def run_simple_test():
    """Run a single test to see if tool is called"""
    print("\n🧪 SIMPLE TEST: Will the agent call the tool?\n")

    task_description = "Analyze this sales chart from the image"

    route_task = Task(
        description=f"Use the 'Select Optimal LLM' tool to route this task: {task_description}",
        expected_output="The tool's JSON output with model selection",
        agent=router_agent
    )

    crew = Crew(
        agents=[router_agent],
        tasks=[route_task],
        verbose=True
    )

    try:
        print(f"📋 Task: {task_description}\n")
        result = crew.kickoff()

        print("\n" + "="*80)
        print("📊 RESULT:")
        print("="*80)
        print(result)
        print("="*80)

        # Check if tool was called
        if "✅ Tool was called successfully!" in str(result):
            print("\n✅ SUCCESS: Tool was called!")
            return True
        else:
            print("\n❌ FAIL: Tool was NOT called")
            print("Agent tried to answer directly instead of using tool")
            return False

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


if __name__ == "__main__":
    success = run_simple_test()

    if success:
        print("\n✅ Ready to integrate into Flow")
    else:
        print("\n⚠️ Need to fix tool calling before Phase 4")
