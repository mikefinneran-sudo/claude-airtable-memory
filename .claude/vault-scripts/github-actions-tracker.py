#!/usr/bin/env python3
"""
GitHub Actions Cost Tracker
Monitors GitHub Actions usage and costs across all repositories

Cost: $0.008/minute for private repos (2,000 free minutes/month on free plan)
Schedule: Weekly
Build Time: 2 hours
ROI: 500%+ (prevents surprise bills)
"""

import os
import pickle
import requests
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# GitHub API settings
GITHUB_API_URL = "https://api.github.com"
SCOPES = []  # GitHub uses personal access token, not OAuth2

def get_github_token():
    """Get GitHub personal access token from environment or file"""
    # Check environment variable first
    token = os.getenv('GITHUB_TOKEN')
    if token:
        return token

    # Check token file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    token_file = os.path.join(script_dir, 'github_token.txt')

    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            return f.read().strip()

    print("\n❌ GitHub token not found!")
    print("\nSetup instructions:")
    print("1. Go to: https://github.com/settings/tokens")
    print("2. Click 'Generate new token (classic)'")
    print("3. Name: 'Actions Cost Tracker'")
    print("4. Scopes: Select 'repo' and 'read:org'")
    print("5. Generate token")
    print("6. Save token to: ~/.env as GITHUB_TOKEN=your_token")
    print("   OR save to: github_token.txt in scripts folder")
    return None

def get_user_repos(token):
    """Get all repositories for authenticated user"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    repos = []
    page = 1

    while True:
        response = requests.get(
            f"{GITHUB_API_URL}/user/repos",
            headers=headers,
            params={'per_page': 100, 'page': page, 'type': 'all'}
        )

        if response.status_code != 200:
            print(f"❌ Error fetching repos: {response.status_code}")
            return []

        page_repos = response.json()
        if not page_repos:
            break

        repos.extend(page_repos)
        page += 1

    return repos

def get_actions_usage(token, owner, repo):
    """Get GitHub Actions usage for a repository"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get workflow runs from last 30 days
    since = (datetime.now() - timedelta(days=30)).isoformat()

    response = requests.get(
        f"{GITHUB_API_URL}/repos/{owner}/{repo}/actions/runs",
        headers=headers,
        params={'created': f'>={since}', 'per_page': 100}
    )

    if response.status_code != 200:
        return None

    data = response.json()
    runs = data.get('workflow_runs', [])

    total_duration = 0
    billable_duration = 0
    run_count = len(runs)

    for run in runs:
        # Duration in milliseconds, convert to minutes
        if run.get('run_duration_ms'):
            duration_minutes = run['run_duration_ms'] / 1000 / 60
            total_duration += duration_minutes

            # Private repos are billable, public repos are free
            if repo.get('private', False):
                billable_duration += duration_minutes

    return {
        'run_count': run_count,
        'total_duration': total_duration,
        'billable_duration': billable_duration,
        'estimated_cost': billable_duration * 0.008  # $0.008 per minute
    }

