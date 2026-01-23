#!/usr/bin/env python3
"""
LifeHub → Notion Sync Script
Syncs Obsidian notes to Notion databases

Usage:
    python3 sync_to_notion.py
    python3 sync_to_notion.py --folder Projects
    python3 sync_to_notion.py --dry-run

Requirements:
    pip3 install notion-client python-frontmatter
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

try:
    from notion_client import Client
    import frontmatter
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print("  pip3 install notion-client python-frontmatter")
    sys.exit(1)

# Configuration
VAULT_PATH = Path("/Users/mikefinneran/Documents/ObsidianVault")
TOKEN_FILE = Path.home() / ".lifehub-notion-token"
CONFIG_FILE = VAULT_PATH / ".scripts" / "notion-sync-config.json"
LOG_FILE = VAULT_PATH / ".scripts" / "notion-sync.log"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NotionSync:
    """Sync Obsidian notes to Notion databases"""

    def __init__(self, token: str, config: Dict[str, Any], dry_run: bool = False):
        """
        Initialize Notion client

        Args:
            token: Notion integration token
            config: Sync configuration
            dry_run: If True, don't actually sync (just log)
        """
        self.client = Client(auth=token) if not dry_run else None
        self.config = config
        self.dry_run = dry_run
        self.stats = {
            'processed': 0,
            'synced': 0,
            'skipped': 0,
            'errors': 0
        }

    def sync_all(self, folder_filter: Optional[str] = None):
        """
        Sync all configured folders to Notion

        Args:
            folder_filter: If provided, only sync this folder
        """
        logger.info("=" * 60)
        logger.info(f"Starting LifeHub → Notion sync {'(DRY RUN)' if self.dry_run else ''}")
        logger.info("=" * 60)

        for mapping in self.config.get('mappings', []):
            folder = mapping['obsidian_folder']

            # Skip if folder filter specified and doesn't match
            if folder_filter and folder != folder_filter:
                continue

            logger.info(f"\nSyncing folder: {folder}")
            self.sync_folder(mapping)

        self.print_stats()

    def sync_folder(self, mapping: Dict[str, Any]):
        """
        Sync a single folder to its Notion database

        Args:
            mapping: Folder-to-database mapping configuration
        """
        folder_path = VAULT_PATH / mapping['obsidian_folder']
        database_id = mapping['notion_database_id']

        if not folder_path.exists():
            logger.warning(f"Folder not found: {folder_path}")
            return

        # Get all markdown files
        md_files = list(folder_path.glob("*.md"))
        logger.info(f"Found {len(md_files)} files")

        for md_file in md_files:
            self.stats['processed'] += 1

            try:
                self.sync_file(md_file, database_id, mapping)
            except Exception as e:
                self.stats['errors'] += 1
                logger.error(f"Error syncing {md_file.name}: {e}")

    def sync_file(self, file_path: Path, database_id: str, mapping: Dict[str, Any]):
        """
        Sync a single file to Notion

        Args:
            file_path: Path to markdown file
            database_id: Notion database ID
            mapping: Configuration for this sync
        """
        # Parse frontmatter and content
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        # Check if should sync
        if not self.should_sync(post, mapping):
            self.stats['skipped'] += 1
            logger.debug(f"Skipped: {file_path.name}")
            return

        # Build Notion properties
        properties = self.build_properties(post, file_path, mapping)

        # Build content blocks
        content = self.build_content(post.content)

        if self.dry_run:
            logger.info(f"[DRY RUN] Would sync: {file_path.name}")
            logger.debug(f"Properties: {json.dumps(properties, indent=2)}")
            self.stats['synced'] += 1
            return

        # Check if page exists
        existing_page = self.find_existing_page(database_id, file_path.stem)

        if existing_page:
            # Update existing page
            self.client.pages.update(
                page_id=existing_page['id'],
                properties=properties
            )
            logger.info(f"Updated: {file_path.name}")
        else:
            # Create new page
            self.client.pages.create(
                parent={"database_id": database_id},
                properties=properties,
                children=content
            )
            logger.info(f"Created: {file_path.name}")

        self.stats['synced'] += 1

    def should_sync(self, post: frontmatter.Post, mapping: Dict[str, Any]) -> bool:
        """
        Determine if file should be synced

        Args:
            post: Parsed frontmatter post
            mapping: Sync configuration

        Returns:
            True if should sync, False otherwise
        """
        metadata = post.metadata

        # Check for explicit sync flag
        if 'sync-to-notion' in metadata:
            return metadata['sync-to-notion'] is True

        # Check for private flag
        if metadata.get('private', False):
            return False

        # Check type filter if specified
        if 'type_filter' in mapping:
            if metadata.get('type') != mapping['type_filter']:
                return False

        # Default: sync
        return True

    def build_properties(self, post: frontmatter.Post, file_path: Path, mapping: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build Notion properties from Obsidian frontmatter

        Args:
            post: Parsed frontmatter post
            file_path: Path to source file
            mapping: Property mappings

        Returns:
            Notion properties dict
        """
        metadata = post.metadata
        prop_map = mapping.get('property_mapping', {})

        properties = {}

        # Title (required) - use filename if no title property
        title_text = metadata.get('title', file_path.stem)
        properties['Name'] = {
            "title": [{"text": {"content": title_text}}]
        }

        # Map other properties
        for obs_prop, notion_prop in prop_map.items():
            if obs_prop not in metadata:
                continue

            value = metadata[obs_prop]
            notion_value = self.convert_property(value, notion_prop)

            if notion_value:
                properties[notion_prop] = notion_value

        return properties

    def convert_property(self, value: Any, prop_name: str) -> Optional[Dict[str, Any]]:
        """
        Convert Obsidian property to Notion property format

        Args:
            value: Property value
            prop_name: Notion property name

        Returns:
            Notion-formatted property or None
        """
        if value is None:
            return None

        # String/text
        if isinstance(value, str):
            # Date format (YYYY-MM-DD)
            if self.is_date(value):
                return {"date": {"start": value}}
            # Select/Status
            else:
                return {"select": {"name": value}}

        # Number
        elif isinstance(value, (int, float)):
            return {"number": value}

        # Boolean
        elif isinstance(value, bool):
            return {"checkbox": value}

        # List (multi-select)
        elif isinstance(value, list):
            return {
                "multi_select": [{"name": str(item)} for item in value]
            }

        return None

    def is_date(self, value: str) -> bool:
        """Check if string is a date in YYYY-MM-DD format"""
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def build_content(self, markdown: str) -> List[Dict[str, Any]]:
        """
        Convert markdown content to Notion blocks

        Args:
            markdown: Markdown content

        Returns:
            List of Notion blocks
        """
        # Simple implementation - convert to paragraph blocks
        # For advanced formatting, use a markdown→Notion parser

        blocks = []
        paragraphs = markdown.split('\n\n')

        for para in paragraphs[:10]:  # Limit to first 10 paragraphs
            if para.strip():
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": para.strip()[:2000]}  # Notion limit
                        }]
                    }
                })

        return blocks

    def find_existing_page(self, database_id: str, title: str) -> Optional[Dict[str, Any]]:
        """
        Find existing Notion page by title

        Args:
            database_id: Notion database ID
            title: Page title to search

        Returns:
            Page object if found, None otherwise
        """
        try:
            response = self.client.databases.query(
                database_id=database_id,
                filter={
                    "property": "Name",
                    "title": {
                        "equals": title
                    }
                }
            )

            if response['results']:
                return response['results'][0]

        except Exception as e:
            logger.debug(f"Error finding page: {e}")

        return None

    def print_stats(self):
        """Print sync statistics"""
        logger.info("\n" + "=" * 60)
        logger.info("Sync Complete!")
        logger.info("=" * 60)
        logger.info(f"Files processed: {self.stats['processed']}")
        logger.info(f"Files synced: {self.stats['synced']}")
        logger.info(f"Files skipped: {self.stats['skipped']}")
        logger.info(f"Errors: {self.stats['errors']}")
        logger.info("=" * 60)


