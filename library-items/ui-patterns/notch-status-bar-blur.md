# 🌫️ iOS PWA Notch / Status-Bar Blur (Locked-Scroll Shell)

**Project**: ONDW Food Delivery PWA
**Settled**: Sep 14-16, 2026 (2 failed attempts, then confirmed working — see "The Cache Trap" below)
**Reference**: ported from a friend's app, BajetBro (`github.com/Tuanwaf/BajetBro`, `src/app.css`'s `.status-bar-blur`)
**Context**: an installed standalone PWA on iOS has no browser chrome — the device's notch/status-bar area sits directly over your page content with no automatic frosting, unlike a regular Safari tab.

---

## The Core Problem

You want the status-bar/notch area to read as a frosted, blurred strip over whatever scrolls underneath it — like a native iOS app's translucent status bar — but only in standalone (installed) mode, and only on devices with a real notch/safe-area inset.

`backdrop-filter` needs to sample the *actual rendered pixels* of the content scrolling behind it. Anything that isolates your blur element onto its own GPU compositing layer cuts it off from that content, and it silently renders as a flat, unblurred rectangle instead — no error, no console warning, just wrong.

---

## What Doesn't Work

```css
/* ❌ position: fixed inside a locked-scroll shell */
.notch-blur {
    position: fixed; /* BajetBro's own original recipe */
    top: 0;
}
/* Fails here because this app's mobile shell locks <body> and scrolls an
   inner <main> instead of the whole page — a `fixed` element pinned to
   the OUTER (locked) body never sees the INNER <main>'s scroll content
   passing behind it. BajetBro's own code comments already document this
   exact trap for any app using a similar locked-shell scroll model. */

/* ❌ Self-isolating GPU layer promotion on the blur element itself */
.notch-blur::after {
    transform: translateZ(0);
    will-change: transform;
    backdrop-filter: blur(3px);
}
/* Looks like a reasonable "force hardware acceleration" addition, but it
   promotes THIS element onto its own isolated compositing layer — cut off
   from whatever's behind it, which is exactly what backdrop-filter needs
   to composite WITH. Renders as a dead, unblurred strip. */
```

---

## What Works — The Pattern (confirmed on iOS installed PWA)

**Step 1**: Use `position: sticky` (not `fixed`) on a zero-height anchor at the top of your locked scroll container, so it stays pinned at the top of whichever element is ACTUALLY scrolling in your shell — not necessarily `<body>`.

**Step 2**: Put the actual visual strip on a `::after` pseudo-element sized to `env(safe-area-inset-top)`, masked so it fades out rather than hard-cutting.

**Step 3**: Do NOT add any `transform`/`will-change`/`isolation` property to the blur element. Let it composite naturally with whatever's behind it.

**Step 4**: Gate the actual `backdrop-filter` to `@media (display-mode: standalone)` — in a normal browser tab, the browser's own chrome already has its own frosting; layering yours on top looks wrong there. Outside standalone mode, `env(safe-area-inset-top)` is also normally `0px` anyway, so the anchor is an invisible strip regardless.

```css
.ow-notch-blur {
    position: sticky;
    top: 0;
    height: 0;      /* the anchor itself takes no layout space */
    z-index: 60;
}
.ow-notch-blur::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: calc(env(safe-area-inset-top, 0px) + 14px);
    pointer-events: none;
    -webkit-mask-image: linear-gradient(to bottom, #000 0%, #000 65%, transparent 100%);
    mask-image: linear-gradient(to bottom, #000 0%, #000 65%, transparent 100%);
}
@media (display-mode: standalone) {
    .ow-notch-blur::after {
        backdrop-filter: blur(3px) saturate(120%);
        -webkit-backdrop-filter: blur(3px) saturate(120%);
    }
}
```

```html
<!-- Placed as the FIRST child of the element that actually scrolls in your
     shell (here, <main> — not <body>, since this app locks <body> and
     scrolls an inner <main> on mobile). -->
<main>
    <div class="ow-notch-blur" aria-hidden="true"></div>
    <!-- ...rest of scrollable page content... -->
</main>
```

---

## The Cache Trap — Why "It Doesn't Work" Might Actually Mean "You Never Actually Tested It"

This pattern went through 2 dead-end attempts (position rewrite, then GPU-layer removal) that each still tested as "not working" on a real device — but the SECOND attempt's code was actually already correct. The real problem was somewhere else entirely: **content-hashed, `immutable`-cached CSS bundles can silently prevent a real device from ever loading your fix at all.**

If your build pipeline bundles this CSS into one hashed output file (e.g. Vite's `app-[hash].css`) served with `Cache-Control: immutable, max-age=31536000` (a full year), a browser or installed PWA that already cached the OLD hash will **never re-check it**, no matter how many times you reload, clear Safari's "website data," or even reinstall the PWA — because from the browser's perspective, the URL simply never changed, so there's nothing to re-fetch.

**Symptom**: you ship a real, correct fix, test it, see no change, and reasonably conclude the code must be wrong — when actually the device just never received the new bytes.

**How to tell the difference**: force a NEW hash before concluding a fix doesn't work. The cheapest way is to edit *any* other line in the same bundled source file (even something unrelated and trivial) so your build tool is forced to emit a new content hash — if the "broken" feature suddenly works after that unrelated edit, the code was fine all along; you were debugging a stale cache, not a bug. Don't treat "I tested it and nothing changed" as proof the code is wrong until you've confirmed a fresh copy actually reached the device — check the Network tab for the new hashed filename, not just "I reloaded the page."

---

## Files in ONDW

| File | Role |
|---|---|
| `resources/css/navigation.css` | `.ow-notch-blur` + `::after` rules (imported into `resources/css/app.css`) |
| `resources/views/layouts/app.blade.php` | `<div class="ow-notch-blur">` injected as first child of `<main>` |
| `public/build/assets/.htaccess` | The `immutable` cache-control header that creates the trap above — see the codebase's own recurring "this file gets wiped by every `npm run build`, must be manually restored" gotcha, tracked separately |

---

## Silent Failure Traps Summary

| Trap | Symptom | Fix |
|---|---|---|
| `position: fixed` inside a locked-scroll shell | Blur renders in the wrong place or not at all relative to actual scroll content | Use `position: sticky` on the element that's actually inside the real scroll container |
| `transform`/`will-change` on the blur element itself | Blur renders as a flat, unblurred rectangle — no error | Remove any property that promotes the blur element to its own isolated compositing layer |
| No `display-mode: standalone` gate | Blur looks wrong/duplicated in a normal browser tab, layered on top of the browser's own chrome | Gate `backdrop-filter` specifically, not the whole element |
| Immutable-cached bundle masks a real fix | "I fixed it but it still doesn't work" across multiple attempts | Force a new content hash (edit anything else in the same bundle) before concluding the code is wrong |
