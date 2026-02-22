---
description: Plan feature implementation using PRISM framework
argument-hint: [feature-description]
model: claude-opus-4-6
allowed-tools: [Read, Grep, Glob, Bash]
---

Plan this feature using the PRISM framework (`~/.claude/guides/PRISM-PLANNING-v1.5.md`):

**Feature**: $ARGUMENTS

---

## P — Problem Definition

### Viability Gate (answer FIRST — before any technical planning)
1. **Should we build this?** Is there evidence this is needed now? Are there real users who will use it?
2. **Is the timing right?** What prerequisites must exist (users, data, deployment)?
3. **Build vs Buy?** Does a mature solution exist that solves 80%+? If yes, justify custom build on business value, not engineering preference.

If viability fails → recommend deferring or buying instead. Stop here.

### Problem Statement (if viable)
- **PROBLEM**: [One sentence — the outcome needed]
- **SUCCESS**: [2-3 measurable acceptance criteria]
- **FAIL IF**: [Top 2-3 ways this breaks]

## R — Recon

Explore the codebase before proposing anything:
- Read all relevant files (components, APIs, models, tests)
- Identify existing patterns to follow (naming, architecture, error handling)
- Map dependencies — what touches what?
- List unknowns that need resolution
- Note existing tests that must still pass

### Production Sync Check (for deployed systems)
```
PRODUCTION SYNC:
  Local repo matches production?  [yes / DRIFT: list files]
  All "missing" files checked on prod? [yes / confirmed missing]
  Production-only files identified? [none / list]
```

### Source Table (MANDATORY)
Every factual claim must be verified and tagged:
- **CODE**: Saw in file (cite file + line)
- **LIVE**: Checked live system (dashboard, CLI, API, curl)
- **DOC**: Found in documentation (cite doc)
- **USER**: Confirmed by user
- **UNVERIFIED**: Could not confirm — must flag in Red Team

```
RECON FINDINGS:
  [claim]                        [source]
  ...                            CODE: path/file.ts:42
  ...                            LIVE: confirmed via curl/ssh
  ...                            UNVERIFIED — inferred, not checked
```
No inferences treated as facts. UNVERIFIED claims on critical path must be resolved before presenting.

## I — Ideate

Generate 2-3 viable approaches. **If an off-the-shelf solution exists, it MUST be one option.** For each:
```
OPTION [X]: [description]
  + [advantage]
  - [risk/cost]
  Effort: [low/med/high]
  Fits patterns: [yes/partially/new]
  Table stakes included: [list what users expect — is it all here?]
```

**Lightweight mode:** If Recon shows <3 files, single obvious approach, no architectural decisions → skip Ideate, go straight to Select with rationale.

## S — Select & Structure

Choose one approach using these criteria (in priority order):
1. Solves the actual problem
2. Fits existing patterns
3. Simplest thing that works
4. Reversible

Then break into steps:
```
SELECTED: Option [X]
RATIONALE: [why this over alternatives — business value, not just engineering fit]

STEPS:
1. [Write failing tests first]
2. [Foundation implementation]
3. [Integration with existing system]
4. [Edge cases and error handling]
5. [Verify — tests pass, no regressions]
```

Max 6-8 steps. More = decompose into sub-tasks.

## Red Team (MANDATORY — do this before presenting)

Attack your own plan. Answer ALL 9 honestly:

1. **Prerequisites exist?** Does every step have its dependencies satisfied? Trace the chain.
2. **Data model makes sense?** Trace the data flow end-to-end.
3. **All claims sourced?** Every factual claim must have a source tag (CODE/LIVE/DOC/USER). Any UNVERIFIED claim on a critical path = risk. If the Viability Gate depends on an unverified claim, resolve it first.
4. **Numbers reasonable?** Defensible against existing baselines?
5. **Second-order effects?** What breaks, slows, or changes downstream?
6. **Table stakes present?** What do users EXPECT this feature to include? If the MVP is missing those expectations, it's broken — not minimal.
7. **Open questions resolved?** Categorize each as: resolved / blocker / deferrable. No footnote questions.
8. **Scope complete?** Does the change set cover EVERY page/file in scope? Cross-reference against sitemap, nav, or file manifest. List every target explicitly.
9. **Data flow traced?** For user input features: trace from action → JS → API → storage → confirmation. What happens at each step if it fails? Are sibling pages consistent?

```
RED TEAM:
  Prerequisites:   [all satisfied / GAP: ...]
  Data model:      [traces clean / ISSUE: ...]
  Claims sourced:  [all tagged CODE/LIVE/DOC/USER / UNVERIFIED: ...]
  Numbers:         [all defensible / SUSPECT: ...]
  Downstream:      [no impact / AFFECTS: ...]
  Table stakes:    [all present / MISSING: ...]
  Open questions:  [all resolved / BLOCKER: ... / DEFERRABLE: ...]
  Scope complete:  [all pages/files covered / MISSING: ...]
  Data flow:       [traced end-to-end / GAP: ... / INCONSISTENCY: ...]
```

**If any check fails, revise the plan above BEFORE presenting.** Do not present a plan you've found holes in.

## M — Measure (Post-Deploy Verify — MANDATORY)

After deploying, run these checks:
```
POST-DEPLOY VERIFY:
  SUCCESS criteria:    [all met / FAILED: ...]
  Failure modes:       [none triggered / TRIGGERED: ...]
  LIVE spot-check:     [all pages verified / ISSUE: ...]
  Cross-page check:    [consistent / INCONSISTENCY: ...]
  Tests:               [pass / FAILING: ...]
```

---

**Do NOT implement yet** — present this plan for approval before writing any code.
