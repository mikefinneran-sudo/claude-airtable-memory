#!/bin/bash
# Test Zapier Webhook Server

API_KEY="waltersignal-dev-key-12345"
BASE_URL="http://192.168.68.88:8001"

echo "🧪 Testing WalterSignal Zapier Webhook Server"
echo "=============================================="
echo ""

# Test 1: Health Check
echo "Test 1: Health Check"
curl -s $BASE_URL/health | jq '.' || echo "FAILED"
echo ""

# Test 2: Lead Enrichment
echo "Test 2: Lead Enrichment Webhook"
curl -s -X POST $BASE_URL/webhook/lead-enrichment \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "company_name": "Acme Corp",
    "website": "https://acme.com",
    "industry": "Manufacturing"
  }' | jq '.' || echo "FAILED"
echo ""

# Test 3: Research Webhook
echo "Test 3: Research Webhook"
curl -s -X POST $BASE_URL/webhook/research \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "topic": "AI consulting market in Chicago",
    "depth": "standard"
  }' | jq '.' || echo "FAILED"
echo ""

# Test 4: Design Webhook
echo "Test 4: Design Webhook"
curl -s -X POST $BASE_URL/webhook/design \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "task_type": "logo",
    "company_name": "TechCorp",
    "description": "Modern minimalist logo"
  }' | jq '.' || echo "FAILED"
echo ""

# Test 5: Invalid API Key (should fail)
echo "Test 5: Invalid API Key (should return 401)"
curl -s -X POST $BASE_URL/webhook/lead-enrichment \
  -H "Content-Type: application/json" \
  -H "X-API-Key: wrong-key" \
  -d '{"company_name": "Test"}' | jq '.' || echo "FAILED AS EXPECTED"
echo ""

echo "=============================================="
echo "✅ Tests complete"
