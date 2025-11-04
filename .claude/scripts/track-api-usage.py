#!/usr/bin/env python3
"""
Track API Token Usage
Monitors Claude API, Perplexity, and other AI service usage
"""

import os
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict

# API Keys from environment
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

# Storage
USAGE_FILE = os.path.expanduser('~/.claude/.api-usage.json')

def get_anthropic_usage():
    """Get Claude API usage from Anthropic Console"""
    if not ANTHROPIC_API_KEY:
        return None

    try:
        # Note: Anthropic doesn't have a direct usage API yet
        # This is placeholder for when they add it
        # For now, track locally via session logs
        return {
            'provider': 'Anthropic',
            'model': 'claude-sonnet-4.5',
            'tokens_used': 0,  # Would come from API
            'cost': 0.0,
            'last_updated': datetime.now().isoformat()
        }
    except Exception as e:
        return {'error': str(e)}

def get_perplexity_usage():
    """Get Perplexity API usage"""
    if not PERPLEXITY_API_KEY:
        return None

    try:
        # Perplexity usage endpoint (if available)
        # Placeholder - check Perplexity docs for actual endpoint
        return {
            'provider': 'Perplexity',
            'queries_used': 0,
            'cost': 0.0,
            'last_updated': datetime.now().isoformat()
        }
    except Exception as e:
        return {'error': str(e)}

def track_session_usage():
    """Track usage from Claude Code session logs"""
    usage_data = {
        'sessions': [],
        'total_input_tokens': 0,
        'total_output_tokens': 0,
        'estimated_cost': 0.0,
        'last_updated': datetime.now().isoformat()
    }

    # Read session archive for token counts
    archive_dir = os.path.expanduser('~/.claude/session-archive')
    if not os.path.exists(archive_dir):
        return usage_data

    # Parse session files for token usage
    # (Claude Code session files contain token counts)
    try:
        for filename in os.listdir(archive_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(archive_dir, filename)
                with open(filepath, 'r') as f:
                    content = f.read()

                    # Extract token counts if present
                    # Format: "Token usage: 12345/200000"
                    if 'Token usage:' in content:
                        # Parse and accumulate
                        pass
    except Exception as e:
        usage_data['error'] = str(e)

    return usage_data

def load_usage_history():
    """Load historical usage data"""
    if not os.path.exists(USAGE_FILE):
        return {
            'daily': defaultdict(dict),
            'weekly': defaultdict(dict),
            'monthly': defaultdict(dict)
        }

    try:
        with open(USAGE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {
            'daily': {},
            'weekly': {},
            'monthly': {}
        }

def save_usage_history(data):
    """Save usage history"""
    with open(USAGE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def update_usage():
    """Update all usage metrics"""
    history = load_usage_history()

    today = datetime.now().strftime('%Y-%m-%d')

    # Get current usage
    anthropic = get_anthropic_usage()
    perplexity = get_perplexity_usage()
    session = track_session_usage()

    # Update daily stats
    if isinstance(history['daily'], dict):
        history['daily'][today] = {
            'anthropic': anthropic,
            'perplexity': perplexity,
            'session': session,
            'timestamp': datetime.now().isoformat()
        }

    save_usage_history(history)

    return history

def get_current_usage():
    """Get current usage summary"""
    history = load_usage_history()

    today = datetime.now().strftime('%Y-%m-%d')

    if isinstance(history['daily'], dict) and today in history['daily']:
        return history['daily'][today]

    return {
        'anthropic': None,
        'perplexity': None,
        'session': None
    }

def estimate_costs(tokens_in, tokens_out, model='claude-sonnet-4.5'):
    """Estimate API costs"""
    # Pricing per 1M tokens (as of Nov 2025)
    pricing = {
        'claude-sonnet-4.5': {'input': 3.00, 'output': 15.00},
        'claude-opus-4': {'input': 15.00, 'output': 75.00},
        'claude-haiku-4': {'input': 0.40, 'output': 2.00}
    }

    rates = pricing.get(model, pricing['claude-sonnet-4.5'])

    cost_input = (tokens_in / 1_000_000) * rates['input']
    cost_output = (tokens_out / 1_000_000) * rates['output']

    return cost_input + cost_output

if __name__ == '__main__':
    print("📊 API Usage Tracker")
    print("")

    usage = update_usage()
    current = get_current_usage()

    print("Current Usage:")
    print(json.dumps(current, indent=2))
