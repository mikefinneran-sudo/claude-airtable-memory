# Level 3: Custom Tools Workshop

## Learning Objectives

1. **Master @tool Decorator Pattern**
   - Understand how CrewAI tools wrap Python functions
   - Write clear docstrings that agents can understand
   - Use type hints for better reliability

2. **Build Reusable Tool Library**
   - Create tools for file operations, APIs, data processing
   - Organize tools by category (file system, Airtable, research, etc.)
   - Handle errors gracefully with helpful messages

3. **Enable Agent Autonomy**
   - Give agents capabilities beyond built-in tools
   - Create domain-specific tools for your business
   - Allow agents to perform actions without human intervention

4. **Tool Design Best Practices**
   - Single responsibility principle
   - Clear, descriptive tool names
   - Structured return values (JSON preferred)
   - Comprehensive error handling

## Tool Library (9 Tools Across 4 Categories)

### File System Tools (3)
- **Read File**: Read contents from any file path
- **Write File**: Write content to file, create directories if needed
- **List Files**: List files matching glob pattern with metadata

### Airtable Tools (2)
- **List Records**: Fetch records from Airtable table
- **Create Record**: Create new record with fields

### Research Tools (1)
- **Perplexity Search**: Web search via Perplexity API

### Data Processing Tools (2)
- **Parse JSON**: Validate and format JSON strings
- **Count Words**: Analyze text statistics

### System Tools (1)
- **Execute Shell Command**: Run shell commands with timeout

## @tool Decorator Pattern

### Basic Structure

```python
from crewai_tools import tool

@tool("Tool Display Name")
def my_custom_tool(param1: str, param2: int) -> str:
    """
    Clear description of what this tool does.
    Agents read this docstring to understand the tool.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        Description of what the tool returns

    Example:
        my_custom_tool("value", 123)
    """
    try:
        # Tool implementation here
        result = do_something(param1, param2)
        return result
    except Exception as e:
        return f"Error: {str(e)}"
```

### Key Components

1. **@tool Decorator**: Registers function as CrewAI tool
   ```python
   @tool("Human-readable name shown to agents")
   ```

2. **Type Hints**: Helps with validation and documentation
   ```python
   def tool_name(file_path: str, max_items: int = 10) -> str:
   ```

3. **Docstring**: Agent uses this to understand the tool
   ```python
   """
   First line: Brief description

   Args: Detailed parameter descriptions
   Returns: What the tool outputs
   Example: How to use it
   """
   ```

4. **Error Handling**: Graceful failures
   ```python
   try:
       # Do work
   except SpecificError:
       return "Error: Helpful message"
   ```

5. **Structured Returns**: JSON/dict preferred
   ```python
   return json.dumps({'status': 'success', 'data': result})
   ```

## Using Tools in Crews

### Method 1: Pass to Agent

```python
from crewai import Agent
from tools.tool_library import read_file_tool, write_file_tool

agent = Agent(
    role="Document Processor",
    goal="Process markdown files",
    tools=[read_file_tool, write_file_tool]
)
```

### Method 2: Pass to Task

```python
from crewai import Task

task = Task(
    description="Read research.md and summarize",
    expected_output="1-paragraph summary",
    agent=agent,
    tools=[read_file_tool]  # Task-specific tools
)
```

### Method 3: All Tools from Library

```python
from tools.tool_library import ALL_TOOLS

agent = Agent(
    role="Research Assistant",
    tools=ALL_TOOLS  # Give agent access to all tools
)
```

## Tool Design Best Practices

### 1. Single Responsibility

**❌ Bad** (does too many things):
```python
@tool("Process File")
def process_file(path: str, action: str):
    """Do various file operations"""
    if action == "read":
        # reading code
    elif action == "write":
        # writing code
    elif action == "delete":
        # deleting code
```

**✅ Good** (separate tools):
```python
@tool("Read File")
def read_file(path: str):
    """Read file contents"""

@tool("Write File")
def write_file(path: str, content: str):
    """Write content to file"""
```

### 2. Clear Docstrings

**❌ Bad**:
```python
def search(q):
    """Search for stuff"""
```

**✅ Good**:
```python
@tool("Perplexity Web Search")
def perplexity_search(query: str, api_key: str) -> str:
    """
    Perform web search using Perplexity AI API for current information.

    Args:
        query: Search query (e.g., "latest AI developments 2025")
        api_key: Perplexity API key (get from https://perplexity.ai)

    Returns:
        JSON with search results, citations, and sources

    Example:
        perplexity_search("CrewAI multi-agent systems", "***REMOVED***xxx")
    """
```

### 3. Structured Returns

**❌ Bad** (plain string):
```python
return f"Found 5 files in /path"
```

**✅ Good** (structured JSON):
```python
return json.dumps({
    'directory': '/path',
    'file_count': 5,
    'files': [
        {'name': 'file1.md', 'size_kb': 12.5},
        {'name': 'file2.md', 'size_kb': 8.2}
    ]
})
```

