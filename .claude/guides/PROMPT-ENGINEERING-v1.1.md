# Prompt Engineering Standards v1.1

**Last Updated:** 2025-11-12
**Version:** 1.1
**Owner:** Mike Finneran

---

## Phase 0: Delegation Check

**Question:** Do you want to execute this task personally, or delegate it to your CrewAI team?

- [ ] **Execute Personally** (Proceed to Phase 1)
- [ ] **Delegate to Hybrid LLM Router** (Use intelligent model routing)
- [ ] **Delegate to CrewAI Team** (Stop here and pass protocol)

---

## Hybrid LLM Router (Intelligent Model Selection)

**Status:** ✅ Active - Production Ready
**Location:** `~/crewai-specialists/llm-router/`
**Fleet:** 20 Local Models (DGX Spark) + 5 Commercial Models (OpenAI/Anthropic/Google)

### When to Use:
- User asks a question that could be answered by an LLM
- Task needs reasoning, coding, analysis, or generation
- Want to minimize costs (use free local models when possible)
- Need best-in-class quality (route to commercial when necessary)

### How It Works:
1. **Classification**: Claude (me!) analyzes your task and selects optimal model
2. **Routing**: I directly call ONE model from fleet of 25
3. **Execution**: Selected model completes the task on DGX
4. **Cost Tracking**: Monitors commercial API usage ($0 for local, actual cost for commercial)

**Key Advantage**: No intermediate GPT-4o-mini call - I'm already here and know your context!

### Usage from Claude Code:
```bash
# I run this command for you when you ask to use your fleet:
sshpass -p 'Wally9381' ssh mikefinneran@192.168.68.88 \
  "cd ~/crewai-specialists/llm-router && source ../venv/bin/activate && \
  python execute_with_model.py '<model>' 'Your task here'"

# Examples:
# python execute_with_model.py 'mistral:7b' 'What is 2+2?'
# python execute_with_model.py 'deepseek-r1:70b' 'Prove √2 is irrational'
# python execute_with_model.py 'claude-sonnet-3.7' 'Write production code'
```

### Model Fleet:

**Local Models (FREE - DGX Spark .88):**
- `mistral:7b` - Simple chat, fastest responses
- `phi4` (14B) - Efficient reasoning
- `gemma2:9b` - Efficient general tasks
- `llava:13b` - Fast vision (image captions)
- `qwen2.5:14b` - JSON generation, structured data
- `mixtral:8x7b` - Default general (balanced speed/quality)
- `deepseek-r1:70b` - Max reasoning (math proofs, logic)
- `deepseek-v3` (671B MoE) - Extreme reasoning with efficiency
- `llama3.1:70b` - Long context (128K tokens)
- `llama3.2-vision:90b` - Max vision (complex charts, OCR)
- `command-r-plus` (104B) - Max RAG with citations
- `gpt-oss:20b` - Agentic tool use, API orchestration

**Commercial Models (PAID - API):**
- `claude-sonnet-3.7` - Best reasoning/coding ($3/$15 per 1M tokens)
- `gpt-4o` - Best multimodal intelligence ($2.5/$10 per 1M tokens)
- `gpt-4o-mini` - Fast commercial ($0.15/$0.60 per 1M tokens)
- `claude-haiku-3.5` - Ultra-fast commercial ($0.25/$1.25 per 1M tokens)
- `gemini-2.0-flash` - Multimodal + web grounding ($0.075/$0.30 per 1M tokens)

### Routing Categories:
- **simple_chat** → mistral:7b (local)
- **efficient_reasoning** → phi4 (local)
- **max_reasoning** → deepseek-r1:70b (local)
- **structured_data** → qwen2.5:14b (local)
- **fast_vision** → llava:13b (local)
- **max_vision** → llama3.2-vision:90b (local)
- **max_quality_reasoning** → claude-sonnet-3.7 (commercial) - *Use when user says "best", "critical", "production-grade"*
- **max_quality_multimodal** → gpt-4o (commercial) - *Use when user says "absolute best"*
- **multimodal_grounded** → gemini-2.0-flash (commercial) - *Use for real-time web data*

### Decision Logic:
**PREFER LOCAL (FREE)** for:
- Simple questions and conversations
- Basic coding tasks
- Math and reasoning problems
- Image analysis and OCR
- Document search and RAG
- JSON generation
- General tasks

**USE COMMERCIAL (PAID)** only when:
- User explicitly requests "best possible", "highest quality", "critical"
- Task is for production/business decisions requiring absolute accuracy
- Local models insufficient for complexity
- Need real-time web grounding

