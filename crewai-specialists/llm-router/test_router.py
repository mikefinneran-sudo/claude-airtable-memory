"""
Test cases for CrewAI Intelligent LLM Router
Validates routing logic with diverse task types
"""

from router_flow import run_router

# Test cases organized by expected routing category
TEST_CASES = {
    "max_vision": [
        "Analyze this sales chart and extract quarterly revenue trends with exact numbers",
        "OCR this document and extract all text with proper formatting",
        "Analyze this complex diagram showing network architecture and explain each component"
    ],

    "fast_vision": [
        "What objects are in this image?",
        "Generate a brief caption for this photo",
        "Is there a person in this picture?"
    ],

    "max_reasoning": [
        "Prove that √2 is irrational using proof by contradiction",
        "Solve: If 3x + 7 = 22 and 2y - 5 = 13, what is x + y?",
        "Explain the halting problem and why it's undecidable"
    ],

    "max_reasoning_moe": [
        "Develop a formal proof for Gödel's incompleteness theorems",
        "Analyze the Nash equilibrium in a 3-player strategic game with complete information",
        "Derive the closed-form solution for the Black-Scholes PDE"
    ],

    "efficient_reasoning": [
        "What's the logical fallacy in: 'All birds can fly. Penguins are birds. Therefore penguins can fly.'",
        "If A implies B, and B implies C, does A imply C?",
        "Explain the birthday paradox in simple terms"
    ],

    "hybrid_reasoner": [
        "Look at this flowchart and determine the output if input is 5",
        "Analyze this geometry diagram and calculate the area of the shaded region",
        "This Venn diagram shows set relationships - what is A ∩ B ∪ C?"
    ],

    "max_rag": [
        "Search through these 500 research papers and find all citations related to 'quantum entanglement' with full bibliographic references",
        "Analyze these legal documents and extract all clauses related to intellectual property with citations",
        "Review this 1000-page technical manual and find all safety warnings with exact page numbers"
    ],

    "fast_rag": [
        "Search this PDF for mentions of 'machine learning'",
        "Find all references to 'revenue' in these financial documents",
        "What does this document say about climate change?"
    ],

    "agentic_tool_use": [
        "Call the weather API for San Francisco, then book a restaurant reservation if it's sunny",
        "Search the web for recent news about AI, then summarize the top 3 articles",
        "Check my calendar, find free slots next week, and send meeting invites"
    ],

    "structured_data": [
        "Generate a JSON schema for a user profile with fields: name, email, age, address",
        "Convert this text into structured JSON: John Doe, 30 years old, lives in NYC",
        "Create a Python dataclass for an e-commerce order with items, total, and shipping info"
    ],

    "simple_chat": [
        "What's 2+2?",
        "Tell me a joke",
        "What's the capital of France?"
    ],

    "instruction_following": [
        "Follow these steps exactly: 1) Uppercase the text 2) Remove vowels 3) Add '!' at the end. Text: hello",
        "Sort these numbers in ascending order then multiply each by 2: 5, 2, 8, 1, 9",
        "Read this sentence backwards and capitalize every 3rd letter: hello world"
    ],

    "long_context": [
        "Summarize this 100,000-word novel and identify recurring themes",
        "Analyze this 500-page legal contract for potential risks",
        "Compare these 10 research papers and identify common methodologies"
    ],

    "max_quality_general": [
        "Design a microservices architecture for an e-commerce platform with high availability and security",
        "Write production-ready Python code for a distributed task queue with Redis and Celery",
        "Explain quantum computing to a PhD physicist, including mathematical formulations"
    ],

    "default_general": [
        "Explain how photosynthesis works",
        "What are the benefits of exercise?",
        "How does the internet work?"
    ],

    "efficient_general": [
        "What's the difference between a list and a tuple in Python?",
        "Explain recursion in one sentence",
        "What is REST?"
    ],

    "korean_multilingual": [
        "한국어로 번역해주세요: Hello, how are you?",
        "Translate this Korean text to English: 안녕하세요",
        "Write a professional business email in Korean"
    ],

    "embeddings": [
        "Generate embeddings for: 'machine learning is a subset of artificial intelligence'",
        "Compare semantic similarity between these two sentences",
        "Create vector representations for RAG pipeline"
    ]
}


