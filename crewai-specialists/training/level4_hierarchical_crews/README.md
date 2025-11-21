# Level 4: Hierarchical Crews with Manager Agents

## Learning Objectives

1. **Understand Hierarchical vs Sequential Process**
   - Sequential: Fixed linear pipeline (A → B → C)
   - Hierarchical: Dynamic delegation by manager agent
   - When to use each pattern

2. **Master Manager Agent Pattern**
   - Manager agent decides task assignment and order
   - Delegates work to specialized worker agents
   - Synthesizes results from multiple agents

3. **Enable Complex Workflows**
   - Multi-phase projects requiring adaptive planning
   - Parallel task execution when appropriate
   - Dynamic re-planning based on intermediate results

4. **Custom Manager Agents**
   - Build custom manager agents (not CrewAI default)
   - Give managers specific expertise (e.g., GTM Strategy Manager)
   - Manager persona influences delegation decisions

## Sequential vs Hierarchical

### Sequential Process (Levels 1-3)

```python
Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.sequential  # Fixed order: task1 → task2 → task3
)
```

**Characteristics:**
- Predictable execution order
- Each task waits for previous task
- Simple to understand and debug
- Best for linear ETL-style workflows

**Use when:**
- Task order is always the same
- Each step depends on previous step
- No need for adaptive planning
- Example: Document processing, report generation

### Hierarchical Process (Level 4)

```python
Crew(
    agents=[manager, worker1, worker2, worker3],
    tasks=[task1, task2, task3, task4],
    process=Process.hierarchical,  # Manager decides order and assignment
    manager_llm="gpt-4"  # Or create custom manager
)
```

**Characteristics:**
- Manager agent coordinates work
- Can execute tasks in parallel
- Adapts plan based on results
- Manager synthesizes final output

**Use when:**
- Complex multi-phase projects
- Task order depends on intermediate results
- Some tasks can run in parallel
- Need intelligent coordination
- Example: GTM strategy, product launch, M&A analysis

## Manager Agent Types

### 1. Default Manager (CrewAI Built-in)

```python
crew = Crew(
    agents=[analyst, writer, reviewer],
    tasks=[research_task, write_task, review_task],
    process=Process.hierarchical,
    manager_llm="gpt-4"  # Use default manager
)
```

**Characteristics:**
- Generic project manager
- No domain expertise
- Basic delegation logic
- Good for simple hierarchical workflows

### 2. Custom Manager Agent (Recommended)

```python
manager = Agent(
    role="GTM Strategy Manager",
    goal="Coordinate team to create comprehensive go-to-market strategy",
    backstory="""
    You are a senior GTM strategist with 15 years of experience launching
    products. You understand the interdependencies between competitive analysis,
    positioning, messaging, and sales strategy. You delegate tasks intelligently,
    ensuring research is complete before strategy development, and messaging
    aligns with competitive positioning.
    """,
    allow_delegation=True,  # Critical for managers
    verbose=True
)

crew = Crew(
    agents=[manager, competitive_analyst, strategist, copywriter],
    tasks=[analysis_task, strategy_task, messaging_task],
    process=Process.hierarchical,
    manager_agent=manager  # Use custom manager
)
```

**Characteristics:**
- Domain-specific expertise
- Understands task interdependencies
- Better delegation decisions
- Persona influences coordination style

## Delegation Patterns

### Pattern 1: Research → Analysis → Synthesis

```python
# Worker agents
researcher = Agent(role="Researcher", allow_delegation=False)
analyst = Agent(role="Analyst", allow_delegation=False)

# Manager coordinates
manager = Agent(
    role="Research Director",
    goal="Produce comprehensive market analysis",
    allow_delegation=True  # Can delegate to workers
)

tasks = [
    Task(description="Research competitor A", agent=researcher),
    Task(description="Research competitor B", agent=researcher),
    Task(description="Analyze market gaps", agent=analyst),
    Task(description="Synthesize final report", agent=manager)
]

crew = Crew(
    agents=[manager, researcher, analyst],
    tasks=tasks,
    process=Process.hierarchical,
    manager_agent=manager
)
```

