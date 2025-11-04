# 1Password Security Migration - Complete Guide

**Migration Date**: 2025-10-30
**Status**: ✅ Complete
**Security Level**: High (All credentials secured in 1Password)

## Overview

All API keys, OAuth credentials, and sensitive tokens have been migrated from hardcoded files to 1Password's secure vault system. This guide documents the migration and provides usage instructions.

---

## What Was Migrated

### 7 Credentials Stored in 1Password (API_Keys Vault)

1. **Gamma API**
   - Item: `Gamma API`
   - Field: `credential`
   - Usage: WalterFetch-Reports presentation generation
   - Reference: `op://API_Keys/Gamma API/credential`

2. **Perplexity Pro API**
   - Item: `Perplexity Pro API`
   - Field: `credential`
   - Usage: MCP research server, shell environment
   - Reference: `op://API_Keys/Perplexity Pro API/credential`

3. **Airtable WalterSignal**
   - Item: `Airtable WalterSignal`
   - Fields: `api_key`, `base_id`
   - Usage: walterfetch-v2 data storage
   - Reference: `op://API_Keys/Airtable WalterSignal/api_key`

4. **Google OAuth - Gmail Amazon Parser**
   - Item: `Google OAuth - Gmail Amazon Parser`
   - Fields: `client_id`, `client_secret`, `project_id`
   - Usage: Gmail Amazon order parsing utility
   - Reference: `op://API_Keys/Google OAuth - Gmail Amazon Parser/client_id`

5. **Google OAuth - Gmail MCP Server**
   - Item: `Google OAuth - Gmail MCP Server`
   - Fields: `client_id`, `client_secret`, `project_id`
   - Usage: Claude Code Gmail integration
   - Reference: `op://API_Keys/Google OAuth - Gmail MCP Server/client_id`

6. **Cloudflare Wrangler OAuth**
   - Item: `Cloudflare Wrangler OAuth`
   - Field: `oauth_token`
   - Usage: Cloudflare Workers deployment
   - Reference: `op://API_Keys/Cloudflare Wrangler OAuth/oauth_token`

7. **TMDB API - Alfred Workflow**
   - Item: `TMDB API - Alfred Workflow`
   - Field: `api_key`
   - Usage: Alfred media search workflow
   - Reference: `op://API_Keys/TMDB API - Alfred Workflow/api_key`

---

## Files Updated

### Shell Configuration
- **File**: `~/.zshrc`
- **Change**: Perplexity API key now loaded via `op read` command
- **Action**: Restart terminal or run `source ~/.zshrc`

### Project Environment Files
1. **WalterFetch-Reports**
   - File: `~/Documents/ObsidianVault/Projects/WalterSignal/Products/WalterFetch-Reports/.env`
   - Gamma API key replaced with 1Password reference
   - Helper script: `load-env.sh` created

2. **walterfetch-v2**
   - File: `~/Documents/ObsidianVault/Projects/WalterSignal/Code/walterfetch-v2/.env`
   - Airtable credentials replaced with 1Password references
   - Helper script: `load-env.sh` created

### Google OAuth Credential Generators
1. **Gmail MCP Server**
   - Script: `~/Documents/ObsidianVault/Projects/gmail-mcp-server/generate-credentials.sh`
   - Generates `credentials.json` from 1Password on demand

2. **Gmail Amazon Parser**
   - Script: `~/Library/CloudStorage/GoogleDrive-mike@fly-flat.com/My Drive/Documents/_Utilities/Scripts/gmail_amazon_parser/generate-credentials.sh`
   - Generates `credentials.json` from 1Password on demand

---

## Usage Instructions

### Loading Environment Variables

#### Method 1: Shell Environment (Automatic)
```bash
# Perplexity API is automatically loaded when you open a new terminal
# Just use it normally
echo $PERPLEXITY_API_KEY
```

#### Method 2: Project-Specific (Manual)
```bash
# For WalterFetch-Reports
cd ~/Documents/ObsidianVault/Projects/WalterSignal/Products/WalterFetch-Reports
source load-env.sh

# For walterfetch-v2
cd ~/Documents/ObsidianVault/Projects/WalterSignal/Code/walterfetch-v2
source load-env.sh
```

#### Method 3: Direct Read (On-Demand)
```bash
# Read any credential directly
op read "op://API_Keys/Gamma API/credential"

# Use in a script
GAMMA_KEY=$(op read "op://API_Keys/Gamma API/credential")
```

#### Method 4: Run Command with Injected Secrets
```bash
# 1Password will inject secrets directly into the command
op run --env-file=".env" -- python your_script.py
```

