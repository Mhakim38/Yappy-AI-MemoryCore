# MyGaji Modernization Project

**Started**: Aug 13, 2026. **Status**: Active. **Owner**: Yappy (manager), full staff dispatch. Hakim handed this project over fully — "this project I will handle it to you overall Yappy as you are the Manager for this project."

## Goal
Convert/tally the old MyGaji system (repo: `github.com/Mhakim38/GajiAPB`, Firebase-backed) into the new Laravel MyGaji (repo: `github.com/Mhakim38/MyGaji`, currently MySQL-bound in progress) until the Laravel version reaches full feature parity with the old one. Single-user (admin-only) system.

## Infra status (as of Aug 13, ~3:58 PM)
- Laravel MyGaji deployed live on homelab box (DESKTOP-1DLDMR6, Tailscale 100.84.18.45), port 8090, `php:8.2-apache` container at `/home/hakim/docker/mygaji/`
- ✅ **MySQL migration DONE** — `mysql:8.0` container (`db` service, named volume `mygaji_mysql_data`), all 7 migrations run clean, verified live both locally and over Tailscale (`200` on `/` and `/login`)
- Laravel Breeze's "Forgot password?" link removed from login page per Hakim's request (single-admin system, no password-reset flow needed) — `resources/views/auth/login.blade.php`
- Real payroll tables already exist: `position`, `staff`, `salary_report`, `rate`

