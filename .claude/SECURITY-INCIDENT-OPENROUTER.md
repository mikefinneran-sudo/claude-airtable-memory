# Security Incident Report - OpenRouter API Key Exposure

**Date**: January 22, 2026
**Severity**: Medium (key auto-deactivated)
**Status**: ✅ Resolved

---

## What Happened

OpenRouter API key was hardcoded in two Python scripts and committed to git:
- `walterfetch-v2/scripts/enrich_contacts_v2.py`
- `walterfetch-v2/scripts/enrich_openrouter.py`

**Exposed key**: `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`

**Commit**: `41c315151f4eda0ef5f73b59e5f15a24cf3cfbd7` (Jan 21, 2026)

**Detection**: OpenRouter automatically detected the exposed key and deactivated it.

---

## Immediate Actions Taken

1. ✅ Removed hardcoded keys from both files
2. ✅ Updated scripts to use `os.environ.get("OPENROUTER_API_KEY")`
3. ✅ Committed security fix
4. ✅ Verified .env is in .gitignore (it is)

---

## What Needs to Happen Next

### 1. Get New OpenRouter API Key

```bash
# Go to OpenRouter dashboard
open https://openrouter.ai/keys

# Create new API key
# Copy the new key (starts with sk-or-v1-*)
```

### 2. Add to Environment Variables

**Local Mac** (.env file):
```bash
cd ~/Code/WalterSignal/walterfetch-v2
echo "OPENROUTER_API_KEY=sk-or-v1-YOUR_NEW_KEY_HERE" >> .env
```

**DGX Server**:
```bash
ssh mikefinneran@192.168.68.62
cd ~/walterfetch-v2
echo "OPENROUTER_API_KEY=sk-or-v1-YOUR_NEW_KEY_HERE" >> .env
```

### 3. Test Scripts Work

```bash
# Should fail without key
python3 scripts/enrich_openrouter.py

# Should work after adding key to .env
source .env
python3 scripts/enrich_openrouter.py
```

---

## Git History Cleanup (Optional)

The exposed key is still in git history (commit `41c3151`). Options:

**Option 1: Leave it** (Recommended)
- Key is already deactivated
- Repo hasn't been pushed to public GitHub
- No additional risk

**Option 2: Rewrite history** (If pushing to public GitHub)
```bash
cd ~/Code/WalterSignal

# Install git-filter-repo
brew install git-filter-repo

# Create pattern file
echo "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==>***REMOVED***" > /tmp/replacements.txt

# Rewrite history
git filter-repo --replace-text /tmp/replacements.txt --force

# Force push (only if you've already pushed to remote)
# git push --force
```

---

## Prevention Measures

### Already in Place ✅
- `.env` in `.gitignore`
- Hookify warnings for hardcoded secrets

### Additional Safeguards

**1. Pre-commit hook** (check for API keys before commit):
```bash
# Create hook
cat > ~/Code/WalterSignal/.git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Block commits with API keys

if git diff --cached | grep -E "sk-[a-zA-Z0-9-]{20,}|api[_-]?key.*=.*['\"][a-zA-Z0-9]{20,}"; then
    echo "❌ BLOCKED: Possible API key detected in commit"
    echo "Move secrets to .env file and use os.environ.get()"
    exit 1
fi
EOF

chmod +x ~/Code/WalterSignal/.git/hooks/pre-commit
```

**2. Use 1Password for secrets**:
```python
# Instead of hardcoding
import subprocess
api_key = subprocess.check_output([
    "op", "item", "get", "OpenRouter",
    "--fields", "credential"
]).decode().strip()
```

**3. Secret scanning tool**:
```bash
# Install gitleaks
brew install gitleaks

# Scan repo
cd ~/Code/WalterSignal
gitleaks detect --verbose
```

---

## Lessons Learned

1. **NEVER hardcode API keys** - Always use environment variables
2. **Review commits before pushing** - Check for secrets
3. **Trust the safety systems** - OpenRouter caught it automatically
4. **Keep .env in .gitignore** - Already working correctly

---

## Current Status

- ✅ Exposed key deactivated
- ✅ Code fixed to use env vars
- ✅ Security commit created
- ⏳ **User needs new API key** from openrouter.ai
- ⏳ Add new key to .env files (local + DGX)

---

## References

- OpenRouter Dashboard: https://openrouter.ai/keys
- Git history cleanup: https://rtyley.github.io/bfg-repo-cleaner/
- Gitleaks: https://github.com/gitleaks/gitleaks
