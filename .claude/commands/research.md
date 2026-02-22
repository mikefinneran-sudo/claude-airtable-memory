---
description: Create comprehensive research document
argument-hint: [topic]
allowed-tools: [WebSearch, WebFetch, Read, Write, Task, Bash, mcp__perplexity]
---

Research the following topic using the **PROBE framework** (`~/.claude/guides/PROBE-RESEARCH-v1.1.md`):

**Topic**: $ARGUMENTS

## PROBE Phases (execute all 5)

### P — Purpose Gate
- What decision does this research inform?
- What do we already know? What would change our mind?
- Select depth tier: Quick Scan (15-30 min) / **Standard** (default, 1-3 hrs) / Deep Dive (4-8+ hrs)
- **Write the Purpose Gate block in the output** (mandatory on all tiers)

### R — Range & Sources
- List dimensions to investigate with depth per dimension (deep / survey / flag)
- Define recency requirement and geographic scope
- Plan source strategy and 5-10 specific search queries before searching
- Select research tools: Perplexity Pro (primary for Quick Scan), WebSearch (gaps/local), WebFetch (primary sources)

### O — Observe & Collect
- Lead with **Perplexity Ask** (`perplexity_ask`) for broad questions, **Perplexity Research** (`perplexity_research`) for key dimensions, then fill gaps with WebSearch
- Collect with provenance: source tag (PRIMARY/SECONDARY/TERTIARY/ANECDOTAL/INFERRED) + URL + date
- Record negative findings (absence is evidence)
- Note contradictions for Benchmark phase
- Saturation check: stop when sources repeat
- **Maintain search log** — record every query and what it returned

### B — Benchmark & Validate
- Cross-reference key claims (2+ independent sources for decision-critical findings)
- Resolve contradictions with reasoning
- Confirmation bias audit: run at least one steel man search
- Confidence tag every finding: VERIFIED / LIKELY / UNCERTAIN / SPECULATIVE

### E — Extract & Deliver
- Answer the Purpose Gate question in one paragraph first
- "So what?" for every major finding — connect to the decision
- Include: Source Table, Search Log, Gaps & Limitations, Recommended Next Steps
- Apply OCEAN scoring (rewrite any dimension <3) — **never skip**
- If tier budget exceeded, acknowledge and justify

## Output
- **Style**: Corporate professional, no excessive emojis, focused and highly readable
- **Naming**: `YYYY-MM-DD - [Topic] Research - v1.md`
- **Location**: `~/Documents/ObsidianVault/Research/`
- **Required sections (all tiers)**: Purpose Gate block, Executive Summary, Key Findings, Source Table, Search Log, OCEAN Scores
- **Required sections (Standard + Deep Dive)**: + Detailed Analysis, Gaps & Limitations, Next Steps
