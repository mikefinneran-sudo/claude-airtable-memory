# Level 2: Reusable Agent Templates Library

## Learning Objectives

1. **Build a Template Library**
   - Create catalog of pre-configured agents for common roles
   - Organize templates by functional area (research, content, engineering, etc.)
   - Document template inputs and use cases

2. **Understand Template Reusability**
   - Same agent template works across multiple crews and projects
   - Placeholder interpolation allows customization without duplication
   - Templates become organizational knowledge assets

3. **Master Template Composition**
   - Combine multiple templates to build complete crews
   - Customize templates with specific inputs for each project
   - Maintain consistency while allowing flexibility

4. **Scale Crew Creation**
   - Reduce time to build new crews (minutes vs hours)
   - Ensure quality through battle-tested templates
   - Enable non-technical users to compose crews

## Template Library Structure

### 22 Agent Templates Across 8 Categories

#### 1. Research & Analysis (3 templates)
- `research_analyst`: Thorough research with source citations
- `competitive_intelligence`: Competitor analysis and market positioning
- `data_analyst`: Data insights and actionable recommendations

#### 2. Content Creation (3 templates)
- `technical_writer`: Clear documentation and tutorials
- `marketing_copywriter`: Persuasive marketing content
- `social_media_manager`: Platform-specific social content

#### 3. Development & Engineering (3 templates)
- `software_architect`: System design and technical architecture
- `code_reviewer`: Code quality and security reviews
- `devops_engineer`: Infrastructure and CI/CD pipelines

#### 4. Business Strategy (3 templates)
- `business_strategist`: Strategic planning and frameworks
- `financial_analyst`: Financial modeling and analysis
- `sales_strategist`: Sales strategy and deal optimization

#### 5. Project Management (3 templates)
- `project_manager`: Project planning and coordination
- `scrum_master`: Agile facilitation and process improvement
- `product_owner`: Feature prioritization and backlog management

#### 6. Quality Assurance (2 templates)
- `qa_engineer`: Testing and quality standards
- `security_auditor`: Security audits and compliance

#### 7. Customer-Facing (2 templates)
- `customer_success_manager`: Customer retention and expansion
- `technical_support`: Issue resolution and troubleshooting

#### 8. Specialized Domains (3 templates)
- `legal_advisor`: Legal compliance and risk management
- `hr_specialist`: Human resources and people operations
- `brand_strategist`: Brand positioning and identity

## Using Templates

### Basic Pattern

```python
from crewai import Agent
import yaml

# 1. Load templates
with open('templates/agent_library.yaml', 'r') as f:
    templates = yaml.safe_load(f)

# 2. Get a template
template = templates['research_analyst']

# 3. Create agent with custom inputs
agent = Agent(
    role=template['role'],
    goal=template['goal'].replace('{topic}', 'AI multi-agent systems'),
    backstory=template['backstory'],
    verbose=True,
    allow_delegation=False
)
```

### Helper Function (Recommended)

```python
def create_agent_from_template(template_name, templates, custom_inputs=None):
    """Create an Agent from a template with custom inputs"""
    template = templates[template_name].copy()

    if custom_inputs:
        for key in ['role', 'goal', 'backstory']:
            if key in template:
                for placeholder, value in custom_inputs.items():
                    template[key] = template[key].replace(f'{{{placeholder}}}', str(value))

    return Agent(
        role=template['role'],
        goal=template['goal'],
        backstory=template['backstory'],
        verbose=template.get('verbose', True),
        allow_delegation=template.get('allow_delegation', False)
    )

# Usage
agent = create_agent_from_template(
    'business_strategist',
    templates,
    {
        'strategy_type': 'Go-To-Market',
        'company': 'WalterSignal',
        'objective': 'acquire 50 customers'
    }
)
```

## Example: GTM Strategy Crew

See `examples/gtm_strategy_crew.py` for a complete example using 4 templates:
- Competitive Intelligence Specialist
- Business Strategy Consultant
- Marketing Copywriter
- Sales Strategy Specialist

This crew creates a complete go-to-market strategy including:
- Competitive analysis with SWOT
- GTM strategy with positioning, channels, pricing
- Product messaging and sales collateral
- Sales playbook with objection handling

**Time saved**: Building from scratch = 2-3 hours. Using templates = 15 minutes.

## Template Placeholders

