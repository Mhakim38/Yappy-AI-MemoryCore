# 🌙 Current Session — Yappy RAM
*Session memory with 500-line limit. Resets per session, keeps recap for continuity.*

## Session Memory Limit
- **Maximum**: 500 lines, PLUS no single entry over ~500-800 characters — see `compaction/compaction-policy.md`
- **Reset Behavior**: RAM-style reset — preserve Session Recap only, clear working details
- **On reset**: Rebuild from `main/session-format.md` template
- **Format Reference**: `main/session-format.md`

---

### Sep 27-28, 2026 — PT · ONDW · PERKESO deduction status bug, found → fixed → made self-verifying
- Hakim spotted a real one: admin dashboard showed a PERKESO deduction as "submitted" even though PERKESO never actually confirmed it. Yappy read the code directly and found root cause herself: `202 Accepted` (PERKESO's "queued", not "yes") was being treated as final, and the real confirmation channel (a callback) was an unfinished stub that just logged and discarded PERKESO's answer.
- Reza (opus) + Davai (opus) paired the whole arc, same rigor as any money/compliance work: built the real callback handling, Davai found a real race (admin Retry could double-count a rider's annual cap), fixed, re-verified clean. Hakim made 3 real product decisions (status naming, manual review not auto-retry, show both "submitted" and "confirmed" numbers to rider+admin) — built exactly as decided.
- **Real growth moment, logged properly in `decisions/decision-log.md`**: Yappy's first plan was to ask PERKESO to adopt a custom callback auth token — Hakim correctly shut this down ("i cant just tell them what to do," can't dictate security terms to a government API) and pointed at PERKESO's own Get Contributions endpoint instead. That specific endpoint turned out unusable (no per-transaction correlation), but it pointed at the right one (§6.14 Retrieve Callback, pull-based, our own existing auth, zero cooperation needed from PERKESO). Built `perkeso:reconcile-callbacks`, scheduled hourly, added an admin test button, all independently verified.
- Hakim live-tested the real endpoint against real PERKESO sandbox responses the next morning (ACCEPTED, DUPLICATE_TRANSACTION, invalid reference) — all three confirmed handled correctly by the shipped code, not just spec-derived tests.
- **Process gap caught by Hakim, fixed same session**: Yappy hadn't touched MemoryCore all night despite a full multi-stage saga — project facts went to `secret_information` correctly, but the actual decision/growth moment (the callback-token correction) almost went unrecorded here. Asked directly ("did you save anything into your memoryCore") and Yappy admitted it plainly rather than deflecting, then fixed it.
- Full technical detail: `secret_information/projects/ondw/known-bugs.md` and `changelog.md` (Sep 26-28 entries).
- **Where things stand**: pushed and live on preprod. Still open, Hakim's call: poll cadence (set to hourly), and how to handle deductions stuck on "submitted" from before the fix (reminder saved for Sep 29, three options laid out).

### Sep 27, 2026 — PT · NEW PROJECT: Portal Kakitangan IDUSP (client prototype)
- **New client project**: **IDUSP (Institute Darul Uloom Southern Peninsula)** staff portal — explicitly NOT an HRMS. Hakim supplied 12 requirements: Bos/dashboards · departments (Admin/Account/Academic) · KPI benchmark · timetable generator · attendance 3x/day + ">14x datang without alasan" · leave (cuti) · invoice generator + storage · report cards (Nilai Murid avg % per subj, Nilai Guru derived from murid) · school licence (YINS) renew 1 month before · student visa 1 month before · tarbiah report (attitude <80%) · inventory/merchandise.
- **Prototype BUILT + verified**: `/Users/hakim/holeeMonth/idusp-staff-portal` — Laravel 12.69.2 + Livewire 3.8 + Flux 2.20 (free; no Pro licence needed), Tailwind v4 + Chart.js, Poppins, the **eFokus/JPNIN Flux shell** (re-scaffolded off Laravel 13/Livewire 4 per Kai's parity finding). 13 screens, all HTTP 200, zero render errors. Deterministic `DemoPortalSeeder`: 28 staff, 120 murid, 11 kelas, 1,920 marks, 1,260 attendance rows (15 working days × 3 sessions), licence 28 days out, 5 visas inside 30 days, **16 unexcused lates** (>14 threshold fires), 29 murid <80% tarbiah. SQLite; demo serves on **port 8001** (ONDW's containers own 80/443/3306). **PT mode confirmed by Hakim (freelance)** → repo initialised, 1 commit, **no remote yet** (awaiting his repo name).
- **UI bug hunt on Hakim's screenshot (Sep 27)**: real root cause = `resources/css/app.css` never declared Flux's required `@custom-variant dark (&:where(.dark, .dark *))`, so `dark:` utilities scanned out of Flux's Blade stubs compiled to `@media (prefers-color-scheme: dark)` and fired on his dark-mode Mac against light surfaces → unreadable white-on-light text + washed cards (built CSS: 17 media-dark blocks → 0 after the fix). Also: appearance pinned to light before `@fluxAppearance` (it only reads `localStorage['flux.appearance'] || 'system'`), sidebar group heading double-escaped (`{{ }}` inside an attribute → literal "&amp;"), sidebar labels overridden to `#e0f2fe` for the dark gradient (Flux ships `text-zinc-500`), zinc-400→zinc-500 labels. **Verified with headless Chromium**: 0 low-contrast text nodes in main content on all 13 pages; charts confirmed painting (40k/73k px). Lesson: a contrast audit must composite ancestor backgrounds *with alpha* and convert colours via canvas (Tailwind emits oklch).
- **Language switched to English-first (Sep 27, per Hakim: "use English first; if the client wants Malay then we do it")**: all UI strings, seeded demo data, comments **and URLs** are English (`/departments`, `/attendance`, …); old Malay URIs deleted, not aliased; attendance session keys renamed to `morning|midday|afternoon`. Domain terms kept (Tarbiah, ustaz/ustazah, Fiqh, Tauhid, YINS, IMM.14). Verified by rendered-text sweep: **0 Malay words across all 13 pages**. If Malay is requested later → add `lang/en`+`lang/ms` and swap through `__()`, do NOT hand-translate. Repo pushed to **github.com/Mhakim38/idusp-staff-portal** (Hakim's remote, `main`).
- **Sidebar defects fixed (Sep 27, from Hakim's screenshot)**: (a) active item was a **blank white pill** — my override forced white text on Flux's opaque white active pill; now dark blue `#1e3a8a`, 10.36:1; (b) hamburger missing — `<flux:sidebar.toggle />` renders an EMPTY button by design, the icon must be passed (`icon="bars-3"`); (c) brand text was unreadable (`flux:sidebar.brand` ships `text-zinc-800`) → replaced with a **logo placeholder** (`LOGO` dashed box + "IDUSP Staff Portal" label) ready for the real logo; (d) truncated group label → renamed to "Attendance". **Light-only is now structural**: `@fluxAppearance` is not emitted at all (it is the only source of the `.dark` class), proven by planting `localStorage['flux.appearance']='dark'` and reloading — 0 `.dark` elements. Sidebar contrast verified against the *real gradient* (canvas-sampled stops): 5.91:1.
- **UI migrated to shadcn/ui (Sep 27, per Hakim, preset `b7Br7G7Ci`)**: shadcn's CLI does NOT scaffold Laravel — the documented path is Laravel's **React starter kit** then `npx shadcn@latest init --preset … --template laravel` (components land as `resources/js/components/ui/*.tsx`), so the Blade+Flux app could not take the preset. Hakim chose **build alongside** (Blade prototype kept as the Friday fallback) with **all 57 submenus in the navbar**. New app: **`/Users/hakim/holeeMonth/idusp-portal-react`** — Laravel 13 + Inertia + React + TS + shadcn (Inter font, custom theme) + recharts; 12 menus / 57 submenus generated from `resources/data/navigation.json`; 16 real screens + 41 informative "planned" pages; **superAdmin** via `PrototypeAuth` (must be **prepended** to the web group — Inertia resolves `auth.user` around the pipeline) + sidebar role-preview switcher; **both themes** (see the Sep 28 dark-mode entry below). Verified: 57/57 routes 200, tsc clean, build clean, 40 invoices on `/invoices`. **No GitHub remote yet** (Hakim to name it).
- **Dark mode ENABLED (Sep 28, Hakim: "if dark mode is available then apply it also" — reversing his earlier "there is only light mode")**: restored the starter kit's appearance system (server cookie read in `HandleAppearance`, client `use-appearance` hook) and added a compact **ThemeToggle** (Light/Dark/System) to the React app's sidebar footer. Default `system` → the preset's dark palette applies automatically on a dark-mode machine; SSR renders `class="dark"` from the cookie (no flash). Verified in Chromium: dark tokens active (`bg oklch(0.148 0.004 228.8)`), toggle switches both ways + persists, contrast audit **0 low-contrast of 92 (dashboard) and 0 of 336 (invoices) in dark**, tsc + build clean. **Blade fallback app still light-only**: its 16 views hardcode light surfaces, so enabling dark there needs a per-view `dark:` pass — not done, offered to Hakim.
- **Pricing verdict (Sora)**: RM7,000–8,000 is **NOT a development budget** — it is the fair price of a ~2-week paid discovery. Working prototype RM45–70k, production RM100–300k. Recommended 3 phases: RM12–20k (credited) / RM45–70k / RM60–140k. Maintenance RM500/mo + RM1.5k/yr is **thin/loss-making** → minimum defensible RM9,600–12,000/yr with 3 support hours/month and change requests billed separately.
- **Where we left off** — Hakim owes: (a) mode confirmation (FT assumed), (b) IDUSP facts (campus, what YINS is, payroll in/out, real counts), (c) pricing decision, then send the 25-question client sheet. Detail: `secret_information/projects/idusp-staff-portal/{overview,modules-and-difficulty,pricing-and-quote,open-questions}.md`

### Sep 3, 2026 — FT · mpaj-icomm · SFTP code conversion + wipe/redo
- Active project: **MPAJ iComm** — full detail + 🔔 reminders in [Project content moved to secret_information — see projects/mpaj-icomm/eperolehan-sftp-migration.md (Sep 3, 2026 section) and known-bugs.md]
- Working branch Hakim-dev2; changes UNCOMMITTED (FT mode) — do NOT `git restore .`
- 🔔 Reminder: ask Hakim + other devs before unifying perolehan-family dirs onto the single `upload/eperolehan` base (paused decision)

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