### Example Routing Decisions:
```
"What's 2+2?" → efficient_reasoning (phi4, local, FREE)
"Explain quantum entanglement" → efficient_reasoning (phi4, local, FREE)
"Write a Python function for prime checking" → structured_data (qwen2.5, local, FREE)
"Prove √2 is irrational" → max_reasoning (deepseek-r1:70b, local, FREE)
"I need the BEST strategic analysis for my board presentation" → max_quality_reasoning (claude-sonnet-3.7, commercial, ~$0.03)
"Generate production-grade distributed system code" → max_quality_reasoning (claude-sonnet-3.7, commercial, ~$0.05)
```

### Cost Monitoring:
- Local models: **$0.00** (unlimited, runs on DGX Spark)
- Commercial models: **Tracked per request** (estimated tokens × rate)
- Prefer local unless quality explicitly demanded

### Integration with Claude Code - AUTOMATIC ROUTING:

**I (Claude) automatically decide:** Answer myself OR route to your fleet

**Route to YOUR FLEET (FREE) when:**
- ✅ **Simple factual questions** → mistral:7b, phi4 (I route these to save you $)
- ✅ **Math/reasoning** → deepseek-r1:70b (your local model is specialized)
- ✅ **Bulk/repetitive tasks** → Local models (unlimited free usage)
- ✅ **You explicitly ask** → "use deepseek", "use my fleet", etc.
- ✅ **Korean language** → solar (specialized model)
- ✅ **Vision/OCR tasks** → llama3.2-vision:90b or llava:13b
- ✅ **RAG/document search** → command-r-plus (specialized)
- ✅ **Embeddings** → nomic-embed-text

**I answer DIRECTLY when:**
- ❌ **Complex analysis** → I'm better than local 7B-14B models
- ❌ **Code generation** → I'm better (unless you want qwen2.5)
- ❌ **Conversation/context** → I have your full conversation history
- ❌ **Planning/strategy** → I excel at this
- ❌ **Quick answers** → Faster for me to answer than SSH roundtrip
- ❌ **Follow-up questions** → I have context, local models don't

**Decision Framework:**
```
IF (simple fact OR pure math OR specialized task):
    → Route to FREE local model
ELSE IF (requires context OR complex reasoning OR I'm clearly better):
    → I answer directly
ELSE IF (user wants "BEST" quality):
    → Route to claude-sonnet-3.7 (paid, ~$0.03)
```

