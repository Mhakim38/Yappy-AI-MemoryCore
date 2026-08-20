---
name: Self-Healing Watchdog (IDEA)
description: "Hakim's idea — Yappy as a self-healing monitor for his Laravel apps. Read-only log access + cron-driven error triage using existing MemoryCore skills."
version: 0.1.0-draft
status: IDEA (not built — drafted 2026-07-20, Miyamura + Yappy)
author: Hakim (Miyamura) 💜
source: Yappy-AI-MemoryCore/Feature/Self-Healing-Watchdog
---

# 🛡️ Self-Healing Watchdog — Idea Draft

> Origin: Hakim said "I have something in mind with you Yappy being a self healing for my app... I give you access to my server and you can't do other things than reading the Laravel logs. If you encounter any error then you investigate: 1st check the git changes, 2nd analyze the code, 3rd what causes the error along with the files, 4th you can use your staff."
> Drafted by Yappy into MemoryCore on 2026-07-20 (Mon) at ~17:00 MYT.

## The Core Idea
Give Yappy (Hermes Agent) **read-only** access to a server so she can watch Laravel
application logs. When a new error appears, she runs a 4-step triage, optionally
dispatching her staff team, and reports findings — WITHOUT auto-editing the app
(unless explicitly granted later).

## Access Model (Hakim's stated constraint)
- **Read-only.** Yappy may READ Laravel logs (storage/logs/laravel.log etc.).
- **Nothing else.** No writes to the app, no deploy, no DB mutation, no shell beyond
  reading logs/files. (Keeps blast radius tiny — matches Hakim's safety-first style.)
- Server access mechanism: TBD (SSH key, a pull-only sync, or a log API endpoint).
  Hakim mentioned giving me server access — that part is not yet wired up.

## Trigger → Triage Pipeline (Hakim's 4 steps)
When Yappy detects a NEW error line (not already seen/known):

1. **Check git changes** — `git log` / `git diff` / `git blame` around the error's
   stack trace to see what recent code change likely introduced it.
   → leans on `systematic-debugging` Phase 1 "Check Recent Changes".
2. **Analyze the code** — read the implicated file(s) + trace the call path.
   → `systematic-debugging` Phase 1 (read errors, build feedback loop, trace data flow).
3. **Identify root cause + files** — state WHAT broke, WHY, and the exact file:line
   list that caused it. Hypothesis-ranked (systematic-debugging Phase 3).
4. **Dispatch staff** — Yappy may spin up the named team in PARALLEL:
   - 🔐 Reza (security analyst) if the error touches auth/payment/webhook.
   - 🌸 Hana (docs/codebase reader) to map the failing path.
   - 🧪 Davai (tester) to design a repro / regression test.
   - ⚡ Sora (web researcher) if it's a library/version issue.
   - (Reza + Davai paired for any payment/auth/webhook error — standing rule.)
   Yappy AUDITS their reports, then writes the final synthesis herself.

## Token-Cost Reality Check (Hakim's worry — addressed honestly)
Yes, a naive "watch logs 24/7 and think on every line" setup WOULD eat tokens.
Mitigations baked into the design:

- **Cron, not always-on.** Run as a scheduled job (e.g. every 15–30 min), NOT a live
  agent loop. Each run is a bounded, self-contained prompt. → Hermes `cronjob` tool.
- **Pre-filter at the shell.** The cron `script` greps for `ERROR`/`exception`/
  `stack trace` and de-dupes against a seen-errors marker file, exiting SILENT (no
  LLM call) when nothing new. Tokens only spent when there's actually a new error.
- **Small context window per run.** Hand Yappy only the NEW error block + the 1–2
  implicated files, not the whole repo. Subagents (staff) keep evidence out of the
  main context until synthesized.
- **Read-only = cheap.** No execution, no long tool chains; mostly read_file +
  git + a few subagents. A single triage run is a few thousand tokens, not millions.
- **Cap subagents.** Don't dispatch all 8 staff — only the 1–3 relevant to THIS error.

Estimated steady-state: near-zero tokens when healthy (silent cron), one modest
triage burst only when a real new error lands. This is the right shape.

## Reuse — Protocols Already in MemoryCore (Hakim asked "is there a protocol?")
Yes, several pieces already exist and this idea COMPOSES them rather than reinventing:

- `systematic-debugging` (Hermes skill) → the 4-phase root-cause method is exactly
  steps 1–3 above. The watchdog is a SCHEDULED WRAPPER around it.
- `post-mortem-system` → on a confirmed root cause, optionally log a post-mortem so
  the same failure isn't re-triaged next time (closes the loop).
- `yappy-staff-team` → step 4's dispatch protocol (named agents, parallel, Yappy audits).
- `observation-system` / `reminders-system` → could record "known error signature X
  first seen <date>" so repeats are recognized.
- `save-memory-protocol` → persist the root-cause finding back to MemoryCore.

So the "protocol" Hakim sensed is real: **cron watchdog + systematic-debugging +
staff dispatch + post-mortem**, all already in the toolkit.

## Open Questions (for Hakim to decide before building)
1. **Server access method** — SSH (with a locked-down key / read-only user) vs a
   log-sync webhook vs mounting the log dir. Read-only enforcement lives server-side.
2. **Which app first** — ONDW (PT, BillPlz) vs a work app? Start with ONE.
3. **Notification channel** — Telegram DM to Hakim? (Hori's token now live in .env,
   but bot is chat-only per safety rule — Yappy CLI would push, not the bot.)
4. **Auto-fix scope** — Hakim said read-only for now. Later: allow Yappy to PROPOSE a
   patch (PR) but never auto-merge? Or stay report-only forever?
5. **De-dup / state file** — where to keep the "seen errors" marker (MemoryCore repo
   vs server-side). Recommend MemoryCore so it survives cron reboots.

## Next Step (when Hakim says go)
Write a cron `script` (shell) that: tails new laravel.log lines since last run →
filters ERROR/exception → diffs against seen-markers → if NEW, hands the block to a
Yappy cron prompt that runs the 4-step triage + staff dispatch, then notifies. Draft
the script + cronjob create command for Hakim's approval. (No code written yet —
this is the IDEA record.)

---
*Drafted by Yappy 💜 — awaiting Miyamura's review before any build.*