Each template includes `{placeholders}` that should be replaced with specific values:

| Template | Placeholders | Example Values |
|----------|-------------|----------------|
| research_analyst | {topic} | "AI multi-agent systems" |
| competitive_intelligence | {competitor} | "LangChain, AutoGen" |
| data_analyst | {dataset} | "customer usage metrics" |
| business_strategist | {strategy_type}, {company}, {objective} | "GTM", "Acme Inc", "increase revenue" |
| marketing_copywriter | {content_type}, {desired_action} | "blog post", "newsletter signup" |
| software_architect | {system}, {requirements} | "payment API", "PCI compliance" |
| qa_engineer | {feature}, {criteria} | "checkout flow", "WCAG 2.1 AA" |

Always check the template's goal and backstory to identify all placeholders.

## Benefits of Template Library

### 1. Speed
- Create new crews in minutes instead of hours
- No need to write agent definitions from scratch
- Focus effort on task descriptions (80/20 rule)

### 2. Quality
- Battle-tested agent definitions
- Consistent role clarity across projects
- Reduced trial-and-error in agent design

### 3. Knowledge Sharing
- Templates capture best practices
- New team members can compose crews immediately
- Organizational knowledge becomes reusable asset

### 4. Consistency
- Same role behaves consistently across projects
- Easier to compare results and performance
- Predictable agent interactions

## Extending the Library

### Adding New Templates

```yaml
# templates/agent_library.yaml

your_new_role:
  role: "Role Title"
  goal: "What this agent achieves using {placeholders}"
  backstory: >
    Who this agent is, their expertise, and approach to work.
    Include relevant skills, experience, and methodology.
  verbose: true
  allow_delegation: false  # true for manager-type roles
```

### Template Design Guidelines

1. **Role**: Short, clear title (2-4 words)
2. **Goal**: Specific outcome with {placeholders} for customization
3. **Backstory**: 2-3 sentences covering:
   - Who they are (expertise level)
   - What they're skilled at (core competencies)
   - How they work (methodology/approach)
4. **Verbose**: true (for training), false (for production)
5. **Allow Delegation**: true only for manager-type roles

### When to Create New Templates

**✅ Create a new template when**:
- You've used the same agent definition 3+ times
- The role is common across industries
- The expertise is specialized and reusable
- You want to standardize a specific role

**❌ Don't create a template when**:
- The role is project-specific and won't be reused
- The definition changes significantly each time
- It's too generic ("Expert", "Specialist" without domain)

## Testing Checklist

- [ ] All templates load without YAML errors
- [ ] Placeholders are clearly identified in comments
- [ ] Backstories follow 2-3 sentence guideline
- [ ] Allow_delegation set appropriately (false for most)
- [ ] Templates are organized by category
- [ ] Example crew uses 3+ templates successfully
- [ ] Helper function interpolates placeholders correctly

## Common Issues

**Issue**: KeyError when replacing placeholders
**Fix**: Ensure placeholder format is `{placeholder}` not `{{placeholder}}`

**Issue**: Agent doesn't behave as expected
**Fix**: Check that backstory aligns with goal, may need more specific task description (80/20 rule)

**Issue**: Too many placeholders making template complex
**Fix**: Simplify template or create specialized version for specific use case

## Comparison: Templates vs Custom

| Aspect | Custom Agents | Template Library |
|--------|--------------|------------------|
| **Setup Time** | 15-30 min per agent | 2-3 min per agent |
| **Consistency** | Varies by author | Standardized |
| **Reusability** | Copy-paste needed | Import and customize |
| **Maintenance** | Update each instance | Update once, all benefit |
| **Onboarding** | Learn by example | Clear catalog to browse |
| **Best For** | Unique, one-off roles | Common, recurring roles |

**Recommendation**: Use templates for 80% of agents, custom definitions for 20% unique roles.

## Next Steps

After completing Level 2, you should:
- Have a library of 20+ reusable agent templates
- Understand how to customize templates with placeholders
- Be able to compose crews in minutes using templates
- Know when to create new templates vs custom agents

**Ready for Level 3?** → Custom tools with `@tool` decorator

## Files Structure

```
level2_agent_templates/
├── templates/
│   └── agent_library.yaml       # 22 agent templates across 8 categories
├── examples/
│   └── gtm_strategy_crew.py     # Complete GTM crew using 4 templates
└── README.md                     # This file
```