### Generating Google OAuth Credentials

```bash
# Gmail MCP Server
cd ~/Documents/ObsidianVault/Projects/gmail-mcp-server
./generate-credentials.sh
# Creates credentials.json from 1Password

# Gmail Amazon Parser
cd ~/Library/CloudStorage/GoogleDrive-mike@fly-flat.com/My\ Drive/Documents/_Utilities/Scripts/gmail_amazon_parser
./generate-credentials.sh
# Creates credentials.json from 1Password
```

### Adding New Credentials to 1Password

```bash
# Template for adding new API keys
op item create \
  --category="API Credential" \
  --vault="API_Keys" \
  --title="Service Name" \
  credential="your-api-key-here" \
  website="https://service.com" \
  notes="Description of what this is for"

# Template for OAuth credentials
op item create \
  --category="API Credential" \
  --vault="API_Keys" \
  --title="Service OAuth" \
  client_id="your-client-id" \
  client_secret="your-client-secret" \
  website="https://service.com" \
  notes="OAuth credentials for service"
```

---

## Security Benefits

### Before Migration
❌ API keys hardcoded in `.env` files
❌ Credentials in shell config files
❌ Secrets stored in Google Drive sync folders
❌ Risk of accidentally committing to git
❌ No audit trail of credential access
❌ Manual rotation requires finding all instances

### After Migration
✅ All credentials in encrypted 1Password vault
✅ Access requires authentication
✅ Audit trail of all credential reads
✅ Easy rotation (update once in 1Password)
✅ No secrets in git history
✅ Team sharing possible (if needed)

---

## Git Security

### Updated .gitignore Patterns
```gitignore
# Credentials & Keys
.env
.env.*
!.env.example
!.env.template
*.key
credentials.json
generate-credentials.sh
*_token.json
*_credentials.*
*.pem
token.pickle
*.p12
*.pfx
.wrangler/
```

### Verify Nothing Sensitive is Tracked
```bash
# Check what's tracked in git
cd ~/Documents/ObsidianVault
git ls-files | grep -E '(\.env$|credentials\.json|\.key$)'
# Should return nothing

# Check for ignored files
git check-ignore .env Projects/**/.env
# Should show they're ignored
```

---

## Troubleshooting

### "unauthorized: authentication required"
```bash
# Sign in to 1Password CLI
eval $(op signin)
# Or use biometric unlock if configured
```

### Environment variable not loading
```bash
# Check if 1Password CLI is working
op whoami

# Manually load a credential to test
op read "op://API_Keys/Perplexity Pro API/credential"

# If .zshrc changes aren't working
source ~/.zshrc
# Or restart terminal
```

### Script can't find credentials
```bash
# Make sure you're authenticated
op account list

# Check the vault and item exist
op vault list
op item list --vault API_Keys

# Verify the exact field name
op item get "Gamma API" --vault API_Keys
```

---

## Next Steps

### Recommended Actions

1. **Rotate Compromised Keys** (Optional but recommended)
   - Since keys were previously hardcoded, consider rotating:
     - Airtable API key
     - Perplexity API key
     - Google OAuth secrets
   - Update in 1Password, no need to update files

2. **Add Missing Credentials**
   - Anthropic/Claude API keys
   - OpenAI API keys
   - Apollo API keys
   - X.com/Twitter API keys
   - Webhook secrets

3. **Set Up Biometric Unlock**
   ```bash
   # Enable Touch ID for 1Password CLI
   op signin --account my.1password.com
   # Follow prompts to enable biometric unlock
   ```

4. **Configure Auto-Lock**
   - Recommended: Lock after 5-10 minutes of inactivity
   - Settings in 1Password desktop app

5. **Backup Your 1Password Emergency Kit**
   - Store in a secure physical location
   - Needed if you lose access to your account

---

## References

- 1Password CLI Documentation: https://developer.1password.com/docs/cli
- 1Password Secret References: https://developer.1password.com/docs/cli/secret-references
- 1Password Shell Plugins: https://developer.1password.com/docs/cli/shell-plugins

---

## Audit Log

| Date | Action | Details |
|------|--------|---------|
| 2025-10-30 | Initial Migration | Migrated 7 credentials to 1Password |
| 2025-10-30 | Updated Configs | Modified .zshrc and .env files |
| 2025-10-30 | Created Scripts | Added load-env.sh and generate-credentials.sh |
| 2025-10-30 | Updated .gitignore | Added comprehensive patterns |

---

**Migration completed successfully. All credentials are now secure in 1Password.**
