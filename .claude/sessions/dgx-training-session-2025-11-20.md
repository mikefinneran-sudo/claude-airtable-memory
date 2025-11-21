# DGX Training & Data Migration Session
**Date:** 2025-11-20
**Duration:** ~6 hours
**Status:** Google Drive migration complete, Training troubleshooting in progress

---

## Session Summary

### ✅ Completed Tasks

#### 1. Created Training Dataset from Obsidian Vault
- **Location:** `~/crewai-specialists/training_data.jsonl`
- **Size:** 9.83 MB
- **Content:** 3,399 training examples from 909 markdown files
- **Source:** Entire Obsidian Vault (`~/Documents/ObsidianVault/`)
- **Format:** Instruction-following pairs for CrewAI agent training

#### 2. Google Drive → DGX Migration
- **Source:** Google Drive (mike.finneran@gmail.com)
- **Destination:** `/mnt/models/google-drive-archive/` on DGX (192.168.68.62)
- **Total Size:** 10GB extracted
- **Files Transferred:** 9,464 files
- **Breakdown:**
  - Google Drive: 2.6GB
  - Google Photos: 3.2GB
  - Gmail: 2.9GB
  - YouTube: 368MB
  - Nest: 448KB
- **Sync Script:** `~/sync-gdrive-to-dgx.sh`
- **Status:** Complete, compressed archives deleted

#### 3. Docker & Unsloth Setup
- **Base Image:** `nvcr.io/nvidia/pytorch:25.09-py3`
- **Custom Image:** `unsloth-ready`
- **Features:**
  - PyTorch 2.9.0a0 with CUDA 13.0
  - Unsloth 2025.11.3
  - All dependencies installed
  - CUDA verified working
- **Location:** DGX at 192.168.68.62

#### 4. GB10 GPU Specifications Confirmed
- **Model:** NVIDIA GB10 (Blackwell architecture)
- **Unified Memory:** 128GB (shared CPU/GPU)
- **Capabilities:** Can fine-tune 70B models, run inference on 200B models
- **Memory Type:** LPDDR5X-9400 (256-bit bus, ~301 GB/s bandwidth)
- **Compute:** ~31 TFLOPS FP32, 1 PFLOP sparse FP4

---

## ⚠️ In Progress / Issues

### Training Attempt - Llama 3.1:70B
- **Status:** Failed
- **Issue:** Container exited with code 1, insufficient logs
- **Attempted Solutions:**
  1. First attempt: No CPU offloading → "Not enough GPU RAM" error
  2. Second attempt: Added `llm_int8_enable_fp32_cpu_offload=True` → Silent failure
- **Scripts Created:**
  - `~/crewai-specialists/finetune_llama.py` (original)
  - `~/crewai-specialists/finetune_llama_gb10.py` (with CPU offload)
  - `~/crewai-specialists/monitor_training_gb10.sh` (monitoring)

### Root Cause Analysis Needed
- Container logs show only PyTorch banner, no actual training output
- Need to debug why script isn't producing logs
- May need to test with smaller model first (Qwen 2.5:14B or Llama 3.1:8B)

---

## Files Created This Session

### Training Scripts
```
~/crewai-specialists/
├── create_training_dataset.py          # Dataset generator
├── training_data.jsonl                 # 3,399 examples (9.83 MB)
├── finetune_llama.py                   # Original training script
├── finetune_llama_gb10.py              # GB10-optimized with CPU offload
├── monitor_training.sh                 # Original monitor
└── monitor_training_gb10.sh            # GB10 monitor
```

### Sync Scripts
```
~/sync-gdrive-to-dgx.sh                # Google Drive → DGX sync
/tmp/gdrive-sync.log                   # Sync progress log
```

### On DGX (192.168.68.62)
```
/mnt/models/google-drive-archive/
├── extracted/Takeout/
│   ├── Drive/                         # 2.6GB
│   ├── Google Photos/                 # 3.2GB
│   ├── Mail/                          # 2.9GB
│   ├── YouTube and YouTube Music/     # 368MB
│   └── Nest/                          # 448KB
└── [original files from Drive sync]

~/training_data.jsonl                  # Uploaded training data
~/finetune_gb10.py                     # Training script
```

### Docker Images
```
unsloth-dgx-spark    # First attempt (Triton build failed)
unsloth-cuda         # Second attempt (incomplete deps)
unsloth-ready        # Final working image
```

---

## Key Commands Reference

### Monitor Training
```bash
~/crewai-specialists/monitor_training_gb10.sh
```

