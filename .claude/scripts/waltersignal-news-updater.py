#!/usr/bin/env python3
"""
WalterSignal News Updater
Fetches top 5 daily AI/GTM news stories and publishes to waltersignal.io/news.html

Search: SearXNG on DGX (primary) → Perplexity API (fallback)
Summarize: Ollama on DGX (primary) → Perplexity API (fallback)
Storage: SQLite (~/Code/WalterSignal/walterfetch-v2/data/news.db)
Deploy: SCP to Lightsail server

Runs daily at 12:30 AM via LaunchAgent
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

# Add walterfetch-v2 to path for news_database module
WALTERFETCH_DIR = Path.home() / "Code" / "WalterSignal" / "walterfetch-v2"
sys.path.insert(0, str(WALTERFETCH_DIR))

from modules.news_database import NewsDatabase

# Configuration
LIGHTSAIL_HOST = "ubuntu@98.89.88.138"
LIGHTSAIL_KEY = os.path.expanduser("~/.ssh/command-center-key.pem")
DEPLOY_PATH = "/var/www/html/api/news.json"

# DGX endpoints
DGX_HOST = os.getenv("DGX_HOST", "192.168.68.62")
SEARXNG_URL = f"http://{DGX_HOST}:8890"
OLLAMA_URL = f"http://{DGX_HOST}:11434"
OLLAMA_MODEL = os.getenv("OLLAMA_SUMMARIZE_MODEL", "qwen3:14b")

CATEGORIES = [
    "AI Training",
    "Web Scraping",
    "GTM Agencies",
    "Cold Email",
    "Clay Automation"
]

SEARCH_QUERIES = [
    "AI model training breakthroughs releases 2026",
    "B2B sales automation GTM tools news",
    "web scraping technology updates",
    "cold email deliverability strategy news",
    "Clay automation outbound sales tools",
]


def get_api_key(key_name: str, op_path: str) -> Optional[str]:
    """Get API key from environment or 1Password."""
    key = os.environ.get(key_name)
    if key:
        return key
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/op", "read", op_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"[ERROR] Failed to get {key_name}: {e}")
    return None


def _searxng_available() -> bool:
    """Check if SearXNG is reachable."""
    try:
        r = requests.get(f"{SEARXNG_URL}/healthz", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def _ollama_available() -> bool:
    """Check if Ollama is reachable."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def search_searxng() -> list[dict]:
    """Search for news using SearXNG on DGX."""
    print("\n[SEARCH] Using SearXNG (local)...")
    all_results = []

    for query in SEARCH_QUERIES:
        try:
            r = requests.get(
                f"{SEARXNG_URL}/search",
                params={"q": query, "format": "json", "categories": "news", "time_range": "day"},
                timeout=15
            )
            r.raise_for_status()
            results = r.json().get("results", [])
            all_results.extend(results[:5])
            print(f"  [{len(results)} results] {query[:50]}")
        except Exception as e:
            print(f"  [ERROR] {query[:40]}: {e}")

    # Deduplicate by URL
    seen_urls = set()
    unique = []
    for r in all_results:
        url = r.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(r)

    print(f"[OK] {len(unique)} unique results from SearXNG")
    return unique[:25]  # Cap at 25 for summarization


def summarize_with_ollama(search_results: list[dict]) -> list[dict]:
    """Use Ollama to pick top 5 and summarize search results."""
    print(f"\n[SUMMARIZE] Using Ollama ({OLLAMA_MODEL})...")

    # Build context from search results
    context_lines = []
    for i, r in enumerate(search_results, 1):
        title = r.get("title", "No title")
        content = r.get("content", "")[:300]
        url = r.get("url", "")
        context_lines.append(f"{i}. [{title}] {content} (URL: {url})")

    context = "\n".join(context_lines)
    categories_str = ", ".join(CATEGORIES)

    prompt = f"""You are a news editor for an AI consulting firm. From the search results below, select the 5 most important and newsworthy stories.

For each story, provide:
- title: A clear, specific headline
- summary: 2-3 sentences explaining significance for AI/sales professionals
- category: One of: {categories_str}
- source_url: The article URL from the search results

Search Results:
{context}

Return ONLY a JSON array with exactly 5 items:
[{{"title": "...", "summary": "...", "category": "...", "source_url": "..."}}]"""

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=120
        )
        r.raise_for_status()
        response_text = r.json().get("response", "")

        # Extract JSON array
        start = response_text.find("[")
        end = response_text.rfind("]") + 1
        if start >= 0 and end > start:
            articles = json.loads(response_text[start:end])
            print(f"[OK] Ollama selected {len(articles)} articles")
            return articles[:5]
        else:
            print("[ERROR] Could not parse JSON from Ollama response")
            return []
    except Exception as e:
        print(f"[ERROR] Ollama summarization failed: {e}")
        return []


