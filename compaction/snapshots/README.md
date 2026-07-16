# 📦 Compaction Snapshots

Pre-compaction backups of `current-session.md` before each Memory-Compaction-System run.

## Purpose
When `current-session.md` approaches 500 lines, a full snapshot is saved here BEFORE any compression. Nothing is ever permanently lost — recover by copying the snapshot back to `main/current-session.md`.

## Naming Convention
`session-YYYY-MM-DD-pre-compaction.md` — date of when compaction was triggered.

## How to Recover
```bash
cp compaction/snapshots/session-YYYY-MM-DD-pre-compaction.md main/current-session.md
```

## Snapshot Log

| File | Date | Lines | Notes |
|------|------|-------|-------|
| session-2026-07-16-pre-compaction.md | Jul 16, 2026 | 2,393 | First compaction — manual (v2.0 consolidation). Contains sessions from May–Jun 2026. |
