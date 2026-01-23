# Perplexity Pro MCP Server

**Purpose:** Integrate Perplexity Pro AI search into Claude Code for enhanced research capabilities

**Created:** 2025-10-20

---

## Features

### 🔍 Three Research Tools:

**1. perplexity_search**
- Quick web search with AI-generated answers
- Citations and sources included
- Domain filtering (search specific sites)
- Recency filtering (hour/day/week/month)
- Best for: Quick facts, current events, specific questions

**2. perplexity_deep_research**
- Iterative deep-dive research
- Multiple follow-up queries automatically
- Structured by focus areas
- Best for: Market research, industry analysis, comprehensive topics

**3. perplexity_compare**
- Compare multiple entities side-by-side
- Structured comparison across criteria
- Best for: Competitive analysis, product comparisons, vendor evaluation

---

## Setup Instructions

### Step 1: Get Perplexity API Key

1. Go to https://perplexity.ai
2. Sign in or create account
3. Subscribe to Perplexity Pro (required for API access)
4. Navigate to Settings → API
5. Generate API key
6. Copy the key

### Step 2: Install Dependencies

```bash
cd /Users/mikefinneran/Documents/ObsidianVault/.mcp/perplexity-research
pip3 install -r requirements.txt
```

### Step 3: Set Environment Variable

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
export PERPLEXITY_API_KEY="pplx-xxxxxxxxxxxxx"
```

Then reload:
```bash
source ~/.zshrc
```

**Or create `.env` file:**
```bash
echo "PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxx" > .env
```

### Step 4: Make Server Executable

```bash
chmod +x /Users/mikefinneran/Documents/ObsidianVault/.mcp/perplexity-research/server.py
```

### Step 5: Configure Claude Code

Add to your Claude Code MCP settings:

**Location:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "perplexity-research": {
      "command": "python3",
      "args": [
        "/Users/mikefinneran/Documents/ObsidianVault/.mcp/perplexity-research/server.py"
      ],
      "env": {
        "PERPLEXITY_API_KEY": "pplx-xxxxxxxxxxxxx"
      }
    }
  }
}
```

**Or if using .env file:**

```json
{
  "mcpServers": {
    "perplexity-research": {
      "command": "python3",
      "args": [
        "/Users/mikefinneran/Documents/ObsidianVault/.mcp/perplexity-research/server.py"
      ]
    }
  }
}
```

### Step 6: Restart Claude Code

Close and reopen Claude Code to load the MCP server.

---

## Usage Examples

### Example 1: Quick Market Research

**In Claude Code:**
```
Use Perplexity to research: "What is the total addressable market for PE deal flow software in 2025?"
```

**Behind the scenes:**
- Claude calls `perplexity_search` tool
- Perplexity searches web + AI generates answer
- Returns with citations

### Example 2: Deep Competitive Analysis

**In Claude Code:**
```
Do deep research on CapIQ vs PitchBook using Perplexity. Focus on: pricing, features, market share, user reviews.
```

**Behind the scenes:**
- Claude calls `perplexity_deep_research`
- Multiple iterative searches
- Comprehensive report generated

### Example 3: Company Comparison

**In Claude Code:**
```
Use Perplexity to compare: CapIQ, PitchBook, and ZoomInfo on pricing, data quality, and PE firm adoption.
```

**Behind the scenes:**
- Claude calls `perplexity_compare`
- Structured comparison across criteria
- Table or detailed analysis returned

---

## Tool Reference

### perplexity_search

**Purpose:** Quick AI-powered web search

**Parameters:**
- `query` (required): The search query
- `search_domain_filter` (optional): Array of domains to search (e.g., `["bloomberg.com", "techcrunch.com"]`)
- `search_recency_filter` (optional): "hour" | "day" | "week" | "month"
- `model` (optional): Model to use (default: "llama-3.1-sonar-large-128k-online")

**Example:**
```python
# Claude Code will call this automatically when you say:
"Search Perplexity for latest funding rounds in PE software, last week only"

# Translates to:
perplexity_search(
    query="latest funding rounds in private equity software",
    recency_filter="week"
)
```

### perplexity_deep_research

**Purpose:** Iterative deep-dive research

**Parameters:**
- `topic` (required): Main topic to research
- `focus_areas` (optional): Array of specific aspects to explore
- `depth` (optional): 1-5, how many follow-up queries (default: 3)

**Example:**
```python
# Claude Code will call this when you say:
"Deep research on Midwest PE market, focus on deal sizes, active firms, and recent trends"

# Translates to:
perplexity_deep_research(
    topic="Midwest private equity market",
    focus_areas=["deal sizes", "active firms", "recent trends"],
    depth=3
)
```

### perplexity_compare

**Purpose:** Structured comparison of entities

**Parameters:**
- `entities` (required): Array of 2+ things to compare
- `comparison_criteria` (optional): What to compare on

**Example:**
```python
# Claude Code will call this when you say:
"Compare CapIQ vs PitchBook on pricing and data quality"

# Translates to:
perplexity_compare(
    entities=["CapIQ", "PitchBook"],
    comparison_criteria=["pricing", "data quality"]
)
```

---

## Cost & API Limits

**Perplexity Pro Subscription:**
- $20/month for Pro account
- Includes API access
- Generous rate limits

**API Pricing:**
- Sonar models: ~$0.001-0.005 per query
- Very affordable for research use

**Rate Limits:**
- Pro accounts: Higher limits than free tier
- Check Perplexity dashboard for current limits

---

