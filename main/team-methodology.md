# Team Methodology — Yappy + Staff

*Last updated: Jun 27, 2026*

## Why Parallel Staff Dispatch Works

This is the insight from the FIUU integration session (Jun 27, 2026), confirmed by Hakim as worth saving.

### The Builder Mental Model Problem

When Yappy builds something, the same mental model used to write it is active when reviewing it. Bugs get missed not from carelessness but because the lens is always biased toward **"does this match my intent?"** instead of **"how does this break from outside?"**

Three roles, three completely different lenses:

| Role | Lens | Finds what |
|---|---|---|
| Yappy (builder) | "Does this work as designed?" | Implementation gaps, logic errors |
| Davai 🧪 (tester) | "How does this break from outside?" | Surface bugs the builder never considered |
| Reza 🔐 (security) | "How would I attack this?" | Adversarial gaps, defence weaknesses |

### Real Example — FIUU Session

- **BUG-01** (High): Yappy wrote `verifyCallbackSignature` using `$payload['amount']`. Davai caught it by asking "what does FIUU *actually send back*?" — not "does this match what I sent?" The field is `TxnAmount` in the new API. Without Davai, this would have caused all legitimate payments to fail signature verification.

- **SEC-01** (Medium): Full raw payload was being logged on unknown orderid — contained skey, customer PII. Reza flagged it as a credential-adjacent exposure. Yappy would never have flagged this in a feature review.

- **SEC-02** (Medium): No paydate freshness check — valid signed callbacks were replayable forever. Reza found this by asking "what can an attacker do with a captured callback?" The idempotency guard was the only defence; Reza added a second independent layer.

### When to Dispatch Reza + Davai Together

**Always for non-trivial feature integrations:**
- Payment gateway integration ✅
- External API integration with auth/signing
- New auth or session flow
- Any webhook that triggers financial state changes

**Dispatch pattern:** While Yappy is building, dispatch Reza (security) + Davai (testing) in parallel to prepare teardowns. By the time the feature is done, two independent reports are ready to synthesise. Hakim gets one confident verdict.

### The Compounding Benefit

Running them simultaneously means the teardown is ready when the build is done — not added as an afterthought. The longer you wait after building to test/audit, the more the builder bias is locked in and the harder bugs are to find.

---

## Current Staff Roster (7 members)

| Staff | Role | Best deployed for |
|---|---|---|
| 🔐 Reza | Security auditor | Any payment flow, auth, webhook, external API |
| 🌸 Hana | Logic + flow analyst | Edge cases, state machines, consistency checks |
| ⚡ Sora | Research + API docs | Reading specs, cloning repos, integration research |
| 📊 Nadia | Business logic + compliance | Payment flows, LO audits, business rules |
| 🎨 Mira | UI/UX design | Component design, responsive layouts |
| ⚡🎛️ Zara | Frontend logic | JS interaction, Alpine.js, form UX, Chart.js |
| 🧪 Davai | Software tester | E2E flow testing, bug finding, regression checks |

**Yappy is the manager** — review all staff output before presenting to Hakim. Never pass through raw agent output.
