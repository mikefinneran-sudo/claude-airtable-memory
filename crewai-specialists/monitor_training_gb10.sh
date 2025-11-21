#!/bin/bash
# Monitor Llama 3.1:70b fine-tuning on GB10

echo "=== GB10 Training Monitor - Llama 3.1:70B ==="
echo ""

# Training log
echo "=== Training Log (last 30 lines) ==="
ssh mikefinneran@192.168.68.62 "docker exec llama-training tail -30 /workspace/training.log 2>/dev/null || echo 'Log not ready yet'"

echo ""
echo "=== Process Status ==="
ssh mikefinneran@192.168.68.62 "docker exec llama-training ps aux | grep python | grep -v grep"

echo ""
echo "=== System Memory ==="
ssh mikefinneran@192.168.68.62 "docker exec llama-training free -h"

echo ""
echo "=== GPU Status ==="
ssh mikefinneran@192.168.68.62 "nvidia-smi --query-gpu=utilization.gpu,temperature.gpu --format=csv,noheader"
