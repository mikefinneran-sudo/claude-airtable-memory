# Contributing to ObsidianVault Scripts

Guidelines for adding, modifying, and maintaining custom scripts in this automation toolkit.

---

## 📋 Before Adding a New Script

**Ask yourself:**
1. **Is it reusable?** Will this script be used more than once?
2. **Does it already exist?** Check the README.md inventory first
3. **Is it documented?** Can others understand what it does?
4. **Is it secure?** Does it handle credentials safely?
5. **Is it tested?** Have you run it successfully at least twice?

---

## ✅ Script Checklist

### Required Elements

Every script must include:

1. **Shebang line**
   ```bash
   #!/bin/bash
   #!/usr/bin/env python3
   ```

2. **Header comment block**
   ```bash
   # Script Name and Purpose
   # Brief description of what this script does
   # Author: Your Name
   # Date: YYYY-MM-DD
   ```

3. **Usage documentation**
   ```bash
   # Usage:
   #   ./script-name.sh [arguments]
   #   python3 script-name.py --flag value
   ```

4. **Dependencies listed**
   ```bash
   # Dependencies:
   #   - Tool 1
   #   - Tool 2
   #   - pip3 install package-name
   ```

5. **Error handling**
   ```bash
   set -e  # Exit on error (bash)
   # OR
   try/except blocks (Python)
   ```

---

## 📝 Naming Conventions

### Shell Scripts (`.sh`)
- Use lowercase with hyphens: `create-daily-note.sh`
- Action-oriented names: `sync-to-notion.sh`
- Setup scripts: `setup-integration-name.sh`

### Python Scripts (`.py`)
- Use lowercase with underscores: `update_metrics.py`
- Module-style names: `sync_calendar.py`
- Avoid abbreviations: `synchronize` not `sync`

### AppleScripts (`.applescript`)
- Use lowercase with hyphens: `create-utm-vm.applescript`
- Descriptive action names

---

## 🗂️ File Organization

### Location Guidelines

```
.scripts/
├── Core automation (daily notes, metrics)
├── Integration scripts (Notion, Gmail, Calendar)
├── Utility scripts (screenshot, API keys)
├── Setup wizards
├── Documentation (.md files)
└── Config files (.json, logs)

.integrations/
├── alfred/workflows/       # Alfred-specific scripts
├── 1password/             # 1Password configs
└── cleanshot/             # CleanShot configs

.mcp/
└── [server-name]/         # MCP servers in subdirectories
    ├── server.py
    └── setup.sh
```

---

## 📄 Documentation Standards

### Inline Comments

**Good:**
```bash
# Calculate yesterday's date for daily note linking
YESTERDAY=$(date -v-1d +%Y-%m-%d)
```

**Bad:**
```bash
# Get date
YESTERDAY=$(date -v-1d +%Y-%m-%d)
```

### Function Documentation

**Python:**
```python
def update_metrics(mrr: int, customers: int, notes: str = "") -> None:
    """
    Update revenue tracking table with current metrics

    Args:
        mrr: Monthly recurring revenue in dollars
        customers: Total customer count
        notes: Optional notes about this update

    Raises:
        FileNotFoundError: If revenue file doesn't exist
    """
```

**Bash:**
```bash
# update_metrics()
# Update revenue tracking in Dashboard.md
# Arguments:
#   $1 - MRR amount
#   $2 - Customer count
# Returns:
#   0 on success, 1 on error
update_metrics() {
    local mrr=$1
    local customers=$2
    # ...
}
```

### README Entry

When adding a script, update `README.md` with:

```markdown
#### `your-script-name.sh`
**Purpose:** One-sentence description
**Features:**
- Feature 1
- Feature 2
- Feature 3

**Usage:**
```bash
./your-script-name.sh [args]
```

**Dependencies:**
- Tool 1
- Tool 2

**Location:** `.scripts/your-script-name.sh:1`
```

---

## 🔒 Security Best Practices

### Never Commit Secrets

**Add to `.gitignore`:**
```
# API Keys and tokens
*.token
.env
*credentials*.json
notion-sync-config.json

# OAuth tokens
token.pickle
token.json

# Logs with potential secrets
*.log
```

### Use 1Password CLI for Credentials

