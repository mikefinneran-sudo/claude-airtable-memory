# Level 5: Human-in-the-Loop (HITL) Patterns

## Learning Objectives

1. **Understand HITL Use Cases**
   - When autonomous agents aren't sufficient
   - Critical decision points requiring human judgment
   - Quality gates and approval workflows

2. **Master Development Pattern**
   - Use `human_input=True` for interactive feedback
   - Test and iterate on task outputs
   - Debug agent behavior with human guidance

3. **Implement Production Pattern**
   - Use webhooks for async approval workflows
   - Build approval queues and notification systems
   - Handle timeouts and fallback scenarios

4. **Design Approval Workflows**
   - Identify tasks requiring human approval
   - Build approval UIs and notification systems
   - Track approval history and audit trails

## When to Use HITL

### ✅ Use Human-in-the-Loop When:

**Critical Decisions:**
- Financial transactions or commitments
- Legal agreements or contracts
- Customer communications before sending
- Product launches or public announcements
- Hiring/firing decisions
- Strategic pivots

**Quality Gates:**
- Content review before publication
- Code review before merge/deploy
- Design approval before implementation
- Campaign approval before launch

**Learning & Improvement:**
- Gathering training data for fine-tuning
- Understanding agent decision patterns
- Debugging unexpected behavior
- Iterating on prompt engineering

**Compliance & Audit:**
- Regulated industries requiring human oversight
- Audit trail requirements
- Risk management checkpoints
- Data privacy decisions

### ❌ Don't Use HITL When:

- Fully automated workflows (ETL, reporting, data processing)
- Low-risk operational tasks
- High-volume repetitive tasks
- Real-time decisions requiring sub-second response
- Tasks where agent accuracy > human accuracy

## Development Pattern: human_input=True

### Basic Usage

```python
from crewai import Task

review_task = Task(
    description="Review the marketing email draft and suggest improvements",
    expected_output="Approved email draft ready to send",
    agent=reviewer_agent,
    human_input=True  # Pauses execution for human feedback
)
```

**What happens:**
1. Agent completes the task
2. Execution pauses
3. Terminal displays agent output
4. User provides feedback via command line
5. Agent incorporates feedback
6. Continues to next task

### Interactive Session

```
Agent Output:
---
Subject: Introducing WalterSignal - AI-Powered Multi-Agent Platform
Body: Dear {{first_name}}, We're excited to announce...
---

Human input (press Enter to skip):
> Subject line too long, make it punchier. Remove "AI-Powered" buzzword.

Agent processes feedback and revises...
```

### Strategic HITL Placement

```python
# Place human_input at critical checkpoints
tasks = [
    Task(description="Research competitors", agent=researcher),
    Task(description="Draft positioning", agent=strategist, human_input=True),  # Checkpoint 1
    Task(description="Create messaging", agent=copywriter),
    Task(description="Design email campaign", agent=marketer, human_input=True),  # Checkpoint 2
    Task(description="Schedule campaign", agent=scheduler)
]
```

**Pattern**: Use HITL sparingly (2-3 checkpoints max) for critical decisions

### Multi-Round Refinement

```python
content_task = Task(
    description="""
    Write a blog post about CrewAI best practices.

    After human feedback, revise until approved.
    Maximum 3 revision rounds.
    """,
    expected_output="Publication-ready blog post (1500-2000 words)",
    agent=writer,
    human_input=True
)
```

Human can iterate multiple times before approving.

## Production Pattern: Webhooks

### Webhook Configuration

```python
from crewai import Task

approval_task = Task(
    description="Create marketing email for product launch",
    expected_output="Email draft (subject + body)",
    agent=copywriter,
    callback=webhook_url  # Send result to webhook for async approval
)
```

### Webhook Flow

```
1. Agent completes task
2. CrewAI sends POST to webhook_url with task output
3. Webhook stores in approval queue
4. Notification sent to approvers (email/Slack)
5. Human reviews in web UI
6. Approval decision sent back to CrewAI
7. Crew continues or revises based on feedback
```

### Webhook Payload Example