def load_token() -> str:
    """Load Notion token from file"""
    if not TOKEN_FILE.exists():
        logger.error(f"Token file not found: {TOKEN_FILE}")
        logger.error("Create it with: echo 'your_token' > ~/.lifehub-notion-token")
        sys.exit(1)

    with open(TOKEN_FILE, 'r') as f:
        return f.read().strip()


def load_config() -> Dict[str, Any]:
    """Load sync configuration"""
    if not CONFIG_FILE.exists():
        logger.warning(f"Config file not found: {CONFIG_FILE}")
        logger.info("Creating default config...")

        default_config = {
            "mappings": [
                {
                    "obsidian_folder": "Projects",
                    "notion_database_id": "REPLACE_WITH_YOUR_DATABASE_ID",
                    "type_filter": "project",
                    "property_mapping": {
                        "status": "Status",
                        "priority": "Priority",
                        "deadline": "Deadline",
                        "client": "Client",
                        "progress": "Progress",
                        "start-date": "Start Date",
                        "owner": "Owner",
                        "category": "Category",
                        "revenue-potential": "Revenue Potential"
                    }
                },
                {
                    "obsidian_folder": "Clients",
                    "notion_database_id": "REPLACE_WITH_YOUR_DATABASE_ID",
                    "type_filter": "client",
                    "property_mapping": {
                        "status": "Status",
                        "industry": "Industry",
                        "company-size": "Company Size",
                        "lifetime-value": "Lifetime Value",
                        "monthly-value": "Monthly Value",
                        "conversion-probability": "Conversion Probability",
                        "first-contact": "First Contact",
                        "last-contact": "Last Contact"
                    }
                },
                {
                    "obsidian_folder": "Daily",
                    "notion_database_id": "REPLACE_WITH_YOUR_DATABASE_ID",
                    "type_filter": "daily-note",
                    "property_mapping": {
                        "date": "Date",
                        "day-of-week": "Day of Week",
                        "week": "Week",
                        "energy-level": "Energy Level",
                        "mood": "Mood"
                    }
                }
            ]
        }

        # Create .scripts directory if needed
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=2)

        logger.info(f"Created config file: {CONFIG_FILE}")
        logger.info("Edit this file to add your Notion database IDs")
        sys.exit(0)

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Sync Obsidian to Notion')
    parser.add_argument('--folder', help='Only sync this folder')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be synced without syncing')
    args = parser.parse_args()

    # Load configuration
    token = load_token()
    config = load_config()

    # Validate config
    for mapping in config['mappings']:
        if 'REPLACE' in mapping['notion_database_id']:
            logger.error(f"Config not set up! Edit {CONFIG_FILE}")
            logger.error("Replace REPLACE_WITH_YOUR_DATABASE_ID with actual database IDs")
            sys.exit(1)

    # Create syncer and run
    syncer = NotionSync(token, config, dry_run=args.dry_run)
    syncer.sync_all(folder_filter=args.folder)


if __name__ == "__main__":
    main()
