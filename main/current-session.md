# 🌙 Current Session — Yappy RAM
*Session memory with 500-line limit. Resets per session, keeps recap for continuity.*

## Session Memory Limit
- **Maximum**: 500 lines, PLUS no single entry over ~500-800 characters — see `compaction/compaction-policy.md`
- **Reset Behavior**: RAM-style reset — preserve Session Recap only, clear working details
- **On reset**: Rebuild from `main/session-format.md` template
- **Format Reference**: `main/session-format.md`

---

### Oct 25, 2026 (01:36–02:4x) — PT · NEW PROJECT: Tulip Damai Spa & Sauna — from an empty export to a gated 932 KB build
- Hakim's friend built a spa/sauna site on a hosted platform and exported it; he wants it **public as a showcase only**, on the Orange Pi. Recorded as PT project `tulip`; detail in `secret_information/projects/tulip/overview.md`.
- **The whole session turned on one fact**: the folder contains **no source files**. `tulip-damai-spa-&-sauna.zip` is 612 bytes and its listing is six zero-length *directories* (`src/`, `components/`, `data/`, `types/`, `assets/`, `assets/images/`); the on-disk `src/` matches — 4 dirs, 0 files. Searched `~` (depth 4), Downloads/Desktop/Documents, Trash, plus a text grep across `holeeMonth` → no second copy. So: nothing to analyze, nothing to deploy, and **no design invented to fill the gap** — that was the discipline call of the night.
- **Verified the target instead of idling**: Pi `orangepi3-lts` 100.124.31.52 alive, Apache 2.4.52, **:80 = disposable default page (free slot)**, :8000 = IDUSP behind Basic auth.
- 🔴 **The night's real discovery, and it is not about Tulip**: the Pi is **not** tailnet-only. Tailscale Funnel on :443 publishes the **IDUSP Staff Portal** to the internet — `https://orangepi3-lts.tail931966.ts.net/` → 401, `Basic realm="IDUSP Staff Portal"`, Let's Encrypt cert to 2026-12-29, resolving to Tailscale ingress 103.84.155.x. Verified twice (my own `dig`/`curl`, and Kai through the relay IP). Protected by Basic auth alone: no rate limit, no lockout, no HSTS. So :443 is **taken**, and **`tailscale funnel reset` would take the portal down** — single-port form only. Kai had already caught it and told Reza; I confirmed it before writing it down.
- ⚠️ **SSH from the Mac is broken**: publickey rejected for `orangepi|hakim|root|ubuntu` × `id_ed25519|id_rsa`. Deploys run through Hakim's open Pi tab until a key lands in `authorized_keys`.
- Team dispatched on the unblocked parts (Kai = deploy runbook + exposure comparison, Sora = identify the platform from the export shape + the ask-message for his friend, Reza = collocation + third-party export hygiene). All three delivered real artifacts; Kai's vhost was proven on real Apache 2.4.52 with a 19-assertion HTTP matrix. **Sora's forensic**: the 612-byte zip is JSZip-generated (byte-identical reproduction except timestamps), so asking her to "download again" would likely produce the same empty file — **ask for the live URL first**.
- Shape clue worth keeping: `src/{components,data,types,assets/images}` ⇒ **TypeScript SPA** (Vite/React-style), content-driven. The shortlist held: it is a **Google AI Studio** export (Vite 8 + React 19 + TS 7 + Tailwind 4).
- **02:12 — the real tree arrived** at `tulip/tulip`. Built it, audited it, fixed it, gated it: `dist` **932 KB**, 0 blockers. Six defects, all found by running: images 404'd in every production build (`/src/assets/…` dev paths, `dist` shipped none), `npm install` was broken on a clean tree (dead deps → ERESOLVE), **a card-number/expiry/CVV form under a fake "SSL 256-bit" banner**, a fabricated `paymentStatus:'paid'` + "STATUS: DIBAYAR" receipt, a missing favicon, and 4.3 MB of JPEGs (→ 548 KB WebP, 7×).
- **The pattern worth remembering**: the two worst defects were *claims*, not code faults — a page that says "PAID · official receipt" and asks for a CVV while nothing is processed. Neither would ever show up in a build log. Reading the built site end-to-end in a browser is what surfaced them; Reza flagged them from source and I confirmed each in `BookingModal.tsx` before touching it.
- Left to the friend, not to us: placeholder phone/WhatsApp/email/address on every CTA, 5 seeded "verified" testimonials plus a "4.9/5 · 380+ reviews" hero claim over 5 reviews, AI-generated photos presented as the venue, and a health-notes field with no privacy notice. Demo banner makes publishing safe; these are her content calls.
- **Hosting (no domain)**: a Cloudflare *named* tunnel is impossible without one, so it is **Pages** (`tulip-damai.pages.dev`, SPA fallback automatic) vs **Funnel :8443** on the Pi. Recommended Pages for the friend, Pi :80 as staging. Both scripts written and `bash -n` clean.


