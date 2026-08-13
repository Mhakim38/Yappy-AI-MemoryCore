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
