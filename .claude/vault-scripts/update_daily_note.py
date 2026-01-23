#!/usr/bin/env python3
"""
WalterSignal Daily Note Auto-Updater
Automatically populates daily notes with project priorities and tasks
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Configuration
VAULT_PATH = Path("/Users/mikefinneran/Documents/ObsidianVault")
DAILY_PATH = VAULT_PATH / "Daily"
PROJECTS_PATH = VAULT_PATH / "Projects"
STATE_FILE = VAULT_PATH / ".scripts" / "daily_note_state.json"

def get_today_note_path():
    """Get path to today's daily note"""
    today = datetime.now().strftime("%Y-%m-%d")
    return DAILY_PATH / f"{today}.md"

def get_waltersignal_priorities():
    """Extract current priorities from WalterSignal project files"""
    priorities = []

    # Check for recent project files
    recent_files = [
        "waltersignal_pitch_deck_slides.md",
        "waltersignal_pitch_deck_plan.md",
        "great_range_outreach_email.md",
        "waltersignal_pe_strategy.md",
        "waltersignal_target_customers.md"
    ]

    # Determine current phase based on what exists
    deck_slides_exists = (PROJECTS_PATH / "waltersignal_pitch_deck_slides.md").exists()
    outreach_exists = (PROJECTS_PATH / "great_range_outreach_email.md").exists()

    if deck_slides_exists and not is_deck_designed():
        priorities.append("[ ] Review [[waltersignal_pitch_deck_slides]] - 17-slide customer deck")
        priorities.append("[ ] Design pitch deck visuals (Gamma.app or Google Slides)")
        priorities.append("[ ] Prepare Great Range Capital outreach")
    elif outreach_exists:
        priorities.append("[ ] Send Great Range Capital pilot offer ($999/mo)")
        priorities.append("[ ] Prepare 10-target sample for demo")
        priorities.append("[ ] Schedule follow-up calls")
    else:
        priorities.append("[ ] Continue WalterSignal development")
        priorities.append("[ ] Review project documentation")
        priorities.append("[ ] Plan next steps")

    return priorities[:3]  # Top 3

def get_revenue_activities():
    """Get revenue-focused activities"""
    activities = [
        "[ ] Draft personalized email to Great Range Capital ($999 pilot)",
        "[ ] Prepare 10-target KC sample for demo",
        "[ ] Schedule ICP definition calls with potential customers"
    ]
    return activities

def get_project_tasks():
    """Get current project tasks"""
    completed = []
    pending = []

    # Check what's been completed today
    if (PROJECTS_PATH / "waltersignal_pitch_deck_slides.md").exists():
        completed.append("[x] ✅ Complete pitch deck content (17 slides, case studies)")

    if (VAULT_PATH / ".git").exists():
        completed.append("[x] ✅ Backup vault to GitHub (private repo)")

    # Pending tasks
    pending.append("[ ] Design pitch deck visuals (Gamma.app recommended)")
    pending.append("[ ] Set up pilot offer workflow (sample → demo → close)")
    pending.append("[ ] Launch first customer outreach campaign")

    return completed, pending

def is_deck_designed():
    """Check if deck has been designed (placeholder logic)"""
    # Could check for exported PDF/PPTX or state file
    return False

def load_state():
    """Load previous state"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    """Save current state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def update_daily_note():
    """Update today's daily note with current priorities"""
    note_path = get_today_note_path()

    # Create daily note if it doesn't exist
    if not note_path.exists():
        create_daily_note_from_template(note_path)

    # Read current note
    with open(note_path, 'r') as f:
        content = f.read()

    # Check if already updated today
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")

    if state.get('last_updated') == today:
        print(f"✓ Daily note already updated today ({today})")
        return

    # Get current priorities and tasks
    priorities = get_waltersignal_priorities()
    revenue_activities = get_revenue_activities()
    completed, pending = get_project_tasks()

    # Build new sections
    priorities_section = "## 🎯 Top 3 Priorities\n\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(priorities)])

    revenue_section = "## 💰 Revenue Activities\n\n" + "\n".join(revenue_activities)

    projects_section = (
        "## 📊 Projects\n\n"
        "### WalterFetch\n" +
        "\n".join(completed + pending) +
        "\n\n### Other Projects\n"
        "- [ ] LifeHub: Review user guide and FAQ for updates"
    )

    ideas_section = (
        "## 💡 Ideas & Notes\n\n"
        "- **Gamma.app for deck design:** AI-powered, faster than manual design\n"
        "- **Next week:** Focus on Tier 3 customer outreach (Great Range, WILsquare, Hadley)\n"
        "- **BI + Target sourcing combo:** Unique differentiation vs competitors"
    )

    # Replace sections in content (basic implementation)
    # More sophisticated parsing could use regex or markdown parser

    if "## 🎯 Top 3 Priorities" in content:
        # Update existing sections
        lines = content.split('\n')
        new_lines = []
        skip_until_next_section = False

        for line in lines:
            if line.startswith("## 🎯 Top 3 Priorities"):
                new_lines.append(priorities_section)
                skip_until_next_section = True
            elif line.startswith("## 💰 Revenue Activities"):
                new_lines.append(revenue_section)
                skip_until_next_section = True
            elif line.startswith("## 📊 Projects"):
                new_lines.append(projects_section)
                skip_until_next_section = True
            elif line.startswith("## 💡 Ideas & Notes"):
                new_lines.append(ideas_section)
                skip_until_next_section = True
            elif line.startswith("##") and skip_until_next_section:
                skip_until_next_section = False
                new_lines.append(line)
            elif not skip_until_next_section:
                new_lines.append(line)

        content = '\n'.join(new_lines)

    # Write updated note
    with open(note_path, 'w') as f:
        f.write(content)

    # Update state
    state['last_updated'] = today
    state['priorities'] = priorities
    save_state(state)

    print(f"✅ Daily note updated: {note_path}")

def create_daily_note_from_template(note_path):
    """Create new daily note from template"""
    today = datetime.now()
    day_name = today.strftime("%A")
    date_str = today.strftime("%Y-%m-%d")

    template = f"""# {date_str} - {day_name}

## 🎯 Top 3 Priorities

1.
2.
3.

## 💰 Revenue Activities

- [ ]
- [ ]
- [ ]

## 📊 Projects

### WalterFetch
- [ ]

### Other Projects
- [ ]

## 💡 Ideas & Notes

-

## ✅ Completed Today

-

## 📈 Metrics

- **Revenue Today:** $
- **New Leads:**
- **Conversations:**

## 🧠 Learnings

-

---

**Energy Level:** ⚡⚡⚡⚡⚡ (1-5)
**Mood:** 😊

## Tomorrow's Focus

1.
2.
3.
"""

    with open(note_path, 'w') as f:
        f.write(template)

    print(f"📝 Created new daily note: {note_path}")

if __name__ == "__main__":
    update_daily_note()
