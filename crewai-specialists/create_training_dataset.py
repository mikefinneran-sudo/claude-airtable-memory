#!/usr/bin/env python3
"""
Create training dataset for Llama 3.1:70b from research files.
Format: Instruction-following pairs for CrewAI agent training.
"""

import os
import json
import glob
from pathlib import Path

# Paths
VAULT_ROOT = os.path.expanduser("~/Documents/ObsidianVault")
OUTPUT_FILE = os.path.expanduser("~/crewai-specialists/training_data.jsonl")

# Exclude patterns (avoid noise from node_modules, .git, etc.)
EXCLUDE_PATTERNS = [
    "node_modules",
    ".git",
    ".obsidian",
    "Archive",
    ".app",  # Avoid .app bundles
]

def extract_markdown_sections(file_path):
    """Extract sections from markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = []
    current_section = {"title": "", "content": ""}

    for line in content.split('\n'):
        if line.startswith('# '):
            if current_section["content"]:
                sections.append(current_section)
            current_section = {"title": line[2:].strip(), "content": ""}
        else:
            current_section["content"] += line + "\n"

    if current_section["content"]:
        sections.append(current_section)

    return sections

def create_training_examples(sections, filename):
    """Convert sections to instruction-following format."""
    examples = []

    for section in sections:
        if len(section["content"].strip()) < 100:  # Skip tiny sections
            continue

        # Create instruction-response pair
        example = {
            "instruction": f"As a CrewAI specialist agent, explain: {section['title']}",
            "input": f"Source: {filename}",
            "output": section["content"].strip()
        }
        examples.append(example)

    return examples

def should_exclude(file_path):
    """Check if file should be excluded."""
    path_str = str(file_path)
    return any(pattern in path_str for pattern in EXCLUDE_PATTERNS)

def main():
    print(f"Scanning ENTIRE Obsidian Vault: {VAULT_ROOT}")
    print(f"Excluding patterns: {', '.join(EXCLUDE_PATTERNS)}\n")

    all_examples = []
    vault_path = Path(VAULT_ROOT)

    # Recursively find ALL markdown files
    print("Finding all markdown files...")
    all_md_files = [
        f for f in vault_path.rglob("*.md")
        if f.is_file() and not should_exclude(f)
    ]

    print(f"✓ Found {len(all_md_files)} markdown files\n")

    if len(all_md_files) == 0:
        print("ERROR: No files found")
        return

    for idx, md_file in enumerate(all_md_files, 1):
        filename = os.path.basename(md_file)
        relative_path = md_file.relative_to(vault_path)
        print(f"[{idx}/{len(all_md_files)}] {relative_path}")

        sections = extract_markdown_sections(md_file)
        examples = create_training_examples(sections, filename)
        all_examples.extend(examples)

        print(f"  → Created {len(examples)} training examples")

    # Write to JSONL format (Unsloth compatible)
    print(f"\nWriting {len(all_examples)} examples to: {OUTPUT_FILE}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for example in all_examples:
            f.write(json.dumps(example) + '\n')

    print(f"✓ Training dataset created: {len(all_examples)} examples")
    print(f"✓ File size: {os.path.getsize(OUTPUT_FILE) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()