### Check Google Drive Data
```bash
ssh mikefinneran@192.168.68.62 "du -sh /mnt/models/google-drive-archive/extracted/Takeout/*"
```

### Docker Container Management
```bash
# List containers
ssh mikefinneran@192.168.68.62 "docker ps -a"

# View logs
ssh mikefinneran@192.168.68.62 "docker logs llama-training"

# Remove failed container
ssh mikefinneran@192.168.68.62 "docker stop llama-training && docker rm llama-training"
```

### DGX Storage
```bash
ssh mikefinneran@192.168.68.62 "df -h"
# Main: 2.4T free on /
# External: 3.4T free on /mnt/models
```

---

## Next Steps

### Immediate (Next Session)
1. **Debug 70B training failure**
   - Try running script interactively (not in background)
   - Check if model downloads successfully
   - Verify dataset loads correctly

2. **Alternative: Start with smaller model**
   - Qwen 2.5:14B (9GB) - Good balance
   - Llama 3.1:8B (4.4GB) - Guaranteed to work
   - Test end-to-end pipeline before returning to 70B

### Medium Term
3. **Batch Training Setup**
   - Train multiple models overnight
   - Compare quality across model sizes
   - Deploy best performers to Ollama

4. **RAG System for Google Data**
   - Index Gmail (2.9GB) for email search
   - Index Drive documents for knowledge retrieval
   - Integrate with CrewAI agents

### Long Term
5. **CrewAI Integration**
   - Test fine-tuned models with existing crews
   - Update crew configs to use local fine-tuned models
   - Benchmark against base models

---

## Environment Details

### Local (Mac)
- **Working Directory:** `~/crewai-specialists/`
- **Obsidian Vault:** `~/Documents/ObsidianVault/` (909 markdown files)
- **Google Drive:** Synced at `~/Library/CloudStorage/GoogleDrive-mike.finneran@gmail.com/`

### DGX Spark (192.168.68.62)
- **OS:** Ubuntu (ARM64)
- **GPU:** NVIDIA GB10 (128GB unified memory)
- **CUDA:** 13.0
- **Driver:** 580.95.05
- **External Storage:** `/mnt/models/` (3.4TB free)
- **Ollama:** v0.12.9 (20+ models installed)

### Docker Environment
- **Base:** `nvcr.io/nvidia/pytorch:25.09-py3`
- **PyTorch:** 2.9.0a0+50eac811a6.nv25.09
- **Unsloth:** 2025.11.3
- **Transformers:** 4.57.1
- **TRL:** 0.23.0
- **CUDA:** Verified working

---

## Lessons Learned

1. **GB10 Memory Architecture**
   - 128GB unified memory requires CPU offloading for 70B models
   - `llm_int8_enable_fp32_cpu_offload=True` and `device_map="auto"` required
   - VRAM stats not exposed via nvidia-smi (shows "Not Supported")

2. **Google Drive Sync**
   - `.gdoc` files are just 178-byte pointers
   - Actual data in Takeout archives
   - rsync works well for large transfers (80-100 MB/s)
   - Always extract and verify before deleting archives

3. **Docker for ML Training**
   - NVIDIA's PyTorch images include optimized CUDA builds
   - Installing packages can overwrite GPU-enabled PyTorch with CPU version
   - Use `--no-deps` when possible to preserve base image packages
   - Container logs via `docker logs` may not capture all output

4. **Training Dataset Quality**
   - 3,399 examples from 909 files is substantial
   - Instruction-following format critical for CrewAI use case
   - Including entire Obsidian Vault provides domain knowledge

---

## Resources & Documentation

### Unsloth Documentation
- Official Dockerfile: `https://raw.githubusercontent.com/unslothai/notebooks/main/Dockerfile_DGX_Spark`
- GB10 support confirmed for 70B fine-tuning

### NVIDIA GB10 Specs
- Can fine-tune 70B models
- Can run inference on 200B models
- Two units can link for 405B models

### Scripts Repository
- All scripts saved in `~/crewai-specialists/`
- Session monitor scripts ready for next attempt

---

## Session End Status

**Completed:**
- ✅ Training dataset created (3,399 examples)
- ✅ Google Drive migrated to DGX (10GB)
- ✅ Docker environment configured
- ✅ GB10 capabilities verified

**Pending:**
- ⏸️ Llama 3.1:70B training (needs debugging)
- ⏸️ Model deployment to Ollama
- ⏸️ CrewAI integration testing

**Ready for Next Session:**
- Training data on DGX
- Docker image built and working
- All scripts in place
- Google data extracted and organized
