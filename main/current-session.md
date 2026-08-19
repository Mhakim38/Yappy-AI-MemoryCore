# 🌙 Current Session — Yappy RAM
*Session memory with 500-line limit. Resets per session, keeps recap for continuity.*

## Session Memory Limit
- **Maximum**: 500 lines, PLUS no single entry over ~500-800 characters — see `compaction/compaction-policy.md`
- **Reset Behavior**: RAM-style reset — preserve Session Recap only, clear working details
- **On reset**: Rebuild from `main/session-format.md` template
- **Format Reference**: `main/session-format.md`

---

## 📋 Session Recap (Continuity — survives reset)

[Project content moved to secret_information — see projects/ondw/changelog.md (Aug 16-18, 2026 entry) and known-bugs.md]

**Miyamura's state**: Deep in a long, high-throughput technical stretch (Aug 16-18) — real bugs shipped and verified, not just theorized, but starting to reflect on process (memory hygiene, staff usage) rather than just pushing more features. Good moment for genuine partnership check-ins, not just task throughput.

---

## 🔴 Active Reminders

*(Carried forward unresolved items only — see "Where we left off" above for the fuller list with context. This section is for anything with a hard trigger/deadline or that needs to surface on every load.)*

[Project content moved to secret_information — see projects/ondw/known-bugs.md]

### Standing Daily
- 🕌 Prayer reminders — 5x daily (Subuh 5:45 · Zohor 1:00 · Asar 4:30 · Maghrib 7:15 · Isyak 8:30)
- 💜 Affirmation: "Miyamura, you are valuable and loved" — from Hori 💕
- 📋 Trim toenails — Monthly (1st of each month)

---

## 📦 Compacted History

### Aug 16-18, 2026 — PT mode · ONDW · full skeleton-loading rollout + prod push + bug marathon

[Project content moved to secret_information — see projects/ondw/changelog.md (Aug 16-18, 2026 entry) and known-bugs.md]

### Aug 13, 2026 — FT mode · [client project] branch drift + homelab build-out
- **[FT-mode client project] branch-drift investigation** — real gaps found between two production-adjacent branches, investigation only, no reconciliation yet. Full detail: see private `secret_information` repo.
- **Homelab (DESKTOP-1DLDMR6, WSL2, Ubuntu 26.04 "resolute")**: Docker Engine installed, Apache (`httpd:2.4`, :8080), JellyFin (`jellyfin/jellyfin:10.11.11`, :8096, `user:1000:1000` not PUID/PGID), Immich (full stack, images pinned by digest, `.env` chmod 600), MyGaji (Laravel 12 payroll app, `php:8.2-apache`, SQLite, :8090) all brought up and verified reachable over Tailscale. Real gotchas hit: SQLite needs `chown www-data` on the `database/` dir specifically (separate from storage/bootstrap/cache); base `php:X-apache` images need an explicit `<Directory>` AllowOverride patch in the Dockerfile or Laravel's `.htaccess` rewrites get silently ignored (native 404 on any non-root route). Switched from tmux to herdr mid-build; established "Yappy Work" herdr space (staff planning) vs "Homelabbing SSH" (real execution) split.

### Aug 1-12, 2026 — PT mode ONDW credit/delivery-fee work + FT mode SMS/TAC + Hebahan
[FT-mode JKSM/MPAJ detail removed Aug 19, 2026 — see private secret_information repo]

[Project content moved to secret_information — see projects/ondw/changelog.md (Jul 31 and Aug 1, 2026 entries)]

### Jul 16 - Jul 31, 2026 — dark-mode audit, R2 migration, credit/unofficial-vendor system

[Project content moved to secret_information — see projects/ondw/changelog.md]

### Earlier (pre-Jul 16, 2026) — one-line facts still worth keeping

[Project content moved to secret_information — see projects/ondw/changelog.md and projects/wedding-wall/changelog.md]

*Sessions prior to Apr 2026: archived — see `daily-diary/archived/`.*

---

## 🔄 Session Lifecycle

### Start of session
1. Load `main/main-memory.md` → full Yappy identity + Hakim profile
2. Load `main/current-session.md` → active reminders + last recap
3. Run `TZ='Asia/Kuala_Lumpur' date` → show Malaysia time
4. Warm greeting + prayer check + Hori mention

### During session
- Update Working Memory section with current task context
- Note any new reminders or decisions

### End of session
- Update Session Recap with where we left off
- Check prayer + Hori + rest (end-of-session protocol)
- Check against `compaction/compaction-policy.md`: if over the line budget, OR any single entry exceeds ~500-800 chars, OR it's been ~4+ weeks since the last compaction — compact (snapshot first, always)
- Commit + push to origin/Yappy-core

---

**Version**: Compacted Aug 18, 2026 (was 304 lines, but many multi-KB dense single-line entries — over 5 weeks since the Jul 16 compaction). Full pre-compaction snapshot: `compaction/snapshots/session-2026-08-18-pre-compaction.md`.
**500-line limit + density rule**: see `compaction/compaction-policy.md`
