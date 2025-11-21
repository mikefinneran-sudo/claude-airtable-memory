# WalterSignal Design Enhancement Crew

## Available External APIs (via 1Password)

This crew has access to:

### 1. **Puppeteer MCP** (Browser Automation)
- Take screenshots of waltersignal.io
- Test mobile responsiveness
- Check interactive elements
- **Used by**: visual_content_analyst

### 2. **Perplexity** (Web Research)
- Competitive analysis of AI/automation websites
- Current design trends research
- Industry best practices
- **Used by**: web_ui_designer, graphic_brand_designer

### 3. **Gamma.app** (Presentation Generation)
- Create design mockup presentations
- Visual style exploration
- Stakeholder presentation materials
- **Used by**: graphic_brand_designer

### 4. **Airtable** (Project Management)
- Track design tasks and timeline
- Resource allocation
- Deliverable tracking
- **Used by**: business_operations_manager

## Enhanced Workflow

1. **Visual Analyst** → Uses Puppeteer to capture screenshots → Vision 90B analyzes
2. **UI Designer** → Uses Perplexity for competitive research → Creates recommendations
3. **Brand Designer** → Uses Gamma for concept mockups → Defines assets
4. **Project Manager** → Uses Airtable to create project tracker → Delivers plan

## Credential Access Pattern

All credentials auto-loaded from 1Password:
```python
import subprocess

def get_1password_credential(item_name, field="credential"):
    """Retrieve credential from 1Password"""
    result = subprocess.run(
        ['op', 'item', 'get', item_name, '--fields', field],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

# Example usage
puppeteer_mcp = get_1password_credential("puppeteer_mcp_url")
perplexity_key = get_1password_credential("PERPLEXITY_API_KEY")
gamma_key = get_1password_credential("gamma_api_key")
airtable_token = get_1password_credential("AIRTABLE_TOKEN")
```

## Running with API Integration

The crew will automatically:
1. ✅ Screenshot waltersignal.io using Puppeteer
2. ✅ Research competitors using Perplexity  
3. ✅ Generate mockups using Gamma
4. ✅ Track tasks in Airtable

**No manual API setup required** - all handled via 1Password!
