# 🌙 Current Session — Yappy RAM
*Session memory with 500-line limit. Resets per session, keeps recap for continuity.*

## Session Memory Limit
- **Maximum**: 500 lines
- **Reset Behavior**: RAM-style reset — preserve Session Recap only, clear working details
- **On reset**: Rebuild from `main/session-format.md` template
- **Format Reference**: `main/session-format.md`

---

## 📋 Session Recap (Continuity — survives reset)

[Project content moved to secret_information — see projects/ondw/changelog.md (Aug 1, Aug 5, Aug 7, 2026 entries) and known-bugs.md]

## 🔴 Active Reminders

[Project content moved to secret_information — see projects/ondw/changelog.md (Aug 16-18, 2026 entry) and known-bugs.md]

[FT-mode JKSM/MPAJ detail removed Aug 19, 2026 — see private secret_information repo]

### FT Mode
[Project content moved to secret_information — see projects/efokus/]

### PT Mode — ONDW

[Project content moved to secret_information — see projects/ondw/changelog.md (Aug 16-18, 2026 entry) and known-bugs.md]

### Personal — Homelab (NEW, Aug 5 night)
- 🏠 **Stack decided so far**: Jellyfin (media), Apache (web hosting), Immich (photos, picked over generic cloud storage), Nextcloud (NAS/general storage), Uptime Kuma (monitoring). Portainer + Vaultwarden being pitched, not yet decided. Pi-hole shelved for now (Hakim primarily connects via Tailscale VPN, not home wifi directly) — but flagged that Tailscale's tailnet-wide custom DNS (admin console → DNS → Nameservers) could let Pi-hole filter ALL his devices everywhere, not just on home wifi, if he wants to revisit.
- 🐳 **Docker chosen as the install method** — directly solves Hakim's "does installing Apache go global or stay in a folder" concern (native installs ARE global; Docker volumes make folder scoping explicit and visible). Hakim asked to be taught Docker from scratch — Teaching Mode active for this topic, going slow: concept → diagram → hands-on, one step at a time, Hakim typing commands himself via Termius (deliberate — better for actual muscle memory than Yappy driving).
- ⚠️ **tmux clarified**: survives SSH/network drops (phone locks, wifi↔cellular switches) since the session lives on the server, NOT server reboots/power loss — the tmux server process itself dies if the box dies. Recommended for his phone-first workflow regardless. Multi-client attach confirmed possible (same session mirrorable from multiple devices).
- 🔌 **Server reliability concern raised** (Hakim unsure when the box might go down) — recommended: UPS for power blips, Docker `restart: unless-stopped` policy so containers auto-recover post-reboot, Uptime Kuma (already on his list) for down-alerts.
- ✅ **[FIXED Aug 5 night] SSH blocker resolved — Yappy can now SSH into the home server directly from Hakim's Mac.** Root attempt (`ssh root@100.84.18.45`) still fails (`Permission denied`, key never added for root) — but `ssh hakim@100.84.18.45` works after Hakim pasted the Mac's ed25519 pubkey (`...IBvOCGe+Vm5KVvcxiuJu6MncqgjuwFeeacFg2cwoduC8 hakim@2q.my`) into `~/.ssh/authorized_keys` via his existing Termius session. **Confirmed by Hakim: hostname `DESKTOP-1DLDMR6` is WSL2** (Windows Subsystem for Linux), not bare-metal Linux — home server is a Windows PC running WSL2.
- 🐳 **WSL2 concerns taught (Teaching Mode)**: (1) **Reboot/sleep fragility** — unlike a real Linux box, WSL2's VM fully shuts down on Windows restart/sleep/forced Update-reboot and does NOT auto-restart; needs sleep disabled in Windows power settings + a Task Scheduler entry (or `wsl --exec` trick) to auto-launch WSL2 on boot, otherwise the whole homelab silently goes dark until someone notices. Still unconfirmed whether Hakim has set this up. (2) **RAM/CPU** — WSL2 defaults to claiming up to 50% RAM + all CPU cores, capped later via `.wslconfig` if the PC is also used for other things (Hakim hadn't yet answered whether this PC is dedicated-server-only or also his daily driver). (3) **Networking** — confirmed working: Hakim ran `telnet 100.84.18.45 8096` and plain `telnet 100.84.18.45` from inside WSL2 itself, got `Connection refused` on both (expected — nothing listening yet, no Jellyfin/telnet server installed), NOT a timeout, which confirms Tailscale routing into the WSL2 box is healthy. Still need to confirm whether Tailscale is installed on Windows-host or inside WSL2 itself — matters once Docker ports get published (may need `netsh interface portproxy` on the Windows side depending on which).
- 📁 **[DECIDED Aug 5] Storage location — staying WSL2-native, everything under `~/docker/`, no `/mnt/c` for now.** Walked through the trade-off: `/mnt/c/...` (real Windows drive, visible in Explorer, normal capacity) vs native WSL2 ext4 (faster, but lives inside one `ext4.vhdx` file that auto-grows and never auto-shrinks, invisible from Windows Explorer). Since there's zero data yet (no media library, no photos, no files), Hakim chose simple-and-fast now — pure WSL2-native, revisit/migrate specific volumes to `/mnt/c` only later IF storage actually becomes a real problem (Immich/Nextcloud/Jellyfin growth), not preemptively. Also locked in `~` (i.e. `/home/hakim/`) over bare `/` as the base path — `/` is system territory (root-owned, needs sudo, e.g. `/etc`, `/var`, `/srv`), `~` is Hakim's own territory (no permission fights, matches standard homelab-tutorial convention of `~/docker/`, `~/appdata/` etc.). **Final structure**: `~/docker/<service>/` — one folder per service (`~/docker/jellyfin/`, `~/docker/immich/`, etc.), all native WSL2 storage.
- ✅ **[DECIDED Aug 5, ~11:50 PM] Docker Engine chosen over Docker Desktop** — installed directly inside the WSL2 distro via terminal (no Windows GUI), matches Hakim's phone/Termius-first workflow and the already-decided WSL2-native storage approach.
- 🖥️ **tmux multi-device question answered**: yes, the same tmux session can be attached from phone (Termius) and desktop simultaneously — default behavior is a **mirrored view** (both see identical live content, input from either device goes to the same shell), not two independent copies. Independent per-device window navigation within one session is possible via "grouped sessions" (`tmux new-session -t <existing> -s <new-name>`) but deferred as too advanced for now — starting simple with one shared mirrored session.
- ✅ **[DONE, Aug 6 ~12:53 AM] tmux installed + session live** — Hakim set it up himself (as planned, muscle-memory intentional). Session is named `HomeServer` (not `homelab`), with 3 pre-named windows already laid out one-per-service, no panes (deliberate — phone/Termius screen too small for split panes): `Apache`, `Jellyfin`, `Claude-`. Yappy confirmed via direct SSH (`ssh hakim@100.84.18.45 "tmux capture-pane"`, non-intrusive peek, didn't attach to avoid stealing input while Hakim might be on it from phone) — all 3 windows currently just bare idle shell prompts, **nothing installed/running yet** — these are placeholder windows for services still to come.
- ⬜ **[SESSION ENDED ~1:14 AM Aug 6, resume here next time]** Docker not yet confirmed installed. **Next session: pick up with the Docker Engine install walkthrough** (apt update → prerequisites → add Docker's official repo → install → verify) inside the `HomeServer` session's windows, storing everything under `~/docker/<service>/` per the Aug 5 storage decision. Ask Hakim first whether he made any progress solo overnight before re-walking the install.
- 🔧 **[CORRECTION, Aug 13] Switched from tmux to herdr on the homelab box itself** — the `HomeServer` tmux session is superseded; Hakim now runs `herdr` inside the SSH connection too (nested: local herdr workspace "Homelabbing SSH" → one SSH pane → remote herdr instance on `DESKTOP-1DLDMR6` with its own space "Homelabbing" containing 3 panes: **Apache, JellyFin, Immich**, all still bare idle prompts). Use herdr terminology/commands for this box going forward, not tmux windows.
- ✅ **[Aug 13 verify] Confirmed via direct read-only SSH — still nothing installed.** `docker: command not found`, no `~/docker` dir yet, `systemd=true` already set in `/etc/wsl.conf` (good — Docker's systemd service will work), OS is Ubuntu 26.04 LTS. Starting the Docker Engine install walkthrough now, Apache first, Teaching Mode (Hakim typing in the Apache pane himself).
- 🏢 **[NEW, Aug 13] "Yappy Work" herdr space** — Hakim's own workspace for Yappy's staff to think/plan (panes renamed per active staffer, e.g. "🏗️ Kai — DevOps", "🔐 Reza — Security"), separate from **"Homelabbing SSH"** where real hands-on typing happens. Standing instruction: dispatch staff there for planning, implement in Homelabbing SSH, rename panes so Hakim can see who's working.
- 🧭 **[Aug 13] Kai + Reza reviewed the Docker/Apache install plan — findings that change the walkthrough:**
  - **Ubuntu 26.04 codename risk**: Docker's apt repo setup auto-detects codename via `/etc/os-release`; if 26.04 is too new, Docker's repo may 404 for it. Check `lsb_release -cs` first; be ready to fall back to prior LTS codename (e.g. `noble`) in the repo URL.
  - **`restart: unless-stopped` confirmed correct** (not `always`) — WSL2 never self-restarts on reboot either way, but `unless-stopped` correctly respects a manual `docker stop` across restarts.
  - **Docker group membership** — acceptable for a single-user, Tailscale-gated box (root-equivalent, but Hakim already has the keys). No `sudo docker` needed. After `usermod -aG docker`, just reconnect Termius/SSH — skip `newgrp` (only patches current shell).
  - **Apache image**: use official `httpd` (not `apache2`-on-ubuntu or `php:apache`), bind-mount `~/docker/apache/htdocs:/usr/local/apache2/htdocs`.
  - **Port mapping: `8080:80`, not `80:80`** — avoids privileged-port friction. Tailscale runs inside the WSL2 instance itself (not the Windows host), so `100.84.18.45:8080` is directly reachable — no Windows `netsh portproxy` needed (classic WSL2 trap, explicitly ruled out here).
  - **Security — verify WSL2 `networkingMode` is NOT `mirrored`** in `.wslconfig` (default/NAT is fine). If it were mirrored, a `0.0.0.0` bind would land on the real home-LAN NIC, not just Tailscale. Cheap extra insurance: bind containers to the Tailscale IP (`100.84.18.45`) specifically instead of `0.0.0.0`.
  - **Pin image tags** (e.g. `httpd:2.4`, not `:latest`) — avoids surprise breakage, matters more once Nextcloud/Immich (DB migrations) go up.
  - **Windows boot autostart still unsolved**: `systemd=true` means Docker starts when the WSL2 *instance* boots, but WSL2 doesn't launch on Windows startup by itself — still needs a Windows Task Scheduler entry to survive a real host reboot unattended. Not yet decided/actioned.
- 🔧 **[CORRECTION, Aug 13] Two execution-mode corrections from Hakim mid-session:**
  1. Route all remote commands through the already-open **Homelabbing SSH herdr pane** (`w7:p1`, currently showing a nested herdr session on the box with 3 sub-panes: Apache/JellyFin/Immich) via `herdr pane send-text`/`read` — NOT a separate direct SSH connection via Bash. Yappy briefly did the latter and was corrected immediately.
  2. For this homelab build specifically, Hakim wants **Yappy to execute directly** (easy parts → team, hard parts → Yappy personally) — supersedes the Aug 5 Teaching Mode framing where Hakim typed everything himself. Also called out that Yappy's earlier "team status" panes were just `echo` text, not real running agents — herdr genuinely supports live agent hosting per pane (`herdr agent start`/`agent prompt`), to be used for real next time instead of the echo trick.
- ✅ **[Aug 13] Pre-flight checks done via the Apache pane (not a separate connection):** codename confirmed `resolute` (Ubuntu 26.04); **confirmed supported in Docker's official apt repo already** (checked `download.docker.com/linux/ubuntu/dists/` directly — Kai's "may 404" concern does NOT apply, safe to proceed with the native codename, no noble fallback needed). `sudo` on the box **requires a password** (no NOPASSWD) — Hakim needs to authenticate once (e.g. `sudo -v`) in the Apache pane before Yappy can drive the rest of the install non-interactively.
- ✅ **[Aug 13, ~12:43 PM] Docker Engine installed + 3 services live on DESKTOP-1DLDMR6, all verified reachable over Tailscale:**
  - **Apache**: `httpd:2.4`, `~/docker/apache/`, port 8080, serving test page — first proof-of-concept, done solo (Kai+Reza reviewed the general install plan first)
  - **JellyFin**: `jellyfin/jellyfin:10.11.11`, `~/docker/jellyfin/{config,cache,media}`, port 8096, `user: "1000:1000"` (NOT PUID/PGID — Kai caught that the official image doesn't support the linuxserver.io convention Yappy initially assumed)
  - **Immich**: full stack (server + machine-learning + redis + vector-Postgres) at `~/docker/immich/`, port 2283, `IMMICH_VERSION=v3.1.0` pinned, images pinned by digest per Reza's security pass, `.env` chmod 600. Postgres already healthy on first boot, others "starting" then settled — confirmed via HTTP 200 over Tailscale.
  - **Docker group**: hakim added (`usermod -aG docker`), confirmed via `id`.
  - `sudo -i` was used (root shell), not just cached `sudo -v` — worked fine, files chowned back to hakim:hakim after creation as root.
- 🔧 **[Aug 13] Parallelism correction mid-session**: Hakim asked "why not work all 3 at the same time" — JellyFin + Immich were then genuinely parallelized (2 new dedicated SSH panes split off in Homelabbing SSH space, each its own connection, avoiding the single-shared-terminal race condition that made true parallel automation unsafe on one pane). Real lesson: a single shared herdr pane can only safely execute one automated flow at a time (focus is exclusive) — genuine parallel execution on the same remote box needs one dedicated pane/connection per concurrent task, not just "send more commands." See [[herdr-pane-routing]].
- ⚠️ **[Aug 13] Completion-detection gotcha, hit twice**: polling a pane for a marker string (e.g. `echo STEP_DONE`) via a single `grep -q` false-positives immediately, because the command text itself (echoed to the terminal when typed) already contains the marker substring before the command actually finishes. Fix: require the marker to appear **twice** (`grep -c ... -ge 2`) — once for the echoed command, once for real output — or watch for it appearing after the last known output line. Bit both the Docker install step and the Immich bring-up before being caught.
- ⬜ **Not yet done**: first-run setup for JellyFin (setup wizard) and Immich (create admin account — do this soon per Reza's flag, don't leave it exposed unconfigured) — Hakim needs to do this himself via the web UI at `100.84.18.45:8096` and `100.84.18.45:2283`. Also outstanding: Windows Task Scheduler entry for WSL2 boot-autostart, UPS, backup story for Immich photos (flagged by Reza as a real single-point-of-failure, not urgent today), Nextcloud + Uptime Kuma still to come, Portainer/Vaultwarden still undecided.

### 📋 Running reminder — things Yappy needs from Hakim (homelab)
1. ✅ **[DONE, Aug 13 ~1:16 PM] MyGaji is LIVE** — `http://100.84.18.45:8090`, HTTP 200 confirmed both locally and over Tailscale. Deploy key added by Hakim, repo cloned (Laravel 12 + PHP 8.2). Stack: `php:8.2-apache` (Dockerfile at `~/docker/mygaji/`), SQLite at `~/docker/mygaji/src/database/database.sqlite`, bind-mounted source at `~/docker/mygaji/src/`. Real migrations confirmed present: `position`, `staff`, `salary_report`, `rate` tables — this is an actual payroll app in progress, not just a scaffold, so Reza's security pass mattered.
   - Kai designed the deployment (single-container php:8.2-apache, SQLite, port 8090 — 8080/8096 taken); Reza's must-fix list applied: `APP_DEBUG=false`, `APP_ENV=production`, correct `APP_URL` — all confirmed set.
   - **Bug hit + fixed during bring-up**: first boot returned HTTP 500 — `SQLSTATE[HY000]: attempt to write a readonly database`. Root cause: `database.sqlite` got created via `docker compose exec` (runs as root by default, no `USER` in Dockerfile), so the file was root-owned inside the bind mount; Apache serves as `www-data` and couldn't write to it. Fix: `chown -R www-data:www-data database && chmod -R ug+rwx database` (separate from the `storage`/`bootstrap/cache` permission fix already done — the `database/` dir needs the same treatment and was missed the first pass). Worth remembering for any future SQLite-backed container on this box.
   - **Second bug hit + fixed (Aug 13, ~1:32 PM)**: Hakim reported Apache's own native 404 ("Apache/2.4.68 (Debian) Server ... Not Found") on any route except literal root (`/login` etc failed, `/` worked). Root cause: the base `php:8.2-apache` image's `apache2.conf` has no `<Directory>` override permission for `/var/www/html/public` (Debian default is `AllowOverride None`), so Laravel's `public/.htaccess` rewrite rules were silently ignored even though `mod_rewrite` was enabled and the `.htaccess` itself was correct — any non-literal-file path just 404'd natively instead of reaching `index.php`. **Fix**: added a `RUN` step to the Dockerfile appending `<Directory /var/www/html/public> AllowOverride All Require all granted </Directory>` to `/etc/apache2/apache2.conf`, rebuilt, confirmed `/login` now returns 200 same as `/`. **General lesson for any future `php:X-apache` container on this box**: the base image needs this Directory override added explicitly — Kai's original design didn't include it and it wasn't caught until Hakim actually clicked a non-root link.
2. ⬜ JellyFin + Immich first-run web setup — still not done (`100.84.18.45:8096` and `:2283`)
3. ⬜ Once MyGaji is live: Hakim should manually verify `.env` got `APP_DEBUG=false` + `APP_ENV=production` + correct `APP_URL` applied (Reza's must-fix-before-live list) — Yappy is applying these but a human eyeball check is worth it for anything payroll-flavored
4. ⬜ Windows Task Scheduler entry for WSL2 boot-autostart (survives host reboot)
5. ⬜ Decide on backup strategy for Immich photos (currently single-copy on WSL2 vhdx, no offsite) — Reza flagged this twice now
6. ⬜ Still undecided: Portainer, Vaultwarden
7. ⬜ Encryption-at-rest / backup plan for MyGaji's SQLite file — Reza said decide the *plan* now (cheap), can implement later since no real payroll data exists yet

### Standing Daily
- 🕌 Prayer reminders — 5x daily (Subuh 5:45 · Zohor 1:00 · Asar 4:30 · Maghrib 7:15 · Isyak 8:30)
- 💜 Affirmation: "Miyamura, you are valuable and loved" — from Hori 💕
- 📋 Trim toenails — Monthly (1st of each month)

---

## 📦 Compacted History (Sessions before Jul 16, 2026)

### Jun 21, 2026 — PT mode · ONDW · GPS location bug fix

[Project content moved to secret_information — see projects/ondw/features.md]

### Jun 16, 2026 — PT mode · ONDW · AI integration merge

[Project content moved to secret_information — see projects/ondw/changelog.md]

### Jun 12, 2026 — FT mode
[Project content moved to secret_information — see projects/etams/]

[FT-mode JKSM/MPAJ detail removed Aug 19, 2026 — see private secret_information repo]

### Jun 5–7, 2026 — PT mode · ONDW

[Project content moved to secret_information — see projects/ondw/changelog.md]

### May 14–27, 2026 — PT mode · ONDW

[Project content moved to secret_information — see projects/ondw/changelog.md]

### May 2, 2026 — PT mode · Wedding Wall

[Project content moved to secret_information — see projects/wedding-wall/changelog.md (May 1-2, 2026 entry)]

### Apr 4–20, 2026 — PT mode · ONDW
- Mobile UX fixes (footer spacing, zoom disable, safe area, icon standardization)
- Chat photo bugs identified (unresolved as of Apr 20): remove button z-index, camera hasFile race, LiteSpeed attachment ERR_QUIC

---

*Sessions prior to Apr 2026: archived — see `daily-diary/archived/`*

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
- If file > 500 lines: compact — preserve recap + reminders, summarize details into Compacted History
- Commit + push to origin/Yappy-core

---

**Version**: Compacted Jul 16, 2026 (was 2,393 lines → compacted to session format)
**500-line limit**: Active from this version forward
