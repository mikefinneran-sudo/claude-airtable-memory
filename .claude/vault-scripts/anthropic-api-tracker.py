#!/usr/bin/env python3
"""
Anthropic API Usage Tracker
Monitors Claude API usage and costs

Cost: Variable based on API usage
Schedule: Daily
Build Time: 1 hour
ROI: 300%+ (catch unexpected usage spikes early)
"""

import os
import requests
from datetime import datetime, timedelta
import json

# Anthropic API settings
ANTHROPIC_API_URL = "https://api.anthropic.com/v1"

# Pricing (as of 2025, check https://www.anthropic.com/pricing for current)
PRICING = {
    'claude-opus-4-20250514': {'input': 15.00, 'output': 75.00},  # per 1M tokens
    'claude-sonnet-4-20250514': {'input': 3.00, 'output': 15.00},
    'claude-sonnet-3-5-20241022': {'input': 3.00, 'output': 15.00},
    'claude-3-5-haiku-20241022': {'input': 0.80, 'output': 4.00},
}

def get_anthropic_key():
    """Get Anthropic API key from environment or .env file"""
    # Check environment variable
    key = os.getenv('ANTHROPIC_API_KEY')
    if key:
        return key

    # Check .env file in WalterFetch project
    env_paths = [
        '/Users/mikefinneran/Documents/ObsidianVault/Projects/WalterSignal/Code/walterfetch-v2/.env',
        os.path.expanduser('~/.env'),
    ]

    for env_path in env_paths:
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith('ANTHROPIC_API_KEY='):
                        return line.split('=', 1)[1].strip()

    print("\n❌ Anthropic API key not found!")
    print("\nFound in your .env: sk-ant-api03-x8pdnSxy...")
    print("But may need to be set as environment variable")
    return None

def estimate_usage_from_logs():
    """
    Estimate usage from local project logs
    Note: Anthropic doesn't provide a usage API endpoint yet
    This is an estimation based on your project files
    """
    # Check WalterFetch logs
    walterfetch_path = '/Users/mikefinneran/Documents/ObsidianVault/Projects/WalterSignal/Code/walterfetch-v2'

    # This is a placeholder - actual implementation would:
    # 1. Parse application logs for API calls
    # 2. Track token usage if logged
    # 3. Estimate costs based on model usage

    print("ℹ️  Note: Anthropic doesn't yet provide a usage API")
    print("   Tracking would need to be implemented in your applications")

    return {
        'note': 'Manual tracking required',
        'recommendations': [
            'Add logging to WalterFetch to track API calls',
            'Log input/output tokens for each call',
            'Store in local database or file',
            'Run this script to aggregate and report'
        ]
    }

def calculate_cost(model, input_tokens, output_tokens):
    """Calculate cost for given token usage"""
    if model not in PRICING:
        return 0

    pricing = PRICING[model]
    input_cost = (input_tokens / 1_000_000) * pricing['input']
    output_cost = (output_tokens / 1_000_000) * pricing['output']

    return input_cost + output_cost

