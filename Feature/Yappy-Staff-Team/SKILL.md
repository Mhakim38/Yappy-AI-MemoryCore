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

*(Add more team members as workload grows — e.g. a code-implementer agent later.)*

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