def run_all_tests(verbose=True):
    """
    Run all test cases and validate routing decisions

    Returns:
        dict: Test results with pass/fail for each category
    """
    results = {
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "by_category": {}
    }

    for expected_category, tasks in TEST_CASES.items():
        print(f"\n{'='*80}")
        print(f"TESTING CATEGORY: {expected_category}")
        print(f"{'='*80}")

        category_results = {
            "expected": expected_category,
            "tests": [],
            "accuracy": 0.0
        }

        for task in tasks:
            results["total_tests"] += 1

            print(f"\n📝 Task: {task[:80]}...")

            try:
                # Run router (suppress verbose output if not in verbose mode)
                result = run_router(task)

                actual_category = result["category"]
                selected_model = result["selected_model"]
                confidence = result.get("confidence", 0.0)

                # Check if routing matched expected category
                passed = (actual_category == expected_category)

                if passed:
                    results["passed"] += 1
                    status = "✅ PASS"
                else:
                    results["failed"] += 1
                    status = f"❌ FAIL (expected {expected_category}, got {actual_category})"

                print(f"\n{status}")
                print(f"   Model: {selected_model} | Confidence: {confidence:.2f}")

                category_results["tests"].append({
                    "task": task,
                    "expected": expected_category,
                    "actual": actual_category,
                    "model": selected_model,
                    "confidence": confidence,
                    "passed": passed
                })

            except Exception as e:
                results["failed"] += 1
                print(f"\n❌ ERROR: {e}")

                category_results["tests"].append({
                    "task": task,
                    "expected": expected_category,
                    "actual": None,
                    "model": None,
                    "confidence": 0.0,
                    "passed": False,
                    "error": str(e)
                })

        # Calculate category accuracy
        passed_in_category = sum(1 for t in category_results["tests"] if t["passed"])
        total_in_category = len(category_results["tests"])
        category_results["accuracy"] = passed_in_category / total_in_category if total_in_category > 0 else 0.0

        results["by_category"][expected_category] = category_results

        print(f"\n📊 Category Accuracy: {category_results['accuracy']:.1%} ({passed_in_category}/{total_in_category})")

    # Print final summary
    print(f"\n\n{'='*80}")
    print("FINAL TEST RESULTS")
    print(f"{'='*80}")
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']} ({results['passed']/results['total_tests']:.1%})")
    print(f"Failed: {results['failed']} ({results['failed']/results['total_tests']:.1%})")
    print(f"\nAccuracy by Category:")

    for category, data in results["by_category"].items():
        print(f"  {category:25s}: {data['accuracy']:>6.1%} ({sum(1 for t in data['tests'] if t['passed'])}/{len(data['tests'])})")

    return results


def run_quick_test():
    """
    Quick smoke test with one task per major category
    """
    quick_tests = {
        "simple_chat": "What's 2+2?",
        "max_reasoning": "Prove that the sum of two even numbers is always even",
        "structured_data": "Generate JSON for a user with name 'Alice' and age 30",
        "fast_vision": "Describe this image briefly",
        "max_rag": "Search 100 PDFs for 'quantum physics' with citations"
    }

    print("="*80)
    print("QUICK SMOKE TEST")
    print("="*80)

    for category, task in quick_tests.items():
        print(f"\n\n{'='*80}")
        print(f"Expected: {category} | Task: {task}")
        print("="*80)

        result = run_router(task)

        status = "✅" if result["category"] == category else "❌"
        print(f"\n{status} Routed to: {result['category']} ({result['selected_model']})")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        # Quick smoke test
        run_quick_test()
    else:
        # Full test suite
        results = run_all_tests(verbose=True)

        # Save results to JSON
        import json
        with open("test_results.json", "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n\n✅ Test results saved to test_results.json")
