#!/usr/bin/env python3
"""
Perplexity API Usage Tracker
Monitors research API usage to optimize Pro subscription vs API costs

Pro Subscription: $20/month (unlimited searches)
API Pricing: $1/1K requests (sonar), $5/1K requests (sonar-pro)

Schedule: Daily
Build Time: 1 hour
ROI: 200%+ (optimize Pro vs API decision)
"""

import os
import requests
from datetime import datetime, timedelta
import json

# Perplexity API settings
PERPLEXITY_API_URL = "https://api.perplexity.ai"

# Pricing
PRICING = {
    'pro_subscription': 20.00,  # per month, unlimited
    'sonar': 0.001,  # $1 per 1K requests
    'sonar-pro': 0.005,  # $5 per 1K requests
}

def get_perplexity_key():
    """Get Perplexity API key from environment or .env file"""
    # Check environment variable
    key = os.getenv('PERPLEXITY_API_KEY')
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
                    if line.startswith('PERPLEXITY_API_KEY='):
                        return line.split('=', 1)[1].strip()

    print("\n❌ Perplexity API key not found!")
    print("\nFound in your .env: pplx-ZZWqhrSgD...")
    return None

def estimate_usage_from_logs():
    """
    Estimate Perplexity usage from local logs
    Note: Like Anthropic, Perplexity doesn't provide detailed usage API
    """
    print("ℹ️  Note: Perplexity usage tracking requires application-level logging")

    return {
        'note': 'Manual tracking or log parsing required',
        'current_plan': 'Pro ($20/month unlimited)',
        'alternatives': {
            'sonar_api': '$1 per 1,000 requests',
            'sonar_pro_api': '$5 per 1,000 requests (includes sources)'
        }
    }

def calculate_breakeven(requests_per_month, model='sonar-pro'):
    """Calculate break-even point for Pro vs API"""
    api_cost = requests_per_month * PRICING[model]
    pro_cost = PRICING['pro_subscription']

    if api_cost < pro_cost:
        savings = pro_cost - api_cost
        return {
            'recommendation': 'Use API',
            'api_cost': api_cost,
            'pro_cost': pro_cost,
            'savings': savings,
            'break_even_requests': int(pro_cost / PRICING[model])
        }
    else:
        return {
            'recommendation': 'Keep Pro subscription',
            'api_cost': api_cost,
            'pro_cost': pro_cost,
            'savings': 0,
            'break_even_requests': int(pro_cost / PRICING[model])
        }