**Flow:**
1. Manager assigns both research tasks (can run in parallel)
2. Manager waits for research completion
3. Manager assigns analysis task
4. Manager synthesizes final report

### Pattern 2: Parallel Execution with Synthesis

```python
# Multiple specialists working in parallel
manager = Agent(role="Product Launch Manager", allow_delegation=True)
copywriter = Agent(role="Copywriter", allow_delegation=False)
designer = Agent(role="Designer", allow_delegation=False)
sales_enablement = Agent(role="Sales Enabler", allow_delegation=False)

tasks = [
    Task(description="Create marketing copy", agent=copywriter),
    Task(description="Design landing page", agent=designer),
    Task(description="Build sales deck", agent=sales_enablement),
    Task(description="Coordinate launch plan", agent=manager)
]

# Manager can execute copy, design, and sales tasks in parallel
# Then synthesize launch plan incorporating all outputs
```

### Pattern 3: Conditional Workflow

```python
manager = Agent(role="QA Manager", allow_delegation=True)
tester = Agent(role="QA Tester", allow_delegation=False)
developer = Agent(role="Developer", allow_delegation=False)

tasks = [
    Task(description="Test feature X", agent=tester),
    Task(description="Fix bugs if found", agent=developer),  # Conditional
    Task(description="Re-test after fixes", agent=tester),   # Conditional
    Task(description="Approve for release", agent=manager)
]

# Manager decides whether to execute fix and re-test tasks
# based on first test results
```

## Key Differences: Sequential vs Hierarchical

| Aspect | Sequential | Hierarchical |
|--------|-----------|--------------|
| **Execution Order** | Fixed, predetermined | Dynamic, manager decides |
| **Parallelization** | No, strictly linear | Yes, manager can parallelize |
| **Adaptation** | No, follows plan exactly | Yes, adjusts based on results |
| **Complexity** | Simple, easy to debug | Complex, requires coordination |
| **Task Assignment** | Pre-assigned to agents | Manager assigns at runtime |
| **Best For** | ETL, pipelines, reporting | Strategy, planning, complex projects |
| **Speed** | Slower (serial execution) | Faster (parallel when possible) |
| **Predictability** | High | Lower (depends on manager decisions) |

## When to Use Hierarchical Process

**✅ Use hierarchical when:**
- Complex multi-phase projects (GTM, M&A, product launch)
- Some tasks can run in parallel
- Task order depends on intermediate results
- Need intelligent re-planning
- Have 4+ tasks with conditional dependencies
- Want manager to synthesize final output

**❌ Use sequential instead when:**
- Simple linear workflow (ETL, document processing)
- All tasks must run in specific order
- No opportunity for parallelization
- Want predictable, debuggable execution
- Have 2-3 tasks in fixed pipeline

## Manager Agent Design Guidelines

### 1. Set allow_delegation=True

```python
manager = Agent(
    role="Strategy Manager",
    goal="Coordinate strategic planning",
    allow_delegation=True  # REQUIRED for managers
)
```

### 2. Give Domain Expertise

```python
# ❌ Generic manager
backstory="You are a project manager who delegates tasks."

# ✅ Domain expert manager
backstory="""
You are a GTM strategy expert with 15 years of B2B SaaS experience.
You understand the critical path: competitive analysis must inform
positioning, positioning drives messaging, and messaging enables sales.
You delegate intelligently and ensure work products build on each other.
"""
```

### 3. Manager Goal = Crew Goal

```python
manager = Agent(
    role="GTM Manager",
    goal="Deliver complete go-to-market strategy for WalterSignal"
    # This should align with overall crew objective
)
```

### 4. Manager Synthesizes Final Output

The manager agent typically performs the final synthesis task:

```python
final_task = Task(
    description="Synthesize competitive analysis, strategy, and messaging into final GTM plan",
    agent=manager,  # Manager does final synthesis
    context=[task1, task2, task3]  # Gets all worker outputs
)
```