def generate_report(repos_data, output_path=None):
    """Generate markdown report of GitHub Actions usage"""
    if output_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, '../github-actions-usage.md')

    total_runs = sum(d['usage']['run_count'] for d in repos_data if d['usage'])
    total_duration = sum(d['usage']['total_duration'] for d in repos_data if d['usage'])
    total_billable = sum(d['usage']['billable_duration'] for d in repos_data if d['usage'])
    total_cost = sum(d['usage']['estimated_cost'] for d in repos_data if d['usage'])

    with open(output_path, 'w') as f:
        f.write("# GitHub Actions Usage Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Period:** Last 30 days\n\n")

        f.write("---\n\n")
        f.write("## Summary\n\n")
        f.write(f"**Total Repositories:** {len(repos_data)}\n")
        f.write(f"**Total Workflow Runs:** {total_runs}\n")
        f.write(f"**Total Duration:** {total_duration:.1f} minutes\n")
        f.write(f"**Billable Duration:** {total_billable:.1f} minutes\n")
        f.write(f"**Estimated Cost:** ${total_cost:.2f}\n\n")

        # Free tier info
        free_minutes = 2000  # GitHub Free plan
        remaining = max(0, free_minutes - total_billable)
        f.write(f"**Free Tier:** 2,000 minutes/month\n")
        f.write(f"**Used:** {total_billable:.0f} minutes ({total_billable/free_minutes*100:.1f}%)\n")
        f.write(f"**Remaining:** {remaining:.0f} minutes\n\n")

        if total_billable > free_minutes:
            overage = total_billable - free_minutes
            overage_cost = overage * 0.008
            f.write(f"⚠️ **OVERAGE:** {overage:.0f} minutes (${overage_cost:.2f})\n\n")

        f.write("---\n\n")
        f.write("## Repository Breakdown\n\n")
        f.write("| Repository | Runs | Duration (min) | Billable (min) | Est. Cost |\n")
        f.write("|------------|------|----------------|----------------|----------|\n")

        # Sort by cost descending
        sorted_repos = sorted(
            [d for d in repos_data if d['usage']],
            key=lambda x: x['usage']['estimated_cost'],
            reverse=True
        )

        for repo_data in sorted_repos:
            repo = repo_data['repo']
            usage = repo_data['usage']

            f.write(f"| {repo['full_name']} | {usage['run_count']} | "
                   f"{usage['total_duration']:.1f} | {usage['billable_duration']:.1f} | "
                   f"${usage['estimated_cost']:.2f} |\n")

        f.write("\n---\n\n")
        f.write("## Cost Optimization Tips\n\n")

        if total_cost > 5:
            f.write("### High Usage Detected\n\n")
            f.write("Your Actions usage is generating significant costs. Consider:\n\n")
            f.write("1. **Reduce workflow frequency** - Run less often or on specific events\n")
            f.write("2. **Use self-hosted runners** - Free for private repos\n")
            f.write("3. **Optimize workflow duration** - Cache dependencies, parallelize jobs\n")
            f.write("4. **Remove unused workflows** - Delete .github/workflows files not in use\n\n")
        else:
            f.write("✅ Your usage is within reasonable limits.\n\n")

        f.write("### General Best Practices\n\n")
        f.write("- Use workflow caching to speed up builds\n")
        f.write("- Run workflows only on relevant branches\n")
        f.write("- Cancel redundant runs automatically\n")
        f.write("- Use self-hosted runners for private repos with high usage\n\n")

        f.write("---\n\n")
        f.write("**Next Report:** Run this script weekly to track trends\n")
        f.write(f"**Script:** `python3 {__file__}`\n")

    return output_path

def main():
    print("🔍 GitHub Actions Cost Tracker")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Get GitHub token
    print("Step 1: Authenticating...")
    token = get_github_token()
    if not token:
        return
    print("✅ Authenticated\n")

    # Get repositories
    print("Step 2: Fetching repositories...")
    repos = get_user_repos(token)
    print(f"✅ Found {len(repos)} repositories\n")

    # Get Actions usage for each repo
    print("Step 3: Analyzing Actions usage...")
    repos_data = []

    for i, repo in enumerate(repos, 1):
        print(f"  [{i}/{len(repos)}] {repo['full_name']}...", end=' ')

        usage = get_actions_usage(token, repo['owner']['login'], repo['name'])

        if usage and usage['run_count'] > 0:
            print(f"✅ {usage['run_count']} runs, ${usage['estimated_cost']:.2f}")
            repos_data.append({'repo': repo, 'usage': usage})
        else:
            print("⊘ No usage")

    print(f"\n✅ Analyzed {len(repos_data)} repositories with Actions usage\n")

    # Generate report
    print("Step 4: Generating report...")
    output_path = generate_report(repos_data)
    print(f"✅ Report saved: {output_path}\n")

    # Display summary
    total_cost = sum(d['usage']['estimated_cost'] for d in repos_data)
    total_billable = sum(d['usage']['billable_duration'] for d in repos_data)

    print("📊 Summary:")
    print(f"   Billable Minutes: {total_billable:.0f}")
    print(f"   Estimated Cost: ${total_cost:.2f}")

    if total_billable > 2000:
        overage = total_billable - 2000
        print(f"   ⚠️ OVERAGE: {overage:.0f} minutes (${overage * 0.008:.2f})")
    else:
        remaining = 2000 - total_billable
        print(f"   ✅ Remaining free minutes: {remaining:.0f}")

    print("\n🎉 Complete!")

if __name__ == '__main__':
    main()
