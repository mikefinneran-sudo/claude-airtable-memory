# DGX Spark GB10 PyTorch Setup Guide

## Hardware Specs
- **GPU:** NVIDIA GB10 (SM_121 architecture)
- **CUDA:** 13.0
- **Unified Memory:** 128GB (shared CPU/GPU)
- **Challenge:** Newest hardware, limited official PyTorch support

## PyTorch Compatibility Issues

### The Problem
PyTorch compatibility errors on DGX Spark are common due to:
- Mismatches between PyTorch, CUDA version, and GB10 hardware
- Official builds lag support for newest CUDA 13.0 and SM_121 architecture
- Can cause GPU unavailability or runtime crashes

### Solution: Use NVIDIA Container or Nightly Builds

**Option 1: NVIDIA PyTorch Container (RECOMMENDED)**
```bash
docker run --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 \
  -v ~/crewai-specialists:/workspace \
  nvcr.io/nvidia/pytorch:25.09-py3 \
  bash
```

**Why this works:**
- Pre-configured with GB10-compatible PyTorch 2.9.0a0
- CUDA 13.0 support built-in
- NVIDIA optimizations included
- Flash Attention 2 enabled

**Option 2: Install PyTorch Nightly (if not using container)**
```bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu130
```

### Verify Installation
```python
import torch
print("Torch:", torch.__version__)
print("CUDA:", torch.version.cuda)
print("GPU available:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0))
```

**Expected output:**
```
Torch: 2.9.0a0+50eac811a6.nv25.09
CUDA: 13.0
GPU available: True
GPU: NVIDIA GB10
```

## Fine-Tuning Setup (Lessons Learned)

### Model Size Constraints
- **70B models:** Fail even with 4-bit quantization (BitsAndBytes doesn't recognize unified memory)
- **8B models:** Work perfectly with 4-bit quantization
- **Recommendation:** Start with 8B, scale up if needed

### Device Map Configuration
**DON'T use:** `device_map="auto"` - Fails on GB10
**DO use:** `device_map={"": 0}` - Forces GPU placement

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Meta-Llama-3.1-8B-bnb-4bit",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
    device_map={"": 0},  # Force GPU placement
)
```

### Precision Settings
GB10 uses **bfloat16** natively:
```python
training_args = TrainingArguments(
    fp16=False,      # Don't use fp16
    bf16=True,       # Use bfloat16
    # ... other args
)
```

## Known Issues & Workarounds

### Issue: "Some modules dispatched on CPU or disk"
**Error:**
```
ValueError: Some modules are dispatched on the CPU or the disk. 
Make sure you have enough GPU RAM to fit the quantized model.
```

**Solution:** Use `device_map={"": 0}` instead of `"auto"`

### Issue: "torch has no attribute 'int1'"
**Cause:** PyTorch version mismatch with torchao
**Solution:** Use NVIDIA container (already has compatible versions)

### Issue: Flash Attention errors
**Cause:** Flash Attention submodules may not support SM_121
**Workarounds:**
- Use NVIDIA container (has patched version)
- Disable Flash Attention if needed
- Wait for official Flash Attention 3 release

## Memory Considerations

**Unified Memory Architecture:**
- 128GB total system memory
- ~96GB available to GPU
- No traditional VRAM distinction
- BitsAndBytes may not recognize this properly

**Practical Limits:**
- 8B 4-bit: ~4-5GB (✅ Works great)
- 70B 4-bit: ~35-40GB (❌ Rejected by transformers library)
- Full 16-bit models: Not recommended

## Training Performance

**Achieved Results (Llama 3.1:8B):**
- Training time: 12.3 minutes (100 steps)
- Dataset: 3,399 examples
- Speed: ~8 seconds per step
- GPU utilization: 70%
- Final loss: 1.474

## Best Practices

1. **Always use NVIDIA container** for GB10 compatibility
2. **Start with 8B models** before attempting larger ones
3. **Use device_map={"": 0}** for model loading
4. **Enable bf16**, not fp16
5. **Monitor memory usage** - unified memory can be tricky
6. **Check forums regularly** - GB10 ecosystem evolving rapidly

## Additional Resources

- NVIDIA PyTorch Container: https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch
- DGX Spark Documentation: https://docs.nvidia.com/dgx/
- Unsloth Documentation: https://github.com/unslothai/unsloth
- Flash Attention Updates: https://github.com/Dao-AILab/flash-attention

## Update Log

**2025-11-20:** Initial setup completed
- Successfully fine-tuned Llama 3.1:8B on CrewAI dataset
- Confirmed NVIDIA container works with GB10
- Documented device_map and precision requirements
