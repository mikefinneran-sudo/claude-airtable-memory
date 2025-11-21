"""
LLM Model Configurations for CrewAI Intelligent Router
Hybrid approach: 20 Local Models (DGX Spark) + 5 Commercial Models (API)
"""

from crewai import LLM
import os

# Base URL for all DGX Ollama models
OLLAMA_BASE_URL = "http://192.168.68.62:11434"

# Router Model (Mission Control) - GPT-4o-mini (Commercial)
# Switched from llama3.2:1b for reliable tool calling and classification
ROUTER_LLM_CONFIG = {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "temperature": 0.1,  # Low temp for consistent routing
    "cost_per_1m_in": 0.15,
    "cost_per_1m_out": 0.60
}

# Create router LLM instance
ROUTER_LLM = LLM(
    model=f"openai/{ROUTER_LLM_CONFIG['model']}",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=ROUTER_LLM_CONFIG["temperature"]
)

# Model Inventory - All 20 models on DGX Spark
MODELS = {
    # Ultra-Large Models (70B+) - High quality, slower inference
    "llama3.2-vision:90b": {
        "llm": LLM(model="ollama/llama3.2-vision:90b", base_url=OLLAMA_BASE_URL),
        "size_gb": 54,
        "params": "90B",
        "specialization": "max_vision",
        "capabilities": ["vision", "multimodal", "ocr", "chart_analysis"],
        "when_to_use": "Complex visual tasks requiring highest accuracy (charts, diagrams, OCR)",
        "speed": "slow",
        "quality": "highest"
    },

    "llama3.1:70b": {
        "llm": LLM(model="ollama/llama3.1:70b", base_url=OLLAMA_BASE_URL),
        "size_gb": 42,
        "params": "70B",
        "specialization": "long_context",
        "capabilities": ["general_purpose", "128k_context", "enterprise_grade"],
        "when_to_use": "Large documents, long context windows (128K tokens)",
        "speed": "slow",
        "quality": "highest"
    },

    "deepseek-r1:70b": {
        "llm": LLM(model="ollama/deepseek-r1:70b", base_url=OLLAMA_BASE_URL),
        "size_gb": 42,
        "params": "70B",
        "specialization": "max_reasoning",
        "capabilities": ["deep_reasoning", "math", "logic", "complex_analysis"],
        "when_to_use": "Complex reasoning, mathematical proofs, logic puzzles",
        "speed": "slow",
        "quality": "highest"
    },

    "deepseek-v3": {
        "llm": LLM(model="ollama/deepseek-v3", base_url=OLLAMA_BASE_URL),
        "size_gb": 404,
        "params": "671B (37B active MoE)",
        "specialization": "max_reasoning_moe",
        "capabilities": ["deep_reasoning", "moe_architecture", "efficient_inference"],
        "when_to_use": "Extremely complex reasoning with MoE efficiency",
        "speed": "medium",  # MoE activates only 37B
        "quality": "highest"
    },

    # Large Models (13B-60B) - Balanced quality/speed
    "command-r-plus": {
        "llm": LLM(model="ollama/command-r-plus", base_url=OLLAMA_BASE_URL),
        "size_gb": 59,
        "params": "104B",
        "specialization": "max_rag",
        "capabilities": ["rag", "document_search", "citations", "retrieval"],
        "when_to_use": "Complex document search with citations and grounded answers",
        "speed": "slow",
        "quality": "highest"
    },

    "qwen2.5:72b": {
        "llm": LLM(model="ollama/qwen2.5:72b", base_url=OLLAMA_BASE_URL),
        "size_gb": 47,
        "params": "72B",
        "specialization": "max_quality_general",
        "capabilities": ["general_purpose", "reasoning", "coding", "multilingual"],
        "when_to_use": "High-quality general tasks, complex coding, multilingual",
        "speed": "slow",
        "quality": "highest"
    },

    "mixtral:8x7b": {
        "llm": LLM(model="ollama/mixtral:8x7b", base_url=OLLAMA_BASE_URL),
        "size_gb": 26,
        "params": "47B (8x7B MoE)",
        "specialization": "default_general",
        "capabilities": ["general_purpose", "moe_architecture", "balanced_speed_quality"],
        "when_to_use": "Default worker for general tasks (good speed/quality balance)",
        "speed": "medium",
        "quality": "high"
    },

    "command-r": {
        "llm": LLM(model="ollama/command-r", base_url=OLLAMA_BASE_URL),
        "size_gb": 18,
        "params": "35B",
        "specialization": "fast_rag",
        "capabilities": ["rag", "document_search", "grounded_answers"],
        "when_to_use": "Fast RAG with good citation quality",
        "speed": "medium",
        "quality": "high"
    },

    "gpt-oss:20b": {
        "llm": LLM(model="ollama/gpt-oss:20b", base_url=OLLAMA_BASE_URL),
        "size_gb": 13,
        "params": "20B",
        "specialization": "agentic_tool_use",
        "capabilities": ["tool_calling", "api_integration", "function_calling"],
        "when_to_use": "Agentic workflows, API calls, tool orchestration",
        "speed": "medium",
        "quality": "high"
    },

    "llava:13b": {
        "llm": LLM(model="ollama/llava:13b", base_url=OLLAMA_BASE_URL),
        "size_gb": 8.0,
        "params": "13B",
        "specialization": "fast_vision",
        "capabilities": ["vision", "image_captions", "fast_inference"],
        "when_to_use": "Simple vision tasks (image descriptions, basic object detection)",
        "speed": "fast",
        "quality": "medium"
    },

    # Medium Models (7B-15B) - Fast, specialized
    "apriel-1.5-15b-thinker": {
        "llm": LLM(model="ollama/MichelRosselli/apriel-1.5-15b-thinker", base_url=OLLAMA_BASE_URL),
        "size_gb": 9.7,
        "params": "15B",
        "specialization": "hybrid_reasoner",
        "capabilities": ["reasoning", "vision", "multimodal_reasoning"],
        "when_to_use": "Visual reasoning tasks (math diagrams, flowcharts with logic)",
        "speed": "fast",
        "quality": "high"
    },

    "phi4": {
        "llm": LLM(model="ollama/phi4", base_url=OLLAMA_BASE_URL),
        "size_gb": 9.1,
        "params": "14B",
        "specialization": "efficient_reasoning",
        "capabilities": ["reasoning", "compact", "efficient"],
        "when_to_use": "Text reasoning tasks requiring good quality but faster than 70B",
        "speed": "fast",
        "quality": "high"
    },

    "qwen2.5:14b": {
        "llm": LLM(model="ollama/qwen2.5:14b", base_url=OLLAMA_BASE_URL),
        "size_gb": 9.0,
        "params": "14B",
        "specialization": "structured_data",
        "capabilities": ["json_generation", "structured_output", "fast_coding"],
        "when_to_use": "JSON generation, structured data extraction, fast coding",
        "speed": "fast",
        "quality": "high"
    },

    "gemma2:9b": {
        "llm": LLM(model="ollama/gemma2:9b", base_url=OLLAMA_BASE_URL),
        "size_gb": 5.4,
        "params": "9B",
        "specialization": "efficient_general",
        "capabilities": ["general_purpose", "efficient", "google_trained"],
        "when_to_use": "General tasks requiring good efficiency",
        "speed": "fast",
        "quality": "medium"
    },

    "mistral:7b": {
        "llm": LLM(model="ollama/mistral:7b", base_url=OLLAMA_BASE_URL),
        "size_gb": 4.4,
        "params": "7B",
        "specialization": "simple_chat",
        "capabilities": ["conversation", "fast_responses", "lightweight"],
        "when_to_use": "Simple chat, fastest conversational responses",
        "speed": "fastest",
        "quality": "medium"
    },

    "nous-hermes2": {
        "llm": LLM(model="ollama/nous-hermes2", base_url=OLLAMA_BASE_URL),
        "size_gb": 6.1,
        "params": "7B",
        "specialization": "instruction_following",
        "capabilities": ["instruction_following", "helpful_assistant"],
        "when_to_use": "Tasks requiring precise instruction following",
        "speed": "fast",
        "quality": "medium"
    },

    "solar": {
        "llm": LLM(model="ollama/solar", base_url=OLLAMA_BASE_URL),
        "size_gb": 6.1,
        "params": "11B",
        "specialization": "korean_multilingual",
        "capabilities": ["multilingual", "korean", "general_purpose"],
        "when_to_use": "Korean language tasks or multilingual needs",
        "speed": "fast",
        "quality": "medium"
    },

    # Small Models (1B-3B) - Ultra-fast
    "llama3.2:1b": {
        "llm": LLM(model="ollama/llama3.2:1b", base_url=OLLAMA_BASE_URL),
        "size_gb": 1.3,
        "params": "1B",
        "specialization": "router",
        "capabilities": ["classification", "ultra_fast", "routing"],
        "when_to_use": "Task classification ONLY (Mission Control router)",
        "speed": "ultra_fast",
        "quality": "low"
    },

    # Specialized Models
    "nomic-embed-text": {
        "llm": LLM(model="ollama/nomic-embed-text", base_url=OLLAMA_BASE_URL),
        "size_gb": 0.274,
        "params": "137M",
        "specialization": "embeddings",
        "capabilities": ["text_embeddings", "vector_search", "similarity"],
        "when_to_use": "Text embeddings for RAG, vector search, semantic similarity",
        "speed": "ultra_fast",
        "quality": "specialized",
        "provider": "ollama"
    },

    # ==============================================================================
    # COMMERCIAL MODELS (API-based, paid per use)
    # ==============================================================================

    "claude-sonnet-3.7": {
        "llm": LLM(
            model="anthropic/claude-3-7-sonnet-20250219",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        ),
        "provider": "anthropic",
        "model_id": "claude-3-7-sonnet-20250219",
        "specialization": "max_quality_reasoning",
        "capabilities": ["reasoning", "coding", "analysis", "long_context"],
        "when_to_use": "Critical tasks requiring best possible reasoning, coding, or analysis",
        "speed": "medium",
        "quality": "absolute_best",
        "cost_per_1m_in": 3.0,
        "cost_per_1m_out": 15.0,
        "context_window": 200000
    },

    "gpt-4o": {
        "llm": LLM(
            model="openai/gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY")
        ),
        "provider": "openai",
        "model_id": "gpt-4o",
        "specialization": "max_quality_multimodal",
        "capabilities": ["multimodal", "vision", "reasoning", "general_purpose"],
        "when_to_use": "Best general intelligence, multimodal tasks, complex analysis",
        "speed": "medium",
        "quality": "absolute_best",
        "cost_per_1m_in": 2.5,
        "cost_per_1m_out": 10.0,
        "context_window": 128000
    },

    "gpt-4o-mini": {
        "llm": LLM(
            model="openai/gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        ),
        "provider": "openai",
        "model_id": "gpt-4o-mini",
        "specialization": "fast_commercial",
        "capabilities": ["general_purpose", "fast", "cost_effective"],
        "when_to_use": "Fast commercial tasks when local models insufficient",
        "speed": "fast",
        "quality": "high",
        "cost_per_1m_in": 0.15,
        "cost_per_1m_out": 0.60,
        "context_window": 128000
    },

    "claude-haiku-3.5": {
        "llm": LLM(
            model="anthropic/claude-3-5-haiku-20241022",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        ),
        "provider": "anthropic",
        "model_id": "claude-3-5-haiku-20241022",
        "specialization": "ultra_fast_commercial",
        "capabilities": ["ultra_fast", "general_purpose", "cost_effective"],
        "when_to_use": "Ultra-fast commercial responses when local insufficient",
        "speed": "ultra_fast",
        "quality": "high",
        "cost_per_1m_in": 0.25,
        "cost_per_1m_out": 1.25,
        "context_window": 200000
    },

    "gemini-2.0-flash": {
        "llm": LLM(
            model="google/gemini-2.0-flash-thinking-exp",
            api_key=os.getenv("GOOGLE_API_KEY")
        ),
        "provider": "google",
        "model_id": "gemini-2.0-flash-thinking-exp",
        "specialization": "multimodal_grounded",
        "capabilities": ["multimodal", "vision", "grounding", "web_search", "thinking"],
        "when_to_use": "Multimodal tasks requiring web grounding or real-time information",
        "speed": "fast",
        "quality": "high",
        "cost_per_1m_in": 0.075,
        "cost_per_1m_out": 0.30,
        "context_window": 1000000
    },

    # ==============================================================================
    # DEPRECATED - Do not use
    # ==============================================================================

    "llama3:70b": {
        "llm": LLM(model="ollama/llama3:70b", base_url=OLLAMA_BASE_URL),
        "size_gb": 39,
        "params": "70B",
        "specialization": "deprecated",
        "capabilities": ["general_purpose"],
        "when_to_use": "DEPRECATED - Use llama3.1:70b instead",
        "speed": "slow",
        "quality": "high",
        "deprecated": True
    }
}

