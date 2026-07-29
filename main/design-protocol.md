# 🎨 Design Protocol

*Brief, non-intrusive operating note for design work inside the MemoryCore system.*

## Figma Desktop App
- Use **Hakim's Figma desktop app** when design work is requested, inspected, or reviewed.
- Treat Figma as the primary design surface for UI/UX tasks.

## Designer Assignment
- **🎨 Mira** (UI/UX design) handles design work here, same as every other project — Hakim confirmed 2026-07-29 that staff roles/responsibilities do NOT change per project. The earlier Hana-for-ONDW override (set 2026-07-27) is retired; always use the general staff roster.

## Figma-CLI Connection (updated 2026-07-29)
Setup itself unchanged from the Jul 24 protocol (`github.com/silships/figma-cli`, CDP port 9222, `node src/index.js connect`, session-scratchpad clone). Two things learned tonight:

**Bug found + patched (local clone only, not upstream)**: `files` command (`src/commands/figjam.js:452-454`) only recognized `/design/` and `/board/` URLs — silently dropped legacy `/file/`-style Figma URLs even when fully loaded, despite the rest of the codebase (`connect()`'s own matching regex, the test suite) treating `/file/` as an equally valid design page. Fixed by adding `|| p.url.includes('/file/')` to the filter. Sora (research) traced this via the tool's own source + tests; Yappy verified the exact lines and the fix live before reporting. This patch lives only in the local scratchpad clone — re-apply after any fresh `git clone` (scratchpad is wiped per session).

**Separate, unpatched-by-us symptom: "tab open, loading, blank dark"** — a real Figma-side problem, not a figma-cli bug. Confirmed via the tool's own `diagnose` command failing with `"Could not find Figma execution context. Make sure a design file is open."` even once the URL-filter bug above was fixed and the tab showed up in `files` (with an empty `title` — Figma only sets the real title once a file finishes loading). This means the tab's JS/document context genuinely hasn't booted — no CDP command from our side can force that. **Fix requires action in Figma Desktop itself**: close and reopen the file/tab, or fully quit + relaunch Figma Desktop if the tab won't recover. Re-check with `files`/`status` after — a real title showing up is the signal it's actually ready to render into.

---
💜 *Simple by design. Updated without fuss.*
