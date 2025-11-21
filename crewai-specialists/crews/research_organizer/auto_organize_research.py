#!/usr/bin/env python3
"""
Automated Research Organizer
Scans all sources → Organizes into NotebookLM format

Usage:
    python3 auto_organize_research.py

Sources:
    - ~/Downloads (local markdown files)
    - Google Drive (Research & Knowledge Base folders)
    - Airtable (Knowledge Management base)
"""
import json
import re
import os
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# =============================================================================
# CONFIGURATION
# =============================================================================

GOOGLE_DRIVE_PERSONAL = Path.home() / "Library/CloudStorage/GoogleDrive-mike.finneran@gmail.com/My Drive"
DOWNLOADS_DIR = Path.home() / "Downloads"
OUTPUT_DIR = Path.home() / "crewai-specialists/outputs/notebooklm-docs"
AIRTABLE_TOKEN_FILE = "/tmp/at_token.txt"

# Topic keywords for auto-categorization
TOPIC_KEYWORDS = {
    'CrewAI & AI Agents': ['crewai', 'crew', 'agent', 'multi-agent', 'orchestration', 'specialists'],
    'Business Intelligence': ['bi automation', 'business intelligence', 'analytics', 'reporting', 'dashboard'],
    'FlyFlat & Hospitality': ['flyflat', 'hotel', 'hospitality', 'cvent', 'groupize', 'booking'],
    'AI/ML Infrastructure': ['dgx', 'ollama', 'llm', 'gpu', 'nvidia', 'deployment', 'model', 'infrastructure'],
    'Sales & Marketing': ['sales', 'marketing', 'growth', 'email', 'outreach', 'strategy', 'lead generation'],
    'Real Estate & Development': ['symbiosis', 'development', 'property', 'real estate', 'acre'],
    'AI Prompting & Education': ['prompt', 'ivy league', 'education', 'persona', 'wispr', 'flow'],
    'General Business': ['business', 'consulting', 'strategy', 'service offering', 'client'],
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def categorize_by_topic(title, content=''):
    """Auto-categorize based on keywords"""
    text = f"{title} {content}".lower()
    topic_scores = {}

    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text)
        if score > 0:
            topic_scores[topic] = score

    if topic_scores:
        return max(topic_scores.items(), key=lambda x: x[1])[0]
    else:
        return 'Other Research'

def get_airtable_token():
    """Get Airtable API token from 1Password or file"""
    if Path(AIRTABLE_TOKEN_FILE).exists():
        return Path(AIRTABLE_TOKEN_FILE).read_text().strip()

    # Try to get from 1Password
    try:
        result = subprocess.run(
            ['op', 'item', 'list', '--categories', 'API Credential', '--format', 'json'],
            capture_output=True, text=True, check=True
        )
        items = json.loads(result.stdout)

        for item in items:
            if 'airtable' in item.get('title', '').lower():
                result = subprocess.run(
                    ['op', 'item', 'get', item['id'], '--format', 'json'],
                    capture_output=True, text=True, check=True
                )
                item_data = json.loads(result.stdout)
                for field in item_data.get('fields', []):
                    if field.get('label') in ['credential', 'token', 'api_key']:
                        token = field.get('value', '')
                        if len(token) > 50:  # Personal Access Token is ~82 chars
                            Path(AIRTABLE_TOKEN_FILE).write_text(token)
                            return token
    except:
        pass

    return None

# =============================================================================
# SOURCE COLLECTORS
# =============================================================================

def collect_downloads():
    """Scan Downloads for markdown research files"""
    files = []

    if not DOWNLOADS_DIR.exists():
        return files

    for md_file in DOWNLOADS_DIR.glob('*.md'):
        try:
            content = md_file.read_text(encoding='utf-8')
        except:
            content = ''

        preview = content[:500] if content else ''
        topic = categorize_by_topic(md_file.stem, content)

        files.append({
            'source': 'Downloads',
            'type': 'Markdown',
            'title': md_file.stem,
            'filename': md_file.name,
            'content': content,
            'preview': preview,
            'topic': topic,
            'size_kb': md_file.stat().st_size / 1024,
            'modified': datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()
        })

    return files