def search_news_perplexity(perplexity_key: str) -> list[dict]:
    """Fallback: Search for news using Perplexity API."""
    print("\n[SEARCH] Falling back to Perplexity API...")

    prompt = f"""Find the 5 most important and newsworthy stories from today or yesterday about:
- AI model training breakthroughs or releases
- B2B sales automation and GTM tools
- Web scraping technology updates
- Cold email deliverability or strategy
- Clay.com or similar automation platforms

For each story, provide:
1. Title (clear, specific headline)
2. Summary (2-3 sentences explaining significance)
3. Category (one of: AI Training, Web Scraping, GTM Agencies, Cold Email, Clay Automation)
4. Source URL (actual article link)

Return as JSON array:
[{{"title": "...", "summary": "...", "category": "...", "source_url": "..."}}]

Only include stories from the last 48 hours. Be specific and factual."""

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {perplexity_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "sonar",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1
            },
            timeout=60
        )
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]

        start = content.find("[")
        end = content.rfind("]") + 1
        if start >= 0 and end > start:
            articles = json.loads(content[start:end])
            print(f"[OK] Found {len(articles)} articles via Perplexity")
            return articles[:5]
        else:
            print("[ERROR] Could not parse JSON from Perplexity response")
            return []

    except Exception as e:
        print(f"[ERROR] Perplexity search failed: {e}")
        return []


def search_news() -> list[dict]:
    """Search for news — SearXNG+Ollama first, Perplexity fallback."""
    if _searxng_available() and _ollama_available():
        results = search_searxng()
        if results:
            articles = summarize_with_ollama(results)
            if articles:
                return articles
        print("[WARN] SearXNG+Ollama produced no results")

    # Fallback to Perplexity
    perplexity_key = get_api_key(
        "PERPLEXITY_API_KEY",
        "op://API_Keys/Perplexity Pro API/credential"
    )
    if perplexity_key:
        return search_news_perplexity(perplexity_key)

    print("[FATAL] Both SearXNG and Perplexity unavailable")
    return []


def add_to_database(db: NewsDatabase, articles: list[dict]) -> int:
    """Add articles to SQLite database, skip duplicates."""
    print("\n[DATABASE] Adding articles...")

    added = 0
    today = datetime.now().strftime("%Y-%m-%d")

    for article in articles:
        title = article.get("title", "").strip()
        if not title:
            continue

        if db.title_exists(title):
            print(f"[SKIP] Already exists: {title[:50]}...")
            continue

        # Validate category
        category = article.get("category", "Industry News")
        if category not in CATEGORIES:
            category = "Industry News"

        success = db.add_article(
            title=title,
            summary=article.get("summary", ""),
            category=category,
            source_url=article.get("source_url", ""),
            date=today,
        )

        if success:
            print(f"[OK] Added: {title[:50]}...")
            added += 1

    print(f"[SUMMARY] Added {added} new articles")
    return added


def export_to_json(db: NewsDatabase) -> Optional[str]:
    """Export all published articles to JSON."""
    print("\n[EXPORT] Generating JSON from database...")

    try:
        json_content = db.export_json()
        records = json.loads(json_content)
        print(f"[OK] {len(records.get('records', []))} published articles")
        return json_content
    except Exception as e:
        print(f"[ERROR] Export failed: {e}")
        return None


def deploy_to_server(json_content: str) -> bool:
    """Deploy news.json to Lightsail server."""
    print("\n[DEPLOY] Uploading to server...")

    tmp_file = "/tmp/news.json"
    with open(tmp_file, "w") as f:
        f.write(json_content)

    try:
        subprocess.run([
            "scp", "-i", LIGHTSAIL_KEY, "-o", "StrictHostKeyChecking=no",
            tmp_file, f"{LIGHTSAIL_HOST}:/tmp/news.json"
        ], check=True, capture_output=True, timeout=30)

        subprocess.run([
            "ssh", "-i", LIGHTSAIL_KEY, "-o", "StrictHostKeyChecking=no",
            LIGHTSAIL_HOST, f"sudo cp /tmp/news.json {DEPLOY_PATH}"
        ], check=True, capture_output=True, timeout=30)

        print("[OK] Deployed news.json to server")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Deploy failed: {e.stderr.decode() if e.stderr else e}")
        return False
    finally:
        os.remove(tmp_file)


def main():
    print("=" * 60)
    print(f"WalterSignal News Updater - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Initialize SQLite database
    db = NewsDatabase()

    try:
        articles = search_news()

        if articles:
            add_to_database(db, articles)
        else:
            print("[WARN] No new articles found")

        # Export and deploy
        json_content = export_to_json(db)
        if json_content:
            deploy_to_server(json_content)
    finally:
        db.close()

    print("\n" + "=" * 60)
    print("Update complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