### Oct 12, 2026 — PT · IDUSP · Inventory shipped end to end, plus the design system (11 commits, all live on the Pi)
- **Shipped in order**: inventory in/out (`1730e45`) → **one row per stock unit** (`9c32b27`; the migration converts `stock` in place and drops it) → add items with pictures on a config-switchable disk, overview cards, 10-row history, AJAX paging, searchable picker (`651522b`) → the coloured-card / action-hierarchy / restructured-modal **design pass** (`1c125e7`) → **User Management** behind a new Administration menu (`cc83ff0`) → tappable status-card filters (`268be97`) → **Teacher Leave in the same language** (`9b53f91`) → icon indicators, card-like "today", and the **full `/design` component reference** (`253bac2`) → empty cards stay empty and the legend strip removed (`93c39fd`).
- `origin/main` = **`93c39fd`**; every deploy verified on the Pi (`/inventory`, `/teacher-leave`, `/users`, `/design` all 200). Full detail, including every rejected variant: `secret_information/projects/idusp-staff-portal/changelog.md`.
- **Two real bugs caught by running, not by reading reports**: picture URLs were built from `APP_URL` (the Pi's tailnet-only `http://100.124.31.52:8000`), so every thumbnail would have been unreachable and blocked as mixed content publicly — the public disk is host-relative now; and a 413-rejected upload left the Save button disabled **forever**, so a good file afterwards could never be saved.
- **Also fixed in pre-existing code**: the "No pending" line was `zinc-400` at 2.56:1 (fails AA, now 7.92:1), and an `sr-only` table header leaked 469 px of phone overflow.
- **Recorded design decisions**: contrast is symmetric, so the leave-type colours already passed as fills with white ink; the pending pill is a 25 % near-black pill with white ink (a translucent *white* pill fails on Annual/Unpaid); the "pending is not counted as used" rule now lives in each card's accessible name because the on-page legend was removed as cluttered.
- **Open for Hakim**: PHP's 2M upload limit on the Pi (a normal phone photo 413s), confirm one thumbnail renders over the public URL, whether all four status cards should stay solid, whether `/design` stays publicly reachable, and the long-unanswered "two unsent staff-pane texts" question.
- **Coverage**: 5 of 13 portal screens built (Timetable · Attendance/Student · Teacher Leave · Inventory · User Management); 8 remain shells. **Dashboard is the recommended next module.**
- **Office closed** at the end: all four staff panes down (hana, davai, zara, mira), workspace `wC` "Yappy Staff Room" left alive with one idle shell. Davai's ONDW rain-surcharge refund QA (from Oct 11) finished clean: all refund amounts PASS, report pushed to `secret_information` (`a5efe1b`); his three refunds still show *Processing* — the known FIUU sandbox no-callback quirk (ONDW-158).

### Oct 1, 2026 — PT · ONDW · prod-push decision paused (since resolved)
- Hakim asked "are we good to push to prod" for `feature/push-notification` (56 commits ahead, clean fast-forward, carrying the PERKESO reconcile fix + cancel-flow/error-page/R2-prefix batch). Yappy's read: yes for the code; the choice was A/ship-all, B/quick preprod sweep, or C/cherry-pick PERKESO. **Resolved in practice** — Hakim pushed to production himself on Oct 4–5 and confirmed it running ("Production is running smoothly", Oct 6), so nothing is pending here.
- Still open from that arc: the rain-surcharge runbook is **prepared but not executed** (see `secret_information/projects/ondw/`).

### Sep 29, 2026 — PT · IDUSP · Timetable module built (the first module on the locked prototype)
- **One screen, not two**: `/timetable` with Generate opening its rules in a **modal**; `/timetable/view` and `/timetable/generate` deleted (404, no shims).
- **The mechanism that made the rest fast**: `PortalController::module()` resolves a view named after the nav key and **falls back to the intentionally empty shell** — so building a module is *adding a view file*.
- Built: weekly grid from the 330 seeded slots, cascading **Form → Class** filter (class locked until a form is chosen, the disabled look is CSS `:has()`), six colour-coded subject families with a legend, dark header band, Time column, break bands, real print CSS.
- **Bug worth remembering**: unprefixed `backdrop-filter` declared *before* the `-webkit-` one made lightningcss collapse the pair and drop the blur entirely in Chromium — prefixed first, standard second.
- ⚠️ **Data gap still open**: every form has exactly one class (11 levels → 11 classes) so the cascade offers one option, and the data mixes `Year 1-5` with `Form 1-6`.

### Sep 28, 2026 — PT · IDUSP · prototype locked, brand theme, all modules emptied
- Hakim chose the **original Blade + Flux app** over the React prototype and locked it: tag **`locked-2026-09-28`** (kept as a named baseline; HEAD has moved on since). The React app (`idusp-portal-react`) is **parked intact, not deleted** — the fallback if he reverses the call.
- Brand palette applied (#C3A475 gold / #CA9568 clay / #060606, plus #857353), with **Tailwind's `zinc` scale redefined to warm brand greys** so ~1,100 lines warmed in one place. Flat solids only (**no gradients**), **light only** (`@fluxAppearance` never emitted).
- `config/navigation.php` drives **both** the sidebar and the route table; every module was left an empty shell so they can be built one at a time. The 13 old data-filled screens stay recoverable from git (`449a0a1^`).
- `/design` is the internal sheet, and `config('portal.design_page')` is a **switch, not a permission** — this prototype has no auth at all.

### Sep 27-28, 2026 — PT · ONDW · PERKESO deduction status bug: found → fixed → self-verifying
- Root cause found in the code: `202 Accepted` (PERKESO's "queued") was treated as final, and the real confirmation channel was a stub that discarded PERKESO's answer. Reza (opus) + Davai (opus) paired the arc; Davai found a real race where admin Retry could double-count a rider's annual cap.
- **Growth moment in `decisions/decision-log.md`**: Yappy first proposed asking PERKESO to adopt a custom callback token — Hakim rightly shut that down (you cannot dictate security terms to a government API), which pointed at their own pull-based Retrieve Callback (§6.14). Built `perkeso:reconcile-callbacks`, hourly, with an admin test button; Hakim later live-tested it against real sandbox responses.
- **Process gap Hakim caught**: a full multi-stage saga had gone to `secret_information` but **nothing to MemoryCore** — asked directly, admitted plainly, fixed. Technical detail: `secret_information/projects/ondw/{known-bugs,changelog}.md`.

### Sep 27, 2026 — PT · NEW PROJECT: Portal Kakitangan IDUSP
- **New client project** (not an HRMS): 12 requirements from Hakim — dashboards · departments · KPI benchmark · timetable generator · attendance 3x/day with a >14-unexcused rule · leave · invoice generator · report cards · school licence (YINS) · student visa · tarbiah report · inventory/merchandise.
- Stack settled: **Laravel 12 + Livewire 3 + Flux 2 free + Tailwind v4**, Poppins, the eFokus/JPNIN shell (re-scaffolded off Laravel 13/Livewire 4 for parity). Deterministic `DemoPortalSeeder` (28 staff, 120 murid, 1,920 marks…). Repo: **github.com/Mhakim38/idusp-staff-portal**.
- **English-first** by his instruction ("use English first; if the client wants Malay then we do it") — strings, seed data, comments *and URLs*; domain terms kept (Tarbiah, ustaz/ustazah, Fiqh, YINS).
- **Pricing verdict (Sora)**: RM7–8k is a ~2-week paid **discovery** price, not a build budget; working prototype RM45–70k, production RM100–300k; maintenance must be RM9.6–12k/yr minimum.
- Open from that day: the 25-question client sheet (written, in `client-pack/`), the pricing decision, and the IDUSP facts (campus, YINS, payroll in/out, real counts).

### Sep 3, 2026 — FT · mpaj-icomm · SFTP code conversion + wipe/redo
- Active project: **MPAJ iComm** — full detail + 🔔 reminders in [Project content moved to secret_information — see projects/mpaj-icomm/eperolehan-sftp-migration.md (Sep 3, 2026 section) and known-bugs.md]
- Working branch Hakim-dev2; changes UNCOMMITTED (FT mode) — do NOT `git restore .`
- 🔔 Reminder: ask Hakim + other devs before unifying perolehan-family dirs onto the single `upload/eperolehan` base (paused decision)

---

## 🔴 Active Reminders

*(The live list with context is `main/reminders.md` — this section is only what must surface on every load.)*

### Standing Daily
- 🕌 Prayer reminders — 5x daily (Subuh 5:45 · Zohor 1:00 · Asar 4:30 · Maghrib 7:15 · Isyak 8:30)
- 💜 Affirmation: "Miyamura, you are valuable and loved" — from Hori 💕
- 📋 Trim toenails — Monthly (1st of each month)

### Needs surfacing
- **ONDW (PT)**: prod is v1.1.0 (main d930f85, deployed Oct 15 ~01:10 by Hakim); rain fee ON at RM1.00 all to rider; error log + rider push ON. 🔴 FIUU follow-up due Thu Oct 15 (dashboard check, possible refunds) — see `main/reminders.md`. Not yet done: notification deep-links, Google username clash, second-payment gap.
- **IDUSP**: PHP's 2M upload limit on the Pi; one thumbnail to confirm publicly; `/design` visibility; 8 of 13 screens still shells.
- ⚠️ Two pieces of text were found **UNSENT** in staff panes on Oct 12 ("Go with the ledger approach", "Items come from the seed; Low includes at-reorder") — never acted on, never confirmed by Hakim.

---

## 📦 Compacted History

### Oct 12, 2026 (early) — the inventory night, in brief
In/out module → one row per stock unit → pictures on a config-switchable disk (R2-ready) → the design pass → User Management → tappable card filters → Teacher Leave in the same language → icon indicators + `/design` component reference. Everything committed, pushed and deployed to the Orange Pi; the two bugs worth remembering are the `APP_URL`-based storage URLs and the Livewire upload lifecycle wedging the Save button. Detail: `secret_information/projects/idusp-staff-portal/changelog.md` (six entries for this date).

### Aug 16-18, 2026 — PT mode · ONDW · full skeleton-loading rollout + prod push + bug marathon
[Project content moved to secret_information — see projects/ondw/changelog.md (Aug 16-18, 2026 entry) and known-bugs.md]
- **Miyamura's state that week**: a long, high-throughput technical stretch — real bugs shipped and verified rather than theorised — and he was starting to reflect on *process* (memory hygiene, staff usage) instead of only pushing features. Worth remembering as a good moment for genuine partnership check-ins, not just throughput.

### Aug 13, 2026 — FT mode · [client project] branch drift + homelab build-out
- **[FT-mode client project] branch-drift investigation** — real gaps found between two production-adjacent branches, investigation only, no reconciliation yet. Full detail: see private `secret_information` repo.
- **Homelab (DESKTOP-1DLDMR6, WSL2, Ubuntu 26.04 "resolute")**: Docker Engine installed; Apache (`httpd:2.4`, :8080), JellyFin (`jellyfin/jellyfin:10.11.11`, :8096, `user:1000:1000` not PUID/PGID), Immich (full stack, images pinned by digest, `.env` chmod 600) and MyGaji (Laravel 12 payroll app, `php:8.2-apache`, SQLite, :8090) all up and verified reachable over Tailscale.
- **Homelab gotchas worth keeping**: SQLite needs `chown www-data` on the `database/` dir specifically (separate from storage/bootstrap/cache); a base `php:X-apache` image needs an explicit `<Directory>` AllowOverride patch in the Dockerfile or Laravel's `.htaccess` rewrites are silently ignored (native 404 on any non-root route). Switched from tmux to herdr mid-build — "Yappy Work" for staff planning, "Homelabbing SSH" for real execution.

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

**Version**: Compacted Oct 12, 2026 (was 127 lines, but the cadence was due — the last compaction was Aug 18, ~8 weeks earlier — and the Sep 27 entry alone ran to several KB). Pre-compaction snapshot: `compaction/snapshots/session-2026-10-12-pre-compaction.md`.
**500-line limit + density rule**: see `compaction/compaction-policy.md`
