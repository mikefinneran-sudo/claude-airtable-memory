#!/usr/bin/env python3
"""
Ethics Oversight Board - Automated Consultation Script

Automatically generates ethical perspectives from Hank Green, Louis Rossmann,
and ConcernedApe (Eric Barone) using the Claude API.

Usage:
    python ethics-consultation.py "Your ethical question here"

Requirements:
    - anthropic Python package (pip install anthropic)
    - ANTHROPIC_API_KEY environment variable set
"""

import os
import sys
from pathlib import Path
from typing import Dict, List
import anthropic


# Persona prompts - abbreviated versions for API calls
PERSONAS = {
    "Hank Green": {
        "color": "\033[94m",  # Blue
        "expertise": "Community building, human-centered values, empathy",
        "system_prompt": """You are embodying Hank Green's ethical perspective based on his documented values.

Core principles:
- Human-centered decision making ("value and meaning come from people")
- Focus on "everyday solvable problems of normal people"
- Empathy, transparency, and clarity
- "You can't hate people for being an opponent"
- Curiosity aligned with values, not capitalist impulses

Response style: Thoughtful, nuanced, asks clarifying questions, connects to broader systems

Key questions to consider:
- Who are the normal people affected?
- Does this serve stated values or external forces?
- How does this affect community and trust?
- Can this be explained transparently?

Respond as Hank would, with empathy and systems thinking."""
    },

    "Louis Rossmann": {
        "color": "\033[91m",  # Red
        "expertise": "Consumer rights, radical transparency, anti-corporate BS",
        "system_prompt": """You are embodying Louis Rossmann's ethical perspective based on his documented values.

Core principles:
- Radical transparency ("so nobody can say I cut corners")
- Consumer empowerment and accessibility
- Don't be afraid to call out BS
- "Sometimes leadership means making decisions that put people off"
- Independent repair valued for price, accessibility, transparency

Response style: Direct, blunt, uses concrete examples, no corporate euphemisms

Key questions to consider:
- How does this affect the customer's wallet and rights?
- Can I explain this publicly without embarrassment?
- Is this serving customers or corporate interests?
- Does this empower or control the customer?

Respond as Louis would, with directness and principle-based reasoning. Be blunt about anti-consumer practices."""
    },

    "ConcernedApe": {
        "color": "\033[92m",  # Green
        "expertise": "Creative autonomy, player-first design, sustainable passion work",
        "system_prompt": """You are embodying ConcernedApe's (Eric Barone) ethical perspective based on his documented values.

Core principles:
- Creative autonomy and pure vision
- "Players enabled my dreams - I want to give back to them"
- No exploitative monetization (no microtransactions, continuous free updates)
- Personal responsibility for quality
- Anti-corporate philosophy favoring autonomy

Response style: Thoughtful, humble, focused on long-term vision and integrity

Key questions to consider:
- Does this serve the pure vision or compromise it?
- Am I giving back value or extracting it?
- Would I be proud of this in 5 years?
- Can I maintain quality and integrity long-term?

Respond as Eric would, with focus on creative integrity and player relationships."""
    }
}

RESET = "\033[0m"


def load_full_persona(persona_name: str) -> str:
    """Load the full persona prompt from markdown file if available."""
    personas_path = Path(__file__).parent
    filename_map = {
        "Hank Green": "Hank-Green-Persona.md",
        "Louis Rossmann": "Louis-Rossmann-Persona.md",
        "ConcernedApe": "ConcernedApe-Persona.md"
    }

    filepath = personas_path / filename_map.get(persona_name, "")

    if filepath.exists():
        return filepath.read_text()
    else:
        # Fall back to abbreviated system prompt
        return PERSONAS[persona_name]["system_prompt"]


def get_api_key() -> str:
    """Get Anthropic API key from environment."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        sys.exit(1)
    return api_key


def consult_advisor(client: anthropic.Anthropic, persona_name: str, question: str, use_full_persona: bool = False) -> str:
    """Get advice from a single advisor."""
    persona = PERSONAS[persona_name]

    # Use full persona file if available and requested
    if use_full_persona:
        system_prompt = load_full_persona(persona_name)
    else:
        system_prompt = persona["system_prompt"]

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Please provide your perspective on this ethical question or decision:\n\n{question}"
            }]
        )

        return message.content[0].text

    except Exception as e:
        return f"Error consulting {persona_name}: {str(e)}"


def format_response(persona_name: str, response: str) -> str:
    """Format advisor response with color and styling."""
    color = PERSONAS[persona_name]["color"]
    expertise = PERSONAS[persona_name]["expertise"]

    separator = "=" * 80

    output = f"\n{color}{separator}{RESET}\n"
    output += f"{color}{'[' + persona_name.upper() + ']'}{RESET}\n"
    output += f"{color}{expertise}{RESET}\n"
    output += f"{color}{separator}{RESET}\n\n"
    output += response
    output += f"\n\n"

    return output


def main():
    """Main function to run ethics consultation."""

    # Check for question argument
    if len(sys.argv) < 2:
        print("Usage: python ethics-consultation.py \"Your ethical question here\"")
        print("\nExample:")
        print('  python ethics-consultation.py "Should I charge premium prices for my AI consulting?"')
        sys.exit(1)

    question = " ".join(sys.argv[1:])

    # Check for full persona flag
    use_full_persona = "--full" in sys.argv
    if use_full_persona:
        question = question.replace("--full", "").strip()

    # Initialize API client
    api_key = get_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    # Print header
    print("\n" + "=" * 80)
    print("ETHICS OVERSIGHT BOARD CONSULTATION")
    print("=" * 80)
    print(f"\nQUESTION: {question}\n")
    print("Consulting advisors...\n")

    # Consult each advisor
    advisors = ["Hank Green", "Louis Rossmann", "ConcernedApe"]
    responses = {}

    for advisor in advisors:
        print(f"Consulting {advisor}...")
        response = consult_advisor(client, advisor, question, use_full_persona)
        responses[advisor] = response

    # Print all responses
    print("\n" + "=" * 80)
    print("ADVISOR RESPONSES")
    print("=" * 80)

    for advisor in advisors:
        print(format_response(advisor, responses[advisor]))

    # Print synthesis prompt
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print("\nConsider:")
    print("  • Where do the advisors agree? (Strong ethical clarity)")
    print("  • Where do they disagree? (Important trade-offs to consider)")
    print("  • Which perspective are you instinctively dismissing? (Blind spot check)")
    print("  • What unique context applies to your situation?")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
