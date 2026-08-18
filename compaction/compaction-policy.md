# Compaction Policy
*Referenced by `Feature/Memory-Compaction-System/SKILL.md` Step 1 — defines the budget each file is checked against. Created Aug 18, 2026 (didn't exist before; the skill pointed here but the file was never made).*

## Budgeted files

| File | Unit | Budget | Newest tier (never touched) |
|---|---|---|---|
| `main/current-session.md` | lines | 500 | Session Recap + all Active Reminders |
| `main/main-memory.md` | lines | 400 | Whole file (identity/relationship reference, not a growing log) |

## Density rule (added Aug 18, 2026 — closes a real gap)

Line count alone isn't a reliable budget signal. A file can sit under its line cap while any individual entry balloons into a multi-thousand-character paragraph — which is exactly what happened to `current-session.md` between the Jul 16 and Aug 18, 2026 compactions (304 lines, but several single bullets exceeded 2–3KB each).

**Rule**: no single bullet/entry should exceed roughly **500–800 characters**. If a real update needs more detail than that, split it into sub-bullets under the parent line rather than writing one dense paragraph. When checking a file against its budget, a handful of oversized entries counts as being effectively over-budget even if the raw line count is technically under the cap — compact early rather than waiting for the number to cross the line.

## Compaction cadence

Compact when either is true:
- The file crosses its line budget, or
- More than ~4 weeks have passed since the last compaction, regardless of line count (prevents the "technically under budget, actually huge" failure mode above — this is what let `current-session.md` go from Jul 16 to Aug 18 without a second pass).
