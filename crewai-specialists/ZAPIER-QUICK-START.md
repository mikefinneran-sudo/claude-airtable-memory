# Zapier Integration - Quick Start

## 🚀 Start Server (on DGX)

```bash
ssh mikefinneran@192.168.68.88
cd ~/crewai-specialists
./start-zapier-server.sh
```

Server runs on: **http://192.168.68.88:8001**

---

## 🧪 Test Locally

```bash
# From your Mac
cd ~/crewai-specialists
./test-webhook.sh
```

Or manually:
```bash
curl http://192.168.68.88:8001/health
```

---

## 🔗 Zapier Setup (3 Steps)

### 1. Create Zap
- Trigger: Your choice (Google Sheets, Airtable, etc.)
- Action: **Webhooks by Zapier** → POST

### 2. Configure Webhook
- **URL:** `http://192.168.68.88:8001/webhook/lead-enrichment`
- **Headers:**
  ```
  Content-Type: application/json
  X-API-Key: waltersignal-dev-key-12345
  ```
- **Data:**
  ```json
  {
    "company_name": "{{trigger.company}}",
    "website": "{{trigger.website}}",
    "industry": "{{trigger.industry}}"
  }
  ```

### 3. Test & Activate
- Send test → Should return JSON with enriched data
- Turn on Zap

---

## 📍 Available Endpoints

| Endpoint | Purpose | Input |
|----------|---------|-------|
| `/webhook/lead-enrichment` | Enrich company data | company_name, website, industry |
| `/webhook/research` | Research topics | topic, depth |
| `/webhook/design` | Design tasks | task_type, description |
| `/health` | Health check | None |

---

## 🔒 Security

**Default API Key:** `waltersignal-dev-key-12345`

**Change it:**
```bash
export ZAPIER_API_KEY="your-secure-key-here"
```

---

## 📚 Full Documentation

See: `ZAPIER-INTEGRATION-GUIDE.md`

---

## 🐛 Troubleshooting

**Server not responding?**
```bash
# Check if running
ssh mikefinneran@192.168.68.88 "ps aux | grep zapier"

# Restart
ssh mikefinneran@192.168.68.88
cd ~/crewai-specialists
./start-zapier-server.sh
```

**Zapier getting 401?**
- Check `X-API-Key` header is set
- Verify key matches server configuration

---

**Status:** ✅ Ready to use
**Version:** 1.0.0
**Created:** 2025-11-12
