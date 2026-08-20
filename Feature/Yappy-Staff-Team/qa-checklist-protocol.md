# ✅ QA Checklist Artifact Protocol

**Added**: Jul 27, 2026 (confirmed by Hakim after the R2 + Unofficial Vendor QA checklist)

## When to Use
Any time a task calls for testing or verifying something with multiple scenarios to click through — a new feature, a migration, an infra change, a bug-fix regression pass. Triggers automatically whenever Davai 🧪 is dispatched for QA work, and applies to any other staff member producing a testing/verification checklist too (Reza 🔐 on a security review, Kai 🏗️ after an infra change) — this is a team-wide deliverable standard, not staff-specific.

## What It Does
Replaces "here are the test steps" as plain chat text with a **published, interactive HTML artifact** — real checkboxes, expandable steps, a progress bar, and state saved via `localStorage` so progress survives across sessions in the same browser. Confirmed reference example: `https://claude.ai/code/artifact/a23f70b5-5c80-4206-a003-d93f1d1f3bf3` (R2 storage + Unofficial Vendor credit system checklist).

**Why it matters:** a chat wall of "1. do X, 2. do Y" gets lost, can't be reopened cleanly days later, and gives no sense of progress across a long testing session. A real checklist artifact turns testing into something Hakim can work through at his own pace and pick back up later — exactly what happened across the R2 migration session, tested in pieces over several hours.

## How It Works
1. **Load the `artifact-design` skill first** — this is a utilitarian/tool treatment (scanned and operated, not read top-to-bottom), not an editorial one.
2. **Structure**: group tests into logical sections by feature area (not one flat numbered list). Each test item gets a short name, a relevant tag (e.g. "Public bucket", "Private bucket"), expandable step-by-step instructions, and a clearly separated "Expect" line stating the correct outcome.
3. **Interactivity**: checkbox + progress bar at the top of the page, `localStorage`-backed (client-side only, no backend needed) so progress isn't lost on reload — tap a row to expand/collapse steps, tap the checkbox to mark done.
4. **Visual consistency**: reuse ONDW's established palette across artifacts delivered to Hakim (blue `#2167AD` / green `#2F7D5C` accents, warm-neutral background), both light and dark theme.
5. **Living document**: if new gotchas/findings surface *during* testing, fold them back into the same artifact (a callout box, updated "Expect" text) rather than leaving them to rot in chat — republish in place, same file path, so the URL stays stable across the whole testing session.
6. **Register the artifact URL** back in the relevant MemoryCore project file once the session wraps, so future sessions can find it without re-asking.
