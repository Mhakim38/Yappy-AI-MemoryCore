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

**Resolved same session**: Yappy can quit/relaunch Figma Desktop directly via `osascript -e 'tell application "Figma" to quit'` — no need to ask Hakim to do it by hand. **Important**: relaunch via `cd <figma-cli clone> && node src/index.js connect` (its own launcher knows to pass `--remote-debugging-port=9222`), NOT a plain `open -a Figma` — a plain relaunch starts Figma without the CDP port, port 9222 never comes up, and the whole connection has to be redone. After the proper relaunch, Figma restored the exact same "ONDW" file itself, now on a canonical `/design/` URL (self-upgraded from the old `/file/` link) with a real title and a fully responsive JS context — confirmed via a live `eval` returning `{file: "ONDW", page: "Page 1", frameCount: 33}` immediately, no hang.

## `recreate-url` / `analyze-url` notes (Aug 14, 2026)
- These commands need the `playwright` npm package, which is NOT a dependency of `figma-cli` itself and was not installed anywhere on Hakim's Mac the first time Mira used it. Fix: `npm install -g playwright` (Chromium was already cached at `~/Library/Caches/ms-playwright`, so no browser download needed) + set `NODE_PATH=$(npm root -g)` before each `recreate-url` call so the tool's dynamically-generated temp script can resolve the module. This is a persistent global npm install, outside any repo — should already be present for future sessions on this same Mac, but if `recreate-url` fails with a module-not-found error, check this first.
- `recreate-url "<url>" --name "<Frame Name>" --width <n> --height <n>` has NO login/cookie/auth support — it hits the URL fresh and unauthenticated via Playwright every time. For any app with auth-gated pages, the target app's auth needs to be temporarily bypassed (e.g. strip middleware on a local dev-only route file, capture, then revert) — there's no way to hand it a session cookie or storageState.
- Reusing an existing Figma file/canvas instead of creating a new one is fine when Hakim says so explicitly — use the `section` command (`section create "<name>" <nodeIds>`) to group new frames under a clearly-named section so they don't visually mix with existing content in that file.
- Mobile-style apps (bottom-nav layout etc.) recreate more accurately at a phone viewport (`--width 390 --height 844`, iPhone-ish) than the tool's desktop default (1440×900), even when the app is technically browser-accessed rather than a native app.

---
💜 *Simple by design. Updated without fuss.*
