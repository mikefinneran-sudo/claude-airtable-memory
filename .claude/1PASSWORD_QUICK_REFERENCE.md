# 1Password Quick Reference Card

## Common Commands

### Authentication
```bash
# Check if signed in
op whoami

# Sign in (if needed)
eval $(op signin)
```

### Reading Credentials
```bash
# Read any credential
op read "op://API_Keys/Service Name/field_name"

# Examples
op read "op://API_Keys/Perplexity Pro API/credential"
op read "op://API_Keys/Airtable WalterSignal/api_key"
op read "op://API_Keys/Gamma API/credential"
```

### Loading Project Environments
```bash
# WalterFetch-Reports
cd ~/Documents/ObsidianVault/Projects/WalterSignal/Products/WalterFetch-Reports
source load-env.sh

# walterfetch-v2
cd ~/Documents/ObsidianVault/Projects/WalterSignal/Code/walterfetch-v2
source load-env.sh
```

### Generating OAuth Files
```bash
# Gmail MCP Server
~/Documents/ObsidianVault/Projects/gmail-mcp-server/generate-credentials.sh

# Gmail Amazon Parser
~/Library/CloudStorage/GoogleDrive-mike@fly-flat.com/My\ Drive/Documents/_Utilities/Scripts/gmail_amazon_parser/generate-credentials.sh
```

### Managing Credentials
```bash
# List all credentials
op item list --vault API_Keys

# View a credential
op item get "Gamma API" --vault API_Keys

# Add new credential
op item create --category="API Credential" --vault="API_Keys" --title="Service Name" credential="key-here"

# Update a credential
op item edit "Service Name" credential="new-key-here"

# Delete a credential (careful!)
op item delete "Service Name" --vault API_Keys
```

## All Your Credentials

| Service | 1Password Reference |
|---------|-------------------|
| Perplexity Pro | `op://API_Keys/Perplexity Pro API/credential` |
| Gamma API | `op://API_Keys/Gamma API/credential` |
| Airtable (Key) | `op://API_Keys/Airtable WalterSignal/api_key` |
| Airtable (Base) | `op://API_Keys/Airtable WalterSignal/base_id` |
| Gmail Parser (Client ID) | `op://API_Keys/Google OAuth - Gmail Amazon Parser/client_id` |
| Gmail Parser (Secret) | `op://API_Keys/Google OAuth - Gmail Amazon Parser/client_secret` |
| Gmail MCP (Client ID) | `op://API_Keys/Google OAuth - Gmail MCP Server/client_id` |
| Gmail MCP (Secret) | `op://API_Keys/Google OAuth - Gmail MCP Server/client_secret` |
| Cloudflare Wrangler | `op://API_Keys/Cloudflare Wrangler OAuth/oauth_token` |
| TMDB (Alfred) | `op://API_Keys/TMDB API - Alfred Workflow/api_key` |

## Troubleshooting

### Not Authenticated
```bash
eval $(op signin)
```

### Variable Not Loading
```bash
# Reload shell config
source ~/.zshrc

# Or restart terminal
```

### Permission Denied
```bash
# Make scripts executable
chmod +x script-name.sh
```

## Full Documentation
See: `~/.claude/1PASSWORD_SECURITY_GUIDE.md`
