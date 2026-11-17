# Procedural 3D showcase site: build + host recipe (sanitised pattern, Nov 17, 2026)
Reusable when a client or Hakim asks for a design-system-driven 3D/scroll "WOW" site. Stack: Three.js + GSAP ScrollTrigger + Lenis, plain static output (no bundler), Apache precompressed brotli. No project secrets here.

## Process
1. Brief file with binding rules (tokens, no emoji, no em/en dashes, no hotlinks, procedural geometry only, phone first, measurable promise).
2. Vet third-party code read-only BEFORE use: `npm pack --ignore-scripts` into a scratch dir outside the repo; compare registry shasum/sha512; scan for network/eval/install hooks; check licence; pin versions older than ~14 days; vendor byte for byte + VENDOR.md; strict CSP (script/style/font self only, no inline).
3. Designer pitch (<=700 words, honest weakness) -> coder feasibility critique with a measurable promise -> build in milestones with an art gate each: static sections, material lab turntable (judge the material before scenes), scroll stages, signature interaction, footer + credits, fix round.
4. Gate: security (vendor integrity, code scan, CSP, licences, what ships) + E2E in real Chrome at 390/768/1440 (pins, anchors, pointer+touch+keyboard, reduced motion, no-JS, no-WebGL, console/network, perf). Look at screenshots yourself; reports can miss visual seams.
5. Task files + short pointer messages for agents (long pasted messages can arrive truncated).

## Techniques
- Everything procedural: lathe from bezier profiles; wood as a 3D solid lookup from a log pith with SMOOTH periodic rings (hard ring edges = pinstripes); anisotropic brass + knurl; procedural PMREM environment; key + rim + hemisphere light.
- Pinning without CLS: tall wrapper + `position: sticky; top: 0; height: 100svh`, scrub from wrapper top to bottom. JS pin (fixed/spacer swap) logs a ~1.0 layout shift per swap.
- Make the hero the SAME live 3D object as the next section (tween the pose); a baked hero still that swaps to the live model jumps. Remove any CSS vignette or dashed border painted over the canvas (draws a seam across the model).
- ScrollTrigger refresh renders each scrubbed timeline at its own progress and stamps later stages' start states over the current pose: replay the chain in order after refresh.
- Anchors to pinned sections scrolling up land at the pin end with Lenis anchors: write own handler that targets the stage start.
- Signature interaction pattern: pointer raycast, atan2 angle unwrapped, critically damped spring, magnetic detents, horizontal-intent after 8 px else native scroll (`touch-action: pan-y`), keyboard arrows, hint that fades after first use.
- ASCII footer: render the live model to a small render target, async readback (`readRenderTargetPixelsAsync` in requestIdleCallback), only on change; two layers (fine model grid, coarse pile grid); reserve the aspect ratio; links as real anchors.
- Precompile all shader programs after the first frame to avoid a mid-scroll compile hitch; keep program count fixed.

## Measuring honestly
Test on mains power (battery under 20% caps rAF at 30 Hz). Make sure the preview server serves the built `dist/` with .br (a stale server on the same port gave false 12.9 s results). Headless desktop GPU is not phone evidence. Report LCP, first live frame, long-frame %, CLS, draw calls, heap, JS size.

## Hosting a static site on Apache
Build in a clean git worktree of the committed hash. Ensure mod_headers + mod_rewrite + mod_mime are on (precompressed .br/.gz served by rewrite in .htaccess; add `RemoveLanguage .br` and `SetEnv no-gzip/no-brotli` in the .br/.gz FilesMatch). Check with curl: br request = one `Content-Encoding: br`, gzip = one, none = none, no Content-Language, CSP present. Keep asset paths RELATIVE so it can sit under a sub-path. Tailscale Funnel allows only ports 443, 8443, 10000; if used, add a path with `--set-path` (prefix stripped) and use the trailing-slash URL.