**Good:**
```bash
API_KEY=$(./get-api-key.sh "Anthropic API")
```

**Bad:**
```bash
API_KEY="sk-ant-1234567890"  # NEVER DO THIS
```

### Store Tokens Securely

```bash
# Token files in home directory (not in git)
TOKEN_FILE="$HOME/.lifehub-notion-token"

# Check file permissions
chmod 600 "$TOKEN_FILE"
```

---

## 🧪 Testing Requirements

### Before Committing

1. **Test the script at least twice**
   - First run: Does it work?
   - Second run: Does it handle existing files?

2. **Test error conditions**
   - Missing files
   - Wrong permissions
   - Invalid arguments
   - Network failures

3. **Test with dry-run (if applicable)**
   ```bash
   python3 script.py --dry-run
   ```

4. **Verify no side effects**
   - Check git status
   - Review modified files
   - Ensure no secrets exposed

### Test Script Template

```bash
#!/bin/bash
# test-your-script.sh

echo "Testing your-script.sh..."

# Test 1: Normal execution
./your-script.sh
if [ $? -eq 0 ]; then
    echo "✅ Test 1 passed"
else
    echo "❌ Test 1 failed"
fi

# Test 2: Handle existing file
./your-script.sh
if [ $? -eq 0 ]; then
    echo "✅ Test 2 passed"
else
    echo "❌ Test 2 failed"
fi

# Test 3: Invalid input
./your-script.sh invalid-arg
if [ $? -ne 0 ]; then
    echo "✅ Test 3 passed (correctly failed)"
else
    echo "❌ Test 3 failed (should have failed)"
fi
```

---

## 📦 Git Workflow

### Adding a New Script

```bash
# 1. Create the script
touch .scripts/new-script.sh
chmod +x .scripts/new-script.sh

# 2. Write and test the script
vim .scripts/new-script.sh
./scripts/new-script.sh  # Test

# 3. Document it
# Add entry to README.md
# Add setup guide if needed

# 4. Commit
git add .scripts/new-script.sh .scripts/README.md
git commit -m "Add new-script.sh: [brief description]

Features:
- Feature 1
- Feature 2

Usage: ./new-script.sh

🤖 Generated with Claude Code"

# 5. Push
git push origin main
```

### Modifying Existing Script

```bash
# 1. Make changes
vim .scripts/existing-script.sh

# 2. Test thoroughly
./scripts/existing-script.sh

# 3. Update documentation if needed
vim .scripts/README.md

# 4. Commit with clear message
git add .scripts/existing-script.sh
git commit -m "Update existing-script.sh: [what changed]

- Change 1
- Change 2

🤖 Generated with Claude Code"

git push origin main
```

---

## 🎯 Code Quality Standards

### Bash Scripts

**Use:**
- `set -e` for early error exit
- `set -u` for undefined variable detection
- Quotes around variables: `"$VARIABLE"`
- Functions for repeated code
- Descriptive variable names

**Example:**
```bash
#!/bin/bash
set -e
set -u

VAULT_PATH="$HOME/Documents/ObsidianVault"
TODAY=$(date +%Y-%m-%d)

create_note() {
    local note_path="$1"

    if [ -f "$note_path" ]; then
        echo "Note already exists"
        return 0
    fi

    touch "$note_path"
    echo "Created: $note_path"
}

main() {
    local note_file="${VAULT_PATH}/Daily/${TODAY}.md"
    create_note "$note_file"
}

main "$@"
```

### Python Scripts

**Use:**
- Type hints
- Docstrings
- f-strings for formatting
- pathlib for file paths
- logging instead of print
- argparse for CLI arguments

**Example:**
```python
#!/usr/bin/env python3
"""
Script description here
"""

import logging
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_file(file_path: Path) -> Optional[str]:
    """
    Process a file and return result

    Args:
        file_path: Path to the file to process

    Returns:
        Processed content or None if error
    """
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return None

    content = file_path.read_text()
    return content.upper()

def main() -> None:
    """Main entry point"""
    vault_path = Path.home() / "Documents" / "ObsidianVault"
    result = process_file(vault_path / "test.md")

    if result:
        logger.info("Processing complete")

if __name__ == "__main__":
    main()
```

---

## 📊 Performance Guidelines