def collect_google_drive():
    """Scan Google Drive Research & Knowledge Base folders"""
    files = []

    if not GOOGLE_DRIVE_PERSONAL.exists():
        print(f"  ⚠️  Google Drive not found at {GOOGLE_DRIVE_PERSONAL}")
        return files

    # Research folder
    research_dir = GOOGLE_DRIVE_PERSONAL / "Research"
    if research_dir.exists():
        for md_file in research_dir.glob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
            except:
                content = ''

            topic = categorize_by_topic(md_file.stem, content)

            files.append({
                'source': 'Google Drive (Research)',
                'type': 'Markdown',
                'title': md_file.stem,
                'filename': md_file.name,
                'content': content,
                'preview': content[:500],
                'topic': topic,
                'size_kb': md_file.stat().st_size / 1024,
                'modified': datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()
            })

    # Knowledge Base folder
    kb_dir = GOOGLE_DRIVE_PERSONAL / "Knowledge Base"
    if kb_dir.exists():
        for md_file in kb_dir.glob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
            except:
                content = ''

            topic = categorize_by_topic(md_file.stem, content)

            files.append({
                'source': 'Google Drive (Knowledge Base)',
                'type': 'Markdown',
                'title': md_file.stem,
                'filename': md_file.name,
                'content': content,
                'preview': content[:500],
                'topic': topic,
                'size_kb': md_file.stat().st_size / 1024,
                'modified': datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()
            })

    # AI Projects
    ai_projects = GOOGLE_DRIVE_PERSONAL / "Project Database/Current Projects/AI Projects"
    if ai_projects.exists():
        for md_file in ai_projects.rglob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
            except:
                content = ''

            topic = categorize_by_topic(md_file.stem, content)

            files.append({
                'source': 'Google Drive (AI Projects)',
                'type': 'Markdown',
                'title': md_file.stem,
                'filename': md_file.name,
                'content': content,
                'preview': content[:500],
                'topic': topic,
                'size_kb': md_file.stat().st_size / 1024,
                'modified': datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()
            })

    return files

def collect_airtable():
    """Extract documents from Airtable Knowledge Management base"""
    items = []

    token = get_airtable_token()
    if not token:
        print("  ⚠️  No Airtable token found, skipping Airtable")
        return items

    try:
        # Fetch Documents table from Knowledge Management base
        import urllib.request

        url = "https://api.airtable.com/v0/appx922aa4LURWlMI/tblbLNQlJ9Ojaz9gK"
        req = urllib.request.Request(url)
        req.add_header('Authorization', f'Bearer {token}')

        with urllib.request.urlopen(req) as response:
            docs_data = json.loads(response.read())

        for record in docs_data.get('records', []):
            fields = record.get('fields', {})

            title = (fields.get('Title') or
                    fields.get('Name') or
                    fields.get('name') or
                    f"Document_{record['id'][:8]}")

            content = (fields.get('Content') or
                      fields.get('Notes') or
                      fields.get('Description') or
                      fields.get('Body') or
                      fields.get('Text') or
                      '')

            url = fields.get('URL') or fields.get('Link') or ''
            tags = fields.get('Tags') or fields.get('Category') or []
            if isinstance(tags, str):
                tags = [tags]

            topic = categorize_by_topic(title, content)
            preview = content[:500] if content else 'No content preview available'

            items.append({
                'source': 'Airtable (Knowledge Management)',
                'type': 'Document',
                'title': title,
                'content': content,
                'preview': preview,
                'url': url,
                'tags': tags,
                'topic': topic,
                'airtable_id': record['id'],
                'created': fields.get('Created') or record.get('createdTime', '')
            })

    except Exception as e:
        print(f"  ⚠️  Airtable error: {e}")

    return items

# =============================================================================
# NOTEBOOKLM GENERATOR
# =============================================================================

def group_by_topic(all_items):
    """Group items by topic"""
    grouped = defaultdict(list)
    for item in all_items:
        grouped[item['topic']].append(item)
    return dict(grouped)

