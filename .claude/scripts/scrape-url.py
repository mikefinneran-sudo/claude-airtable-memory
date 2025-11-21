#!/usr/bin/env python3
"""
Simple web scraping utility using requests + BeautifulSoup
Can use Smartproxy for IP rotation if needed

Usage:
    python3 scrape-url.py <url>
    python3 scrape-url.py <url> --proxy  # Use Smartproxy
    python3 scrape-url.py <url> --js     # Use Playwright for JS-heavy sites
"""

import sys
import argparse
import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path

def scrape_simple(url, use_proxy=False):
    """Scrape using requests (fast, no JS support)"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    proxies = None
    if use_proxy:
        # Load from .env or environment
        proxy_user = os.getenv('SMARTPROXY_USERNAME', 'smart-apyzl0fyvpog')
        proxy_pass = os.getenv('SMARTPROXY_PASSWORD', 'jWCC4mR8S8LJiMyY')
        proxy_url = f'http://{proxy_user}:{proxy_pass}@gate.smartproxy.com:7000'
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }

    response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract useful content
    result = {
        'url': url,
        'title': soup.title.string if soup.title else 'No title',
        'text': soup.get_text(strip=True, separator='\n'),
        'links': [a.get('href') for a in soup.find_all('a', href=True)],
        'images': [img.get('src') for img in soup.find_all('img', src=True)],
    }

    return result

def scrape_js(url):
    """Scrape using Playwright (handles JavaScript)"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: Playwright not installed. Run: pip install playwright && playwright install")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')

        content = page.content()
        title = page.title()

        browser.close()

        soup = BeautifulSoup(content, 'html.parser')

        result = {
            'url': url,
            'title': title,
            'text': soup.get_text(strip=True, separator='\n'),
            'links': [a.get('href') for a in soup.find_all('a', href=True)],
            'images': [img.get('src') for img in soup.find_all('img', src=True)],
        }

        return result

def main():
    parser = argparse.ArgumentParser(description='Scrape a URL and extract content')
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('--proxy', action='store_true', help='Use Smartproxy for IP rotation')
    parser.add_argument('--js', action='store_true', help='Use Playwright for JavaScript-heavy sites')
    parser.add_argument('--output', '-o', help='Save to file (optional)')

    args = parser.parse_args()

    try:
        if args.js:
            print(f"Scraping {args.url} with Playwright (JS support)...")
            result = scrape_js(args.url)
        else:
            print(f"Scraping {args.url} with requests...")
            result = scrape_simple(args.url, use_proxy=args.proxy)

        # Print results
        print(f"\nTitle: {result['title']}")
        print(f"\nLinks found: {len(result['links'])}")
        print(f"Images found: {len(result['images'])}")
        print(f"\nContent preview (first 500 chars):")
        print(result['text'][:500])

        if args.output:
            with open(args.output, 'w') as f:
                f.write(f"URL: {result['url']}\n")
                f.write(f"Title: {result['title']}\n\n")
                f.write(result['text'])
            print(f"\nFull content saved to: {args.output}")

        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