## Use Cases for WalterSignal

### Market Research
```
"Use Perplexity to research the size of the PE deal sourcing software market"
```

### Competitive Intelligence
```
"Deep research on how PE firms currently source acquisition targets, focus on tools they use and pain points"
```

### Company Background
```
"Research Great Range Capital using Perplexity: founding, portfolio, investment criteria, recent deals"
```

### Industry Analysis
```
"Compare the manufacturing, healthcare, and business services sectors for PE investment appeal in the Midwest"
```

### Pricing Research
```
"What do CapIQ, PitchBook, and similar tools charge annually? Find recent pricing information."
```

### Trend Analysis
```
"What are the latest trends in private equity deal sourcing? Filter to last month only."
```

---

## Troubleshooting

### "PERPLEXITY_API_KEY environment variable not set"

**Solution:**
1. Verify API key is in environment: `echo $PERPLEXITY_API_KEY`
2. If empty, add to `~/.zshrc` and reload
3. Or use `.env` file in server directory

### "Error calling Perplexity API: 401 Unauthorized"

**Solution:**
- API key is invalid or expired
- Regenerate key in Perplexity settings
- Update environment variable

### "MCP server not showing up in Claude Code"

**Solution:**
1. Check `claude_desktop_config.json` is correct
2. Restart Claude Code completely
3. Check server.py is executable: `ls -la server.py`
4. Test server manually: `python3 server.py`

### "Module 'mcp' not found"

**Solution:**
```bash
pip3 install -r requirements.txt
```

---

## Advanced Configuration

### Custom Models

Perplexity offers different model sizes:
- `llama-3.1-sonar-small-128k-online` (fastest, cheapest)
- `llama-3.1-sonar-large-128k-online` (balanced, default)
- `llama-3.1-sonar-huge-128k-online` (most accurate, slower)

Specify in Claude Code:
```
"Search Perplexity using the huge model for maximum accuracy: [query]"
```

### Domain Filtering

Restrict searches to specific sites:
```
"Search Perplexity for PE software news, only from bloomberg.com and techcrunch.com"
```

### Recency Filtering

Get only recent results:
```
"Search Perplexity for PE deals announced in the last day"
```

---

## Comparison: Perplexity vs WebSearch vs WebFetch

| Feature | Perplexity MCP | WebSearch (Built-in) | WebFetch (Built-in) |
|---------|----------------|---------------------|-------------------|
| **AI-Generated Answers** | ✅ Yes | ❌ No (raw results) | ❌ No (raw HTML) |
| **Citations** | ✅ Yes | ❌ No | ❌ No |
| **Current Events** | ✅ Excellent | ✅ Good | ⚠️ Limited |
| **Domain Filtering** | ✅ Yes | ❌ No | ✅ Yes (one site) |
| **Recency Filtering** | ✅ Yes | ⚠️ Limited | ❌ No |
| **Deep Research** | ✅ Built-in | ❌ Manual | ❌ Manual |
| **Cost** | 💰 $20/mo + API | ✅ Free | ✅ Free |
| **Best For** | Research, analysis | Quick searches | Fetch specific page |

**When to use each:**
- **Perplexity:** Market research, competitive analysis, comprehensive questions
- **WebSearch:** Quick fact-checking, when citations not needed
- **WebFetch:** Scraping specific page content, extracting data

---

## Examples in Practice

### WalterSignal Use Case 1: Market Sizing

**Request:**
```
How big is the total addressable market for PE deal sourcing software? Use Perplexity for the most current data.
```

**Result:**
- Perplexity searches recent reports, articles, market research
- AI synthesizes findings
- Returns estimate with sources cited
- Saves hours vs. manual research

### WalterSignal Use Case 2: Competitive Analysis

**Request:**
```
Do deep research on CapIQ vs PitchBook: pricing, features, PE firm satisfaction, market share. Use Perplexity.
```

**Result:**
- Deep research mode: 3-5 iterative searches
- Comprehensive comparison generated
- Recent user reviews included
- Actionable competitive intelligence

### WalterSignal Use Case 3: Customer Research

**Request:**
```
Research Great Range Capital using Perplexity: recent deals, portfolio companies, investment thesis, team.
```

**Result:**
- Finds recent press releases, LinkedIn profiles
- Portfolio analysis from multiple sources
- Deal history compiled
- Ready for personalized outreach

---

## Integration with Prompt Database

### New Prompt to Add:

**File:** `Prompts/Research/perplexity-market-research.md`

```markdown
# Perplexity: Comprehensive Market Research

**Tool:** Perplexity MCP
**Use Case:** Deep market research with AI-powered synthesis

## The Prompt

Use Perplexity to do deep research on [TOPIC], focusing on:
- Market size and growth trends
- Key players and market share
- Recent developments and news
- Industry analysis and expert opinions

Use deep research mode for comprehensive coverage.
```

---

## Future Enhancements

**Planned:**
- [ ] Add image search capability
- [ ] Export results to Obsidian notes automatically
- [ ] Batch research (multiple queries in sequence)
- [ ] Custom research templates
- [ ] Integration with BI report generation
- [ ] Automated citation formatting

---

## Resources

- [Perplexity API Docs](https://docs.perplexity.ai)
- [MCP Protocol Spec](https://modelcontextprotocol.io)
- [Claude Code MCP Guide](https://docs.anthropic.com/claude/docs/mcp)

---

**Status:** Ready for testing ✅
**Last Updated:** 2025-10-20
**Maintained By:** Mike Finneran
