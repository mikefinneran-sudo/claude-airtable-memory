#!/bin/bash
# Start Zapier Webhook Server on DGX

cd ~/crewai-specialists
source venv/bin/activate

# Set API key if not already set
if [ -z "$ZAPIER_API_KEY" ]; then
    export ZAPIER_API_KEY="waltersignal-dev-key-12345"
    echo "⚠️  Using default API key"
fi

echo "🚀 Starting WalterSignal Zapier Webhook Server..."
echo "📍 API Key: ${ZAPIER_API_KEY:0:10}..."
echo "🔗 Server URL: http://192.168.68.88:8001"
echo "📚 API Docs: http://192.168.68.88:8001/docs"
echo ""
echo "To stop: Ctrl+C or kill the process"
echo ""

python zapier_webhook_server.py
