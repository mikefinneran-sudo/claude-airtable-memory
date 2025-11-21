# Quick Start Guide

Get started with your Virtual Ethics Oversight Board in under 5 minutes.

## Choose Your Method

### Method 1: Interactive AI Chat (Easiest)

**Best for**: Quick questions, conversational exploration, single perspective

1. Open a new Claude chat (or any AI chat interface)
2. Copy one of the persona prompts:
   - `Hank-Green-Persona.md` for human-centered perspective
   - `Louis-Rossmann-Persona.md` for consumer rights perspective
   - `ConcernedApe-Persona.md` for creative integrity perspective
3. Paste the entire persona prompt into the chat
4. Ask your ethical question

**Example**:
```
[Paste Hank-Green-Persona.md contents]

Now here's my question: Should I use dark patterns to increase
sign-ups for my SaaS product?
```

**Tip**: Open three separate chats to get all three perspectives simultaneously.

---

### Method 2: Decision Framework (Most Thorough)

**Best for**: Major decisions, documented reasoning, comprehensive analysis

1. Open `Decision-Framework-Template.md`
2. Copy the entire template
3. Fill in each section:
   - Your decision context
   - Answer questions from each advisor's perspective
   - Synthesize the insights
4. Save your completed framework for future reference

**Time**: 30-60 minutes for a thorough analysis

**Benefit**: Creates a documented decision-making process you can review later

---

### Method 3: Automated Script (Most Efficient)

**Best for**: Getting all three perspectives quickly, multiple questions

**Setup** (one-time):
```bash
# Install required package
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'
```

**Usage**:
```bash
cd /Users/mikefinneran/.claude/projects/Ethics-Oversight-Board

python ethics-consultation.py "Should I implement a freemium model or charge upfront?"
```

**Output**: Formatted responses from all three advisors in your terminal

---

## Example Questions to Try

### AI Consulting Business
- "Should I charge premium prices or keep rates accessible?"
- "Should I use Claude, GPT, or open-source models for client work?"
- "How do I handle clients who want to use AI to replace workers?"

### Product Development
- "Should I add a free tier with limited features?"
- "How much user data should I collect for product improvement?"
- "Should I add AI features everyone wants but I think are harmful?"

### Technology Ethics
- "Should I build automation that might eliminate jobs?"
- "How transparent should I be about AI limitations with clients?"
- "Should I work with clients in morally gray industries?"

### Personal/Professional
- "Should I work 80-hour weeks to launch faster?"
- "How do I handle a client asking for something I think is unethical?"
- "Should I open-source my proprietary tools?"

---

## Tips for Better Consultations

### Be Specific
❌ "Should I charge more?"
✅ "Should I raise my hourly rate from $150 to $300 for AI consulting, even though this will price out small businesses?"

### Provide Context
Include:
- Who is affected
- What values are in tension
- What you're inclined to do and why
- What worries you about your choice

### Look for Patterns
- **Consensus = clarity**: When all three agree, you have strong ethical grounding
- **Disagreement = trade-offs**: Different perspectives reveal what you're sacrificing
- **Dismissal = blind spot**: The advisor you want to ignore might see your weakness

### Follow Up
After getting initial perspectives, ask:
- "What if I can't afford to do what you're suggesting?"
- "How would you handle [specific constraint]?"
- "What would change your recommendation?"

---

## Quick Reference: When to Consult Each Advisor

### Consult Hank Green When:
- Community or trust is involved
- Communication strategy matters
- Balancing growth with values
- Navigating disagreement or criticism
- Platform/algorithm decisions

### Consult Louis Rossmann When:
- Pricing decisions
- Customer rights or empowerment
- Transparency questions
- Industry practices you're unsure about
- Tempted to "do what everyone else does"

### Consult ConcernedApe When:
- Monetization strategy
- Creative integrity at stake
- Work-life sustainability
- Considering compromises for growth
- Relationship with customers/users

---

## Next Steps

1. **Try the example**: Start with `EXAMPLE-CONSULTATION.md` to see the system in action
2. **Pick a real decision**: Choose something you're actually facing
3. **Use one method**: Try the approach that fits your style
4. **Document your process**: Save your consultations for future reference
5. **Iterate**: The more you use it, the more you'll internalize these perspectives

---

## Need Help?

- **Read the main README**: `README.md` has comprehensive documentation
- **Check the example**: `EXAMPLE-CONSULTATION.md` shows a full consultation
- **Review persona files**: Each advisor's file has detailed principles and response patterns

**Remember**: This system supplements your judgment, it doesn't replace it. Use these perspectives as input, then make decisions that align with your unique context and values.
