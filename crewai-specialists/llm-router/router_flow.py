"""
CrewAI Intelligent LLM Router - Strategy 3B Implementation
Uses CrewAI Flows with @router decorator for explicit Python routing logic
Implements "Conscious Router" pattern with llama3.2:1b as Mission Control
"""

from crewai import Agent, Crew, Task, LLM
from crewai.flow import Flow, start, listen, router
from pydantic import BaseModel
from typing import Literal
import json

from model_configs import ROUTER_LLM, MODELS, get_model_by_category, get_all_active_models

# Define routing categories as Literal type
RoutingCategory = Literal[
    "max_vision", "fast_vision",
    "max_reasoning", "max_reasoning_moe", "efficient_reasoning", "hybrid_reasoner",
    "max_rag", "fast_rag",
    "agentic_tool_use",
    "structured_data",
    "simple_chat", "instruction_following",
    "long_context", "max_quality_general", "default_general", "efficient_general",
    "korean_multilingual", "embeddings"
]

class TaskClassification(BaseModel):
    """Schema for router agent output"""
    category: RoutingCategory
    confidence: float
    reasoning: str

class RouterDecision(BaseModel):
    """Router decision with selected model"""
    task_description: str
    category: RoutingCategory
    selected_model: str
    confidence: float
    reasoning: str

