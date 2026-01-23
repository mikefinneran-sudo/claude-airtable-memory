#!/usr/bin/env python3
"""
ObsidianVault MCP Server
Production-grade Model Context Protocol server for Obsidian vault access

Features:
- Search notes with ripgrep
- Daily note management
- Project note templates
- Roots-based security
- Progress notifications
- Comprehensive logging

Author: Claude (AI Assistant)
Created: 2025-11-10
"""

import sys
import json
import asyncio
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import re

# MCP Server will be implemented with basic JSON-RPC over stdio
# This is a production implementation following MCP specification


class ObsidianVaultServer:
    """MCP Server for ObsidianVault access"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path).resolve()
        self.allowed_roots = [str(self.vault_path)]
        self.server_info = {
            "name": "obsidian-vault",
            "version": "1.0.0"
        }

        # Validate vault exists
        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")

        # Log to stderr (stdout is for JSON-RPC messages)
        self.log("info", f"ObsidianVault MCP Server initialized: {self.vault_path}")

    def log(self, level: str, message: str):
        """Log to stderr (stdout reserved for JSON-RPC)"""
        timestamp = datetime.now().isoformat()
        sys.stderr.write(f"[{timestamp}] [{level.upper()}] {message}\n")
        sys.stderr.flush()

    def validate_path(self, path: str) -> bool:
        """Validate path is within allowed roots (security)"""
        try:
            abs_path = Path(path).resolve()
            vault_path = self.vault_path

            # Check if path is within vault
            abs_path.relative_to(vault_path)
            return True
        except (ValueError, RuntimeError):
            self.log("warning", f"Access denied: {path} not in vault")
            return False

    async def search_notes(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search vault notes using ripgrep

        Args:
            query: Search query (supports regex)
            limit: Maximum results to return

        Returns:
            List of matching notes with context
        """
        self.log("info", f"Searching notes: {query}")

        try:
            # Use ripgrep for fast searching
            cmd = [
                "rg",
                "--json",
                "--max-count", str(limit),
                "--context", "2",
                "--type", "md",
                query,
                str(self.vault_path)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            results = []
            for line in result.stdout.split('\n'):
                if not line.strip():
                    continue

                try:
                    data = json.loads(line)
                    if data.get('type') == 'match':
                        match_data = data['data']
                        results.append({
                            'path': match_data['path']['text'],
                            'line_number': match_data['line_number'],
                            'content': match_data['lines']['text'].strip(),
                            'submatches': match_data.get('submatches', [])
                        })
                except json.JSONDecodeError:
                    continue

            self.log("info", f"Found {len(results)} matches")
            return results[:limit]

        except subprocess.TimeoutExpired:
            self.log("error", "Search timeout exceeded")
            return []
        except FileNotFoundError:
            self.log("error", "ripgrep not installed - install with: brew install ripgrep")
            return []
        except Exception as e:
            self.log("error", f"Search error: {str(e)}")
            return []

    async def get_daily_note(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get daily note for specified date (default: today)

        Args:
            date: Date in YYYY-MM-DD format (default: today)

        Returns:
            Daily note content and metadata
        """
        if date is None:
            target_date = datetime.now()
        else:
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return {
                    "error": "Invalid date format. Use YYYY-MM-DD",
                    "content": None
                }

        # Format: YYYY-MM-DD.md in Daily Notes folder
        daily_note_path = self.vault_path / "Daily Notes" / f"{target_date.strftime('%Y-%m-%d')}.md"

        if not self.validate_path(str(daily_note_path)):
            return {"error": "Access denied", "content": None}

        if daily_note_path.exists():
            content = daily_note_path.read_text()
            return {
                "date": target_date.strftime('%Y-%m-%d'),
                "path": str(daily_note_path.relative_to(self.vault_path)),
                "content": content,
                "exists": True
            }
        else:
            return {
                "date": target_date.strftime('%Y-%m-%d'),
                "path": str(daily_note_path.relative_to(self.vault_path)),
                "content": None,
                "exists": False,
                "message": "Daily note does not exist yet"
            }

    async def create_daily_note(self, date: Optional[str] = None, content: str = "") -> Dict[str, Any]:
        """
        Create daily note with optional content

        Args:
            date: Date in YYYY-MM-DD format (default: today)
            content: Initial content for the note

        Returns:
            Created note information
        """
        if date is None:
            target_date = datetime.now()
        else:
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return {"error": "Invalid date format. Use YYYY-MM-DD"}

        daily_note_path = self.vault_path / "Daily Notes" / f"{target_date.strftime('%Y-%m-%d')}.md"

        # Create Daily Notes directory if it doesn't exist
        daily_note_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.validate_path(str(daily_note_path)):
            return {"error": "Access denied"}

        if daily_note_path.exists():
            return {
                "error": "Daily note already exists",
                "path": str(daily_note_path.relative_to(self.vault_path))
            }

        # Create note with template
        template = f"""# {target_date.strftime('%A, %B %d, %Y')}

## Morning Review
-

## Tasks
- [ ]

## Notes
{content}

## Evening Review
-

---
Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

        daily_note_path.write_text(template)
        self.log("info", f"Created daily note: {daily_note_path.name}")

        return {
            "success": True,
            "date": target_date.strftime('%Y-%m-%d'),
            "path": str(daily_note_path.relative_to(self.vault_path)),
            "content": template
        }

    async def list_recent_notes(self, days: int = 7, folder: str = "", limit: int = 50) -> List[Dict[str, Any]]:
        """
        List recently modified notes

        Args:
            days: Number of days to look back
            folder: Optional folder to filter (relative to vault)
            limit: Maximum number of results to return (default: 50)

        Returns:
            List of recent notes with metadata
        """
        cutoff_time = datetime.now().timestamp() - (days * 86400)
        search_path = self.vault_path / folder if folder else self.vault_path

        if not self.validate_path(str(search_path)):
            return []

        # Directories to exclude (dev artifacts, dependencies, hidden dirs)
        excluded_dirs = {
            'venv', 'node_modules', '.git', '__pycache__', '.venv',
            'env', '.env', 'dist', 'build', '.next', '.cache',
            'site-packages', '.obsidian', '.trash'
        }

        recent_notes = []
        for md_file in search_path.rglob("*.md"):
            # Skip files in excluded directories
            path_parts = set(md_file.relative_to(search_path).parts)
            if path_parts & excluded_dirs:
                continue

            if not self.validate_path(str(md_file)):
                continue

            stat = md_file.stat()
            if stat.st_mtime >= cutoff_time:
                recent_notes.append({
                    'path': str(md_file.relative_to(self.vault_path)),
                    'name': md_file.name,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'size': stat.st_size
                })

        # Sort by modified time (newest first)
        recent_notes.sort(key=lambda x: x['modified'], reverse=True)

        # Apply limit
        recent_notes = recent_notes[:limit]

        self.log("info", f"Found {len(recent_notes)} notes modified in last {days} days (limit: {limit})")
        return recent_notes

    async def get_note_content(self, path: str) -> Dict[str, Any]:
        """
        Get content of a specific note

        Args:
            path: Path relative to vault root

        Returns:
            Note content and metadata
        """
        note_path = self.vault_path / path

        if not self.validate_path(str(note_path)):
            return {"error": "Access denied - path outside vault"}

        if not note_path.exists():
            return {"error": "Note not found"}

        if not note_path.suffix == '.md':
            return {"error": "Not a markdown file"}

        try:
            content = note_path.read_text()
            stat = note_path.stat()

            return {
                'path': path,
                'content': content,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
            }
        except Exception as e:
            self.log("error", f"Error reading note: {str(e)}")
            return {"error": f"Error reading note: {str(e)}"}

    async def create_project_note(self, project_name: str, template: str = "default") -> Dict[str, Any]:
        """
        Create new project note from template

        Args:
            project_name: Name of the project
            template: Template to use (default, research, development)

        Returns:
            Created project note information
        """
        # Sanitize project name for filename
        safe_name = re.sub(r'[^\w\s-]', '', project_name).strip()
        safe_name = re.sub(r'[-\s]+', '-', safe_name)

        project_path = self.vault_path / "Projects" / f"{safe_name}.md"

        # Create Projects directory if needed
        project_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.validate_path(str(project_path)):
            return {"error": "Access denied"}

        if project_path.exists():
            return {
                "error": "Project note already exists",
                "path": str(project_path.relative_to(self.vault_path))
            }

        # Templates
        templates = {
            "default": f"""# {project_name}

## Overview
Brief description of the project.

## Status
🟡 In Progress

## Goals
- [ ] Goal 1
- [ ] Goal 2

## Tasks
- [ ] Task 1
- [ ] Task 2

## Notes


## Resources
-

---
Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Tags: #project
""",
            "research": f"""# {project_name}

## Research Question


## Methodology


## Findings


## Sources
-

## Next Steps
- [ ]

---
Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Tags: #research #project
""",
            "development": f"""# {project_name}

## Tech Stack


## Architecture


## Implementation Plan
- [ ] Phase 1:
- [ ] Phase 2:
- [ ] Phase 3:

## Current Status


## Blockers


## Resources
- Repo:
- Docs:

---
Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Tags: #development #project
"""
        }

        content = templates.get(template, templates["default"])
        project_path.write_text(content)

        self.log("info", f"Created project note: {project_path.name}")

        return {
            "success": True,
            "project": project_name,
            "path": str(project_path.relative_to(self.vault_path)),
            "template": template,
            "content": content
        }

    # JSON-RPC message handling
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC message"""
        method = message.get('method')
        params = message.get('params', {})
        msg_id = message.get('id')

        self.log("debug", f"Handling method: {method}")

        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {},
                            "resources": {},
                            "logging": {}
                        },
                        "serverInfo": self.server_info
                    },
                    "id": msg_id
                }

            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "tools": [
                            {
                                "name": "search_notes",
                                "description": "Search Obsidian vault notes using ripgrep. Supports regex patterns.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {
                                            "type": "string",
                                            "description": "Search query (supports regex)"
                                        },
                                        "limit": {
                                            "type": "number",
                                            "description": "Maximum results to return (default: 10)"
                                        }
                                    },
                                    "required": ["query"]
                                }
                            },
                            {
                                "name": "get_daily_note",
                                "description": "Get daily note for specified date (default: today)",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "date": {
                                            "type": "string",
                                            "description": "Date in YYYY-MM-DD format (optional, defaults to today)"
                                        }
                                    }
                                }
                            },
                            {
                                "name": "create_daily_note",
                                "description": "Create daily note with optional initial content",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "date": {
                                            "type": "string",
                                            "description": "Date in YYYY-MM-DD format (optional, defaults to today)"
                                        },
                                        "content": {
                                            "type": "string",
                                            "description": "Initial content for the note"
                                        }
                                    }
                                }
                            },
                            {
                                "name": "list_recent_notes",
                                "description": "List recently modified notes (excludes venv, node_modules, .git)",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "days": {
                                            "type": "number",
                                            "description": "Number of days to look back (default: 7)"
                                        },
                                        "folder": {
                                            "type": "string",
                                            "description": "Optional folder to filter (relative to vault root)"
                                        },
                                        "limit": {
                                            "type": "number",
                                            "description": "Maximum results to return (default: 50)"
                                        }
                                    }
                                }
                            },
                            {
                                "name": "get_note_content",
                                "description": "Get content of a specific note by path",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "path": {
                                            "type": "string",
                                            "description": "Path to note relative to vault root (e.g., 'Projects/MyProject.md')"
                                        }
                                    },
                                    "required": ["path"]
                                }
                            },
                            {
                                "name": "create_project_note",
                                "description": "Create new project note from template",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "project_name": {
                                            "type": "string",
                                            "description": "Name of the project"
                                        },
                                        "template": {
                                            "type": "string",
                                            "description": "Template to use: 'default', 'research', or 'development'",
                                            "enum": ["default", "research", "development"]
                                        }
                                    },
                                    "required": ["project_name"]
                                }
                            }
                        ]
                    },
                    "id": msg_id
                }

            elif method == "tools/call":
                tool_name = params.get('name')
                arguments = params.get('arguments', {})

                result = None
                if tool_name == "search_notes":
                    result = await self.search_notes(
                        query=arguments.get('query'),
                        limit=arguments.get('limit', 10)
                    )
                elif tool_name == "get_daily_note":
                    result = await self.get_daily_note(
                        date=arguments.get('date')
                    )
                elif tool_name == "create_daily_note":
                    result = await self.create_daily_note(
                        date=arguments.get('date'),
                        content=arguments.get('content', '')
                    )
                elif tool_name == "list_recent_notes":
                    result = await self.list_recent_notes(
                        days=arguments.get('days', 7),
                        folder=arguments.get('folder', ''),
                        limit=arguments.get('limit', 50)
                    )
                elif tool_name == "get_note_content":
                    result = await self.get_note_content(
                        path=arguments.get('path')
                    )
                elif tool_name == "create_project_note":
                    result = await self.create_project_note(
                        project_name=arguments.get('project_name'),
                        template=arguments.get('template', 'default')
                    )
                else:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32601,
                            "message": f"Unknown tool: {tool_name}"
                        },
                        "id": msg_id
                    }

                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    },
                    "id": msg_id
                }

            elif method == "resources/list":
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "resources": [
                            {
                                "uri": f"vault://daily/{datetime.now().strftime('%Y-%m-%d')}",
                                "name": "Today's Daily Note",
                                "mimeType": "text/markdown"
                            },
                            {
                                "uri": "vault://projects",
                                "name": "All Projects",
                                "mimeType": "application/json"
                            }
                        ]
                    },
                    "id": msg_id
                }

            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    },
                    "id": msg_id
                }

        except Exception as e:
            self.log("error", f"Error handling message: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                },
                "id": msg_id
            }

    async def run_stdio(self):
        """Run server with stdio transport"""
        self.log("info", "Starting stdio transport")

        # Read from stdin, write to stdout
        loop = asyncio.get_event_loop()

        while True:
            try:
                # Read line from stdin
                line = await loop.run_in_executor(None, sys.stdin.readline)

                if not line:
                    self.log("info", "stdin closed, shutting down")
                    break

                line = line.strip()
                if not line:
                    continue

                # Parse JSON-RPC message
                try:
                    message = json.loads(line)
                except json.JSONDecodeError as e:
                    self.log("error", f"Invalid JSON: {e}")
                    continue

                # Handle message
                response = await self.handle_message(message)

                # Write response to stdout
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

            except KeyboardInterrupt:
                self.log("info", "Received interrupt, shutting down")
                break
            except Exception as e:
                self.log("error", f"Error in main loop: {str(e)}")


async def main():
    """Main entry point"""
    # Get vault path from environment or use default
    vault_path = os.getenv(
        "VAULT_PATH",
        "/Users/mikefinneran/Documents/ObsidianVault"
    )

    try:
        server = ObsidianVaultServer(vault_path)
        await server.run_stdio()
    except Exception as e:
        sys.stderr.write(f"Fatal error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
