#!/usr/bin/env python3
"""
Manual Rotation Guide Generator
For services that don't support automated API key rotation
"""

MANUAL_ROTATION_GUIDES = {
    "Perplexity Pro": {
        "url": "https://www.perplexity.ai/settings/api",
        "steps": [
            "1. Go to Perplexity API settings: https://www.perplexity.ai/settings/api",
            "2. Click 'Create API Key'",
            "3. Name it: 'MCP Server - [DATE]'",
            "4. Copy the new key",
            "5. Update 1Password: op item edit 'Perplexity Pro API' credential='NEW_KEY'",
            "6. Test with: op read 'op://API_Keys/Perplexity Pro API/credential'",
            "7. Restart any services using the key",
            "8. Delete the old key in Perplexity settings"
        ],
        "test_command": "curl -H 'Authorization: Bearer YOUR_KEY' https://api.perplexity.ai/chat/completions",
        "rotation_frequency": "Every 90 days"
    },

    "Gamma API": {
        "url": "https://gamma.app/settings/api",
        "steps": [
            "1. Go to Gamma API settings: https://gamma.app/settings/api",
            "2. Generate new API key",
            "3. Copy the new key",
            "4. Update 1Password: op item edit 'Gamma API' credential='NEW_KEY'",
            "5. Test with your WalterFetch-Reports project",
            "6. Revoke old key in Gamma settings"
        ],
        "test_command": "Run your Gamma integration and verify it works",
        "rotation_frequency": "Every 90 days"
    },

    "Google OAuth": {
        "url": "https://console.cloud.google.com",
        "steps": [
            "1. Go to Google Cloud Console: https://console.cloud.google.com",
            "2. Select your project (gmail-amazon-parser or gen-lang-client)",
            "3. Navigate to APIs & Services > Credentials",
            "4. Click on your OAuth 2.0 Client ID",
            "5. Regenerate client secret",
            "6. Update 1Password:",
            "   op item edit 'Google OAuth - Gmail MCP Server' client_secret='NEW_SECRET'",
            "7. Regenerate credentials.json files:",
            "   ~/Documents/ObsidianVault/Projects/gmail-mcp-server/generate-credentials.sh",
            "8. Re-authenticate any applications using these credentials"
        ],
        "test_command": "Run your Gmail MCP server and test authentication",
        "rotation_frequency": "Every 180 days (Google recommends annually)"
    },

    "TMDB API": {
        "url": "https://www.themoviedb.org/settings/api",
        "steps": [
            "1. Go to TMDB API settings: https://www.themoviedb.org/settings/api",
            "2. Regenerate API key (if option available)",
            "3. Update 1Password: op item edit 'TMDB API - Alfred Workflow' api_key='NEW_KEY'",
            "4. Update Alfred workflow configuration if needed",
            "5. Test Alfred workflow"
        ],
        "test_command": "Use Alfred to search for a movie",
        "rotation_frequency": "Every 180 days"
    }
}


def generate_rotation_checklist(service: str) -> str:
    """Generate a rotation checklist for a service"""
    if service not in MANUAL_ROTATION_GUIDES:
        return f"No rotation guide available for {service}"

    guide = MANUAL_ROTATION_GUIDES[service]

    checklist = f"""
# {service} - API Key Rotation Checklist

**Frequency**: {guide['rotation_frequency']}
**Settings URL**: {guide['url']}

## Steps

{chr(10).join(guide['steps'])}

## Testing

{guide['test_command']}

## Verification

- [ ] New key added to 1Password
- [ ] Old key revoked in service settings
- [ ] All applications using the key have been updated
- [ ] Test command executed successfully
- [ ] Documented rotation in audit log

## Audit Log Command

```bash
echo "{{
  \\"timestamp\\": \\"$(date -Iseconds)\\",
  \\"service\\": \\"{service}\\",
  \\"status\\": \\"success\\",
  \\"details\\": \\"Manual rotation completed\\"
}}" >> ~/.mcp/credential-rotation/logs/audit.jsonl
```

---
Generated: $(date)
"""
    return checklist


def generate_all_checklists():
    """Generate rotation checklists for all services"""
    output_dir = Path(__file__).parent.parent / "checklists"
    output_dir.mkdir(exist_ok=True)

    for service in MANUAL_ROTATION_GUIDES.keys():
        checklist = generate_rotation_checklist(service)
        filename = service.replace(" ", "_").lower() + "_rotation.md"

        with open(output_dir / filename, 'w') as f:
            f.write(checklist)

        print(f"✅ Generated checklist: {filename}")


if __name__ == "__main__":
    import sys
    from pathlib import Path

    if len(sys.argv) > 1:
        service = " ".join(sys.argv[1:])
        print(generate_rotation_checklist(service))
    else:
        print("Generating all rotation checklists...")
        generate_all_checklists()
        print("\nGenerated checklists in: ~/.mcp/credential-rotation/checklists/")