class DynamicModelFlow(Flow):
    """
    CrewAI Flow that intelligently routes tasks to optimal LLM models

    Architecture:
    1. get_task() - Accept task input
    2. classify_task() - Use llama3.2:1b router to classify task
    3. route_by_category() - @router decorator for explicit Python routing
    4. run_task_with_model() - Execute task with selected model
    """

    @start
    def get_task(self, task_description: str):
        """Entry point: Accept task description"""
        print(f"\n📝 Received task: {task_description[:100]}...")
        return {"task_description": task_description}

    @listen(get_task)
    def classify_task(self, inputs: dict) -> dict:
        """
        Use llama3.2:1b (Mission Control) to classify the task
        Ultra-fast 1B model dedicated to routing decisions
        """
        task_description = inputs["task_description"]

        print(f"\n🧠 Mission Control (llama3.2:1b) classifying task...")

        # Create router agent with few-shot examples
        router_agent = Agent(
            role="Task Classification Specialist",
            goal="Classify incoming tasks into the optimal routing category",
            backstory="""You are Mission Control for a fleet of 20 specialized LLM models.
            Your job is to analyze each task and determine which model is best suited for it.
            You are extremely fast (1.3GB, 1B params) and focused only on classification.""",
            llm=ROUTER_LLM,
            verbose=True
        )

        # Classification task with few-shot examples from research
        classification_task = Task(
            description=f"""
Analyze this task and classify it into ONE of these categories:

VISION TASKS:
- max_vision: Complex charts, diagrams, OCR, detailed image analysis
- fast_vision: Simple image captions, basic object detection

REASONING TASKS:
- max_reasoning: Complex math proofs, logic puzzles, deep analysis
- max_reasoning_moe: Extremely complex reasoning (uses 671B MoE model)
- efficient_reasoning: Text reasoning (faster than 70B models)
- hybrid_reasoner: Visual reasoning (math diagrams, flowcharts)

RETRIEVAL/RAG TASKS:
- max_rag: Complex document search with citations
- fast_rag: Fast RAG with good citation quality

TOOL/AGENT TASKS:
- agentic_tool_use: API calls, tool orchestration, function calling

DATA TASKS:
- structured_data: JSON generation, data extraction

CHAT TASKS:
- simple_chat: Basic conversation, fast responses
- instruction_following: Precise instruction execution

CONTEXT TASKS:
- long_context: Large documents (128K tokens)
- max_quality_general: High-quality general tasks, complex coding
- default_general: General tasks (balanced speed/quality)
- efficient_general: General tasks (fast, lightweight)

SPECIALIZED:
- korean_multilingual: Korean language tasks
- embeddings: Text embeddings, vector search

FEW-SHOT EXAMPLES:
1. "Analyze this sales chart and extract revenue trends" → max_vision
2. "Prove that √2 is irrational" → max_reasoning
3. "What's the weather like today?" → simple_chat
4. "Generate JSON schema for user profile" → structured_data
5. "Search 500 PDFs for mentions of 'quantum computing' with citations" → max_rag
6. "Call the weather API and book a restaurant" → agentic_tool_use

TASK TO CLASSIFY:
{task_description}

Return ONLY valid JSON:
{{
    "category": "<one of the categories above>",
    "confidence": <0.0 to 1.0>,
    "reasoning": "<brief explanation>"
}}
""",
            agent=router_agent,
            expected_output="JSON object with category, confidence, and reasoning"
        )

        # Execute classification
        crew = Crew(
            agents=[router_agent],
            tasks=[classification_task],
            verbose=True
        )

        result = crew.kickoff()

        # Parse classification result
        try:
            classification = json.loads(str(result))
            print(f"\n✅ Classification: {classification['category']} (confidence: {classification['confidence']})")
            print(f"   Reasoning: {classification['reasoning']}")

            return {
                "task_description": task_description,
                "category": classification["category"],
                "confidence": classification["confidence"],
                "reasoning": classification["reasoning"]
            }
        except Exception as e:
            print(f"\n⚠️  Classification parsing failed: {e}")
            print(f"   Falling back to default_general")
            return {
                "task_description": task_description,
                "category": "default_general",
                "confidence": 0.5,
                "reasoning": "Fallback due to classification error"
            }

    @router(classify_task)
    def route_by_category(self, inputs: dict) -> str:
        """
        Explicit Python routing logic based on classification
        Uses @router decorator to select which method to call next
        """
        category = inputs["category"]

        print(f"\n🎯 Routing to category: {category}")

        # Explicit routing map (all categories must be handled)
        routing_map = {
            "max_vision": "run_max_vision",
            "fast_vision": "run_fast_vision",
            "max_reasoning": "run_max_reasoning",
            "max_reasoning_moe": "run_max_reasoning_moe",
            "efficient_reasoning": "run_efficient_reasoning",
            "hybrid_reasoner": "run_hybrid_reasoner",
            "max_rag": "run_max_rag",
            "fast_rag": "run_fast_rag",
            "agentic_tool_use": "run_agentic_tool_use",
            "structured_data": "run_structured_data",
            "simple_chat": "run_simple_chat",
            "instruction_following": "run_instruction_following",
            "long_context": "run_long_context",
            "max_quality_general": "run_max_quality_general",
            "default_general": "run_default_general",
            "efficient_general": "run_efficient_general",
            "korean_multilingual": "run_korean_multilingual",
            "embeddings": "run_embeddings"
        }

        return routing_map.get(category, "run_default_general")

    # Route handlers - one for each category
    @listen(route_by_category)
    def run_max_vision(self, inputs: dict):
        return self._execute_with_model(inputs, "llama3.2-vision:90b")

    @listen(route_by_category)
    def run_fast_vision(self, inputs: dict):
        return self._execute_with_model(inputs, "llava:13b")

    @listen(route_by_category)
    def run_max_reasoning(self, inputs: dict):
        return self._execute_with_model(inputs, "deepseek-r1:70b")

    @listen(route_by_category)
    def run_max_reasoning_moe(self, inputs: dict):
        return self._execute_with_model(inputs, "deepseek-v3")

    @listen(route_by_category)
    def run_efficient_reasoning(self, inputs: dict):
        return self._execute_with_model(inputs, "phi4")

    @listen(route_by_category)
    def run_hybrid_reasoner(self, inputs: dict):
        return self._execute_with_model(inputs, "apriel-1.5-15b-thinker")

    @listen(route_by_category)
    def run_max_rag(self, inputs: dict):
        return self._execute_with_model(inputs, "command-r-plus")

    @listen(route_by_category)
    def run_fast_rag(self, inputs: dict):
        return self._execute_with_model(inputs, "command-r")

    @listen(route_by_category)
    def run_agentic_tool_use(self, inputs: dict):
        return self._execute_with_model(inputs, "gpt-oss:20b")

    @listen(route_by_category)
    def run_structured_data(self, inputs: dict):
        return self._execute_with_model(inputs, "qwen2.5:14b")

    @listen(route_by_category)
    def run_simple_chat(self, inputs: dict):
        return self._execute_with_model(inputs, "mistral:7b")

    @listen(route_by_category)
    def run_instruction_following(self, inputs: dict):
        return self._execute_with_model(inputs, "nous-hermes2")

    @listen(route_by_category)
    def run_long_context(self, inputs: dict):
        return self._execute_with_model(inputs, "llama3.1:70b")

    @listen(route_by_category)
    def run_max_quality_general(self, inputs: dict):
        return self._execute_with_model(inputs, "qwen2.5:72b")

    @listen(route_by_category)
    def run_default_general(self, inputs: dict):
        return self._execute_with_model(inputs, "mixtral:8x7b")

    @listen(route_by_category)
    def run_efficient_general(self, inputs: dict):
        return self._execute_with_model(inputs, "gemma2:9b")

    @listen(route_by_category)
    def run_korean_multilingual(self, inputs: dict):
        return self._execute_with_model(inputs, "solar")

    @listen(route_by_category)
    def run_embeddings(self, inputs: dict):
        return self._execute_with_model(inputs, "nomic-embed-text")

    def _execute_with_model(self, inputs: dict, model_name: str) -> dict:
        """
        Execute the task using the selected model
        """
        task_description = inputs["task_description"]
        category = inputs["category"]
        reasoning = inputs["reasoning"]

        model_config = MODELS.get(model_name)
        if not model_config:
            print(f"⚠️  Model {model_name} not found, using default")
            model_config = MODELS.get("mixtral:8x7b")
            model_name = "mixtral:8x7b"

        print(f"\n🚀 Executing with {model_name}")
        print(f"   Size: {model_config['size_gb']} GB | Params: {model_config['params']}")
        print(f"   Speed: {model_config['speed']} | Quality: {model_config['quality']}")
        print(f"   Why: {model_config['when_to_use']}")

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

        # Execute task
        execution_task = Task(
            description=task_description,
            agent=worker_agent,
            expected_output="Complete response to the task"
        )

        crew = Crew(
            agents=[worker_agent],
            tasks=[execution_task],
            verbose=True
        )

        result = crew.kickoff()

        return {
            "task_description": task_description,
            "category": category,
            "selected_model": model_name,
            "model_params": model_config['params'],
            "model_size_gb": model_config['size_gb'],
            "routing_reasoning": reasoning,
            "result": str(result)
        }


def run_router(task_description: str) -> dict:
    """
    Convenience function to run the router flow

    Usage:
        result = run_router("Analyze this sales chart and extract trends")
    """
    flow = DynamicModelFlow()
    result = flow.kickoff(task_description=task_description)
    return result


if __name__ == "__main__":
    # Test the router with sample tasks
    test_tasks = [
        "What's 2+2?",  # Should route to simple_chat
        "Prove that the sum of two even numbers is always even",  # Should route to max_reasoning
        "Generate a JSON schema for a user profile with name, email, and age",  # Should route to structured_data
    ]

    print("=" * 80)
    print("CREWAI INTELLIGENT LLM ROUTER - TEST MODE")
    print("=" * 80)

    for task in test_tasks:
        print(f"\n\n{'=' * 80}")
        print(f"TEST: {task}")
        print("=" * 80)

        result = run_router(task)

        print(f"\n✅ RESULT:")
        print(f"   Category: {result['category']}")
        print(f"   Model: {result['selected_model']} ({result['model_params']}, {result['model_size_gb']} GB)")
        print(f"   Output: {result['result'][:200]}...")
