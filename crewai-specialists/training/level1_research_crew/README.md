# Level 1: YAML-Based Crew Configuration

## Learning Objectives

1. **Master YAML Configuration Pattern**
   - Separate agent definitions (`agents.yaml`) from task definitions (`tasks.yaml`)
   - Load configs dynamically in `crew.py`
   - Understand the benefits of declarative vs imperative configuration

2. **Apply the 80/20 Rule**
   - 80% effort on task `description` and `expected_output`
   - 20% effort on agent `role`, `goal`, and `backstory`
   - Observe how detailed task descriptions drive quality output

3. **Sequential Process Flow**
   - Understand linear pipeline: Task 1 → Task 2 → Task 3
   - Use `context` to pass outputs between tasks
   - When to use sequential vs hierarchical process

4. **Input Interpolation**
   - Use `{placeholder}` syntax in YAML
   - Pass inputs when calling `crew.kickoff(inputs={...})`
   - Make crews reusable with dynamic parameters

## Files Structure

```
level1_research_crew/
├── config/
│   ├── agents.yaml          # 3 agent definitions
│   └── tasks.yaml           # 3 task definitions
├── tools/                   # (empty - for Level 2)
├── outputs/                 # Generated NotebookLM documents
├── crew.py                  # Main crew runner
└── README.md               # This file
```

## Agents Defined

### 1. research_collector
- **Role**: Research File Collector
- **Goal**: Discover and catalog research files
- **Key Skill**: Metadata extraction from multiple source types

### 2. content_categorizer
- **Role**: Content Categorization Specialist
- **Goal**: Analyze and group content by topic
- **Key Skill**: Keyword matching + semantic analysis

### 3. document_formatter
- **Role**: NotebookLM Document Formatter
- **Goal**: Create publication-ready markdown
- **Key Skill**: YAML frontmatter + structured document generation

## Tasks Pipeline

### Task 1: collect_research_files
- **Input**: `{source_location}`, `{topic_filter}`
- **Output**: JSON array of file metadata
- **Agent**: research_collector
- **80/20 Focus**: Detailed extraction requirements, exact JSON schema

### Task 2: categorize_content
- **Input**: Output from Task 1
- **Output**: Same JSON with added `topic` field
- **Agent**: content_categorizer
- **Context**: `collect_research_files`
- **80/20 Focus**: Precise categorization algorithm, 9 predefined topics

### Task 3: create_notebooklm_documents
- **Input**: Output from Task 2, `{output_dir}`
- **Output**: List of markdown file paths
- **Agent**: document_formatter
- **Context**: `collect_research_files`, `categorize_content`
- **80/20 Focus**: Exact markdown structure, YAML frontmatter spec, quality standards

## Running the Crew

```bash
cd ~/crewai-specialists/training/level1_research_crew
python3 crew.py
```

**Expected behavior**:
1. Scans ~/Downloads for CrewAI-related markdown files
2. Categorizes each file by topic
3. Creates NotebookLM documents in outputs/
4. Prints detailed progress and learning takeaways

## Key Learnings

### 1. YAML Benefits
- **Reusability**: Same agents/tasks can be used in multiple crews
- **Maintainability**: Changes to agent personas don't require code edits
- **Clarity**: Declarative configs are easier to read than Python code
- **Version Control**: YAML diffs show exactly what changed

### 2. 80/20 Rule in Practice
Compare these two approaches:

**❌ Bad (50/50 split)**:
```yaml
agent:
  role: "Senior Research Analyst with 15 years of experience..."
  goal: "Find files"
task:
  description: "Find research files"
```

**✅ Good (80/20 split)**:
```yaml
agent:
  role: "Research File Collector"
  goal: "Discover and catalog research files"
task:
  description: >
    Scan {source_location} for all markdown files containing {topic_filter}.
    Extract: file path, filename, size, modified timestamp, 500-char preview.
    Return structured JSON with exact schema: {...}
```

### 3. Sequential vs Hierarchical
**Sequential** (used here):
- Fixed linear pipeline
- Predictable order
- Best for: ETL workflows, document processing, reporting

**Hierarchical** (Level 4):
- Dynamic task delegation
- Manager agent decides order
- Best for: Complex workflows, adaptive planning, multi-phase projects

### 4. Context Passing
Tasks can access outputs from previous tasks:
```yaml
task2:
  context:
    - task1  # Gets output from task1 automatically
```

This creates a dependency chain and enables data flow through the pipeline.

## Comparison to Original Script

### Original (`auto_organize_research.py`)
- ✅ Works quickly (~2 seconds)
- ✅ Simple Python script
- ❌ Not reusable for other workflows
- ❌ Hardcoded logic
- ❌ No agent collaboration

### Level 1 Crew (`crew.py`)
- ✅ Reusable agents/tasks via YAML
- ✅ Agent collaboration and context passing
- ✅ Easy to modify behavior without code changes
- ✅ Demonstrates CrewAI best practices
- ⚠️ Slower (LLM calls for each agent)
- ⚠️ More complex setup

**When to use each**:
- **Script**: Production automation where speed matters
- **Crew**: When you need flexibility, agent reasoning, or complex workflows

## Next Steps

After completing Level 1, you should understand:
- How to structure agents.yaml and tasks.yaml
- Why the 80/20 rule improves output quality
- How sequential process creates linear pipelines
- How to use input interpolation for dynamic crews

**Ready for Level 2?** → Custom tools with `@tool` decorator

## Testing Checklist

- [ ] `crew.py` runs without errors
- [ ] Agents loaded from `agents.yaml`
- [ ] Tasks loaded from `tasks.yaml`
- [ ] Sequential process executes in order
- [ ] Input placeholders get interpolated
- [ ] Output files created in `outputs/`
- [ ] NotebookLM documents are valid markdown
- [ ] Understand why 80/20 rule matters

## Common Issues

**Issue**: `ModuleNotFoundError: No module named 'crewai'`
**Fix**: Run from DGX or install CrewAI: `pip install crewai`

**Issue**: `KeyError: 'agent_name'`
**Fix**: Check that agent name in tasks.yaml matches agents.yaml exactly

**Issue**: Tasks run out of order
**Fix**: Check `context` dependencies - tasks wait for context tasks to complete

**Issue**: Placeholders not replaced
**Fix**: Ensure inputs dict keys match {placeholder} names exactly