### Optimization Tips

1. **Avoid unnecessary file reads**
   ```bash
   # Bad: Read file multiple times
   cat file.txt | grep "pattern1"
   cat file.txt | grep "pattern2"

   # Good: Read once
   content=$(cat file.txt)
   echo "$content" | grep "pattern1"
   echo "$content" | grep "pattern2"
   ```

2. **Use appropriate tools**
   - `grep` for searching
   - `sed` for inline edits
   - `awk` for column processing
   - Python for complex logic

3. **Cache expensive operations**
   ```python
   # Cache API responses
   cache_file = Path(".cache/api-response.json")
   if cache_file.exists():
       data = json.loads(cache_file.read_text())
   else:
       data = fetch_from_api()
       cache_file.write_text(json.dumps(data))
   ```

---

## 🐛 Debugging

### Enable Debug Mode

**Bash:**
```bash
#!/bin/bash
set -x  # Print commands before executing
set -v  # Print input lines as they are read
```

**Python:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

**Script not executable:**
```bash
chmod +x script.sh
```

**Wrong interpreter:**
```bash
# Check shebang
head -1 script.sh

# Should be:
#!/bin/bash
#!/usr/bin/env python3
```

**Path issues:**
```bash
# Use absolute paths
VAULT_PATH="$HOME/Documents/ObsidianVault"
# Not relative:
# VAULT_PATH="../ObsidianVault"
```

---

## 📞 Getting Help

If you're stuck:

1. **Check existing scripts** - Look for similar functionality
2. **Read the docs** - Check setup guides in `.scripts/`
3. **Test incrementally** - Add one feature at a time
4. **Use debug mode** - Enable verbose logging
5. **Ask for review** - Commit and ask for feedback

---

## ✨ Examples

### Simple Utility Script

```bash
#!/bin/bash
# open-note.sh
# Opens a specific note in Obsidian by name
# Usage: ./open-note.sh "Note Name"

set -e

VAULT_NAME="ObsidianVault"
NOTE_NAME="$1"

if [ -z "$NOTE_NAME" ]; then
    echo "Usage: $0 <note-name>"
    exit 1
fi

# URL encode the note name
ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$NOTE_NAME'))")

# Open in Obsidian
open "obsidian://open?vault=${VAULT_NAME}&file=${ENCODED}"

echo "✅ Opened: $NOTE_NAME"
```

### Python Integration Script

```python
#!/usr/bin/env python3
"""
Export daily notes to JSON for external tools
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VAULT_PATH = Path.home() / "Documents" / "ObsidianVault"
DAILY_DIR = VAULT_PATH / "Daily"
OUTPUT_FILE = VAULT_PATH / "exports" / "daily-notes.json"

def parse_daily_note(file_path: Path) -> Dict:
    """Parse a daily note and extract metadata"""
    content = file_path.read_text()

    # Simple parsing (enhance as needed)
    return {
        "date": file_path.stem,
        "file": str(file_path),
        "word_count": len(content.split()),
        "line_count": len(content.splitlines())
    }

def export_notes() -> None:
    """Export all daily notes to JSON"""
    notes = []

    for md_file in sorted(DAILY_DIR.glob("*.md")):
        try:
            note_data = parse_daily_note(md_file)
            notes.append(note_data)
            logger.info(f"Parsed: {md_file.name}")
        except Exception as e:
            logger.error(f"Error parsing {md_file.name}: {e}")

    # Create exports directory
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    # Write JSON
    OUTPUT_FILE.write_text(json.dumps(notes, indent=2))
    logger.info(f"✅ Exported {len(notes)} notes to {OUTPUT_FILE}")

def main() -> None:
    """Main entry point"""
    logger.info("Starting daily notes export...")
    export_notes()
    logger.info("Complete!")

if __name__ == "__main__":
    main()
```

---

## 📅 Maintenance Schedule

### Weekly
- Review error logs
- Test critical scripts (daily note, metrics)
- Check for outdated dependencies

### Monthly
- Update documentation
- Review and archive old logs
- Check for security updates

### Quarterly
- Full script audit
- Update README with new scripts
- Review and optimize slow scripts

---

**Last Updated:** 2025-10-28
**Questions?** Review existing scripts or documentation files
