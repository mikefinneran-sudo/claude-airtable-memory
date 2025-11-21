# WalterSignal Zapier Integration Guide

## 🎯 Overview

This integration allows Zapier to trigger your CrewAI specialists via webhooks for automated workflows.

**Architecture:**
```
Zapier → Webhook → FastAPI Server (DGX) → CrewAI Crew → Response → Zapier
```

## 📋 Available Endpoints

### 1. Lead Enrichment (`/webhook/lead-enrichment`)
**Use case:** Automatically enrich leads from your CRM

**Input:**
```json
{
  "company_name": "Acme Corp",
  "website": "https://acme.com",
  "industry": "Manufacturing",
  "fields_to_enrich": ["company_info", "decision_makers", "pain_points", "tech_stack"]
}
```

**Output:**
```json
{
  "success": true,
  "crew_type": "lead_enrichment",
  "execution_id": "enrich_20251112_170000",
  "result": {
    "company_name": "Acme Corp",
    "enriched_fields": {
      "company_info": {...},
      "decision_makers": [...],
      "pain_points": [...],
      "tech_stack": [...]
    }
  }
}
```

### 2. Research (`/webhook/research`)
**Use case:** Automated research on topics

**Input:**
```json
{
  "topic": "AI consulting market in Chicago",
  "depth": "deep",
  "output_format": "markdown"
}
```

### 3. Design (`/webhook/design`)
**Use case:** Trigger design crew for logos, branding

**Input:**
```json
{
  "task_type": "logo",
  "company_name": "TechCorp",
  "description": "Modern tech company needs minimalist logo"
}
```

---

## 🚀 Setup Instructions

### Step 1: Install Dependencies on DGX

```bash
# SSH to DGX
ssh mikefinneran@192.168.68.88

# Navigate to crewai-specialists
cd ~/crewai-specialists

# Activate virtual environment
source venv/bin/activate

# Install FastAPI dependencies
pip install -r requirements-zapier.txt
```

### Step 2: Set API Key (Security)

```bash
# Generate secure API key
export ZAPIER_API_KEY="waltersignal-$(openssl rand -hex 16)"

# Save to .env file
echo "ZAPIER_API_KEY=$ZAPIER_API_KEY" >> .env

# Remember this key for Zapier configuration
echo "Your API key: $ZAPIER_API_KEY"
```

### Step 3: Start the Server

```bash
# Run the webhook server
python zapier_webhook_server.py

# Server starts on port 8001
# API Docs available at: http://192.168.68.88:8001/docs
```

### Step 4: Test Locally

```bash
# Test health check
curl http://192.168.68.88:8001/health

# Test lead enrichment
curl -X POST http://192.168.68.88:8001/webhook/lead-enrichment \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "company_name": "Acme Corp",
    "website": "https://acme.com",
    "industry": "Manufacturing"
  }'
```

---

## 🔗 Zapier Configuration

### Option 1: Using Zapier Webhooks by Zapier

1. **Create new Zap**
2. **Trigger:** Choose your source app (Google Sheets, Airtable, etc.)
3. **Action:** Search for "Webhooks by Zapier"
4. **Event:** POST
5. **URL:** `http://192.168.68.88:8001/webhook/lead-enrichment`
6. **Headers:**
   ```
   Content-Type: application/json
   X-API-Key: YOUR_ZAPIER_API_KEY
   ```
7. **Data:** Map fields from your trigger:
   ```json
   {
     "company_name": "{{trigger.company_name}}",
     "website": "{{trigger.website}}",
     "industry": "{{trigger.industry}}"
   }
   ```
8. **Test:** Send test webhook
9. **Activate:** Turn on your Zap

### Option 2: Public URL (Using ngrok or Cloudflare Tunnel)

If DGX is not publicly accessible, use ngrok:

```bash
# Install ngrok on DGX
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/

# Start tunnel
ngrok http 8001

# Use the ngrok URL in Zapier (e.g., https://abc123.ngrok.io/webhook/lead-enrichment)
```

---

## 🎬 Example Workflows

### Workflow 1: CRM Lead Enrichment
**Trigger:** New row in Google Sheets
**Action:** Webhook to `/webhook/lead-enrichment`
**Result:** Enriched data → Update same row in Google Sheets

**Zap Steps:**
1. Trigger: Google Sheets - New Row
2. Action: Webhooks - POST to lead-enrichment endpoint
3. Action: Google Sheets - Update Row with enriched data

### Workflow 2: Automated Content Research
**Trigger:** New card in Trello (Content Ideas board)
**Action:** Webhook to `/webhook/research`
**Result:** Research summary → Comment on Trello card

**Zap Steps:**
1. Trigger: Trello - New Card
2. Action: Webhooks - POST to research endpoint
3. Action: Trello - Create Comment with research results

### Workflow 3: Client Onboarding
**Trigger:** New customer in Stripe
**Action:** Webhook to `/webhook/research` (research their industry)
**Result:** Custom strategy doc → Email to client

**Zap Steps:**
1. Trigger: Stripe - New Customer
2. Action: Webhooks - POST to research endpoint
3. Action: Gmail - Send Email with research findings

---

## 🔒 Security Best Practices

1. **API Key Authentication:** Always use strong API keys
2. **HTTPS Only:** Use ngrok or Cloudflare tunnel for production
3. **IP Whitelisting:** Configure firewall to only accept Zapier IPs
4. **Rate Limiting:** Add rate limits to prevent abuse
5. **Logging:** Monitor webhook activity for suspicious patterns

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8001 is in use
sudo lsof -i :8001

# Kill existing process
sudo kill -9 <PID>

# Restart server
python zapier_webhook_server.py
```

### Zapier can't reach webhook
1. Check DGX is accessible from public internet
2. Verify firewall allows port 8001
3. Use ngrok tunnel for testing
4. Check API key is correct

### Webhook returns 401 Unauthorized
- Verify `X-API-Key` header is set in Zapier
- Check API key matches server configuration
- Ensure header name is exact: `X-API-Key` (case-sensitive)

### Slow responses
- CrewAI crews can take 30-120 seconds
- Increase Zapier webhook timeout (default 30s)
- Consider async processing with webhooks for long-running tasks

---

## 📊 Monitoring

### View Server Logs
```bash
# View real-time logs
tail -f ~/crewai-specialists/webhook_server.log

# Search for errors
grep ERROR ~/crewai-specialists/webhook_server.log
```

### Check API Health
```bash
# Health check
curl http://192.168.68.88:8001/health

# Should return:
# {"status": "healthy", "service": "WalterSignal CrewAI Webhook Server"}
```

---

## 🚀 Next Steps

1. **Test locally first** - Verify endpoints work before connecting Zapier
2. **Create your first Zap** - Start with lead enrichment workflow
3. **Monitor performance** - Track execution times and success rates
4. **Scale up** - Add more crew types and workflows as needed

---

## 📝 Notes

- Server runs on port **8001** (to avoid conflicts with other services)
- API key can be changed in `.env` file
- Interactive API docs available at `/docs` endpoint
- All webhooks return standardized JSON responses

---

**Created:** 2025-11-12
**Version:** 1.0.0
**Status:** Ready for testing
