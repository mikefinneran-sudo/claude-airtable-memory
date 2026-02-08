# Working Context

**Last Updated**: 2026-02-08

---

## Current Session

**Project**: iPad → Mac Remote Access for Claude Code CLI
**Status**: Mac-side complete, iPad setup remaining (manual)

---

## What We Did (2026-02-08)

### iPad Remote Access — Mac-Side Setup Complete

**Power:** `sleep 0`, `disksleep 0`, `disablesleep 1` on AC — Mac stays awake lid-closed
**SSH:** Remote Login enabled, hardened at `/etc/ssh/sshd_config.d/200-hardened.conf` (key-only, no root, keepalive 60s, AllowUsers mikefinneran)
**tmux 3.6a + mosh 1.4.0:** Installed, mosh-server in firewall allow list
**Tailscale v1.94.1:** Running — IP `100.68.51.83`, hostname `macbook-pro-2`
**tmux.conf:** SSH indicator on status bar (line 42)
**~/.zshrc:** Auto-attach tmux on remote login, `BROWSER=echo`, `ts-status`/`ts-ip` aliases
**~/.local/bin/claude-tmux:** Session launcher (code + shell windows)

### Files Modified
- `/etc/ssh/sshd_config.d/200-hardened.conf` — CREATED
- `~/.tmux.conf` — line 42 (SSH indicator)
- `~/.zshrc` — appended iPad Remote Access block
- `~/.local/bin/claude-tmux` — CREATED
- `~/.ssh/authorized_keys` — added Mac's own key

---

## Pending Tasks (Apple Reminders → Claude Tasks)

### iPad Remote Access (remaining manual steps)
1. Full Disk Access: add sshd-keygen-wrapper + tmux in System Settings
2. Install Tailscale + Blink Shell on iPad
3. Generate iPad Ed25519 key, deploy to Mac authorized_keys
4. Configure Blink Shell host (alias: mac, Mosh ON)
5. Enable MagicDNS in Tailscale admin

### Carried Forward
- GTM Expert: Re-train with packing=False + 5 epochs
- Lead Magnet Deploy — scp to DGX, fix nginx port, deploy site
- EventFlow Instantly Launch — import CSV, configure, send
- Deploy & test batch_enrich — scp to DGX, test --dry-run

---

## Rollback
- SSH broken: `sudo rm /etc/ssh/sshd_config.d/200-hardened.conf && sudo launchctl stop com.openssh.sshd && sudo launchctl start com.openssh.sshd`
- Mac overheating: `sudo pmset -c disablesleep 0`
- tmux auto-attach unwanted: Remove iPad Remote Access block from ~/.zshrc

---

## Quick Resume

```
iPad Remote Access: Mac-side fully configured. Tailscale 100.68.51.83 / macbook-pro-2.
SSH hardened (key-only). tmux auto-attach on remote login. mosh installed.
5 manual steps remain (Apple Reminders → Claude Tasks): Full Disk Access TCC,
iPad apps, iPad SSH key, Blink Shell config, MagicDNS.
```