# Routing Categories (Hybrid: Local + Commercial)
ROUTING_CATEGORIES = {
    # Local Models (Free) - Prefer these when possible
    "max_vision": "llama3.2-vision:90b",
    "fast_vision": "llava:13b",
    "max_reasoning": "deepseek-r1:70b",
    "max_reasoning_moe": "deepseek-v3",
    "efficient_reasoning": "phi4",
    "hybrid_reasoner": "apriel-1.5-15b-thinker",
    "max_rag": "command-r-plus",
    "fast_rag": "command-r",
    "agentic_tool_use": "gpt-oss:20b",
    "structured_data": "qwen2.5:14b",
    "simple_chat": "mistral:7b",
    "instruction_following": "nous-hermes2",
    "long_context": "llama3.1:70b",
    "default_general": "mixtral:8x7b",
    "efficient_general": "gemma2:9b",
    "korean_multilingual": "solar",
    "embeddings": "nomic-embed-text",

    # Commercial Models (Paid) - Use when local insufficient
    "max_quality_reasoning": "claude-sonnet-3.7",        # Best reasoning/coding
    "max_quality_multimodal": "gpt-4o",                  # Best multimodal
    "fast_commercial": "gpt-4o-mini",                    # Fast + cheap
    "ultra_fast_commercial": "claude-haiku-3.5",         # Ultra-fast
    "multimodal_grounded": "gemini-2.0-flash"            # Multimodal + web grounding
}

def get_model_by_category(category: str) -> dict:
    """Get model configuration by routing category"""
    model_name = ROUTING_CATEGORIES.get(category)
    if model_name:
        return MODELS.get(model_name)
    return None

def get_all_active_models() -> dict:
    """Get all non-deprecated models"""
    return {k: v for k, v in MODELS.items() if not v.get("deprecated", False)}

def is_local_model(model_name: str) -> bool:
    """Check if model is local (Ollama) or commercial (API)"""
    model = MODELS.get(model_name)
    if not model:
        return False
    return model.get("provider", "ollama") == "ollama"

def get_commercial_models() -> dict:
    """Get all commercial (paid API) models"""
    return {k: v for k, v in MODELS.items()
            if v.get("provider") not in ["ollama", None] and not v.get("deprecated", False)}
