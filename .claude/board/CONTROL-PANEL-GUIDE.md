# Board Advisors Control Panel Guide

**Access your virtual board of directors through the web interface**

---

## Quick Start

### 1. Start the Control Panel

```bash
cd ~/.claude/projects/persistent-memory/web-gui
PORT=5001 python3 app.py
```

The control panel will be available at: **http://localhost:5001**

### 2. Login

Default password: `changeme`

To set a custom password:
```bash
export WEB_PASSWORD="your-secure-password"
PORT=5001 python3 app.py
```

---

## Features

### Board Advisors Tab

Navigate to the **Board Advisors** tab to access:

#### 1. Ask the Board
- **Full Board**: Get strategic guidance from all 7 members
- **Individual Members**: Direct questions to specific advisors
- Questions are automatically logged in `~/.claude/board/meetings/questions-YYYY-MM.md`

#### 2. View Board Members
Click any board member card to view:
- Complete profile and background
- Expertise and focus areas
- Key questions they ask
- Example scenarios and recommendations
- Integration with C-Suite

#### 3. Board Registry
- Overview of all 7 permanent members
- Diversity metrics (57% women, 3 continents, age 34-62)
- Progressive values alignment

#### 4. Rotating Thought Leader
- Q4 2025: Chef/Hospitality Expert
- Q1 2026: Urban Planner/Architect
- Q2 2026: Climate Scientist
- Q3 2026: Social Justice Organizer

---

## Your Board Members

### 1. Dr. Angela Simmons - Board Chair (56, USA)
- **Focus**: Governance, CEO coaching, strategic oversight
- **Based on**: Rosalind Brewer, Lisa Su
- **Best for**: Overall strategic direction, CEO development

### 2. Dr. Maya Chen - AI Strategy & Ethics (34, UK/China)
- **Focus**: AI technical strategy, responsible AI, ethics
- **Based on**: Fei-Fei Li, Andrew Ng
- **Best for**: AI technology decisions, ethical considerations

### 3. Marcus Johnson - Enterprise Growth (44, USA)
- **Focus**: Revenue growth, partnerships, enterprise sales
- **Based on**: Progressive consulting leaders
- **Best for**: Sales strategy, client acquisition, partnerships

### 4. Patricia Williams, CPA - Finance & Audit (53, UK)
- **Focus**: Financial oversight, risk management, audit
- **Based on**: Ursula Burns
- **Best for**: Financial decisions, pricing, profitability

### 5. Dr. Carmen Rodriguez - Talent & Culture (48, Mexico/USA)
- **Focus**: People strategy, culture, leadership development
- **Based on**: Progressive CHRO leaders
- **Best for**: Hiring, retention, organizational culture

### 6. David Kim - Industry & Client (62, South Korea)
- **Focus**: Client excellence, quality, industry expertise
- **Based on**: Kenneth Frazier
- **Best for**: Client relationships, service quality, healthcare expertise

### 7. Elena Vasquez - Innovation & Ecosystem (37, Singapore)
- **Focus**: Innovation, partnerships, future trends
- **Based on**: Reid Hoffman, Melinda French Gates
- **Best for**: Emerging tech, strategic partnerships, innovation

---

## Example Questions to Ask

### Strategic Questions (Full Board)
- "Should we expand to Europe in 2026?"
- "What's our competitive moat in AI consulting?"
- "Should we raise capital or grow organically?"

### AI Strategy (Dr. Maya Chen)
- "Should we build proprietary AI models or use APIs?"
- "How do we ensure our AI work is ethical?"
- "What AI trends should we be watching?"

### Revenue Growth (Marcus Johnson)
- "How do we move upmarket to Fortune 500?"
- "Should we partner with AWS or stay platform-agnostic?"
- "What's the right pricing model for our services?"

### Finance (Patricia Williams)
- "When should we hire a full-time CFO?"
- "What's our path to 20% EBITDA margins?"
- "Should we accept 90-day payment terms?"