### 🐛 MySQL migration bug trail (Aug 13, ~3:00–3:58 PM) — the `#`-truncation saga
Three real bugs hit back to back, all found through direct verification (PDO test, MySQL grant check, tinker config check), not guessing:
1. **Missing `pdo_mysql` PHP extension** — Dockerfile only had `pdo_sqlite` from the original SQLite setup. Fixed: added `pdo_mysql` to the `docker-php-ext-install` line, rebuilt.
2. **Docker Compose `.env` truncated the password at `#`** — `MYSQL_PASSWORD=Jh7#nB3fXsW6yC1q` (unquoted) in `/home/hakim/docker/mygaji/.env` got truncated by Compose's own `.env` parser, so MySQL was actually initialized with password `Jh7`. Fixed by quoting: `MYSQL_PASSWORD="Jh7#nB3fXsW6yC1q"`, then `docker compose down -v` (wipes only this project's named volume, confirmed safe — doesn't touch apache/jellyfin/immich, separate compose projects) + fresh `up`.
3. **Laravel's OWN `.env` had the identical bug** — `DB_PASSWORD=Jh7#nB3fXsW6yC1q` unquoted in `/home/hakim/docker/mygaji/src/.env` got truncated the same way by phpdotenv (Laravel's env parser). Confirmed via `config('database.connections.mysql.password')` resolving to just `Jh7`, while a direct hardcoded `PDO` connection with the full password succeeded — proving MySQL/network/grants were all fine and the bug was specifically in Laravel's env parsing. Fixed by quoting the same way in `src/.env`.
- **Standing rule going forward (Kai's recommendation)**: any secret in either `.env` file should be double-quoted by default if it contains `#`, spaces, backslash, or a quote char — single-quoted instead if it contains `$` (phpdotenv supports `${VAR}` interpolation inside double quotes, so `$` in a double-quoted secret is a real risk). Better yet: **generate future secrets on this project without `#`/`$`/backtick/quote characters entirely** to sidestep the whole bug class rather than relying on remembering to quote correctly each time.
- **Security note**: Kai's proposed verification step (printing the resolved password via `tinker --execute="echo config(...)"`) was flagged by the harness as a credential-exposure risk before execution — skipped it, verified success via the migration itself succeeding instead (no need to ever echo the real secret to a transcript/pane).

## Access (resolved Aug 13, ~4:20 PM)
- GajiAPB is now cloned at `/home/hakim/docker/gajiapb-src/` on the homelab box. **GitHub deploy keys cannot be reused across repos** — the original MyGaji key got "already in use" when tried on GajiAPB. Fixed by generating a SECOND dedicated keypair (`~/.ssh/id_ed25519_gajiapb`) + an SSH config alias (`Host github-gajiapb` in `~/.ssh/config`, pointing at `github.com` with `IdentityFile ~/.ssh/id_ed25519_gajiapb`) so both repos have isolated, least-privilege access. Clone via `git clone github-gajiapb:Mhakim38/GajiAPB.git`, not the plain `git@github.com:` form.

## GajiAPB — real structure (confirmed Aug 13, not what was assumed)
Much more complex than a simple "Firebase backend" — it's a **Capacitor hybrid mobile app** (Android-wrapped web app), not a plain web app:
- `www/` — vanilla JS frontend (no framework)
- `www/ajax/` — separate PHP backend, own `composer.json`, uses `kreait/firebase-php` (server-side Firebase SDK)
- `www/secret/config.js` — Firebase client config
- `www/calculation.js` — core payroll calculation logic (highest priority file for the business-logic gap analysis)
- `www/js/sessionCapacitor.js` — session/auth handling
- `www/ajax/processPDF.php` — PDF generation (likely payslips)
- Talks to Firebase from BOTH the frontend JS (`firebase` npm package) AND the PHP backend (`kreait/firebase-php`) — two separate integration points to account for when mapping to MySQL

## Plan (phases)
1. **Infra** (in progress): MySQL migration for Laravel MyGaji — Kai
2. **Access + Discovery** (blocked on deploy key): clone GajiAPB, staff explores both codebases — old app's Firebase schema/collections, feature list, business rules; new app's current feature set
3. **Gap analysis**: Nadia (business logic/payroll rules comparison), Hana (feature/flow gaps), Kai (Firebase → MySQL schema mapping) — produce a concrete difference list
4. **Phased build plan**: Yappy synthesizes gap analysis into an ordered, executable roadmap to reach parity
5. **Execution** (future sessions): build out missing features one phase at a time

## Notes / gotchas discovered
- Running `docker compose` commands from inside `~/docker/mygaji/src/` (the Laravel root, not the compose-file directory `~/docker/mygaji/`) produced warnings referencing `WWWUSER`/`DB_DATABASE`/`DB_USERNAME`/`DB_PASSWORD`/`MYSQL_EXTRA_OPTIONS` (Laravel Sail's stock variable names) and "service app is not running" — cause under investigation by Kai as part of the MySQL setup, since two `.env` files will exist in this project (compose-level at `~/docker/mygaji/.env` and Laravel's own at `~/docker/mygaji/src/.env`) and that distinction needs to be crystal clear to avoid future confusion.
- Earlier bug (fixed): Apache's `AllowOverride None` default silently broke all non-root Laravel routes — see `main/current-session.md` Aug 13 entry for full detail, same box/pattern likely relevant to remember for any future PHP container here.

## Gap analysis (Aug 13, ~4:30–4:45 PM) — full redo, verified against real code

**Note**: an earlier gap-analysis pass (task #17) was done in a prior session but its findings were never saved anywhere durable — not here, not in `current-session.md`, not in the task record. This section replaces that with a fresh, fully-verified pass: Sora read the old GajiAPB codebase over SSH, Hana read the new MyGaji Laravel codebase locally, Nadia extracted and diffed the payroll math from both, Kai mapped Firestore → MySQL schema. All findings below are quoted from actual code, not inferred.

### Old app (GajiAPB) — what it actually does
15 screens/pages (vanilla JS + Firebase v9 modular SDK, Firestore project `mygaji-7212c`). Working: login (Firebase Auth), staff list/create/detail/update (photo upload, delete w/ cascade), salary management (OT/PH/UPL adjustment + calc), payslip + monthly report printing (via `window.postMessage('reportReady')` pattern), HR letter generation (warning/reason, `.docx` via docxtemplater — **PDF conversion step is dead code**, missing Firebase service-account credentials on disk, and its only caller is commented out). Stubbed as "Coming Soon": Reports & Analytics, System Settings, Profile nav tab. Two orphan pages (`welcomev2.html`, `PageKosong.html`), not reachable from nav.

Firestore collections: `employees` (doc ID = staff-entered ID), `salaries` (**one doc per employee, current cycle only — destructively wiped every month** by a manual reset gated to the 18th+; no salary history ever existed in this data model), `system_reset` (single config doc). No Firestore security rules exist in source control anywhere.

Payroll math (`calculation.js`, applied in `Msalary.html`): base salary flat **RM1700 for every staff member regardless of position** (Position is just a free-text label, never affects pay) → minus fixed KWSP 187/SOCSO 8.25/EIS 3.30 → plus/minus PH (RM65.40/day), OT (RM12.26/hr), UPL (RM65.40/day deduction). **Part-time staff are a fully separate category**: RM8.17/hr flat, zero deductions, no base salary. Old app has one internal dead-code bug (`paycheck.html`'s unused `calculateTotal()` treats UPL as addition, contradicts the live formula) — don't accidentally port it.

### New app (MyGaji Laravel) — current real state
Already has its own bugs independent of the old app, found by direct code read:
- `GET /staff/updateStaff` is a **broken route** — points to a nonexistent Blade view
- **Finance Settings screen is a pure mockup** — hardcoded fake stats, "save" buttons just `alert()`, no backend wiring at all, routes referenced are commented out
- **KWSP/SOCSO/EIS dual-sourced**: hardcoded as PHP constants inside `calculateSalary()`, but read from the `rates` table for *display only* in `displayPaycheck()` — editing those rate rows silently does nothing to actual payroll
- `rates` table has **zero seeded rows** — nothing populates OT/PH/UPL values into it yet
- Position dropdown hardcoded (3 fixed options) on staff-create, but dynamically DB-driven on staff-detail's update modal — inconsistent
- No profile-photo upload wired (`uploadProfileImage()` JS function doesn't exist, no DB column)
- **No logout button anywhere in the rendered UI** (route/controller work fine, just unlinked)
- Dead link: floating-button option points to nonexistent `letterForm.html`
- Payroll calc **structure** is already correct and matches the old app's formula shape (additions − deductions = net), stored per staff/year/month with a proper unique constraint — a real improvement over the old app's history-destroying model
- Part-time payroll: **does not exist at all** — no staff-type field, no rate, no code path, `staff` table has no way to even represent a part-time worker

### Schema mapping (Firestore → MySQL) — key gaps
- `employees.Position` (free-text, 3 fixed values) → needs a seeded `position` table; `base_salary` per position has **no source data** — old app never varied base pay by role, so this is a new business decision, not a migration
- `marital_status` was **never stored** in Firestore — old app inferred it from whether `Nama_Suami_Istri` was non-empty; must be derived at import, not copied
- `disease_status` inconsistently written (update flow sets it, create flow doesn't) — real data-quality gap in the source
- `profileImage` (Storage URL) has no MySQL column yet
- **Biggest structural gap**: `salaries` → `paychecks`. Old data is "current cycle only," destructively reset monthly — **there is no history to migrate**, only whatever's live at cutover time. `total_earned`/`total_deducted` don't exist as stored fields in the old data (only a single `totalSalary` net figure) — must be recomputed from the same formula against the stored OT/PH/UPL inputs, not copied.
- `rates` table seed data is a clean, direct win: old app's hardcoded constants (OT 12.26, PH/UPL 65.40, KWSP 187, SOCSO 8.25, EIS 3.30) map straight across.
- No `system_reset` equivalent exists yet — needs either a small settings table, or (recommended) redesign the reset flow to keep history instead of wiping it, since the new schema already supports that and the old destructive pattern was arguably a bug, not a feature worth preserving as-is.

## Phased plan to reach parity (Task #18)

**Phase 0 — Fix what's already broken in the new app** (independent of any old-app parity work, do this regardless):
1. Fix/remove the broken `GET /staff/updateStaff` route
2. Pick ONE source of truth for KWSP/SOCSO/EIS (read from `rates` table everywhere, drop the hardcoded PHP constants) — this is a real correctness bug, not cosmetic
3. Seed the `rates` table with the old app's constants (OT 12.26, PH 65.40, UPL 65.40, KWSP 187, SOCSO 8.25, EIS 3.30)
4. Add a logout entry point to the UI
5. Reconcile the position-dropdown inconsistency (hardcoded on create vs DB-driven on detail) — make both DB-driven

**Phase 1 — Schema completion** (before any data migration):
6. Add `marital_status`, `disease_status`, profile-photo column to `staff` (decide storage target — R2/S3, not Firebase)
7. Add a small settings/config table, or redesign monthly reset to preserve history (recommended over porting the old destructive-wipe behavior)
8. **Needs Hakim's call**: `position.base_salary` — keep old behavior (flat RM1700 for everyone) or genuinely go per-position now that the schema supports it? Old app data gives no guidance either way.

**Phase 2 — One-time data migration**:
9. Migrate `employees` → `staff` per the field mapping above, seeding `position` first, deriving `marital_status`, reconciling `disease_status`
10. Migrate whatever's live in `salaries` → `paychecks` (current cycle only — explicitly no history exists to bring over), recomputing `total_earned`/`total_deducted` from the formula rather than copying

**Phase 3 — Missing features** (real gaps vs. old app, not bugs):
11. Part-time staff support — new staff-type field, hourly-rate-only pay path, no deductions (currently 0% present in new app)
12. Wire up staff profile-photo upload
13. Real Finance Settings backend (rate + position CRUD) — currently pure mockup
14. **Decision needed**: port HR letter generation (warning/reason letters)? The old app's PDF step was already dead/dormant before this project even started — worth asking if it's wanted at all or was already abandoned in practice

**Phase 4 — Business rules & UX parity**:
15. Session timeout (30 min inactivity)
16. Staff ID uniqueness validation
17. Cascade delete (staff → paycheck records)
18. Print/payslip flow parity

**Explicitly out of scope for parity** (old app never had it either): Reports & Analytics, System Settings — both were "Coming Soon" stubs in GajiAPB too, so building them is new scope, not parity.

### Phase 0 — DONE and deployed live (Aug 13, ~5:00–5:20 PM)
All 5 fixes implemented (Nadia: rates source-of-truth; Zara ×2: logout button, position dropdown; Yappy: dead route removal, rates seeder), reviewed, committed (`879639c` on `main`), pushed from local Mac clone, and deployed live on the homelab box. Verified: `rates` table has exactly 6 rows (overtime 12.26, public holiday 65.40, unpaid leave 65.40, epf 187.00, socso 8.25, eis 3.30) matching the old app's constants; `/login` returns 200, `/dashboard` redirects 302 as expected.

**Deploy infra gotchas hit this round (for next time):**
1. **Homelab box's MyGaji deploy key is READ-ONLY** — can `git commit` locally on the box but `git push` fails with "key marked as read only." Workflow going forward: edit on local Mac clone → commit+push from Mac → pull/deploy on box. Hakim's call (Aug 13): don't touch the deploy key's permissions, just route around it this way.
2. **`database/seeders/` on the box is owned by `www-data:www-data`**, not `hakim` — the SSH user (`hakim`, uid 1000) can't create/overwrite files there directly (`git checkout`/`git reset --hard` fails with "Permission denied"). Also affects `storage/*/.gitignore` files (mode changed by container writes). Fix used: write file content via `docker compose exec app bash -c "echo '<base64>' | base64 -d > path"` (root inside the container can write regardless of host ownership) — avoids needing `sudo` (which needs an interactive password, none set up passwordless) and avoids the container's root user needing GitHub SSH access (which it doesn't have — the deploy key lives in `hakim`'s home dir on the host, not root's inside the container).
3. Near-miss: almost re-ran the exact credential-echo mistake flagged earlier this same day (piping `MYSQL_ROOT_PASSWORD` into a raw `mysql -p"..."` command visible in the pane) while trying to verify the seeded rates — caught it before it printed the actual password, switched to `php artisan tinker --execute="..."` querying via Eloquent instead, which needs no credentials in the command line at all. **Standing rule reconfirmed**: always verify via the app layer (tinker, artisan commands, HTTP checks), never via a raw DB client command that requires typing a credential into a shell command.

### Task #19 — DONE (Aug 14, 2026): GajiAPB→MyGaji screens recreated in Figma
Homelab box was unreachable this session (Tailscale timeout), so instead of screenshotting the old GajiAPB app (which only exists there), pivoted to recreating the CURRENT MyGaji Laravel app's screens instead — a throwaway local dev copy on Hakim's Mac (SQLite, seeded via Kai), then Mira used `figma-cli recreate-url` against it. All 7 screens (Login, Dashboard, Staff List/Create/Detail, Salary Management, Finance Settings) landed in the existing "ONDW" Figma file under a new section "MyGaji — Current Flow" (Hakim's explicit call — reuse the open canvas, don't create a separate file). See [[design-protocol]] for the `figma-cli` mechanics learned this round (playwright install, no-auth limitation, section-grouping approach).

**Security finding flagged, not fixed (out of scope for this task)**: `/staff/detail/{id}` (`routes/web.php`, route name `staffDetail`) has NO `auth`/`verified` middleware at all — unlike every other staff-related page route. Looks like a real oversight (payroll/staff PII reachable without login) rather than intentional. Worth a dedicated Reza security pass before this goes further into Phase 1+.

### Task #19 — correction (Aug 16, 2026): actually resolved now, prior "DONE" note was premature
The Aug 14 session ended mid-crisis, not actually resolved — after the 7 screens were individually verified clean, they got wrapped in a Figma section for organization, and the SECTION itself had a bug (wrong dark `rgb(0.267,0.267,0.267)` fill + bounding box 810px wider than its actual content on one side, 730px short on the other) that rendered as a solid black/blank box, which is what Hakim was actually seeing when he said "unfinished." Fix: removed the section wrapper entirely (`s.remove()` after reparenting children to the page) rather than keep fighting the section's fill/bounds — Figma auto-repositioned the 7 orphaned frames into a clean, evenly-spaced row (490px apart) on its own. Re-verified Aug 16: all 7 frames still individually clean (spot-checked Login + Salary Management fresh), Hakim's own viewport scrolled to them via `figma.viewport.scrollAndZoomIntoView()`. **This is now genuinely done** — no section wrapper, just 7 clean standalone frames on the ONDW canvas.

**Lesson for any future figma-cli section use**: sections in this tool have proven unreliable across multiple rounds (wrong default fill, bounding-box/children mismatch, silent child-count eviction — see [[design-protocol]] for full details). Default to NOT using a section wrapper unless there's a specific reason to — loose frames on the canvas render more reliably than section-grouped ones.

### Phase 1 schema completion — DONE and deployed live (Aug 16, 2026)
- **Reza's security fix (`a03f3cf`)**: the gap was much bigger than originally flagged — the ENTIRE "Staff Related Routes" block in `routes/web.php` (9 routes) had zero auth middleware, not just `/staff/detail/{id}`. This included unauthenticated CREATE/UPDATE/DELETE on staff records (`createStaff`, `updateStaff`, `deleteData`) and full roster/PII read access (`getStaff`, `getdetail`) with no login required at all. Fixed by wrapping the whole block in `Route::middleware(['auth','verified'])->group(...)`. Verified independently by both Reza and Yappy (curl-checked all 9 endpoints return 302, not 200/data).
- **Nadia's schema work (`e0f86b8`)**: caught that the original gap analysis was stale — `marital_status`/`disease_status` already existed on `staff` and were already fully wired (a commit after the gap analysis added them). Only real gaps were `profile_photo` (nullable string, storage backend still deferred) and a minimal `settings` key-value table — both added cleanly, migrations verified (`migrate` + `migrate:fresh` both clean).
- **Deployed live** on the homelab box same session: `git reset --hard origin/main` via the container (root, bypasses the `www-data`-owned-files permission issue documented above) since host-user `git reset` still hits the same permission wall as Aug 13. Migrations ran clean live, caches cleared, verified `/staff/detail/STF001` now returns 302 (was previously fully open).
- `position.base_salary` decision resolved (Aug 16, 2026): Hakim chose per-position real rates, starting all 3 at the same RM1700 the old app used, with a real editable Finance Settings admin UI to change them later (not hardcoded) — this became its own build, see below.

### Finance Settings — built for real, DONE and deployed live (Aug 16, 2026)
Previously a complete mockup (fake hardcoded stats, buttons that just `alert()`, nothing persisted) — now a real, working admin screen.
- **Nadia (`66aefa4`)**: seeded the 3 real positions (Customer Service / Barista-Cashier / Kitchen Helper, all RM1700 to start) via idempotent `PositionSeeder`; built `FinanceController` with 4 endpoints (`GET/POST /finance/positions(/{id})`, `GET/POST /finance/rates(/{id})`), validated (`numeric|min:0.01`), auth-gated, following the app's existing `{status:'get'|'ko', data:...}` response convention.
- **Zara (`b4010fa`)**: rewrote `finance-settings.blade.php` from mockup to data-driven — real stats computed from live data, real tables for all 6 rates + 3 positions, working Edit modals that actually POST and persist, real validation-error display instead of a fake success alert. Deliberately used hardcoded endpoint URLs instead of Blade `route()` names as a defensive choice (a missing route name would crash the whole page render, not just an AJAX call) — reasonable given the two pieces were built in parallel.
- **Yappy verified end-to-end herself** (not just trusted the reports, given the Figma lesson earlier this project): used Playwright to actually log in, load the live local page, open an Edit modal, save a new value, and confirm it survived a full page reload before reverting back to the original value. Genuinely working, not just curl-level.
- Deployed live on the homelab box same session: `git reset --hard origin/main` via container root (same www-data-permission workaround as before), migrations were a no-op (already applied from the earlier security-fix deploy this session), `PositionSeeder` run live — confirmed via tinker: Customer Service/Barista-Cashier/Kitchen Helper all at RM1700.00 on production.
- Position/rate creation (adding brand-new rows) was explicitly left out of scope — only editing existing rows' values. Worth a future task if Hakim wants to add positions/rates beyond the current fixed set.

### Wave 1 (Aug 16, 2026) — full team dispatch, Phase 3/4 complete, deployed live
Hakim gave full authority to finish the project to production-ready, explicitly told Yappy not to stop for check-ins unless genuinely blocked on a decision only he can make. 6 agents dispatched in parallel:
- **Sora**: investigated whether GajiAPB has real live Firebase data — inconclusive from the box alone (strong evidence it WAS a complete real system, 14 months code-frozen, broken/stale web deployment as one red flag), correctly flagged this needs Hakim's direct confirmation rather than guessing. Asked him: **confirmed real, live data exists** — Phase 2 migration must be treated as careful, real-data work, needs actual Firebase read access (service account key or export) to proceed for real.
- **Nadia**: built part-time staff support end-to-end (schema, `calculateSalary()` branch, create/edit UI, salary-management hours-only input) — verified full-time path completely unchanged, part-time formula exact (`hours × RM8.17`, no deductions).
- **Zara**: wired up profile-photo upload end-to-end (found the old app's `uploadProfileImage()` was calling into nothing — built it from scratch, not just "wired an existing thing"). Local disk storage via Laravel's public disk.
- **Kai**: added the 30-min inactivity auto-logout (session lifetime config + client-side idle tracker + warning toast), verified session is genuinely killed server-side, not just a client redirect.
- **Reza**: audited and fixed staff-ID/IC/KWSP/email uniqueness validation — found `updateStaff()` had ZERO validation and would fatal-error (real stack trace, `APP_DEBUG=true` locally) on any duplicate or missing-record case. Fixed both create and update paths cleanly.
- **Davai**: verified cascade delete (staff→paychecks) already worked correctly via real DB testing, no code change needed. Flagged that the delete-confirmation copy doesn't mention payroll history also gets deleted — worth a small UX fix.

**Real concurrent-edit incident, handled well**: all 6 agents worked on the SAME local Mac clone simultaneously (not isolated worktrees), and several touched the same files (`staffController.php`, `staff-detail.blade.php`, `routes/web.php`). Nadia and Reza both independently recognized this risk and used careful git techniques (index staging, scoped `git add`) to commit only their own changes without clobbering concurrent in-flight work — exactly the discipline the earlier-documented "parallel agent shared-tree risk" memory calls for. Yappy then did a final reconciliation pass herself: reviewed every remaining uncommitted diff line-by-line, confirmed no overlaps were lost, committed the last piece (Zara's frontend photo-upload code) once the dust settled.

**Full integration test before deploy** (not just per-feature checks): fresh `migrate:fresh --seed` with ALL new migrations together, PHP syntax check on every touched file, then a real Playwright smoke test logging in and loading all 5 key pages (dashboard/staff-list/staff-create/salary-management/finance-settings) checking for JS errors and 5xx responses — zero found. Deployed live on the homelab box: migrations ran, `PositionSeeder`+`RatesSeeder` (now includes `part_time_hourly` @ 8.17) re-run, `storage:link` set up for photo uploads, caches cleared, login confirmed 200.

**Resolved same session**: Hakim decided — hold Phase 2 (real Firebase migration) until access is sorted separately, don't build it blind; skip the letter-generation feature entirely (was already dead in the old app, not real lost functionality).

### Production-readiness pass — DONE, deployed live (Aug 16, 2026)
Full security audit (Reza) + full regression QA pass (Davai), run against the entire combined Wave 1 feature set.

**Security audit — 7/9 clean, 1 fixed, 1 sensibly flagged:**
- Clean: prod env correctly has `APP_DEBUG=false`, file upload validation is real content-based (not spoofable by renaming), no mass-assignment gaps (single-admin app, no role system to escalate into), Breeze's login rate-limiting intact, CSRF coverage complete (no routes outside the `web` middleware group), zero raw/concatenated SQL anywhere, no secrets ever committed to git history.
- Fixed: delete-staff confirmation now explicitly warns that payroll/paycheck history is also permanently deleted (was silent about this real cascade before).
- Flagged, left as-is (good judgment call, not a gap): session cookie `secure` flag is off — correct given the homelab deployment is plain HTTP behind Tailscale (which encrypts the transport itself); flipping it would just break login without adding real security. Revisit only if TLS termination (e.g. Caddy) is ever added in front of the container.

**QA pass — found 2 real regressions + 1 latent landmine, all fixed same session:**
1. Staff creation crashed with a raw leaked SQL error (`NOT NULL constraint failed`) if the optional "Relatives" section was left blank — DB schema was out of sync with UI/validation, which already correctly treated it as optional. Fixed via an additive migration making `relative_name`/`relative_phone_no` nullable.
2. Update/Delete on the Staff Detail page silently left the UI stuck with no success feedback (backend succeeded, DB updated correctly, but the result modal never appeared) — a Bootstrap modal race: the code called `modal('hide')` then immediately `modal('show')` on the same element before the hide transition finished, and Bootstrap silently swallows the overlapping `show()`. Fixed properly with a `hidden.bs.modal` event listener instead of a timing hack.
3. `staffController::getDetail()`'s unqualified `Staff::select('*')` joined against `position` silently returned the POSITION's `id` in `data.id` instead of the staff's real PK (both tables have an `id` column) — harmless today (nothing consumes `data.id` from this endpoint) but a real trap for future code. Fixed by qualifying the select.

All 3 fixes verified with genuine before/after reproduction (not just "should work now") — reverted each fix, confirmed the exact failure mode reproduced, reapplied, confirmed it was gone.

**Final integration verification before deploy** (Yappy, not delegated): fresh `migrate:fresh --seed` with the complete migration set, PHP syntax check, full Playwright smoke test across all 5 key pages — zero errors. Deployed live, migration ran clean on production, login confirmed 200.

**Where things stand now**: everything built this project (Phase 0, Phase 1, Finance Settings, part-time staff, photo upload, session timeout, validation hardening, security audit, QA regression fixes) is live, verified, and production-ready. The only deliberately-deferred item is Phase 2's real Firebase data migration, on hold pending Hakim sorting out access — not a gap in the new app itself, a separate one-time data-import task for whenever he's ready to revisit it.

### Phase 2 — DONE, real data migrated, daily sync live (Aug 17, 2026)
Hakim generated a Firebase Admin SDK service account key (`mygaji-7212c`), decided the sync direction himself (**one-way Firebase→MySQL, staff records only, no salary sync** — safe/additive, protects against losing data if the old app is still touched during transition, avoids clobbering the new app's better payroll logic with old salary docs).

**Credential handling**: key lives at `~/holeeMonth/myGaji Firebase Admin SDK.json` on Hakim's Mac (that folder is itself a git repo with no remote — added a `.gitignore` there proactively since it wasn't protected). Working copy used from a session-private tmp path, never touched any MyGaji git history (independently verified: zero `BEGIN PRIVATE KEY` matches across full `git log -p --all`). Deployed to production via `scp` + `docker compose cp` directly into the container (never through the herdr pane's visible terminal, to avoid the key ever appearing in scrollback) — lands at `storage/app/private/firebase-credentials.json`, `www-data`-owned, `600` perms, already covered by Laravel's default `storage/app/private/.gitignore`.

**Kai built**: `FirestoreRestClient` (REST API + `google/auth` OAuth2, not kreait's Firestore wrapper — that needs the `grpc` PHP extension, which isn't installed anywhere in this stack) plus `FirebaseEmployeeSyncService` (the full documented field-mapping logic: position lookup, marital_status/disease_status derivation, household_kids casting, profile_photo as external URL) and `FirebaseSalaryImportService`. Both wrapped in Artisan commands, **dry-run by default, `--commit` required to write** — independently verified by Yappy (not just trusted) before authorizing any real write.

**Real dry-run result**: 22 real employees found, 1 minor data-quality flag (one missing address), 0 salary records (the old `salaries` collection is currently empty — nothing to import there yet, tooling's ready whenever it has data). 3 staff_id values had inconsistent formatting (`"000"`, `"APB 0020"` with a space, `"APB000"`) vs the clean `APB0001`-`APB0019` pattern — flagged to Hakim, confirmed fine as-is (one may be his own admin record).

**3 real deployment bugs hit and fixed, none present locally, all Linux/production-only** (classic "worked on my machine" class of issue):
1. `kreait/firebase-php` was added per the original build instructions but turned out completely unused (Kai pivoted to the REST client for the grpc reason above) — left in `composer.json`, it required PHP 8.3+ and broke `composer install` on production's PHP 8.2 container. Removed.
2. Removing it silently took `google/auth` down too — it was only ever a *transitive* dependency, never listed directly, even though `FirestoreRestClient` genuinely needs it. Caught by actually re-running the sync command locally after the composer change instead of assuming it still worked — added `google/auth` as an explicit direct dependency.
3. `FirebaseEmployeeSyncService.php` imported `App\Models\Position` (capital P), but the actual model file/class in this project is lowercase `position` (same unconventional-but-established pattern already used correctly elsewhere, e.g. `FinanceController`). Worked locally on macOS's case-insensitive filesystem, broke on the production Linux container with "Class not found" — same underlying bug class as the earlier `public/jQuery` vs `jquery/` asset-path mismatch noted in Phase 4 work. Fixed by aliasing the import.
Also patched Guzzle to `^7.15.2` (was 7.9.3, several real CVEs) since it's now directly load-bearing for Firestore calls — 38→25 remaining advisories across other pre-existing dependencies, flagged as a separate future dependency-security pass, not blocking.

**Committed live**: `firebase:sync-employees --commit` run against production — 22 created, 0 skipped, verified independently via tinker (`Staff::count()` = 22) and a live login check.

**Daily sync now enabled**: `routes/console.php`'s `Schedule::command('firebase:sync-employees --commit')->dailyAt('03:00')` uncommented and deployed; a host-level cron entry (`* * * * * ... docker compose exec -T app php artisan schedule:run`) added on the homelab box (none existed before) to actually trigger Laravel's scheduler; confirmed registered and correctly due (`php artisan schedule:list` showed "Next Due: 22 hours from now" matching the 3 AM schedule).

### Mobile-first visual redesign — design system + 2 Figma mockup directions ready for Hakim's pick (Aug 18, 2026)
Hakim asked for a real visual redesign via `/design` + `/ui-ux-pro-max` skills, mobile-first (app is used almost entirely on phones). Full team dispatch (Mira), design work only — zero backend/route/JS changes, this whole pass is CSS/visual layer only.

**Design system** (`/Users/hakim/holeeMonth/MyGaji/design-system/mygaji/MASTER.md`): Mira rejected the `ui-ux-pro-max` script's raw first pass (misclassified MyGaji as a marketing-landing-page product, wrong shape for a working payroll tool) and built a grounded spec instead — refined the EXISTING brand (gold `#FFCC09`/green `#2F5E2C`, kept) rather than replacing with generic SaaS colors, standardized on Poppins+Inter (fixing a real pre-existing bug where the login page silently force-overrides fonts via `* { font-family }` while every other screen loads a different one), consolidated 3 different reds into one danger token, and produced a full mobile-correctness checklist (16px input floor for iOS zoom, 44px touch targets, safe-area handling — with a flagged coupling constraint: top nav and bottom nav share CSS classes, so a naive safe-area fix would clip the top nav's logo). Includes a frozen list of every JS-queried selector that must never be renamed.

**Figma mockups — 2 directions, 3 screens each** (Login/Dashboard/Staff List), in a new section "MyGaji Redesign Options" in the ONDW Figma file, separate from the existing 7 current-state frames (untouched):
- **Direction A "Refined Brand"**: bold gold pill buttons, gold-filled icon badges, soft shadows — closest to today's app, professionalized.
- **Direction B "Modern Minimal"**: dark-outline/ghost buttons (not gold-on-white — would fail the spec's own contrast rule), flat cards with hairline borders instead of shadows, status shown as a small dot instead of a filled pill, gold/green reserved for small accents only.

**Tooling note**: the `figma-cli` scratchpad this whole project relied on had been garbage-collected by Aug 18 (4 days after Aug 14 setup) — genuinely gone, not a subagent access issue (confirmed by Yappy's own direct call failing identically). Re-cloned fresh in under 2 minutes, see [[design-protocol]] for the exact recipe. Figma Desktop's CDP connection itself survived independently — only the daemon needed restarting from the new clone.

**2 real bugs caught by the mandatory screenshot-verify step** (not trusted from command output): `render-batch` left 5 orphaned debris frames outside any section after erroring on an unsupported `bg="transparent"` prop (found + deleted); login heading text rendered left-aligned instead of centered due to a CLI renderer quirk with `Text` nodes inside `w="fill"` flex containers (fixed by an explicit `align="center"`); Direction B's dashboard card grid wrapped to 1 column instead of 2×2 due to a width math error carried over from Direction A's card dimensions (fixed).

**Status**: waiting on Hakim to pick a direction (or ask for changes) before any real Blade/CSS implementation begins — this was an explicit gate he requested, not skipped.

**Login/access note for Hakim**: MyGaji is intentionally single-admin (same as the old app — its Firebase Auth was also admin-only, nothing per-employee). The 22 migrated staff are payroll/HR records, not user accounts — they don't log in themselves in either app.

### 🔴 Real gap found + fixed same session: production had ZERO user accounts
Hakim asked "is there login credentials for me to login" and it turned out to be a genuine, serious gap, not a rhetorical question — the `users` table on the live production homelab box was **completely empty** (`User::count()` = 0). `AdminSeeder` was never wired into `DatabaseSeeder`'s default `run()` (a pre-existing project pattern, confirmed multiple times this project) and had apparently never been run manually on production either, across this entire multi-day project — meaning Hakim had no way to log into his own live app this whole time until this was caught.

**Fixed**: created a real admin account directly via tinker on production (not by running the existing `AdminSeeder`, since that hardcodes the SAME test password — `Mu@473266` — that's been echoed in plaintext across dozens of agent reports and messages throughout this project's testing; reusing it for the real production account would mean a widely-transcript-exposed password protecting real payroll data). Generated a fresh random password instead, gave it to Hakim directly in chat (the one legitimate time to do so, since he needs it to log in), and told him to change both email/password via the Profile page once in.

**Lesson**: `SuperHakim@mygaji.com` / `Mu@473266` (from `AdminSeeder.php`) should be treated as a **dev/test-only credential going forward** — it's fine for local dev seeding (that's what it's for), but must never be treated as the real production login again now that a distinct one exists. Worth being suspicious of assuming a seeder "must have already been run" on any environment — verify (`User::count()`), don't assume, especially for anything auth-related on a live system.

## Full session detail
See `main/current-session.md` (Aug 13, 2026 entries) for the play-by-play of the initial deploy + bugs hit/fixed.