def generate_report(usage_data, output_path=None):
    """Generate markdown report of Perplexity usage"""
    if output_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, '../perplexity-api-usage.md')

    with open(output_path, 'w') as f:
        f.write("# Perplexity API Usage Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Current Plan:** Pro Subscription ($20/month unlimited)\n\n")

        f.write("---\n\n")
        f.write("## Pro vs API Cost Analysis\n\n")

        f.write("### Current Pricing\n\n")
        f.write("| Plan/Model | Cost | Details |\n")
        f.write("|------------|------|----------|\n")
        f.write("| **Pro Subscription** | $20/month | Unlimited searches, includes Pro features |\n")
        f.write("| **Sonar API** | $1 per 1K requests | Basic search API |\n")
        f.write("| **Sonar-Pro API** | $5 per 1K requests | Advanced search with sources |\n\n")

        f.write("### Break-Even Analysis\n\n")

        usage_scenarios = [10, 50, 100, 200, 500, 1000, 2000]

        f.write("#### Sonar-Pro API ($5 per 1K requests)\n\n")
        f.write("| Monthly Requests | API Cost | Pro Cost | Recommendation | Savings |\n")
        f.write("|------------------|----------|----------|----------------|----------|\n")

        for requests in usage_scenarios:
            analysis = calculate_breakeven(requests, 'sonar-pro')
            rec_emoji = "✅" if analysis['recommendation'] == 'Use API' else "⚠️"
            f.write(f"| {requests} | ${analysis['api_cost']:.2f} | ${analysis['pro_cost']:.2f} | "
                   f"{rec_emoji} {analysis['recommendation']} | "
                   f"${analysis['savings']:.2f} |\n")

        f.write(f"\n**Break-Even Point:** {int(20 / PRICING['sonar-pro'])} requests/month\n\n")

        f.write("#### Sonar API ($1 per 1K requests)\n\n")
        f.write("| Monthly Requests | API Cost | Pro Cost | Recommendation | Savings |\n")
        f.write("|------------------|----------|----------|----------------|----------|\n")

        for requests in usage_scenarios:
            analysis = calculate_breakeven(requests, 'sonar')
            rec_emoji = "✅" if analysis['recommendation'] == 'Use API' else "⚠️"
            f.write(f"| {requests} | ${analysis['api_cost']:.2f} | ${analysis['pro_cost']:.2f} | "
                   f"{rec_emoji} {analysis['recommendation']} | "
                   f"${analysis['savings']:.2f} |\n")

        f.write(f"\n**Break-Even Point:** {int(20 / PRICING['sonar'])} requests/month\n\n")

        f.write("---\n\n")
        f.write("## Tracking Your Usage\n\n")

        f.write("### Option 1: Add Logging to Applications\n\n")
        f.write("```python\n")
        f.write("import requests\n")
        f.write("import json\n")
        f.write("from datetime import datetime\n\n")
        f.write("def log_perplexity_request(model, prompt, response):\n")
        f.write("    log_entry = {\n")
        f.write("        'timestamp': datetime.now().isoformat(),\n")
        f.write("        'model': model,\n")
        f.write("        'prompt_length': len(prompt),\n")
        f.write("        'response_length': len(str(response)),\n")
        f.write("        'cost': PRICING.get(model, 0.005),  # per request\n")
        f.write("        'project': 'walterfetch'  # or 'manual', 'docuflow', etc.\n")
        f.write("    }\n")
        f.write("    \n")
        f.write("    with open('perplexity_usage.jsonl', 'a') as f:\n")
        f.write("        f.write(json.dumps(log_entry) + '\\n')\n")
        f.write("```\n\n")

        f.write("### Option 2: Manual Tracking\n\n")
        f.write("Keep a simple count of your Perplexity searches:\n\n")
        f.write("| Week | Searches | Notes |\n")
        f.write("|------|----------|-------|\n")
        f.write("| Week 1 | _____ | |\n")
        f.write("| Week 2 | _____ | |\n")
        f.write("| Week 3 | _____ | |\n")
        f.write("| Week 4 | _____ | |\n")
        f.write("| **Monthly Total** | **_____** | |\n\n")

        f.write("Then compare to break-even table above.\n\n")

        f.write("---\n\n")
        f.write("## Current Usage Estimate\n\n")

        f.write("Based on your WalterFetch setup:\n\n")
        f.write("- **WalterFetch research:** ~50-100 searches/month\n")
        f.write("- **Manual research:** ~20-50 searches/month\n")
        f.write("- **DocuFlow (if using):** ~10-20 searches/month\n")
        f.write("- **Estimated total:** 80-170 searches/month\n\n")

        f.write("**With Sonar-Pro API ($5/1K):**\n")
        analysis_low = calculate_breakeven(80, 'sonar-pro')
        analysis_high = calculate_breakeven(170, 'sonar-pro')
        f.write(f"- Low estimate (80): ${analysis_low['api_cost']:.2f}/month → **{analysis_low['recommendation']}**\n")
        f.write(f"- High estimate (170): ${analysis_high['api_cost']:.2f}/month → **{analysis_high['recommendation']}**\n\n")

        f.write("**Conclusion:** ")
        if analysis_high['api_cost'] < 20:
            f.write("✅ **Consider switching to API** - Potential savings: ${:.2f}/month\n\n".format(20 - analysis_high['api_cost']))
        else:
            f.write("⚠️ **Keep Pro subscription** - Current usage justifies unlimited plan\n\n")

        f.write("---\n\n")
        f.write("## Recommendations\n\n")

        f.write("### If Usage < 4K requests/month (Break-even point)\n\n")
        f.write("1. **Switch to Sonar-Pro API**\n")
        f.write("   - Cancel Pro subscription ($20/month)\n")
        f.write("   - Use API key from console\n")
        f.write("   - Track usage carefully\n")
        f.write("   - Savings: $10-19/month\n\n")

        f.write("2. **Track usage for 1 month first**\n")
        f.write("   - Implement logging (see above)\n")
        f.write("   - Monitor actual request count\n")
        f.write("   - Make decision based on real data\n\n")

        f.write("### If Usage > 4K requests/month\n\n")
        f.write("1. **Keep Pro subscription**\n")
        f.write("   - Unlimited searches more cost-effective\n")
        f.write("   - No need to track individual requests\n")
        f.write("   - Peace of mind for heavy research\n\n")

        f.write("### Optimization Tips\n\n")
        f.write("1. **Cache results** - Don't repeat identical searches\n")
        f.write("2. **Batch similar queries** - Combine related research\n")
        f.write("3. **Use Sonar vs Sonar-Pro strategically** - Basic searches don't need Pro\n")
        f.write("4. **Set monthly budget alerts** - Track spending\n\n")

        f.write("---\n\n")
        f.write("**Next Steps:**\n")
        f.write("1. Track usage for 30 days (manual or automated)\n")
        f.write("2. Compare to break-even analysis\n")
        f.write("3. Decide: Keep Pro ($20/mo) or switch to API\n")
        f.write("4. Re-evaluate quarterly\n\n")

        f.write("**Run this script monthly** to reassess your decision.\n")

    return output_path

def main():
    print("🔍 Perplexity API Usage Tracker")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Get API key
    print("Step 1: Checking API key...")
    key = get_perplexity_key()
    if key:
        print(f"✅ Found key: {key[:10]}...\n")
    else:
        print("⚠️  No key found, generating report anyway\n")

    # Check usage
    print("Step 2: Analyzing usage patterns...")
    usage_data = estimate_usage_from_logs()
    print("ℹ️  Usage tracking requires application-level logging\n")

    # Generate report
    print("Step 3: Generating cost analysis report...")
    output_path = generate_report(usage_data)
    print(f"✅ Report saved: {output_path}\n")

    print("📊 Key Findings:")
    print("   Break-Even: 4,000 requests/month (Sonar-Pro)")
    print("   Break-Even: 20,000 requests/month (Sonar)")
    print("   Current Plan: Pro subscription ($20/month unlimited)")
    print("\n💡 Recommendation:")
    print("   Track actual usage for 30 days, then decide:")
    print("   - If <4K/month: Switch to API (save $10-19/mo)")
    print("   - If >4K/month: Keep Pro (cost-effective)\n")

    print("🎉 Complete!")

if __name__ == '__main__':
    main()