### People & Culture (Dr. Carmen Rodriguez)
- "How do we retain top talent?"
- "What culture do we need as we scale?"
- "When do we add leadership layers?"

### Client Excellence (David Kim)
- "How do we ensure consistent quality?"
- "Should we specialize in one industry?"
- "What makes us indispensable to clients?"

### Innovation (Elena Vasquez)
- "What emerging technologies should we explore?"
- "Which partnerships would 10x our impact?"
- "How will AI change consulting in 3 years?"

---

## Question Logging

All questions are automatically logged to:
```
~/.claude/board/meetings/questions-YYYY-MM.md
```

Format:
```markdown
## 2025-10-31 14:30 - Question to angela-simmons

**Question**: Should we expand to Europe in 2026?

**Response**: [To be addressed in next board meeting]
```

You can review these logs to prepare for board meetings or track strategic decisions.

---

## Integration with C-Suite

The Board Advisors work alongside your Executive Knowledge System:

**Flow**:
1. **CTO/COO/CFO/CMO**: Execute day-to-day operations, log experiences
2. **Board**: Review executive logs, provide strategic guidance
3. **Executives**: Implement board guidance, report outcomes
4. **Pattern Library**: Capture learnings for future decisions

**Example**:
- CTO discovers "API/UI Boundary Pattern" works well
- Board reviews CTO experience log
- Board advises: "This could be our methodology differentiator"
- CMO markets: "Hybrid AI Implementation Methodology"
- Board evaluates impact on sales

---

## Security Notes

### Production Deployment

**Set a strong password**:
```bash
export WEB_PASSWORD="your-very-secure-password-here"
export SECRET_KEY="your-secret-key-for-sessions"
PORT=5001 python3 app.py
```

**Use HTTPS** in production (not just HTTP)

**Firewall**: Only allow access from trusted IPs

### Local Development

For local use only (default setup):
- Password: `changeme`
- Only accessible from localhost (127.0.0.1)
- No external network access

---

## Troubleshooting

### Port Already in Use

If port 5001 is in use, try a different port:
```bash
PORT=5002 python3 app.py
```

### Board Members Not Showing

Ensure profiles exist:
```bash
ls -la ~/.claude/board/*/PROFILE.md
```

Should show 7 profiles:
- angela-simmons/PROFILE.md
- maya-chen/PROFILE.md
- marcus-johnson/PROFILE.md
- patricia-williams/PROFILE.md
- carmen-rodriguez/PROFILE.md
- david-kim/PROFILE.md
- elena-vasquez/PROFILE.md

### Questions Not Logging

Check directory exists and is writable:
```bash
mkdir -p ~/.claude/board/meetings
ls -la ~/.claude/board/meetings/
```

---

## Advanced Features

### API Access

You can also interact programmatically:

```python
import requests

# Ask a question
response = requests.post('http://localhost:5001/api/ask-board',
    json={
        'member_id': 'maya-chen',
        'question': 'Should we build proprietary AI models?'
    },
    cookies={'session': 'your-session-cookie'}
)

print(response.json())
```

### Mobile Access

To access from mobile device on same network:

```bash
# Find your local IP
ifconfig | grep "inet "

# Start server on all interfaces
python3 app.py --host 0.0.0.0 --port 5001
```

Then access from mobile: `http://your-local-ip:5001`

**Warning**: Only do this on trusted networks!

---

## Next Steps

1. **Start using the board**: Ask your first strategic question
2. **Review profiles**: Get to know each board member's expertise
3. **Schedule quarterly meetings**: Set up regular board review sessions
4. **Integrate with C-Suite**: Link board guidance to executive execution
5. **Track decisions**: Use question logs to measure board impact

---

**Created**: 2025-10-31
**Control Panel**: http://localhost:5001
**Board Directory**: ~/.claude/board/
**Questions Log**: ~/.claude/board/meetings/

Your virtual board of directors is ready to provide strategic guidance!
