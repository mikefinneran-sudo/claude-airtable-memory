"""
Elite Research Organization Crew - Custom Tools
Integrated from Level 3 Training: Custom Tools Workshop

Tools provided:
- File System: list_files_tool, read_file_tool, write_file_tool
- Airtable: airtable_list_records
- Data Processing: parse_json_tool, count_words_tool
"""

from crewai_tools import tool
from pathlib import Path
import json
import urllib.request
import urllib.parse
from typing import Dict, Any
from datetime import datetime

# ==============================================================================
# FILE SYSTEM TOOLS
# ==============================================================================

@tool("List Files")
def list_files_tool(directory: str, pattern: str = "*") -> str:
    """
    List files in a directory matching a glob pattern.

    Args:
        directory: Directory path to search
        pattern: Glob pattern to match (e.g., "*.md", "**/*.py")

    Returns:
        JSON list of file paths with metadata

    Example:
        list_files_tool("/path/to/dir", "*.md")
    """
    try:
        dir_path = Path(directory).expanduser()
        if not dir_path.exists():
            return f"Error: Directory not found at {directory}"

        if not dir_path.is_dir():
            return f"Error: {directory} is not a directory"

        files = []
        for file_path in dir_path.glob(pattern):
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    'path': str(file_path),
                    'name': file_path.name,
                    'size_kb': round(stat.st_size / 1024, 2),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })

        files.sort(key=lambda x: x['modified'], reverse=True)

        return json.dumps({
            'directory': directory,
            'pattern': pattern,
            'file_count': len(files),
            'files': files
        }, indent=2)

    except Exception as e:
        return f"Error listing files: {str(e)}"


@tool("Read File")
def read_file_tool(file_path: str) -> str:
    """
    Read the contents of a file from the file system.

    Args:
        file_path: Absolute or relative path to the file

    Returns:
        File contents as string, or error message

    Example:
        read_file_tool("/path/to/document.md")
    """
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"Error: File not found at {file_path}"

        if not path.is_file():
            return f"Error: {file_path} is a directory, not a file"

        content = path.read_text(encoding='utf-8')
        return content

    except PermissionError:
        return f"Error: Permission denied reading {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool("Write File")
def write_file_tool(file_path: str, content: str) -> str:
    """
    Write content to a file, creating directories if needed.

    Args:
        file_path: Path where file should be written
        content: Text content to write to the file

    Returns:
        Success message with file path, or error message

    Example:
        write_file_tool("/path/to/output.md", "# Document\\n\\nContent here")
    """
    try:
        path = Path(file_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(content, encoding='utf-8')
        size_kb = path.stat().st_size / 1024

        return f"✅ File written successfully: {file_path} ({size_kb:.1f}KB)"

    except PermissionError:
        return f"Error: Permission denied writing to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


# ==============================================================================
# AIRTABLE TOOLS
# ==============================================================================

@tool("Airtable - List Records")
def airtable_list_records(base_id: str, table_id: str, api_token: str, max_records: int = 100) -> str:
    """
    List records from an Airtable table.

    Args:
        base_id: Airtable base ID (starts with 'app')
        table_id: Table ID or name
        api_token: Airtable Personal Access Token
        max_records: Maximum records to return (default 100)

    Returns:
        JSON array of records with fields and metadata

    Example:
        airtable_list_records("appXXX", "Tasks", "patXXX...", 10)
    """
    try:
        url = f"https://api.airtable.com/v0/{base_id}/{urllib.parse.quote(table_id)}"
        url += f"?maxRecords={max_records}"

        req = urllib.request.Request(url)
        req.add_header('Authorization', f'Bearer {api_token}')

        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            return json.dumps(data, indent=2)

    except urllib.error.HTTPError as e:
        return f"Airtable API Error: {e.code} - {e.reason}"
    except Exception as e:
        return f"Error accessing Airtable: {str(e)}"


# ==============================================================================
# DATA PROCESSING TOOLS
# ==============================================================================

@tool("Parse JSON")
def parse_json_tool(json_string: str) -> str:
    """
    Parse and validate JSON string, returning formatted output.

    Args:
        json_string: JSON string to parse

    Returns:
        Pretty-printed JSON or error message with details

    Example:
        parse_json_tool('{"name": "test", "value": 123}')
    """
    try:
        data = json.loads(json_string)
        return json.dumps(data, indent=2, sort_keys=True)
    except json.JSONDecodeError as e:
        return f"JSON Parse Error: {e.msg} at line {e.lineno}, column {e.colno}"
    except Exception as e:
        return f"Error parsing JSON: {str(e)}"


@tool("Count Words")
def count_words_tool(text: str) -> str:
    """
    Count words, characters, lines, and paragraphs in text.

    Args:
        text: Text content to analyze

    Returns:
        JSON with word count, character count, lines, paragraphs

    Example:
        count_words_tool("Sample text\\n\\nWith paragraphs")
    """
    lines = text.split('\n')
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    words = text.split()

    stats = {
        'characters': len(text),
        'characters_no_spaces': len(text.replace(' ', '')),
        'words': len(words),
        'lines': len(lines),
        'paragraphs': len(paragraphs),
        'avg_word_length': round(sum(len(w) for w in words) / len(words), 1) if words else 0
    }

    return json.dumps(stats, indent=2)


# Tool catalog for reference
ALL_TOOLS = [
    list_files_tool,
    read_file_tool,
    write_file_tool,
    airtable_list_records,
    parse_json_tool,
    count_words_tool
]
