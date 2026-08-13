# MyGaji Modernization Project

**Started**: Aug 13, 2026. **Status**: Active. **Owner**: Yappy (manager), full staff dispatch. Hakim handed this project over fully — "this project I will handle it to you overall Yappy as you are the Manager for this project."

## Goal
Convert/tally the old MyGaji system (repo: `github.com/Mhakim38/GajiAPB`, Firebase-backed) into the new Laravel MyGaji (repo: `github.com/Mhakim38/MyGaji`, currently MySQL-bound in progress) until the Laravel version reaches full feature parity with the old one. Single-user (admin-only) system.

## Infra status (as of Aug 13, ~2:00 PM)
- Laravel MyGaji deployed live on homelab box (DESKTOP-1DLDMR6, Tailscale 100.84.18.45), port 8090, `php:8.2-apache` container at `/home/hakim/docker/mygaji/`
- Was SQLite, **migrating to MySQL now** (Hakim's explicit preference, he's familiar with MySQL) — Kai designing the compose service + credentials + Laravel .env update
- Laravel Breeze's "Forgot password?" link removed from login page per Hakim's request (single-admin system, no password-reset flow needed) — `resources/views/auth/login.blade.php`
- Real payroll tables already exist: `position`, `staff`, `salary_report`, `rate`

## Blocking on Hakim
- **GajiAPB deploy key**: same SSH key as MyGaji (`ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDPInnRTb0l3NFBkGRkuyhZY/47H5yKUOV7Pq/N8WLUp hakim@DESKTOP-1DLDMR6`), needs adding as a **read-only deploy key** at `github.com/Mhakim38/GajiAPB/settings/keys`. Blocks the entire gap-analysis phase — can't compare against a repo Yappy can't read.

## Plan (phases)
1. **Infra** (in progress): MySQL migration for Laravel MyGaji — Kai
2. **Access + Discovery** (blocked on deploy key): clone GajiAPB, staff explores both codebases — old app's Firebase schema/collections, feature list, business rules; new app's current feature set
3. **Gap analysis**: Nadia (business logic/payroll rules comparison), Hana (feature/flow gaps), Kai (Firebase → MySQL schema mapping) — produce a concrete difference list
4. **Phased build plan**: Yappy synthesizes gap analysis into an ordered, executable roadmap to reach parity
5. **Execution** (future sessions): build out missing features one phase at a time

## Notes / gotchas discovered
- Running `docker compose` commands from inside `~/docker/mygaji/src/` (the Laravel root, not the compose-file directory `~/docker/mygaji/`) produced warnings referencing `WWWUSER`/`DB_DATABASE`/`DB_USERNAME`/`DB_PASSWORD`/`MYSQL_EXTRA_OPTIONS` (Laravel Sail's stock variable names) and "service app is not running" — cause under investigation by Kai as part of the MySQL setup, since two `.env` files will exist in this project (compose-level at `~/docker/mygaji/.env` and Laravel's own at `~/docker/mygaji/src/.env`) and that distinction needs to be crystal clear to avoid future confusion.
- Earlier bug (fixed): Apache's `AllowOverride None` default silently broke all non-root Laravel routes — see `main/current-session.md` Aug 13 entry for full detail, same box/pattern likely relevant to remember for any future PHP container here.

## Full session detail
See `main/current-session.md` (Aug 13, 2026 entries) for the play-by-play of the initial deploy + bugs hit/fixed.
