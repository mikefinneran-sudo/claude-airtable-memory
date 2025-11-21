#!/usr/bin/env python3
"""
Simple CLI wrapper for the hybrid LLM router
Usage: python route_task.py "Your task here"
"""

import sys
from router_flow import run_router

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python route_task.py 'Your task here'")
        sys.exit(1)

    task = " ".join(sys.argv[1:])

    print(f"\n🚀 Routing task to hybrid LLM fleet...")
    print(f"📝 Task: {task}\n")

    result = run_router(task)

    print(f"\n{'='*80}")
    print("✅ RESULT")
    print('='*80)
    print(f"\n📊 Category: {result.get('category', 'N/A')}")
    print(f"🤖 Model: {result.get('selected_model', 'N/A')}")
    print(f"📍 Type: {'LOCAL (FREE)' if result.get('is_local') else 'COMMERCIAL (PAID)'}")
    print(f"💰 Cost: ${result.get('cost_usd', 0):.6f}")
    print(f"\n📄 Output:\n{result.get('result', 'No result')}\n")