```json
{
  "task_id": "email_draft_20250115",
  "agent": "Marketing Copywriter",
  "output": {
    "subject": "Introducing WalterSignal",
    "body": "Dear {{first_name}}, We're excited...",
    "metadata": {
      "word_count": 250,
      "tone": "professional",
      "cta": "Schedule Demo"
    }
  },
  "context": {
    "product": "WalterSignal CrewAI Platform",
    "audience": "Mid-market CTOs",
    "campaign": "Q1 2025 Launch"
  },
  "timestamp": "2025-01-15T10:30:00Z"
}
```

### Approval System Components

#### 1. Webhook Receiver (FastAPI Example)

```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

class ApprovalRequest(BaseModel):
    task_id: str
    agent: str
    output: dict
    context: dict

@app.post("/approve")
async def receive_approval_request(request: ApprovalRequest, background_tasks: BackgroundTasks):
    # Store in database
    await store_in_approval_queue(request)

    # Send notification to approvers
    background_tasks.add_task(notify_approvers, request.task_id)

    return {"status": "queued", "task_id": request.task_id}
```

#### 2. Approval UI (Web Dashboard)

- List pending approvals with filters
- Display agent output with formatting
- Show context (product, audience, campaign)
- Provide approve/reject/revise actions
- Allow inline edits and feedback
- Track approval history

#### 3. Notification System

```python
def notify_approvers(task_id: str):
    """Send notifications via email and Slack"""
    task = get_approval_task(task_id)

    # Email notification
    send_email(
        to=approvers,
        subject=f"Approval Needed: {task.agent}",
        body=f"New approval request: {task_id}\\n\\nReview: https://app.example.com/approvals/{task_id}"
    )

    # Slack notification
    send_slack_message(
        channel="#approvals",
        message=f"🔔 New approval request from {task.agent}\\n<{approval_url}|Review Now>"
    )
```

#### 4. Timeout & Fallback

```python
# Set approval timeout
approval_task = Task(
    description="Create email draft",
    agent=copywriter,
    callback=webhook_url,
    timeout=3600  # 1 hour timeout
)

# Fallback logic in webhook handler
async def handle_timeout(task_id: str):
    """Handle approval timeout"""
    task = get_approval_task(task_id)

    if task.priority == "high":
        # Escalate to manager
        notify_manager(task_id)
    else:
        # Auto-reject and log
        reject_task(task_id, reason="Timeout")
        log_timeout(task_id)
```

## Development vs Production Patterns

| Aspect | Development (`human_input=True`) | Production (Webhooks) |
|--------|--------------------------------|----------------------|
| **Interaction** | Synchronous (terminal) | Asynchronous (web UI) |
| **Use Case** | Testing, iteration, debugging | Deployed workflows |
| **User Experience** | Command-line prompts | Web dashboard + notifications |
| **Scalability** | 1 user at a time | Multiple approvers, queues |
| **Timeout Handling** | User must be present | Automatic timeout + fallback |
| **Approval History** | Not tracked | Database audit trail |
| **Multi-User** | No | Yes (approval routing) |
| **Best For** | Development, POCs | Production deployments |

## HITL Design Patterns

### Pattern 1: Quality Gate

```python
# Use HITL as final approval before action
tasks = [
    Task(description="Generate content", agent=writer),
    Task(description="Review for quality", agent=editor, human_input=True),  # Gate
    Task(description="Publish to website", agent=publisher)
]
```

### Pattern 2: Iterative Refinement

```python
# Multiple HITL checkpoints for refinement
tasks = [
    Task(description="Draft outline", agent=planner, human_input=True),
    Task(description="Write content", agent=writer),
    Task(description="Review draft", agent=editor, human_input=True),
    Task(description="Finalize", agent=publisher)
]
```

### Pattern 3: Critical Decision Point

```python
# HITL for high-stakes decisions only
tasks = [
    Task(description="Analyze market data", agent=analyst),
    Task(description="Recommend pricing", agent=strategist, human_input=True),  # Critical!
    Task(description="Update pricing system", agent=engineer)
]
```

### Pattern 4: Approval Routing

```python
# Route to different approvers based on content
def route_approval(task_output):
    if task_output['budget'] > 10000:
        return "CFO"
    elif task_output['risk_level'] == "high":
        return "Legal"
    else:
        return "Manager"

# Implement in webhook handler
approver = route_approval(request.output)
notify_specific_approver(approver, request.task_id)
```

## Best Practices

### 1. Minimize HITL Checkpoints
- Each checkpoint adds friction and latency
- Place HITL only at critical decision points
- Aim for 1-3 checkpoints max per crew

