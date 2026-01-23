#!/usr/bin/env python3
"""
Credential Rotation MCP Server
Provides Claude Code with credential rotation management capabilities
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime

# MCP imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
)

# Add local modules to path
sys.path.append(str(Path(__file__).parent))
from rotation_framework import (
    RotationScheduler,
    RotationAudit,
    OnePasswordManager,
    setup_logging
)


class CredentialRotationMCP:
    def __init__(self):
        self.app = Server("credential-rotation")
        self.base_dir = Path(__file__).parent
        self.logs_dir = self.base_dir / "logs"
        self.config_dir = self.base_dir / "config"

        # Setup logging
        setup_logging(self.logs_dir)

        # Initialize components
        self.audit = RotationAudit(self.logs_dir / "audit.jsonl")
        self.scheduler = RotationScheduler(
            self.config_dir / "rotation_config.json",
            self.logs_dir / "audit.jsonl"
        )
        self.op = OnePasswordManager()

        self.setup_handlers()

    def setup_handlers(self):
        """Register MCP tool handlers"""

        @self.app.list_tools()
        async def list_tools() -> List[Tool]:
            """List available credential rotation tools"""
            return [
                Tool(
                    name="check_rotation_status",
                    description=(
                        "Check rotation status for all credentials. "
                        "Shows last rotation date, days since rotation, and whether rotation is needed."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="rotate_credential",
                    description=(
                        "Rotate a specific credential. Supports: Cloudflare (automated), "
                        "Airtable, Perplexity, Gamma, Google OAuth (manual with guidance)."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "service": {
                                "type": "string",
                                "enum": ["Cloudflare", "Airtable", "Perplexity", "Gamma", "Google OAuth"],
                                "description": "Service to rotate credentials for"
                            },
                            "force": {
                                "type": "boolean",
                                "description": "Force rotation even if not due",
                                "default": False
                            }
                        },
                        "required": ["service"]
                    }
                ),
                Tool(
                    name="get_rotation_history",
                    description=(
                        "Get rotation history for a specific service or all services. "
                        "Shows audit log of all rotation attempts."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "service": {
                                "type": "string",
                                "description": "Service name (optional - omit for all services)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of records to return",
                                "default": 10
                            }
                        }
                    }
                ),
                Tool(
                    name="get_manual_rotation_guide",
                    description=(
                        "Get step-by-step manual rotation instructions for services "
                        "that don't support automated rotation (Perplexity, Gamma, Google OAuth, TMDB)."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "service": {
                                "type": "string",
                                "enum": ["Perplexity Pro", "Gamma API", "Google OAuth", "TMDB API"],
                                "description": "Service to get rotation guide for"
                            }
                        },
                        "required": ["service"]
                    }
                ),
                Tool(
                    name="test_credential",
                    description=(
                        "Test if a credential in 1Password is working correctly. "
                        "Makes a test API call to verify the credential."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "service": {
                                "type": "string",
                                "description": "Service to test"
                            }
                        },
                        "required": ["service"]
                    }
                ),
                Tool(
                    name="schedule_rotation",
                    description=(
                        "Configure automatic rotation schedule for a service. "
                        "Sets rotation frequency and enables/disables automated rotation."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "service": {
                                "type": "string",
                                "description": "Service name"
                            },
                            "rotation_days": {
                                "type": "integer",
                                "description": "Days between rotations (e.g., 90)",
                                "minimum": 1
                            },
                            "enabled": {
                                "type": "boolean",
                                "description": "Enable automated rotation",
                                "default": True
                            }
                        },
                        "required": ["service", "rotation_days"]
                    }
                )
            ]

        @self.app.call_tool()
        async def call_tool(name: str, arguments: Any) -> List[TextContent]:
            """Handle tool calls"""

            if name == "check_rotation_status":
                return await self.check_rotation_status()

            elif name == "rotate_credential":
                return await self.rotate_credential(
                    arguments["service"],
                    arguments.get("force", False)
                )

            elif name == "get_rotation_history":
                return await self.get_rotation_history(
                    arguments.get("service"),
                    arguments.get("limit", 10)
                )

            elif name == "get_manual_rotation_guide":
                return await self.get_manual_rotation_guide(arguments["service"])

            elif name == "test_credential":
                return await self.test_credential(arguments["service"])

            elif name == "schedule_rotation":
                return await self.schedule_rotation(
                    arguments["service"],
                    arguments["rotation_days"],
                    arguments.get("enabled", True)
                )

            else:
                raise ValueError(f"Unknown tool: {name}")

    async def check_rotation_status(self) -> List[TextContent]:
        """Check rotation status for all credentials"""
        try:
            # Get list of all credentials in 1Password
            credentials = [
                {"name": "Perplexity Pro", "op_item": "Perplexity Pro API", "policy_days": 90},
                {"name": "Gamma API", "op_item": "Gamma API", "policy_days": 90},
                {"name": "Airtable", "op_item": "Airtable WalterSignal", "policy_days": 90},
                {"name": "Google OAuth - MCP", "op_item": "Google OAuth - Gmail MCP Server", "policy_days": 180},
                {"name": "Google OAuth - Parser", "op_item": "Google OAuth - Gmail Amazon Parser", "policy_days": 180},
                {"name": "Cloudflare", "op_item": "Cloudflare Wrangler OAuth", "policy_days": 90},
                {"name": "TMDB API", "op_item": "TMDB API - Alfred Workflow", "policy_days": 180},
            ]

            status_report = "# Credential Rotation Status\n\n"
            status_report += f"**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

            for cred in credentials:
                last_rotation = self.audit.get_last_rotation(cred["name"])
                needs_rotation = self.audit.needs_rotation(cred["name"], cred["policy_days"])

                status_report += f"## {cred['name']}\n"
                status_report += f"- **1Password Item**: `{cred['op_item']}`\n"
                status_report += f"- **Rotation Policy**: Every {cred['policy_days']} days\n"

                if last_rotation:
                    days_since = (datetime.now() - last_rotation).days
                    status_report += f"- **Last Rotation**: {last_rotation.strftime('%Y-%m-%d')} ({days_since} days ago)\n"
                    status_report += f"- **Next Rotation Due**: {cred['policy_days'] - days_since} days\n"
                else:
                    status_report += f"- **Last Rotation**: Never\n"

                status_report += f"- **Status**: {'⚠️ Needs Rotation' if needs_rotation else '✅ Up to date'}\n\n"

            return [TextContent(type="text", text=status_report)]

        except Exception as e:
            return [TextContent(type="text", text=f"Error checking rotation status: {str(e)}")]

    async def rotate_credential(self, service: str, force: bool = False) -> List[TextContent]:
        """Rotate a specific credential"""
        try:
            if service == "Cloudflare":
                from modules.cloudflare_rotator import CloudflareRotator
                rotator = CloudflareRotator()
                success = rotator.rotate(self.audit)

                if success:
                    return [TextContent(
                        type="text",
                        text=f"✅ Successfully rotated Cloudflare credentials!\n\nThe new token has been stored in 1Password."
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"❌ Failed to rotate Cloudflare credentials. Check logs for details."
                    )]

            else:
                # Services that require manual rotation
                guide = await self.get_manual_rotation_guide(service)
                return [TextContent(
                    type="text",
                    text=f"{service} requires manual rotation.\n\n{guide[0].text}"
                )]

        except Exception as e:
            return [TextContent(type="text", text=f"Error rotating credential: {str(e)}")]

    async def get_rotation_history(self, service: str = None, limit: int = 10) -> List[TextContent]:
        """Get rotation history"""
        try:
            if not self.audit.audit_file.exists():
                return [TextContent(type="text", text="No rotation history found.")]

            history = []
            with open(self.audit.audit_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if service is None or entry['service'] == service:
                            history.append(entry)
                    except:
                        continue

            # Get most recent entries
            history = history[-limit:]

            report = "# Rotation History\n\n"
            if service:
                report += f"**Service**: {service}\n\n"

            for entry in reversed(history):
                status_emoji = "✅" if entry['status'] == 'success' else "❌"
                report += f"## {status_emoji} {entry['service']}\n"
                report += f"- **Timestamp**: {entry['timestamp']}\n"
                report += f"- **Status**: {entry['status']}\n"
                if entry.get('details'):
                    report += f"- **Details**: {entry['details']}\n"
                report += "\n"

            return [TextContent(type="text", text=report)]

        except Exception as e:
            return [TextContent(type="text", text=f"Error getting history: {str(e)}")]

    async def get_manual_rotation_guide(self, service: str) -> List[TextContent]:
        """Get manual rotation guide"""
        try:
            from modules.manual_rotation_guide import generate_rotation_checklist
            checklist = generate_rotation_checklist(service)
            return [TextContent(type="text", text=checklist)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting guide: {str(e)}")]

    async def test_credential(self, service: str) -> List[TextContent]:
        """Test if a credential works"""
        try:
            result = "Testing credential functionality...\n\n"

            if service == "Cloudflare":
                from modules.cloudflare_rotator import CloudflareRotator
                rotator = CloudflareRotator()
                token = self.op.read('op://API_Keys/Cloudflare Wrangler OAuth/oauth_token')
                if rotator.test_credential(token):
                    result += "✅ Cloudflare token is working!"
                else:
                    result += "❌ Cloudflare token test failed"

            elif service == "Airtable":
                from modules.airtable_rotator import AirtableRotator
                rotator = AirtableRotator()
                token = self.op.read('op://API_Keys/Airtable WalterSignal/api_key')
                if rotator.test_credential(token):
                    result += "✅ Airtable token is working!"
                else:
                    result += "❌ Airtable token test failed"

            else:
                result += f"⚠️  Automated testing not available for {service}"

            return [TextContent(type="text", text=result)]

        except Exception as e:
            return [TextContent(type="text", text=f"Error testing credential: {str(e)}")]

    async def schedule_rotation(self, service: str, rotation_days: int, enabled: bool) -> List[TextContent]:
        """Schedule automatic rotation"""
        try:
            config_file = self.config_dir / "rotation_config.json"
            config_file.parent.mkdir(exist_ok=True)

            # Load or create config
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
            else:
                config = {"services": {}}

            # Update config
            config["services"][service] = {
                "rotation_days": rotation_days,
                "enabled": enabled,
                "last_updated": datetime.now().isoformat()
            }

            # Save config
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)

            status = "enabled" if enabled else "disabled"
            return [TextContent(
                type="text",
                text=f"✅ Rotation schedule updated for {service}:\n- Frequency: Every {rotation_days} days\n- Status: {status}"
            )]

        except Exception as e:
            return [TextContent(type="text", text=f"Error scheduling rotation: {str(e)}")]

    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(
                read_stream,
                write_stream,
                self.app.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = CredentialRotationMCP()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
