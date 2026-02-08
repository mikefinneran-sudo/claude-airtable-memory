# Working Context

**Last Updated**: 2026-02-08

---

## Current Session

**Project**: DGX Utilization & Data Sovereignty — Tech Stack Evaluation
**Status**: Phases 1-4 complete. NAS purchase (Phase 5) deferred to next month.

---

## What We Did (2026-02-08)

### Phase 1: ComfyUI on DGX
- Installed ComfyUI v0.12.3 at `~/ComfyUI/` with PyTorch 2.10+cu130
- Running as systemd service: `systemctl --user status comfyui` (port 8188)
- SDXL checkpoint downloaded (6.5GB). FLUX-dev needs HuggingFace login.
- Rewrote `replicate_tool.py` → ComfyUI local first, Replicate cloud fallback

### Phase 2: SearXNG + Ollama
- SearXNG Docker deployed on port 8890 (`~/searxng/`)
- Rewrote `waltersignal-news-updater.py` → SearXNG+Ollama first, Perplexity fallback
- Test run successful: 6 results from SearXNG, Ollama curated 5, deployed to Lightsail

### Phase 3: DGX Cleanup
- SGLang killed (port 30000), n8n stopped (0 workflows)
- Ollama models unloaded from VRAM (load on-demand)
- Neo4j, Vaultwarden, 1Password Connect kept

### Phase 4: Embedding Audit
- 100% local verified: ChromaDB + nomic-embed-text-v1.5, zero cloud embedding calls

### Files Modified
- `~/Code/WalterSignal/waltersignal-crews/tools/replicate_tool.py` — ComfyUI+Replicate
- `~/.claude/scripts/waltersignal-news-updater.py` — SearXNG+Ollama+Perplexity
- `~/.claude/projects/-Users-mikefinneran/memory/MEMORY.md` — DGX services section

### DGX Changes (192.168.68.62)
- `~/ComfyUI/` — installed, systemd service enabled
- `~/searxng/` — docker-compose, settings.yml
- `~/.config/systemd/user/comfyui.service` — created
- SGLang container removed, n8n stopped

---

## Pending Tasks

### Immediate
- [ ] HuggingFace login on DGX → download FLUX-dev checkpoint
- [ ] Test ComfyUI SDXL generation via API end-to-end

### Carried Forward
- GTM Expert: Re-train with packing=False + 5 epochs
- Lead Magnet Deploy — scp to DGX, fix nginx port, deploy site
- EventFlow Instantly Launch — import CSV, configure, send
- Deploy & test batch_enrich — scp to DGX, test --dry-run

### Phase 5 (Next Month)
- UGREEN NAS DH2300 + 2x4TB IronWolf (~$370)
- Setup RAID 1, Time Machine, S3 Hyper Backup

---

## Quick Resume

```
DGX stack optimized. ComfyUI on :8188 (SDXL ready, FLUX needs HF login).
SearXNG on :8890 + Ollama replacing Perplexity for batch search.
SGLang killed, n8n stopped. All embeddings verified local.
replicate_tool.py and news updater rewritten with local-first + cloud fallback.
```