**Examples:**
- "What's 2+2?" → **Fleet** (mistral:7b, instant, FREE)
- "Prove √2 is irrational" → **Fleet** (deepseek-r1:70b, specialized, FREE)
- "Explain the architecture we discussed earlier" → **Me** (need context)
- "Write me a Python function for quicksort" → **Me** (I'm better at code)
- "I need OCR from this image" → **Fleet** (llama3.2-vision:90b, FREE)
- "I need the BEST strategic analysis" → **Fleet** (claude-sonnet-3.7, PAID ~$0.03)

**Transparency**: I'll tell you when I'm routing: "Routing to deepseek-r1:70b (free)..."

---

## Phase 1: The Core Protocol (The Foundation)

This is the lean, universal foundation for any task.

### 1. Objective
[A single, clear sentence describing the final, desired outcome.]

### 2. Core Context
[Provide the essential background, project, or problem statement. All non-essential details are moved to modules.]

### 3. Persona
**Prompt:** "Act as an expert with [X] years of experience in [domain], specializing in [specialization]. You are [Adjective 1] and [Adjective 2]."

**Why:** A specific, detailed persona is critical. Vague personas ("act as a marketer") are ineffective, but exhaustive personas demonstrably improve accuracy and style.

### 4. Few-Shot Examples (Demonstrations)
[Provide 2-5 examples of the desired input/output. Use clear delimiters.]

**Example:**
```markdown
<example>
<input>
[Input Example 1]
</input>
<output>
[Output Example 1]
</output>
</example>

<example>
<input>
[Input Example 2]
</input>
<output>
[Output Example 2]
</output>
</example>
```

**Why:** Showing is more effective than telling. This is the most reliable way to enforce a specific format, style, or logical pattern.

### 5. Task & Deliverables
[A clear, itemized breakdown of the task. Use decomposition.]

- **Deliverable 1:**
- **Deliverable 2:**
- **Deliverable 3:**

**Why:** Breaking complex tasks into smaller, sequential steps is a core best practice that prevents cognitive overload and improves accuracy.

### 6. Constraints & Guardrails

**Mandates (Must Do):**
- [e.g., "Must use Python 3.10+"]
- [e.g., "Must cite all claims using the provided context"]

**Guardrails (Must NOT Do):**
- [e.g., "Must NOT use buzzwords like 'synergy' or 'leverage'"]
- [e.g., "Must NOT generate code without error handling"]

**Why:** Explicit Negative Prompting provides clear boundaries and is highly effective at eliminating "edge cases" and refining output quality, which positive instructions alone cannot do.

### 7. Reasoning Requirement
**Instruction:** "You MUST explain your reasoning process step-by-step before providing the final answer. Use a 'Chain of Thought' (CoT) to break down the problem, identify key components, and build your solution."

**Why:** Mandating Chain of Thought (CoT) forces the AI to use intermediate reasoning steps, which significantly improves accuracy on complex tasks and makes the output verifiable.

### 8. Validation & Rejection Criteria
**Instruction:** "After generating your response, you MUST validate it against the following criteria. If it fails, you MUST refine it until it passes."

- **[Criterion 1]:** [e.g., "Is the tone professional and solution-oriented?"]
- **[Criterion 2]:** [e.g., "Are all deliverables from section 5 present?"]
- **[Criterion 3]:** [e.g., "Does the solution follow all constraints?"]

**Why:** This operationalizes your Success Criteria as Rejection Criteria, creating a built-in iterative feedback loop where the AI self-corrects before delivering the final output.

---

## Phase 2: Modular Augments (For Specialized Tasks)

Instead of one-size-fits-all templates, you now "plug in" these specialized modules to the Core Protocol when needed.

### RAG (Research) Module
**Purpose:** To prevent hallucinations and ground the AI in specific knowledge.

**Prompt (Add to Section 6):**
- "You MUST answer the query using *only* the information from the `<context>` provided below."
- "Do NOT use any outside knowledge."
- "If the answer is not in the `<context>`, you MUST state: 'The provided context does not contain the answer to this question.'"

**Prompt (Add to Section 7):**
- "Chain of Thought: First, identify key facts in the retrieved context. Then, reason step-by-step how these facts answer the query."

**(Optional) HyDE:** For complex retrieval, first ask the AI: "Write a hypothetical paragraph answering {user query}. Use this text to find relevant documents."

### Decomposition (Code Gen) Module
**Purpose:** To generate accurate, complex code.

**Prompt (Add to Section 5):** Decompose the task aggressively.
- "1. Define the 'User' data model in Python."
- "2. Write the API endpoint for POST /login."
- "3. Write error handling for invalid passwords."

**Prompt (Add to Section 6):** Use "leading words" to nudge the model.
- "The Python function begins with: `import...`"

### Style Guide (Content) Module
**Purpose:** To generate content with a precise, non-generic style.

**Prompt (Add to Section 3 - Persona):** Replace vague Tone ("friendly") with a rich style description.
- "Style Guide: 'Fireside Chat Style'. Write in a warm, conversational style... Use contractions and everyday language... Aim to sound like you're speaking naturally to a good friend over coffee."

**Prompt (Add to Section 4 - Examples):** Provide a 1-2 paragraph example of the desired style.

### Framework (Business Strategy) Module
**Purpose:** To get structured, high-level analysis instead of generic advice.

**Prompt (Add to Section 5):** Embed a specific analytical framework.
- "Conduct a detailed SWOT analysis... Then, transform the SWOT into a TOWS matrix, creating specific strategies in each quadrant (SO, ST, WO, WT)."
- "Evaluate my business model using the 9 components of the Business Model Canvas."

---

## Phase 3: The Execution Protocol (How to Use It)

This is the most critical enhancement. You should no longer use a "fire-and-forget" approach.

### P1: Static Execution (For Simple Tasks)
1. Run the "Augmented Prompt" once
2. Accept the output
3. *Use this for low-stakes, simple tasks*

### P2: Dynamic Execution (For Complex Tasks)
This implements the "Rejection Loop Method" and is the elite standard for quality.

**Step 1:** Run the "Augmented Prompt" (Genesis Prompt)

**Step 2:** Provide 1-3 rounds of manual feedback, using your Validation Criteria
- "Reject: Too generic."
- "Reject: Uses buzzwords (Constraint #1)."
- "Keep: The tone of the introduction."

**Step 3:** Engage the "Self-Critique" step
- **Prompt:** "Now, using the rejection criteria we have established, generate 5 new options. First, analyze your own options against the criteria. Then, show me only the 3 options that pass your own quality check."

---

*Reference this guide when delegating tasks to AI systems*