### 2. Provide Rich Context
```python
Task(
    description="""
    Create email campaign for Q1 product launch.

    Context for approver:
    - Product: WalterSignal CrewAI Platform
    - Audience: Mid-market CTOs (100-1000 employees)
    - Goal: 50 demo signups
    - Budget: $5,000
    - Previous campaign CTR: 2.3%
    """,
    agent=marketer,
    human_input=True
)
```

### 3. Set Clear Approval Criteria
```python
Task(
    description="""
    Write blog post about CrewAI best practices.

    Approval criteria:
    - 1500-2000 words
    - Includes 3+ code examples
    - SEO optimized (keyword density 1-2%)
    - Passes plagiarism check
    - Professional tone
    """,
    expected_output="Publication-ready blog post meeting all criteria",
    agent=writer,
    human_input=True
)
```

### 4. Track Approval Metrics
- Average approval time
- Approval vs rejection rate
- Revision rounds per task
- Approver response times
- Bottleneck identification

### 5. Handle Edge Cases
```python
# Timeout handling
timeout_seconds = 7200  # 2 hours

# Offline approvers
fallback_approvers = ["manager@example.com", "backup@example.com"]

# Partial approvals
allow_inline_edits = True  # Approver can edit without full rejection

# Audit trail
log_approval_decision(task_id, approver, decision, feedback, timestamp)
```

## Security Considerations

### 1. Authentication & Authorization
```python
# Verify webhook authenticity
def verify_webhook_signature(request):
    signature = request.headers.get('X-Webhook-Signature')
    expected = hmac.new(secret_key, request.body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)

# Check approver permissions
def can_approve(user, task):
    if task.type == "financial" and task.amount > 10000:
        return user.role == "CFO"
    return user.role in ["Manager", "Director", "Executive"]
```

### 2. Sensitive Data Handling
```python
# Redact sensitive info before sending to webhook
def sanitize_for_approval(output):
    redacted = output.copy()
    redacted['api_keys'] = "[REDACTED]"
    redacted['passwords'] = "[REDACTED]"
    redacted['ssn'] = redacted['ssn'][:3] + "-XX-XXXX"
    return redacted
```

### 3. Audit Logging
```python
# Log all approval decisions
def log_approval(task_id, approver, decision, reason):
    log_entry = {
        'task_id': task_id,
        'approver': approver,
        'decision': decision,  # approved, rejected, revised
        'reason': reason,
        'timestamp': datetime.now().isoformat(),
        'ip_address': request.remote_addr
    }
    audit_log.insert(log_entry)
```

## Common Issues

**Issue**: Agent doesn't incorporate human feedback
**Fix**: Include instruction in task description: "Revise based on human feedback until approved"

**Issue**: Webhook URL unreachable
**Fix**: Use ngrok for local testing, ensure production URL is public

**Issue**: Approvers miss notifications
**Fix**: Multi-channel notifications (email + Slack + SMS for critical)

**Issue**: Approval bottlenecks
**Fix**: Set SLAs, escalation rules, and fallback approvers

**Issue**: No audit trail
**Fix**: Log all decisions with approver, timestamp, decision, and reason

## Next Steps

After completing Level 5, you have mastered:
- YAML-based crew configuration (Level 1)
- Reusable agent templates (Level 2)
- Custom tools with @tool decorator (Level 3)
- Hierarchical crews with managers (Level 4)
- Human-in-the-Loop patterns (Level 5)

**You're now ready to:**
- Build production CrewAI workflows
- Design complex multi-agent systems
- Implement approval workflows
- Scale crew development across teams

## Files Structure

```
level5_hitl_patterns/
├── development/
│   └── (examples with human_input=True)
├── production/
│   └── (webhook-based approval system)
├── examples/
│   └── (complete HITL workflows)
└── README.md  # This file
```

## Testing Checklist

- [ ] Understand when to use HITL vs full automation
- [ ] Tested `human_input=True` in development
- [ ] Designed webhook payload structure
- [ ] Built approval queue and notification system
- [ ] Implemented timeout and fallback logic
- [ ] Created approval UI mockup
- [ ] Set up audit logging
- [ ] Tested with multiple approvers
- [ ] Documented approval criteria
- [ ] Measured approval workflow metrics
