# Active Reminders
*Persistent reminders that survive session changes. Updated at session end.*

## Open
- **IDUSP staff portal — confirm mode (FT vs PT)** — prototype assumed FT (no client-code commits). Flagged Sep 27, 2026.
- **IDUSP — unverified client facts to ask**: campus location, what **YINS** stands for/which authority issues the licence, whether payroll (EPF/SOCSO/EIS/PCB) is in scope, student/staff counts, academic calendar, e-Invoice applicability. Web search was rate-limited when this was researched.
- **IDUSP — pricing decision + send the 25-question sheet** (`secret_information/projects/idusp-staff-portal/open-questions.md`). RM7–8k = discovery price, not a build budget; see `pricing-and-quote.md`.
- **eFokus (FT) — two defects found while reading it for parity, NOT fixed (unasked)**: `league/flysystem-aws-s3-v3` is not installed, so its `s3`/R2 disk would fail if used (may be intentionally unused — verify first); `APP_TIMEZONE=Asia/Kuala_Lumpur` in `.env` is a no-op because Laravel 12 hard-codes `'timezone' => 'UTC'` in `config/app.php`.

## Completed
- **Test Unofficial Vendor + Rider Credit system live** (completed 2026-07-29, originally flagged 2026-07-27): Hakim clicked through the full flow live end-to-end — full detail in `secret_information/projects/ondw/changelog.md` (Jul 29, 2026 entry).
- **Update MemoryCore design protocol** (completed 2026-07-27): Created `main/design-protocol.md` with Figma desktop app usage and Hana as the designated designer.
- **Consolidate MemoryCore structure** (completed 2026-08-18, originally flagged 2026-06-18 in the now-archived `complete-reminders-list.md` and never actually done): current-session.md compacted (was overdue since Jul 16), `identity-core.md`/`relationship-memory.md` archived into `main/backups/2026-08-18/` after confirming main-memory.md covers everything load-bearing (Protocol Location Index carried forward + corrected), `complete-reminders-list.md` archived as fully superseded by this file, stale PT-mode git-permission line in main-memory.md fixed, `ondw-project.md` checklist refreshed, missing `compaction/compaction-policy.md` created (the compaction skill referenced it but it never existed).
<!-- Resolved reminders move here. Format: -->
<!-- - **Title** (completed YYYY-MM-DD): What was done and the outcome -->
