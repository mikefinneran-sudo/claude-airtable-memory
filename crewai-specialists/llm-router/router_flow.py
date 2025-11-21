"""
CrewAI Intelligent LLM Router - Hybrid Strategy 3B Implementation
Uses CrewAI Flows with direct method calling for explicit Python routing logic
Hybrid: GPT-4o-mini classifier + 20 Local Models + 5 Commercial Models
"""

from crewai import Agent, Crew, Task, LLM
from crewai.flow import Flow, start, listen
from pydantic import BaseModel
from typing import Literal
import json
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

from model_configs import ROUTER_LLM, MODELS, get_model_by_category, get_all_active_models, is_local_model

# Define routing categories as Literal type (Local + Commercial)
RoutingCategory = Literal[
    # Local Models (Free)
    "max_vision", "fast_vision",
    "max_reasoning", "max_reasoning_moe", "efficient_reasoning", "hybrid_reasoner",
    "max_rag", "fast_rag",
    "agentic_tool_use",
    "structured_data",
    "simple_chat", "instruction_following",
    "long_context", "default_general", "efficient_general",
    "korean_multilingual", "embeddings",
    # Commercial Models (Paid)
    "max_quality_reasoning", "max_quality_multimodal",
    "fast_commercial", "ultra_fast_commercial", "multimodal_grounded"
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

    @start()
    def get_task(self):
        """Entry point: Accept task description from state"""
        task_description = self.state.get("task_description", "")
        print(f"\n📝 Received task: {task_description[:100]}...")
        return {"task_description": task_description}

    @listen(get_task)
    def classify_task(self) -> dict:
        """
        Use GPT-4o-mini (Mission Control) to classify the task
        Fast, reliable commercial router (switched from llama3.2:1b for better accuracy)
        """
        task_description = self.state.get("task_description", "")

        print(f"\n🧠 Mission Control (GPT-4o-mini) classifying task...")

        # Create router agent with few-shot examples
        router_agent = Agent(
            role="Task Classification Specialist",
            goal="Classify incoming tasks into the optimal routing category (local or commercial models)",
            backstory="""You are Mission Control for a hybrid fleet of 25 LLM models:
            - 20 local models (free, on DGX Spark)
            - 5 commercial models (paid, OpenAI/Anthropic/Google)

            Your job is to analyze each task and route it to the most cost-effective model.
            Prefer local models when possible. Use commercial models only when:
            - Task requires absolute best quality
            - Local models insufficient for task complexity
            - User explicitly requests premium quality""",
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

COMMERCIAL MODELS (Use only when necessary):
- max_quality_reasoning: Critical reasoning/coding requiring absolute best (Claude Sonnet 3.7)
- max_quality_multimodal: Best multimodal intelligence (GPT-4o)
- fast_commercial: Fast commercial when local insufficient (GPT-4o-mini)
- ultra_fast_commercial: Ultra-fast commercial (Claude Haiku 3.5)
- multimodal_grounded: Multimodal + web grounding (Gemini 2.0 Flash)

FEW-SHOT EXAMPLES:
1. "Analyze this sales chart and extract revenue trends" → max_vision (local)
2. "Prove that √2 is irrational" → max_reasoning (local)
3. "What's the weather like today?" → simple_chat (local)
4. "Generate JSON schema for user profile" → structured_data (local)
5. "Search 500 PDFs for mentions of 'quantum computing' with citations" → max_rag (local)
6. "Call the weather API and book a restaurant" → agentic_tool_use (local)
7. "Write production-grade distributed system code for my startup's core architecture" → max_quality_reasoning (commercial)
8. "Provide comprehensive strategic analysis for board presentation" → max_quality_reasoning (commercial)
9. "Analyze this complex image and search web for related context" → multimodal_grounded (commercial)
10. "I need the absolute best answer possible" → max_quality_multimodal (commercial)

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

    @listen(classify_task)
    def route_and_execute(self):
        """
        Route to appropriate model handler and execute it
        Uses direct method calling - no @router decorator needed
        """
        category = self.state.get("category", "default_general")

        print(f"\n🎯 Routing to category: {category}")

        # Direct routing - call the appropriate method based on category
        if category == "max_vision":
            return self.run_max_vision()
        elif category == "fast_vision":
            return self.run_fast_vision()
        elif category == "max_reasoning":
            return self.run_max_reasoning()
        elif category == "max_reasoning_moe":
            return self.run_max_reasoning_moe()
        elif category == "efficient_reasoning":
            return self.run_efficient_reasoning()
        elif category == "hybrid_reasoner":
            return self.run_hybrid_reasoner()
        elif category == "max_rag":
            return self.run_max_rag()
        elif category == "fast_rag":
            return self.run_fast_rag()
        elif category == "agentic_tool_use":
            return self.run_agentic_tool_use()
        elif category == "structured_data":
            return self.run_structured_data()
        elif category == "simple_chat":
            return self.run_simple_chat()
        elif category == "instruction_following":
            return self.run_instruction_following()
        elif category == "long_context":
            return self.run_long_context()
        elif category == "efficient_general":
            return self.run_efficient_general()
        elif category == "korean_multilingual":
            return self.run_korean_multilingual()
        elif category == "embeddings":
            return self.run_embeddings()
        # Commercial models
        elif category == "max_quality_reasoning":
            return self.run_max_quality_reasoning()
        elif category == "max_quality_multimodal":
            return self.run_max_quality_multimodal()
        elif category == "fast_commercial":
            return self.run_fast_commercial()
        elif category == "ultra_fast_commercial":
            return self.run_ultra_fast_commercial()
        elif category == "multimodal_grounded":
            return self.run_multimodal_grounded()
        else:  # default_general or unknown category
            return self.run_default_general()

    # Route handlers - called directly by route_and_execute()
    # No decorators needed - these are regular methods
    def run_max_vision(self):
        return self._execute_with_model("llama3.2-vision:90b")

    def run_fast_vision(self):
        return self._execute_with_model("llava:13b")

    def run_max_reasoning(self):
        return self._execute_with_model("deepseek-r1:70b")

    def run_max_reasoning_moe(self):
        return self._execute_with_model("deepseek-v3")

    def run_efficient_reasoning(self):
        return self._execute_with_model("phi4")

    def run_hybrid_reasoner(self):
        return self._execute_with_model("apriel-1.5-15b-thinker")

    def run_max_rag(self):
        return self._execute_with_model("command-r-plus")

    def run_fast_rag(self):
        return self._execute_with_model("command-r")

    def run_agentic_tool_use(self):
        return self._execute_with_model("gpt-oss:20b")

    def run_structured_data(self):
        return self._execute_with_model("qwen2.5:14b")

    def run_simple_chat(self):
        return self._execute_with_model("mistral:7b")

    def run_instruction_following(self):
        return self._execute_with_model("nous-hermes2")

    def run_long_context(self):
        return self._execute_with_model("llama3.1:70b")

    def run_default_general(self):
        return self._execute_with_model("mixtral:8x7b")

    def run_efficient_general(self):
        return self._execute_with_model("gemma2:9b")

    def run_korean_multilingual(self):
        return self._execute_with_model("solar")

    def run_embeddings(self):
        return self._execute_with_model("nomic-embed-text")

    # Commercial model handlers
    def run_max_quality_reasoning(self):
        return self._execute_with_model("claude-sonnet-3.7")

    def run_max_quality_multimodal(self):
        return self._execute_with_model("gpt-4o")

    def run_fast_commercial(self):
        return self._execute_with_model("gpt-4o-mini")

    def run_ultra_fast_commercial(self):
        return self._execute_with_model("claude-haiku-3.5")

    def run_multimodal_grounded(self):
        return self._execute_with_model("gemini-2.0-flash")

    def _execute_with_model(self, model_name: str) -> dict:
        """
        Execute the task using the selected model (local or commercial)
        """
        task_description = self.state.get("task_description", "")
        category = self.state.get("category", "unknown")
        reasoning = self.state.get("reasoning", "")

        model_config = MODELS.get(model_name)
        if not model_config:
            print(f"⚠️  Model {model_name} not found, using default")
            model_config = MODELS.get("mixtral:8x7b")
            model_name = "mixtral:8x7b"

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

        # Calculate cost for commercial models (rough estimate)
        cost_usd = 0.0
        if not is_local:
            # Rough token estimation: ~1.3 tokens per word
            input_tokens = len(task_description.split()) * 1.3
            output_tokens = len(str(result).split()) * 1.3
            cost_in = (input_tokens / 1_000_000) * model_config.get("cost_per_1m_in", 0)
            cost_out = (output_tokens / 1_000_000) * model_config.get("cost_per_1m_out", 0)
            cost_usd = cost_in + cost_out
            print(f"\n💰 Estimated cost: ${cost_usd:.6f} (~{int(input_tokens)} in, ~{int(output_tokens)} out tokens)")

        return {
            "task_description": task_description,
            "category": category,
            "selected_model": model_name,
            "model_params": model_config.get('params', 'N/A'),
            "model_size_gb": model_config.get('size_gb', 0),
            "routing_reasoning": reasoning,
            "is_local": is_local,
            "provider": provider,
            "cost_usd": cost_usd,
            "result": str(result)
        }


def run_router(task_description: str) -> dict:
    """
    Convenience function to run the router flow

    Usage:
        result = run_router("Analyze this sales chart and extract trends")
    """
    flow = DynamicModelFlow()
    result = flow.kickoff(inputs={"task_description": task_description})

    # kickoff() returns the final dict from route_and_execute()
    return result if isinstance(result, dict) else {"error": f"Unexpected result type: {type(result)}"}


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
