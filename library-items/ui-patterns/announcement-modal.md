# 📣 Announcement / Broadcast Modal (illustration + bottom sheet) Pattern

**Status**: Level 1 (Designed + mockup, build in progress; promote to Proven once shipped)
**Source**: ONDW (sanitised, brand-neutral) | **Framework**: Blade/Alpine/Tailwind, but the HTML/CSS/SVG is framework-free
**Date Added**: Oct 23, 2026 | **Live demo file**: `announcement-modal/mockup.html` (open in a browser; 2 tabs: user modal + admin page)

## What it is
A "monthly update"-style popup: spot illustration on top, title, optional date line, message, one pinned Continue button. Admin side: a form with image choice (default illustration / upload), recommended-size callout, live Preview, schedule, active toggle. Inspired by a salary-app "time to calculate" popup (illustration + friendly line + pill button).

## Why it feels good (the craft)
- **Bottom sheet on phones, centred card from `sm:`** (thumb reach, absorbs long text). Optional layout switch: `sheet` | `center` per broadcast.
- Only the body scrolls (`min-height:0; overflow-y:auto; overscroll-behavior:contain`); image, close and Continue stay put; footer has a white-to-transparent fade and `env(safe-area-inset-bottom)`.
- Media is a fixed 3:2 frame: default art = inline SVG `meet` (never cropped); uploads = `object-fit:cover` (admin sees the exact crop in Preview).
- Mobile-native rules: no tap highlight, `:active` scale, hover only inside `@media (hover:hover) and (pointer:fine)`, 44px targets (Continue 48), reduced-motion respected, `role=dialog aria-modal`, focus trap + restore, Esc/backdrop = close.
- One accent colour, max 3 uses per screen. Errors may use a semantic red (text + icon, never colour alone).
- `white-space:pre-line` + `overflow-wrap:anywhere` for admin-typed text; ALWAYS escape (`{{ }}`), never raw HTML.

## Default illustration = hand-coded inline SVG
A spot illustration needs no stock file: write 300x200 `viewBox` shapes (circles, rounded rects, paths), ink outlines + cream fills + the single accent on one object. About 1.5 KB, reusable at 96-112 px (radio card / empty state). Code: see `const ART` in `announcement-modal/mockup.html`. Licensed stock art is the upgrade path; unknown-licence art must be checked before commercial use.

## Server-side rules worth copying (Laravel)
- Show **after every login**: server session key `broadcast_seen = "{id}:{updated_at}"`, set at first render; login regenerates the session so it shows again; a newly published/edited one shows once in an already-open session.
- Long-lived logins (PWA): add a re-show cooldown (e.g. 12 h) so people who never log out still get reminded.
- Schedule: `starts_at`/`ends_at` nullable + `is_active`; live = active AND in window; newest wins, one at a time.
- Cache the active row 60 s with a null-sentinel, clear on write; wrap in try/catch so it can never break a page.
- Image upload: jpg/png/webp only, server-generated name, soft recommended size (1200x800, 3:2) warn-not-reject, hard cap on bytes and pixels (decompression bombs), delete old object on replace.
- `type`: `announcement` | `promo` (ad) with optional https-only CTA (`rel=noopener`).
- Suppress on checkout/payment routes; defer other prompts (install/push) while open.

## Validation checklist
390x844 and desktop, light/dark, long text scrolls with Continue visible, no-image and broken-image fallback, `<script>` in message renders inert, keyboard trap/Escape, iOS standalone body-scroll lock.