## Example: GTM Strategy with Hierarchical Process

```python
from crewai import Agent, Task, Crew, Process

# Manager
gtm_manager = Agent(
    role="Go-To-Market Strategy Manager",
    goal="Deliver comprehensive GTM strategy for product launch",
    backstory="Expert GTM strategist who coordinates competitive analysis, positioning, messaging, and sales enablement.",
    allow_delegation=True
)

# Workers
competitive_analyst = Agent(role="Competitive Intelligence Specialist", allow_delegation=False)
strategist = Agent(role="Business Strategist", allow_delegation=False)
copywriter = Agent(role="Marketing Copywriter", allow_delegation=False)
sales_expert = Agent(role="Sales Strategist", allow_delegation=False)

# Tasks
competitive_research = Task(
    description="Analyze competitors and identify market gaps",
    expected_output="SWOT analysis with market opportunities",
    agent=competitive_analyst
)

positioning_strategy = Task(
    description="Develop positioning based on competitive analysis",
    expected_output="Positioning statement and key differentiators",
    agent=strategist,
    context=[competitive_research]
)

messaging = Task(
    description="Create messaging aligned with positioning",
    expected_output="Value prop, elevator pitch, website copy",
    agent=copywriter,
    context=[competitive_research, positioning_strategy]
)

sales_playbook = Task(
    description="Build sales playbook with objection handling",
    expected_output="Sales playbook with demo script and objections",
    agent=sales_expert,
    context=[competitive_research, positioning_strategy, messaging]
)

final_synthesis = Task(
    description="Synthesize all outputs into cohesive GTM strategy",
    expected_output="Complete GTM strategy document ready for exec review",
    agent=gtm_manager,
    context=[competitive_research, positioning_strategy, messaging, sales_playbook]
)

# Hierarchical crew with custom manager
crew = Crew(
    agents=[gtm_manager, competitive_analyst, strategist, copywriter, sales_expert],
    tasks=[competitive_research, positioning_strategy, messaging, sales_playbook, final_synthesis],
    process=Process.hierarchical,
    manager_agent=gtm_manager  # Custom manager coordinates
)

result = crew.kickoff()
```

**What happens:**
1. Manager assigns competitive_research to analyst
2. Once complete, manager assigns positioning_strategy
3. Manager can parallelize messaging and sales_playbook (both depend on positioning)
4. Manager synthesizes final GTM strategy incorporating all outputs

## Common Issues

**Issue**: Tasks execute in wrong order
**Fix**: Check task `context` dependencies - manager respects these

**Issue**: Manager doesn't delegate
**Fix**: Ensure `allow_delegation=True` on manager agent

**Issue**: Workers try to delegate
**Fix**: Set `allow_delegation=False` on all non-manager agents

**Issue**: Unpredictable results
**Fix**: This is normal for hierarchical - manager makes dynamic decisions

**Issue**: Manager skips tasks
**Fix**: Ensure tasks have clear descriptions and expected outputs

## Next Steps

After completing Level 4, you should:
- Understand when to use hierarchical vs sequential
- Be able to design custom manager agents
- Know how to structure tasks for delegation
- Recognize patterns for parallel execution

**Ready for Level 5?** → Human-in-the-Loop (HITL) patterns

## Files Structure

```
level4_hierarchical_crews/
├── config/
│   └── (example hierarchical crew configs)
├── examples/
│   └── (example GTM crew with custom manager)
└── README.md  # This file
```

## Testing Checklist

- [ ] Manager agent has `allow_delegation=True`
- [ ] Worker agents have `allow_delegation=False`
- [ ] Manager has domain expertise in backstory
- [ ] Tasks have clear context dependencies
- [ ] Final synthesis task assigned to manager
- [ ] Process set to `Process.hierarchical`
- [ ] Custom manager or manager_llm specified
- [ ] Understand execution may vary between runs
