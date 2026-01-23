#!/bin/bash
# ============================================================
# Master Automation Runner
# Runs all cost tracking automations
#
# Usage:
#   ./run-all-trackers.sh           # Run all
#   ./run-all-trackers.sh github    # Run specific tracker
#
# Schedule: Run weekly for cost tracking
# ============================================================

SCRIPT_DIR="/Users/mikefinneran/Documents/ObsidianVault/.scripts"
LOG_DIR="$SCRIPT_DIR/logs"
REPORT_DIR="/Users/mikefinneran/Documents/ObsidianVault"

# Create log directory
mkdir -p "$LOG_DIR"

# Timestamp for this run
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
MASTER_LOG="$LOG_DIR/master_run_$TIMESTAMP.log"

echo "============================================================" | tee "$MASTER_LOG"
echo "🤖 SpecialAgentStanny - Cost Tracking Automation" | tee -a "$MASTER_LOG"
echo "⏰ $(date)" | tee -a "$MASTER_LOG"
echo "============================================================" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"

# ============================================================
# Run Gmail Invoice Fetcher
# ============================================================
run_gmail() {
    echo "📧 Running Gmail Invoice Fetcher..." | tee -a "$MASTER_LOG"
    python3 "$SCRIPT_DIR/fetch-subscription-invoices.py" >> "$MASTER_LOG" 2>&1
    if [ $? -eq 0 ]; then
        echo "   ✅ Gmail invoices fetched" | tee -a "$MASTER_LOG"
    else
        echo "   ❌ Gmail fetcher failed" | tee -a "$MASTER_LOG"
    fi
    echo "" | tee -a "$MASTER_LOG"
}

# ============================================================
# Run GitHub Actions Tracker
# ============================================================
run_github() {
    echo "🐙 Running GitHub Actions Tracker..." | tee -a "$MASTER_LOG"
    python3 "$SCRIPT_DIR/github-actions-tracker.py" >> "$MASTER_LOG" 2>&1
    if [ $? -eq 0 ]; then
        echo "   ✅ GitHub Actions usage tracked" | tee -a "$MASTER_LOG"
    else
        echo "   ❌ GitHub tracker failed" | tee -a "$MASTER_LOG"
    fi
    echo "" | tee -a "$MASTER_LOG"
}

# ============================================================
# Run Anthropic API Tracker
# ============================================================
run_anthropic() {
    echo "🤖 Running Anthropic API Tracker..." | tee -a "$MASTER_LOG"
    python3 "$SCRIPT_DIR/anthropic-api-tracker.py" >> "$MASTER_LOG" 2>&1
    if [ $? -eq 0 ]; then
        echo "   ✅ Anthropic usage analyzed" | tee -a "$MASTER_LOG"
    else
        echo "   ❌ Anthropic tracker failed" | tee -a "$MASTER_LOG"
    fi
    echo "" | tee -a "$MASTER_LOG"
}

# ============================================================
# Run Perplexity API Tracker
# ============================================================
run_perplexity() {
    echo "🔍 Running Perplexity API Tracker..." | tee -a "$MASTER_LOG"
    python3 "$SCRIPT_DIR/perplexity-api-tracker.py" >> "$MASTER_LOG" 2>&1
    if [ $? -eq 0 ]; then
        echo "   ✅ Perplexity usage analyzed" | tee -a "$MASTER_LOG"
    else
        echo "   ❌ Perplexity tracker failed" | tee -a "$MASTER_LOG"
    fi
    echo "" | tee -a "$MASTER_LOG"
}

# ============================================================
# Main execution
# ============================================================

if [ $# -eq 0 ]; then
    # Run all trackers
    run_gmail
    run_github
    run_anthropic
    run_perplexity
else
    # Run specific tracker
    case $1 in
        gmail)
            run_gmail
            ;;
        github)
            run_github
            ;;
        anthropic)
            run_anthropic
            ;;
        perplexity)
            run_perplexity
            ;;
        *)
            echo "Usage: $0 [gmail|github|anthropic|perplexity]"
            exit 1
            ;;
    esac
fi

# ============================================================
# Summary
# ============================================================

echo "============================================================" | tee -a "$MASTER_LOG"
echo "🎉 Automation Run Complete" | tee -a "$MASTER_LOG"
echo "⏰ $(date)" | tee -a "$MASTER_LOG"
echo "============================================================" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"

echo "📊 Reports Generated:" | tee -a "$MASTER_LOG"
[ -f "$REPORT_DIR/subscription-invoices.md" ] && echo "   ✅ subscription-invoices.md" | tee -a "$MASTER_LOG"
[ -f "$REPORT_DIR/github-actions-usage.md" ] && echo "   ✅ github-actions-usage.md" | tee -a "$MASTER_LOG"
[ -f "$REPORT_DIR/anthropic-api-usage.md" ] && echo "   ✅ anthropic-api-usage.md" | tee -a "$MASTER_LOG"
[ -f "$REPORT_DIR/perplexity-api-usage.md" ] && echo "   ✅ perplexity-api-usage.md" | tee -a "$MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"

echo "📁 Log saved: $MASTER_LOG"
echo ""
echo "🚀 Next: Review reports in Obsidian Vault root"
