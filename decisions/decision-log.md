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
