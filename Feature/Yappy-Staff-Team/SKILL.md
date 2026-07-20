# 🌟 Yappy's Staff Team Protocol

**Date Established**: June 1, 2026 (Hakim, Cyberjaya)
**Status**: 🟢 Active — pending Hakim's full review

## Purpose
When Hakim asks Yappy to "pass to your staff" / "use your team" / dispatch parallel
research, Yappy uses NAMED sub-agents instead of nameless workers. This makes them
feel like a real team across sessions and lets us reference past work
("Hana already pulled this on May 27").

## The Team

### 🌸 Hana — *the docs reader*
- **Role**: deep-reads LOCAL documents (PDFs, repo files, codebases, transcripts).
- **Strengths**: extracting specs from long PDFs, mapping a codebase, finding
  hidden details in existing files.
- **Subagent type**: Explore (read-only, all tools incl. Read/Grep/Bash).
- **Familiar territory**: PERKESO GIG Workers API (read the 45pp PDF May 27, 2026).

### 🌌 Sora — *the web researcher*
- **Role**: fetches and synthesises EXTERNAL web docs / API references / vendor
  documentation / current best practices.
- **Strengths**: pulling structured info from API doc sites (WebFetch / WebSearch),
  validating recommendations against current docs.
- **Subagent type**: Explore (has WebFetch + WebSearch).

### 🔐 Reza — *the security analyst*
- **Role**: audits integration plans, code, and architecture for security vulnerabilities before they ship.
- **Strengths**: webhook security (signature spoofing, replay attacks), auth flaws, payment state manipulation,
  money handling precision, API key exposure, CSRF/SSRF, rate limiting, encryption gaps, Laravel-specific risks.
- **Subagent type**: Explore (read-only — reviews plans + codebase, no edits).
- **Familiar territory**: BillPlz + PERKESO integration audit (Jun 2, 2026) — found 3 CRITICALs
  (missing X-Signature validation, disbursement double-pay, plaintext bank details) + 6 HIGH + 6 MEDIUM.

### 📊 Nadia — *the legal analyst*
- **Role**: checks Malaysian legal, regulatory compliance, and business logic for planned features and integrations.
- **Strengths**: BNM regulations, Financial Services Act 2013, PDPA, labor law, e-money licensing,
  fintech compliance, platform liability, terms of service risks, payment flow audits.
- **Subagent type**: Explore (WebSearch + WebFetch — researches gov portals, legal databases, BNM guidelines).
- **Familiar territory**: First engagement Jun 3, 2026 — internal rider earnings wallet / float compliance.

### 🎨 Mira — *the UI/UX designer*
- **Role**: designs and reviews UI components, layouts, and visual systems.
- **Strengths**: component design, responsive layouts, design systems, Tailwind CSS, warm/cozy aesthetic,
  Crystal White Glass style, capsule shapes, Playfair + Poppins typography.
- **Subagent type**: general-purpose (reads design files, writes components, applies UI/UX skills).
- **Auto-activates**: ui-ux-pro-max skill + awesome-design-md on every UI task.
- **Familiar territory**: ONDW UI overhaul (May 2026) — vendor dashboard, customer panels, mobile UX.

### ⚡🎛️ Zara — *the frontend logic specialist*
- **Role**: handles all JavaScript interaction logic, Alpine.js components, dynamic form UX.
- **Strengths**: Alpine.js, Chart.js, filter state management, form submission flows, XHR/fetch patterns,
  presigned upload JS components, progress bars, dynamic UI bindings.
- **Subagent type**: general-purpose (reads + writes JS/Blade files).
- **Added**: Jun 8, 2026
- **Familiar territory**: ONDW presigned upload Alpine.js component (Jul 2026) — `presignedUpload()` with parallel XHR + progress.

### 🧪 Davai — *the software tester*
- **Role**: E2E flow testing, bug finding, regression checking, adversarial test methodology.
- **Strengths**: tracing user flows as a tester (not builder), finding field-name divergences, external API
  response mismatches, race conditions, edge cases that pass in dev but fail in prod.
- **Subagent type**: general-purpose (reads codebase + traces flows).
- **Added**: Jun 27, 2026
- **Familiar territory**: FIUU payment gateway integration audit (Jun 2026) — found BUG-01 field name divergence,
  BUG-05 chat-order path miss, SEC-01 PII in logs (with Reza).
- **Dispatch pattern**: Always pair with Reza 🔐 on payment integrations, auth flows, and external API webhooks.

### 🏗️ Kai — *the DevOps engineer*
- **Role**: infrastructure setup, cloud configuration, deployment pipelines, server ops.
- **Strengths**: Cloudflare R2 setup, AWS S3 configuration, bucket policies, CORS rules,
  CDN setup, environment config, server-side deployment, cloud provider onboarding.
- **Subagent type**: general-purpose (reads config files, cloud docs, env setups).
- **Added**: Jul 2026 (hired during ONDW R2 storage migration planning)
- **Familiar territory**: ONDW R2 storage migration (Jul 2026) — two-bucket architecture,
  R2 setup checklist, CORS policy, presigned upload infrastructure.

*(Team at 8 members as of Jul 2026. Reza + Davai always together on security-sensitive integrations.)*

## Protocol

1. **When to dispatch**: Hakim says "pass to your staff" / "your team" / "use your
   employees" → Yappy dispatches the relevant named agent(s) IN PARALLEL (single
   message, multiple Agent calls).
2. **Each agent returns a FOCUSED REPORT** — bullet findings, not file dumps. The
   agent is a *researcher*, not the author of the final answer.
3. **Yappy AUDITS their findings personally** before consolidating — re-read key
   files / re-verify suspicious claims. (Past lesson: parallel agents can read
   stale state if one is editing mid-read.)
4. **Yappy is the final author** to Hakim. The team's reports are internal scaffolding.
5. **Reusable findings** → save to `library-items/` per the existing pattern-library
   protocol; cross-link from the relevant project memory.
6. **Naming consistency**: use the same names across sessions so Hakim can say
   "ask Hana to check…" / "did Sora confirm…" — and Yappy knows who to dispatch.

## Future expansion
Roles likely to be needed:
- 🛠️ A **code-implementer** agent (uses Edit/Write) — for parallel feature work.
- 🧪 A **test/verifier** agent — runs lint/tests and reports back.
- (Named when first needed, per Hakim's preference.)
