# Session Memory - 2025-01-07

## Session Started
2025-01-07

## Resume After Restart

### DGX Drive Mapping (IN PROGRESS)
**Status:** macFUSE installed, needs restart

**After restart, run:**
```bash
brew install gromgit/fuse/sshfs-mac
mkdir -p ~/mnt/dgx
sshfs mikefinneran@192.168.68.62:/home/mikefinneran ~/mnt/dgx
```
Password: `Wally9381`

---

## Completed This Session

### 1. AeroDyne BT-1 Form Data Gathered
Indiana Business Tax Application ready to fill:
- Business: AERODYNE, LLC
- Address: 6730 Palmilla Ct, Fort Wayne, IN 46835
- SOS Control #: 202507071906060
- EIN: 39-3054211
- CEO: Michael J. Finneran
- Phone: 260-443-4043
- Business Type: Retail knife sales (NAICS 453998)
- Purpose: Sales tax registration

### 2. Vault Cleanup - CrewAI Folders
**Confirmed NOT in use:** Both `crewai-specialists` folders were inactive
- Old training materials, stale documentation
- Referenced wrong IP (192.168.68.81 vs current 192.168.68.62)
- Active CrewAI code lives in `/[1] WalterSignal/Code/waltersignal-crews/`
**User cleaned up the folders**

### 3. Discovered Blade Mafia Project
New Next.js e-commerce platform in `/blade-mafia/`:
- Stack: Next.js 16, React 19, Supabase, Stripe, Tailwind
- Business: Group buy platform for premium knives
- Membership: Standard ($9.99/mo, Cost+10%), Elite ($19.99/mo, Cost+5%)

---

## Previous Session Context
- Edge Collective knife club MVP (~/edge-collective/)
- Principal Crafts website (principalcrafts.com) - LIVE
- WalterSignal Gamma presentations

---

*Session saved: 2025-01-07*