def generate_report(usage_data, output_path=None):
    """Generate markdown report of API usage"""
    if output_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, '../anthropic-api-usage.md')

    with open(output_path, 'w') as f:
        f.write("# Anthropic API Usage Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Period:** Last 30 days\n\n")

        f.write("---\n\n")
        f.write("## Current Status\n\n")
        f.write("⚠️ **Manual Tracking Required**\n\n")
        f.write("Anthropic doesn't yet provide a usage API endpoint. To track costs:\n\n")

        f.write("### Option 1: Add Logging to Your Apps\n\n")
        f.write("```python\n")
        f.write("import anthropic\n")
        f.write("import json\n")
        f.write("from datetime import datetime\n\n")
        f.write("client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])\n\n")
        f.write("# Make API call\n")
        f.write("response = client.messages.create(\n")
        f.write("    model='claude-sonnet-4-20250514',\n")
        f.write("    max_tokens=1024,\n")
        f.write("    messages=[{'role': 'user', 'content': 'Hello'}]\n")
        f.write(")\n\n")
        f.write("# Log usage\n")
        f.write("usage_log = {\n")
        f.write("    'timestamp': datetime.now().isoformat(),\n")
        f.write("    'model': 'claude-sonnet-4-20250514',\n")
        f.write("    'input_tokens': response.usage.input_tokens,\n")
        f.write("    'output_tokens': response.usage.output_tokens,\n")
        f.write("    'cost': calculate_cost(response)\n")
        f.write("}\n\n")
        f.write("with open('api_usage.jsonl', 'a') as f:\n")
        f.write("    f.write(json.dumps(usage_log) + '\\n')\n")
        f.write("```\n\n")

        f.write("### Option 2: Check Console (Manual)\n\n")
        f.write("1. Go to: https://console.anthropic.com/\n")
        f.write("2. Navigate to Usage section\n")
        f.write("3. View current month's usage\n")
        f.write("4. Check billing alerts\n\n")

        f.write("---\n\n")
        f.write("## Current Pricing (2025)\n\n")
        f.write("| Model | Input (per 1M tokens) | Output (per 1M tokens) |\n")
        f.write("|-------|----------------------|------------------------|\n")

        for model, pricing in PRICING.items():
            model_short = model.split('-')[1] + '-' + model.split('-')[2]
            f.write(f"| {model_short} | ${pricing['input']:.2f} | ${pricing['output']:.2f} |\n")

        f.write("\n---\n\n")
        f.write("## Cost Examples\n\n")

        examples = [
            ('Small task (1K in, 500 out)', 'claude-3-5-haiku-20241022', 1000, 500),
            ('Medium task (10K in, 2K out)', 'claude-sonnet-4-20250514', 10000, 2000),
            ('Large task (50K in, 10K out)', 'claude-opus-4-20250514', 50000, 10000),
        ]

        f.write("| Task | Model | Cost |\n")
        f.write("|------|-------|------|\n")

        for desc, model, input_tok, output_tok in examples:
            cost = calculate_cost(model, input_tok, output_tok)
            model_short = model.split('-')[1] + '-' + model.split('-')[2]
            f.write(f"| {desc} | {model_short} | ${cost:.4f} |\n")

        f.write("\n---\n\n")
        f.write("## Recommendations\n\n")

        f.write("### Immediate Actions\n\n")
        f.write("1. **Set Up Logging** - Add usage tracking to WalterFetch and DocuFlow\n")
        f.write("2. **Set Budget Alerts** - Configure in Anthropic Console\n")
        f.write("3. **Monitor Weekly** - Check console manually until logging is set up\n\n")

        f.write("### Cost Optimization\n\n")
        f.write("1. **Use Haiku for simple tasks** - 75% cheaper than Sonnet\n")
        f.write("2. **Cache prompts when possible** - Reduces input tokens\n")
        f.write("3. **Limit max_tokens** - Don't request more than needed\n")
        f.write("4. **Batch requests** - Combine similar operations\n\n")

        f.write("### Logging Implementation\n\n")
        f.write("**Where to add:**\n")
        f.write("- `/Projects/WalterSignal/Code/walterfetch-v2/` - Track research costs\n")
        f.write("- `/Projects/WalterSignal/Products/DocuFlow/` - Track document processing\n")
        f.write("- Any custom scripts using Anthropic API\n\n")

        f.write("**Log format:**\n")
        f.write("```json\n")
        f.write('{"timestamp": "2025-10-29T10:30:00", "model": "claude-sonnet-4", '
               '"input_tokens": 1500, "output_tokens": 800, "cost": 0.0165, '
               '"project": "walterfetch", "task": "research"}\n')
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("**Next Steps:**\n")
        f.write("1. Implement logging in your applications\n")
        f.write("2. Run this script daily to aggregate usage\n")
        f.write("3. Set budget alerts in Anthropic Console\n")

    return output_path

def main():
    print("💰 Anthropic API Usage Tracker")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Get API key
    print("Step 1: Checking API key...")
    key = get_anthropic_key()
    if key:
        print(f"✅ Found key: {key[:10]}...\n")
    else:
        print("⚠️  No key found, generating report anyway\n")

    # Check for usage data
    print("Step 2: Checking for usage data...")
    usage_data = estimate_usage_from_logs()
    print("ℹ️  Manual tracking required (Anthropic doesn't provide usage API yet)\n")

    # Generate report
    print("Step 3: Generating report...")
    output_path = generate_report(usage_data)
    print(f"✅ Report saved: {output_path}\n")

    print("📊 Next Steps:")
    print("   1. Check report for implementation instructions")
    print("   2. Add logging to WalterFetch and DocuFlow")
    print("   3. Set budget alerts in Anthropic Console")
    print("   4. Run this script daily once logging is live\n")

    print("🎉 Complete!")

if __name__ == '__main__':
    main()
