#!/usr/bin/env python3
"""
GitHub → Airtable Sync Script

Syncs GitHub repositories to Airtable Projects table:
- Fetches all repos from mikefinneran-sudo
- Updates existing projects with GitHub URLs
- Creates new projects for repos not in Airtable
- Syncs last commit dates and activity

Uses:
- 1Password for credentials
- Airtable API
- GitHub CLI (gh)
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import requests

# Configuration
AIRTABLE_BASE_ID = "app6g0t0wtruwLA5I"
PROJECTS_TABLE_ID = "tblzpsBt1zyPKzeq1"  # Projects table
GITHUB_USERNAME = "mikefinneran-sudo"
API_BASE = "https://api.airtable.com/v0"

# Logging
LOG_DIR = os.path.expanduser("~/.claude/logs")
os.makedirs(LOG_DIR, exist_ok=True)

class GitHubAirtableSync:
    """Sync GitHub repos to Airtable projects"""

    def __init__(self):
        self.sync_log = []
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.airtable_token = self.get_airtable_token()
        self.github_token = self.get_github_token()
        self.headers = {
            "Authorization": f"Bearer {self.airtable_token}",
            "Content-Type": "application/json"
        }

    def get_airtable_token(self) -> str:
        """Get Airtable token from 1Password"""
        # Try different field names in 1Password with --reveal flag
        for field_name in ["api_key", "credential", "password"]:
            try:
                result = subprocess.run(
                    ["op", "item", "get", "Airtable WalterSignal", "--fields", field_name, "--reveal"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                token = result.stdout.strip()
                if token and token != "null":
                    self.log(f"✅ Retrieved Airtable token from 1Password (field: {field_name})")
                    return token
            except subprocess.CalledProcessError:
                continue

        self.log("⚠️  Could not get Airtable token from 1Password, trying environment variable")

        # Fallback to environment variable
        token = os.getenv("AIRTABLE_TOKEN")
        if token:
            self.log("✅ Using Airtable token from environment variable")
            return token

        self.log("❌ No Airtable token found in 1Password or environment")
        sys.exit(1)

    def get_github_token(self) -> Optional[str]:
        """Get GitHub token from 1Password (optional, gh CLI works without it)"""
        try:
            result = subprocess.run(
                ["op", "item", "get", "GitHub mikefinneran-sudo", "--fields", "credential"],
                capture_output=True,
                text=True,
                check=True
            )
            token = result.stdout.strip()
            if token:
                self.log("✅ Retrieved GitHub token from 1Password")
                return token
        except subprocess.CalledProcessError:
            self.log("ℹ️  No GitHub token in 1Password, using gh CLI default auth")
            return None

    def log(self, message: str):
        """Log message to console and internal log"""
        print(message)
        self.sync_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def get_github_repos(self) -> List[Dict[str, Any]]:
        """Fetch all repos from GitHub using gh CLI"""
        self.log("\n📦 Fetching GitHub repositories...")

        try:
            result = subprocess.run(
                [
                    "gh", "repo", "list", GITHUB_USERNAME,
                    "--limit", "100",
                    "--json", "name,url,description,isPrivate,pushedAt,createdAt"
                ],
                capture_output=True,
                text=True,
                check=True
            )

            repos = json.loads(result.stdout)
            self.log(f"✅ Found {len(repos)} GitHub repositories")
            return repos

        except subprocess.CalledProcessError as e:
            self.log(f"❌ Error fetching GitHub repos: {e.stderr}")
            return []
        except json.JSONDecodeError as e:
            self.log(f"❌ Error parsing GitHub response: {e}")
            return []

    def get_airtable_projects(self) -> List[Dict[str, Any]]:
        """Fetch all projects from Airtable"""
        self.log("\n📋 Fetching Airtable projects...")

        url = f"{API_BASE}/{AIRTABLE_BASE_ID}/{PROJECTS_TABLE_ID}"
        all_records = []
        offset = None

        while True:
            params = {"offset": offset} if offset else {}
            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code != 200:
                self.log(f"❌ Error fetching Airtable projects: {response.status_code}")
                self.log(f"Response: {response.text}")
                break

            data = response.json()
            all_records.extend(data.get('records', []))

            offset = data.get('offset')
            if not offset:
                break

        self.log(f"✅ Found {len(all_records)} Airtable projects")
        return all_records

    def match_repo_to_project(self, repo: Dict[str, Any], projects: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Find matching Airtable project for GitHub repo"""
        repo_name = repo['name'].lower()

        # Try exact match on project name
        for project in projects:
            project_name = project['fields'].get('Project Name', '').lower()
            github_url = project['fields'].get('GitHub Repo', '')

            # Match by URL
            if github_url and repo['url'] in github_url:
                return project

            # Match by name similarity
            if repo_name in project_name or project_name in repo_name:
                return project

        return None

    def update_project_github_url(self, project_id: str, github_url: str, last_commit: str, project_name: str):
        """Update existing project with GitHub URL and last commit date"""
        url = f"{API_BASE}/{AIRTABLE_BASE_ID}/{PROJECTS_TABLE_ID}/{project_id}"

        data = {
            "fields": {
                "GitHub Repo": github_url,
                "Notes": f"GitHub repo linked on {self.timestamp}\nLast commit: {last_commit}"
            }
        }

        response = requests.patch(url, headers=self.headers, json=data)

        if response.status_code == 200:
            self.log(f"  ✅ Updated '{project_name}' with GitHub URL")
            return True
        else:
            self.log(f"  ❌ Failed to update '{project_name}': {response.text}")
            return False

    def create_project_from_repo(self, repo: Dict[str, Any]) -> bool:
        """Create new Airtable project from GitHub repo"""
        url = f"{API_BASE}/{AIRTABLE_BASE_ID}/{PROJECTS_TABLE_ID}"

        # Determine project status based on recent activity
        pushed_at = datetime.fromisoformat(repo['pushedAt'].replace('Z', '+00:00'))
        days_since_push = (datetime.now(pushed_at.tzinfo) - pushed_at).days

        if days_since_push <= 7:
            status = "In Progress"
            priority = "High"
        elif days_since_push <= 30:
            status = "In Progress"
            priority = "Medium"
        else:
            status = "Paused"
            priority = "Low"

        # Determine product line from repo name
        product_line = "Infrastructure"
        if "walter" in repo['name'].lower() or "fetch" in repo['name'].lower():
            product_line = "WalterFetch"
        elif "stanny" in repo['name'].lower():
            product_line = "SpecialAgentStanny"
        elif "life" in repo['name'].lower() or "obsidian" in repo['name'].lower():
            product_line = "LifeHub"

        # Determine tags
        tags = []
        name_lower = repo['name'].lower()
        desc_lower = (repo.get('description') or '').lower()

        if any(word in name_lower or word in desc_lower for word in ['ai', 'claude', 'agent']):
            tags.append("AI")
        if any(word in name_lower or word in desc_lower for word in ['automat', 'sync', 'script']):
            tags.append("Automation")
        if 'client' in desc_lower or 'flyflat' in name_lower:
            tags.append("Client Work")
        if 'research' in desc_lower or 'study' in desc_lower:
            tags.append("Research")
        if 'internal' in desc_lower or 'utility' in name_lower or 'tool' in name_lower:
            tags.append("Internal")

        if not tags:
            tags = ["Internal"]  # Default tag

        data = {
            "fields": {
                "Project Name": repo['name'].replace('-', ' ').title(),
                "Status": status,
                "Priority": priority,
                "Product Line": product_line,
                "Description": repo.get('description', 'Synced from GitHub'),
                "Owner": "Mike Finneran",
                "GitHub Repo": repo['url'],
                "Tags": tags,
                "Notes": f"Auto-created from GitHub on {self.timestamp}\nLast pushed: {repo['pushedAt'][:10]}"
            }
        }

        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            self.log(f"  ✅ Created project '{data['fields']['Project Name']}'")
            return True
        else:
            self.log(f"  ❌ Failed to create project '{repo['name']}': {response.text}")
            return False

    def sync(self):
        """Main sync logic"""
        self.log("🔄 Starting GitHub → Airtable Sync")
        self.log("=" * 60)

        # Fetch data
        github_repos = self.get_github_repos()
        airtable_projects = self.get_airtable_projects()

        if not github_repos:
            self.log("❌ No GitHub repos found, aborting sync")
            return

        # Track stats
        stats = {
            "repos_checked": len(github_repos),
            "projects_updated": 0,
            "projects_created": 0,
            "errors": 0
        }

        self.log("\n🔗 Matching repos to projects...")

        for repo in github_repos:
            repo_name = repo['name']
            last_commit = repo['pushedAt'][:10]  # YYYY-MM-DD

            # Find matching project
            matching_project = self.match_repo_to_project(repo, airtable_projects)

            if matching_project:
                # Update existing project
                project_id = matching_project['id']
                project_name = matching_project['fields'].get('Project Name', 'Unknown')
                current_github_url = matching_project['fields'].get('GitHub Repo', '')

                if not current_github_url:
                    # Project exists but GitHub URL is empty - update it
                    if self.update_project_github_url(project_id, repo['url'], last_commit, project_name):
                        stats['projects_updated'] += 1
                    else:
                        stats['errors'] += 1
                else:
                    self.log(f"  ℹ️  '{project_name}' already has GitHub URL")
            else:
                # Create new project
                self.log(f"\n📌 Creating new project for '{repo_name}'...")
                if self.create_project_from_repo(repo):
                    stats['projects_created'] += 1
                else:
                    stats['errors'] += 1

        # Summary
        self.log("\n" + "=" * 60)
        self.log("✅ Sync Complete!")
        self.log(f"\n📊 Statistics:")
        self.log(f"   GitHub repos checked: {stats['repos_checked']}")
        self.log(f"   Projects updated: {stats['projects_updated']}")
        self.log(f"   Projects created: {stats['projects_created']}")
        self.log(f"   Errors: {stats['errors']}")

        # Write log file
        self.write_log()

    def write_log(self):
        """Write sync log to file"""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file = os.path.join(LOG_DIR, f"github-airtable-sync_{timestamp}.log")

        with open(log_file, 'w') as f:
            f.write("GitHub → Airtable Sync Log\n")
            f.write(f"Time: {self.timestamp}\n")
            f.write("=" * 60 + "\n\n")
            f.write("\n".join(self.sync_log))

        self.log(f"\n📝 Log saved to: {log_file}")

def main():
    """Main entry point"""
    try:
        syncer = GitHubAirtableSync()
        syncer.sync()
    except KeyboardInterrupt:
        print("\n\n⚠️  Sync interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
