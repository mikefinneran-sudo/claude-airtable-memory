#!/bin/bash
# Monitor Llama 3.1:70b fine-tuning on DGX

echo "=== CrewAI Training Academy - Live Monitor ==="
echo ""

ssh mikefinneran@192.168.68.62 "docker exec unsloth-training tail -100 /tmp/training.log"

echo ""
echo "=== GPU Status ==="
ssh mikefinneran@192.168.68.62 "docker exec unsloth-training nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader"

echo ""
echo "=== Process Status ==="
ssh mikefinneran@192.168.68.62 "docker exec unsloth-training ps aux | grep python | grep -v grep"