def create_notebooklm_document(topic, items, output_dir):
    """Create NotebookLM-ready markdown for a topic"""

    markdown = f"""---
title: "{topic} - Research Collection"
sources: ["Downloads", "Google Drive", "Airtable"]
created: "{datetime.now().isoformat()}"
items_included: {len(items)}
auto_generated: true
---

# {topic}

**Total Items**: {len(items)}
**Sources**: Downloads + Google Drive + Airtable
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Contents

"""

    # Table of contents
    for i, item in enumerate(items, 1):
        markdown += f"{i}. {item['title']} ({item['source']})\n"

    markdown += "\n---\n\n"

    # Detailed items
    for i, item in enumerate(items, 1):
        markdown += f"## {i}. {item['title']}\n\n"
        markdown += f"**Source**: {item['source']}\n"
        markdown += f"**Type**: {item['type']}\n"

        if item.get('filename'):
            markdown += f"**File**: `{item['filename']}`\n"

        if item.get('url'):
            markdown += f"**URL**: {item['url']}\n"

        if item.get('tags') and item['tags']:
            markdown += f"**Tags**: {', '.join(item['tags'])}\n"

        if item.get('size_kb'):
            markdown += f"**Size**: {item['size_kb']:.1f} KB\n"

        if item.get('modified'):
            markdown += f"**Modified**: {item['modified']}\n"

        if item.get('created'):
            markdown += f"**Created**: {item['created']}\n"

        markdown += "\n### Content\n\n"

        if item['content']:
            content = item['content'][:10000]
            if len(item['content']) > 10000:
                content += "\n\n*[Content truncated - original was longer]*"
            markdown += content + "\n\n"
        else:
            markdown += f"*Preview*: {item['preview']}\n\n"

        markdown += "---\n\n"

    # Save to file
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    safe_topic = re.sub(r'[^\w\s-]', '', topic).strip().replace(' ', '_')
    filename = f"{safe_topic.lower()}_research.md"

    output_file = output_path / filename
    output_file.write_text(markdown, encoding='utf-8')

    return output_file

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("🔬 AUTO RESEARCH ORGANIZER")
    print("=" * 80 + "\n")

    # Collect from all sources
    print("📁 Collecting from Downloads...")
    downloads_files = collect_downloads()
    print(f"   Found {len(downloads_files)} files\n")

    print("☁️  Collecting from Google Drive...")
    gdrive_files = collect_google_drive()
    print(f"   Found {len(gdrive_files)} files\n")

    print("📊 Collecting from Airtable...")
    airtable_items = collect_airtable()
    print(f"   Found {len(airtable_items)} documents\n")

    # Combine
    all_items = downloads_files + gdrive_files + airtable_items
    print(f"📚 Total Research Items: {len(all_items)}\n")

    if not all_items:
        print("⚠️  No research items found!")
        return

    # Group by topic
    print("🏷️  Categorizing by topic...")
    grouped = group_by_topic(all_items)

    for topic, items in sorted(grouped.items()):
        print(f"   - {topic}: {len(items)} items")
    print()

    # Create NotebookLM documents
    print("📝 Creating NotebookLM documents...\n")

    created_files = []
    for topic, items in sorted(grouped.items()):
        print(f"   Creating {topic}...")
        output_file = create_notebooklm_document(topic, items, OUTPUT_DIR)
        created_files.append(output_file)
        size_kb = output_file.stat().st_size / 1024
        print(f"   ✓ {output_file.name} ({size_kb:.0f}KB, {len(items)} items)")

    print("\n" + "=" * 80)
    print("✅ COMPLETE\n")
    print(f"Created {len(created_files)} NotebookLM documents in:")
    print(f"  {OUTPUT_DIR}\n")

    # Summary by source
    sources_count = defaultdict(int)
    for item in all_items:
        sources_count[item['source']] += 1

    print("📊 Sources Breakdown:")
    for source, count in sorted(sources_count.items()):
        print(f"  - {source}: {count} items")

    print("\n📋 NEXT STEPS:")
    print("1. Go to https://notebooklm.google.com")
    print("2. Upload the documents you want to analyze")
    print("3. Start asking questions!\n")
    print("=" * 80)

if __name__ == "__main__":
    main()