### 4. Error Handling

**❌ Bad** (crashes):
```python
def read_file(path):
    return Path(path).read_text()  # Crashes if file doesn't exist
```

**✅ Good** (graceful failure):
```python
def read_file(path: str) -> str:
    try:
        p = Path(path)
        if not p.exists():
            return f"Error: File not found at {path}"
        return p.read_text()
    except PermissionError:
        return f"Error: Permission denied reading {path}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### 5. Sensible Defaults

```python
@tool("List Files")
def list_files(directory: str, pattern: str = "*", max_files: int = 100) -> str:
    """
    List files with sensible defaults.

    Args:
        directory: Path to search
        pattern: Glob pattern (default: "*" for all files)
        max_files: Maximum results (default: 100)
    """
```

## Common Tool Patterns

### API Wrapper Tool

```python
@tool("Airtable Create Record")
def airtable_create(base_id: str, table: str, token: str, fields: Dict) -> str:
    """Create record in Airtable"""
    try:
        url = f"https://api.airtable.com/v0/{base_id}/{table}"
        # API call logic
        return json.dumps(response_data)
    except Exception as e:
        return f"Airtable Error: {str(e)}"
```

### File Operation Tool

```python
@tool("Write Markdown File")
def write_markdown(file_path: str, content: str) -> str:
    """Write markdown file with frontmatter support"""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return f"✅ Saved: {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### Data Processing Tool

```python
@tool("Extract JSON Field")
def extract_json_field(json_str: str, field_path: str) -> str:
    """
    Extract nested field from JSON using dot notation.

    Example:
        extract_json_field('{"user": {"name": "John"}}', 'user.name')
        Returns: "John"
    """
    try:
        data = json.loads(json_str)
        for key in field_path.split('.'):
            data = data[key]
        return str(data)
    except Exception as e:
        return f"Error: {str(e)}"
```

## Testing Tools

### Test Individual Tool

```python
from tools.tool_library import read_file_tool

# Test with sample file
result = read_file_tool("/tmp/test.md")
print(result)
```

### Test in Agent

```python
from crewai import Agent, Task, Crew
from tools.tool_library import read_file_tool

agent = Agent(
    role="File Reader",
    goal="Read and summarize file",
    tools=[read_file_tool]
)

task = Task(
    description="Read /tmp/test.md and count words",
    expected_output="Word count as integer",
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

## Security Considerations

### 1. Input Validation

```python
@tool("Execute Safe Command")
def safe_command(command: str) -> str:
    """Only allow whitelisted commands"""
    allowed = ['ls', 'pwd', 'whoami']
    cmd = command.split()[0]
    if cmd not in allowed:
        return f"Error: Command '{cmd}' not allowed"
    # Execute
```

### 2. Path Traversal Prevention

```python
@tool("Read File Safely")
def read_safe(file_path: str, allowed_dir: str = "/safe/dir") -> str:
    """Prevent reading files outside allowed directory"""
    path = Path(file_path).resolve()
    allowed = Path(allowed_dir).resolve()

    if not str(path).startswith(str(allowed)):
        return "Error: Access denied"

    return path.read_text()
```

### 3. API Key Management

```python
@tool("Secure API Call")
def api_call_secure(endpoint: str, api_key: str) -> str:
    """Never log or print API keys"""
    # Do NOT print api_key
    headers = {'Authorization': f'Bearer {api_key}'}
    # Make request
    return response  # Don't include api_key in response
```

## When to Create Custom Tools

**✅ Create a custom tool when:**
- Agents need to interact with your specific APIs
- You have domain-specific operations to perform
- Built-in tools don't cover your use case
- You need custom error handling or data processing
- Operation will be reused across multiple crews

**❌ Don't create a tool when:**
- Built-in tools already do what you need
- Operation is one-time use (put in task description instead)
- It's faster to use standard Python in crew script
- Security risks outweigh benefits

## Next Steps

After completing Level 3, you should:
- Have a library of 10+ custom tools
- Understand @tool decorator pattern
- Know how to write agent-friendly docstrings
- Be able to give agents new capabilities

**Ready for Level 4?** → Hierarchical crews with manager agents

## Files Structure

```
level3_custom_tools/
├── tools/
│   └── tool_library.py          # 9 custom tools with @tool decorator
├── examples/
│   └── (add example crew using tools)
└── README.md                     # This file
```

## Testing Checklist

- [ ] All tools have @tool decorator
- [ ] Docstrings follow standard format (description, args, returns, example)
- [ ] Type hints on all parameters and returns
- [ ] Error handling returns helpful messages
- [ ] Returns are structured (JSON preferred)
- [ ] Tool names are clear and descriptive
- [ ] Single responsibility - each tool does one thing
- [ ] Security considerations addressed (if applicable)
