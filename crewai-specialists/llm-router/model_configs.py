"""
LLM Model Configurations for CrewAI Intelligent Router
All models run on DGX Spark @ 192.168.68.88:11434
"""

from crewai import LLM

# Base URL for all DGX Ollama models
OLLAMA_BASE_URL = "http://192.168.68.88:11434"

# Router Model (Mission Control) - llama3.2:1b
# Ultra-fast classification agent (1.3GB, optimized for speed)
ROUTER_LLM = LLM(
    model="ollama/llama3.2:1b",
    base_url=OLLAMA_BASE_URL,
    temperature=0.1  # Low temp for consistent routing decisions
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
        "quality": "specialized"
    },

    # DEPRECATED - Do not use
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

# Routing Categories (from research document)
ROUTING_CATEGORIES = {
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
    "max_quality_general": "qwen2.5:72b",
    "default_general": "mixtral:8x7b",
    "efficient_general": "gemma2:9b",
    "korean_multilingual": "solar",
    "embeddings": "nomic-embed-text"
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
