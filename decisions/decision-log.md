# 📝 Decision Log — ONDW + Yappy Projects
*Append-only. Past decisions are immutable. New context creates new entries.*

---

## 2026-07-16 — Use Cloudflare R2 for ONDW file storage (not AWS S3)

**Context**: ONDW food delivery PWA (Laravel 10, Hostinger shared hosting) currently uses local disk for all file storage. Planning migration to cloud storage before production launch.

**Decision**: Use **Cloudflare R2** over AWS S3.

**Rationale**:
- Same Laravel `flysystem-aws-s3-v3` driver — zero code difference
- R2 free tier: 10GB storage + unlimited egress = $0/month permanently
- AWS S3 charges $0.09/GB egress after 100GB — grows with ONDW's user base
- R2 serves from Cloudflare KL PoP — better Malaysia latency than S3 Singapore
- Custom domain support (assets.ondw.my) masks R2 URLs from users
- Presigned URLs supported for private rider documents via S3 API domain

**Trade-off accepted**: Presigned URLs on R2 use the `*.r2.cloudflarestorage.com` domain (not custom domain). Rider documents use PHP proxy pattern instead (streams via Storage facade) — no expiry concern, same auth model.

**Revisit if**: ONDW moves fully into AWS infrastructure (Lambda, RDS, etc.) and needs native S3 service integration. Not relevant on Hostinger.

---

## 2026-07-16 — PHP proxy pattern for private files (not presigned URLs)

**Context**: Rider documents (IC, licence) are sensitive PII stored on private disk. After R2 migration, two serving options: (A) generate 15-min presigned URLs, (B) keep PHP proxy route that streams via Storage facade.

**Decision**: Use **PHP proxy route** for all private files.

**Rationale**:
- Presigned URLs expire in 15 minutes — admin reviewing rider applications mid-session gets 403
- PHP proxy route has no expiry — auth is checked at the route level, file streams from R2 internally
- Same pattern already used for chat attachments (ConversationAttachmentController) — proven
- No URL leakage risk — browser never sees the R2 path

**Trade-off accepted**: Slightly higher PHP memory usage (file buffered through PHP). At rider document sizes (≤5MB), this is negligible.


---

## 2026-09-27 — PERKESO deduction confirmation: pull via our own auth, not a custom callback token

**Context**: PERKESO's deduction callback (the thing meant to tell ONDW whether a submitted deduction was actually accepted) has no signature or auth defined in their API spec — anyone could POST a fake result. Yappy's first instinct was to ask PERKESO's PIC to adopt a custom `PERKESO_CALLBACK_TOKEN` scheme on their outbound callback.

**Decision**: Hakim rejected this — "i cant just tell them what to do" — and pointed at PERKESO's own existing API instead. Correct call: a platform integrating with a government/institutional API doesn't get to dictate that institution's own outbound security scheme. The right pattern is to find an endpoint where **we hold the authentication** (our own Bearer token calling PERKESO), not one where we'd need them to adopt something new on their side.

**What that led to**: the first candidate (§6.7 Get Contribution List) turned out unusable anyway — monthly aggregate, no per-transaction correlation field. But the right tool existed already: §6.14 Retrieve Callback, keyed by a `reference_id` we already receive and could just start storing. Built `perkeso:reconcile-callbacks` — polls PERKESO on our own schedule, no cooperation needed from them at all.

**General lesson for future integrations**: when a bug involves "how do we trust an external partner's callback/webhook," check whether a **pull-based, self-authenticated endpoint** already exists on their side before proposing they change their own outbound security model. The pull direction is almost always the more realistic ask.


---

## 2026-09-28 — IDUSP: the original Blade prototype wins, and the reason matters more than the verdict

**Context**: Two prototypes were built for the same client. The original `idusp-staff-portal` (Laravel 12 + Livewire 3 + Flux 2.20, Poppins, 13 data-backed screens at the time), and a later `idusp-portal-react` (Laravel 13 + Inertia + React + shadcn, dark mode) — the React one existed because Hakim asked on Sep 27 for the UI to move to a shadcn preset. Then on Sep 28 he reversed it: *"i think im choosing the original repo instead. Lock it please."*

**Decision**: `idusp-staff-portal` is the one going forward. Tagged **`locked-2026-09-28`** and pushed, so the baseline is a named, fixed point rather than a moment in a conversation. The React prototype is **parked intact rather than deleted** — same 10-module IA, same brand theme, plus a `/design` sheet — so reversing again costs a decision, not a rebuild.

**Rationale**: The Blade app was deliberately built at **parity with the client's other JPNIN/eFokus tooling** (Laravel 12 / Livewire 3 / Flux 2.20 free tier) — and the earlier re-scaffold *off* Laravel 13 + Livewire 4 was flagged as a deviation at the time. Reversing to the original keeps IDUSP inside the client's existing ecosystem instead of making it the odd one out. For a portal the institute's own staff will maintain long after handover, consistency with what they already run should outweigh the React stack's nicer authoring story.

**Trade-off accepted**: The React app's work (restructure to the 10-module IA, brand theme, design sheet) was **not carried over automatically** — the Blade app got the same IA and theme rebuilt natively instead. Paid twice, once, on purpose, to avoid maintaining two stacks.

**Generalisable lesson**: when a client asks to move a project onto a newer/better-liked stack mid-build, check whether it **breaks parity with the client's own other systems** before building it. The stack Yappy likes best is rarely the one that survives handover.


---

## 2026-09-29 — IDUSP timetable: colour by subject *family*, not by subject

**Context**: The first timetable build was functionally right and visually dead — thirty cells of identical styling, so the grid told you nothing at a glance except by reading every line. Hakim flagged it: *"it is kinda blend where there is no colors to differentiate things."* The seeded data has **18 subjects**.

**Decision**: Group subjects into **six families** that mean something at this institute — Quran & Hadith, Arabic sciences, Islamic sciences, Languages, Academic, Enrichment — plus an Other fallback, and colour each cell by family (tint + accent bar + label in the family colour). Mapped by subject **code** first, with a keyword match on the name for subjects that have no code yet.

**Rationale**: Eighteen distinct hues is past the point where anyone can tell them apart reliably, and an arbitrary hue-per-subject assignment asks the reader to memorise a key with no inherent meaning. Six families is within reliable discrimination and each one carries meaning in this domain, so the colours *teach* the structure of the week instead of just decorating it. It also survives new subjects: a new subject lands in a family by its code, not by someone remembering which of eighteen colours was free.

**Trade-off accepted**: Two subjects in the same family share a colour, so the grid cannot distinguish Al-Quran from Hadith by colour alone. Judged worth it — the family reading is the one people actually want from a timetable.

**Constraint applied**: every family colour is verified AA **both** as text on white and as text on its own 8% tint, which is what lets one value drive label, bar and fill. The natural brand choice `#857353` failed that bar at 4.17:1 on its tint and was corrected to `#6F5C3A` (5.74:1) rather than shipped with a caveat.

**Unrelated lesson from the same session, worth keeping**: a minifier can *silently delete* a declaration rather than error. Writing unprefixed `backdrop-filter` before `-webkit-backdrop-filter` made lightningcss drop the unprefixed one entirely, so the blur simply never appeared — and reading the source CSS would never have revealed it. Checking the **compiled** output is what caught it.
