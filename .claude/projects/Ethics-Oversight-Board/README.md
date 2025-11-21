# Virtual Ethics Oversight Board

A multi-perspective ethical decision-making framework featuring three distinct advisory voices: Hank Green, Louis Rossmann, and ConcernedApe (Eric Barone).

## Purpose

This system provides diverse ethical perspectives on business decisions, product development, technology ethics, and personal/professional integrity questions. Each advisor brings a unique lens shaped by their documented principles and public work.

## The Advisory Board

### Hank Green
**Expertise**: Community building, science communication, ethical technology use, misinformation
**Core Values**:
- Human-centered decision-making (people over profit)
- Curiosity aligned with values, not just capitalist impulses
- Focus on "everyday solvable problems of normal people"
- Empathy, transparency, and clarity in communication
- Constructive engagement with disagreement

**When to Consult**: Community impact, communication strategy, balancing values with growth, navigating disagreement

### Louis Rossmann
**Expertise**: Consumer rights, business transparency, anti-monopoly practices, right to repair
**Core Values**:
- Radical transparency in all business dealings
- Consumer empowerment and accessibility
- Willingness to call out harmful practices
- Leadership through unpopular but principled decisions
- Anti-corporate practices that harm consumers

**When to Consult**: Pricing decisions, customer rights, transparency questions, standing up to industry norms

### ConcernedApe (Eric Barone)
**Expertise**: Creative autonomy, sustainable development, player-first design, passion-driven work
**Core Values**:
- Complete creative control and pure vision
- Player/customer responsibility and accountability
- No exploitative monetization (microtransactions, dark patterns)
- Continuous improvement and free value delivery
- Give back to those who supported you
- Perfection and care in execution

**When to Consult**: Monetization strategy, creative integrity, work-life sustainability, customer relationship philosophy

## How to Use This System

### Method 1: Interactive AI Chat
Use the individual persona prompts (`Hank-Green-Persona.md`, `Louis-Rossmann-Persona.md`, `ConcernedApe-Persona.md`) with Claude or another LLM. Each file contains a detailed persona prompt that embodies that advisor's perspective.

**Usage**:
1. Open a new Claude chat
2. Copy the persona prompt for your chosen advisor
3. Present your ethical dilemma or decision
4. Repeat with other advisors for multiple perspectives

### Method 2: Decision Framework Template
Use the structured decision framework (`Decision-Framework-Template.md`) to systematically work through a decision by considering what questions each advisor would ask.

**Usage**:
1. Copy the template
2. Fill in your decision context
3. Answer the questions from each advisor's perspective
4. Review patterns and conflicts in the responses
5. Make an informed decision

### Method 3: Automated Consultation Script
Run the Python script (`ethics-consultation.py`) to automatically generate responses from all three advisors using the Claude API.

**Usage**:
```bash
python ethics-consultation.py "Should I charge premium prices for my AI consulting services?"
```

## Use Cases

- **AI Consulting Business Decisions**: Pricing, client relationships, tool choices, business practices
- **Product/Tool Development**: Feature decisions, user privacy, monetization strategies
- **Technology Ethics**: Data usage, automation impact, accessibility, right to repair
- **Personal/Professional Integrity**: Career choices, work-life balance, maintaining values under pressure

## Files in This System

- `README.md` (this file) - System overview and usage guide
- `Hank-Green-Persona.md` - AI persona prompt embodying Hank Green's perspective
- `Louis-Rossmann-Persona.md` - AI persona prompt embodying Louis Rossmann's perspective
- `ConcernedApe-Persona.md` - AI persona prompt embodying ConcernedApe's perspective
- `Decision-Framework-Template.md` - Structured template for systematic decision analysis
- `ethics-consultation.py` - Automated script for generating all three perspectives

## Decision-Making Principles

When consulting this board, look for:

1. **Consensus**: When all three advisors align, you have strong ethical clarity
2. **Productive Tension**: Disagreement often reveals important trade-offs to consider
3. **Missing Perspectives**: Notice which advisor's concerns you're instinctively dismissing
4. **Values Alignment**: Which advisor's perspective resonates most with your core values?

## Recommended Workflow

1. **Initial Gut Check**: What does your intuition say?
2. **Consult All Three**: Get perspectives from each advisor
3. **Identify Conflicts**: Where do they disagree and why?
4. **Consider Context**: What unique factors apply to your specific situation?
5. **Make Decision**: Choose a path informed by multiple perspectives
6. **Document Reasoning**: Record why you decided as you did for future reference

## Limitations & Disclaimers

- These are interpretations based on publicly available interviews, videos, and statements
- Real people are more nuanced than any persona can capture
- This system supplements (doesn't replace) your own judgment and values
- Consider consulting actual experts for legal, financial, or specialized decisions

---

**Created**: 2025-10-31
**Version**: 1.0
**Last Updated**: 2025-10-31
