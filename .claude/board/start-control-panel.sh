#!/bin/bash
# Start Board Advisors Control Panel

echo "🎯 Starting Board Advisors Control Panel..."
echo ""

# Check if password is set
if [ -z "$WEB_PASSWORD" ]; then
    echo "⚠️  Warning: Using default password 'changeme'"
    echo "   Set WEB_PASSWORD environment variable for custom password"
    echo ""
fi

# Navigate to web-gui directory
cd ~/.claude/projects/persistent-memory/web-gui

# Check if port 5001 is available
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo "❌ Port 5001 is already in use"
    echo "   Kill the existing process or use a different port:"
    echo "   PORT=5002 python3 app.py"
    exit 1
fi

# Start the server
echo "✅ Starting server on http://localhost:5001"
echo ""
echo "📋 Access your Board of Directors at:"
echo "   http://localhost:5001"
echo ""
echo "🔐 Default login password: changeme"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

PORT=5001 python3 app.py
