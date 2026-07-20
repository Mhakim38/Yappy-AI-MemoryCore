# ☁️ ONDW — Cloudflare R2 Storage Migration Plan
*PT mode · Created: Thu Jul 16, 2026 · Last updated: Mon Jul 20, 2026*
*Status: **PRESIGNED UPLOAD BACKEND COMPLETE — 17 commits on `feature/s3-r2-storage`***
*Next: Configure R2/S3 bucket CORS, then wire up AJAX proof forms*

---

## Project Domains
- **Production**: `ondewei.my`
- **Preprod**: `preprod.ondewei.my`
- **CDN (public files)**: `assets.ondewei.my` → CNAME to `ondewei-public` R2 bucket (prod only)

---

## Decision Summary
Migrate ONDW from Hostinger local disk → **Cloudflare R2** (S3-compatible, cheapest at scale).
- Same `flysystem-aws-s3-v3` Laravel driver — zero code difference between AWS S3 and R2
- R2 free tier: 10GB + unlimited egress = **RM 0/month permanently**
- **Two separate buckets** — `ondewei-public` (CDN) and `ondewei-private` (PHP proxy only)
- Public files (menu photos, avatars): served via `301 → assets.ondewei.my` CDN — ONDW server CPU = 0
- Private files (rider docs, proofs, attachments): served via Laravel PHP proxy — client never sees R2 URL
- PHP proxy chosen over signed URLs (Reddit rule #5): no expiry = no broken links, auth re-checked every request
- Full architectural rationale: `decisions/decision-log.md`

---

## Two-Bucket Architecture (CRITICAL)

| Bucket | Disk | Contents | Access | Custom Domain |
|---|---|---|---|---|
| `ondewei-public` | `r2` | menu-items/, avatars/ | Public CDN | `assets.ondewei.my` ✅ |
| `ondewei-private` | `r2-private` | rider_documents/, delivery_proofs/, pickup-proofs/, conversation_attachments/ | PHP proxy only | ❌ NEVER |

⚠️ **Why two buckets**: Cloudflare R2 custom domain exposes the ENTIRE bucket. One bucket = rider ICs and delivery proofs accessible at guessable `assets.ondewei.my/rider_documents/1/ic.pdf`.

---

## Bucket Folder Structure (in each bucket, under `{APP_ENV}/` root prefix)

```
ondewei-public/
└── production/
    ├── menu-items/{uuid}.webp       ← one per menu item
    └── avatars/{uuid}.jpg           ← one per user

ondewei-private/
└── production/
    ├── rider_documents/{rider_id}/  ← IC, matric, licence, roadtax, vehicle photo
    ├── delivery_proofs/{order_id}/  ← rider captured at delivery
    ├── pickup-proofs/{order_id}/    ← customer captured at pickup collection
    └── conversation_attachments/{conversation_id}/
```

`APP_ENV` root prefix: local dev → `local/...`, production → `production/...`. Prevents test file pollution in same bucket. Applied transparently by Flysystem — app code never writes the prefix manually.

---

## Phase 1 — Prerequisites ✅ ALL DONE

- [x] Install `league/flysystem-aws-s3-v3 ^3.0` (commit 1c9e68d)
- [x] Fix `MenuItem.image_url` stored full URL → now stores relative path. Backfill migration added.
- [x] Fix pickup-proofs auth gap → `storage.pickup-proof` route added (customer+admin only)
- [x] Fix rider doc route hardcoded `storage_path()` → buffered R2 proxy with local fallback
- [x] Add rate limits — PATCH /profile (10/min), POST /auth/google/complete (3/min), POST /rider/orders/{id}/deliver (10/min)
- [x] Confirm delivery proof disk — was public, now r2-private

---

## Phase 2 — Storage Config ✅ DONE (commits 50b537a, e11467c)

`config/filesystems.php` has both disks. `.env.example` has all vars.

**`.env` values to fill (testing on personal AWS S3):**
```
R2_ACCESS_KEY=<IAM key>
R2_SECRET_KEY=<IAM secret>
R2_ENDPOINT=                                   ← blank for AWS S3
R2_REGION=ap-southeast-1                       ← AWS Singapore region
R2_PUBLIC_BUCKET=ondewei-test-public           ← create this S3 bucket
R2_PUBLIC_URL=https://ondewei-test-public.s3.ap-southeast-1.amazonaws.com
R2_PRIVATE_BUCKET=ondewei-test-private         ← create this S3 bucket
```

**`.env` values for production (Cloudflare R2):**
```
R2_ACCESS_KEY=<R2 API token key>
R2_SECRET_KEY=<R2 API token secret>
R2_ENDPOINT=https://<account_id>.r2.cloudflarestorage.com
R2_REGION=auto
R2_PUBLIC_BUCKET=ondewei-public
R2_PUBLIC_URL=https://assets.ondewei.my
R2_PRIVATE_BUCKET=ondewei-private
```

---

## Phase 3.5 — Presigned Upload Architecture ✅ BACKEND COMPLETE (commits 1632611–26dc336, Jul 20)

### Why presigned uploads
Files uploaded via Hostinger shared hosting caused "Takes a long time on loading" — every byte goes through Hostinger before reaching R2. Presigned architecture eliminates that:
```
Browser → POST /upload/presigned (gets URL+key, <1ms) → PUT file directly to R2 (bypasses Hostinger) → POST form with key string → save key to DB
```

### What was built (5 commits today)
| # | File | Change |
|---|---|---|
| 1 | `PresignedUploadController` | NEW — POST /upload/presigned, 3 scopes, all Reza P0+P1 security |
| 2 | `routes/web.php` | Route + throttle:20,1 |
| 3 | `RiderDocumentUpdateRequest` | rules → accept `*_key` strings |
| 4 | `Rider/ProfileDocumentController` | loop → read key strings, removed ImageCompression |
| 5 | `Rider/OrderController` | accept proof_photo OR proof_photo_key |
| 6 | `Customer/OrderController` | accept pickup_proof_photo OR pickup_proof_photo_key |
| 7 | `resources/js/presigned-upload.js` | NEW Alpine component (Zara) |
| 8 | `resources/js/app.js` | import presigned-upload |
| 9 | `resources/views/profile/edit.blade.php` | x-data + data-presigned-scope on rider doc form |
| 10 | `resources/css/app.css` | [x-cloak] { display: none } |

### Security controls implemented (Reza P0–P1)
- P0: Server constructs key from auth identity (never from client)
- P0: mime_type allowlist per scope (image/jpeg, image/png, application/pdf)
- P0: Extension from mime_type map, not filename
- P0: Ownership check for delivery_proof (rider_id match) and pickup_proof (customer_id match)
- P1: Rate limit 20 req/min, TTL 15 min

### Field naming convention
- File input `name="ic_document"` → JS uploads → injects `<input type="hidden" name="ic_document_key" value="r2-key">`
- Controller receives `ic_document_key` string
- Same pattern: `proof_photo_key`, `pickup_proof_photo_key`

### What's live vs pending
- ✅ Rider profile document update (profile/edit.blade.php) — fully wired
- ⬜ Registration form — no auth yet, traditional upload still active
- ⬜ Delivery proof (conversations/show.blade.php + _rider-proof-modal.blade.php) — AJAX forms, need separate JS integration
- ⬜ Customer pickup proof (customer/orders/show.blade.php) — AJAX form, need separate JS integration

### CORS on bucket — STATUS
- [x] AWS S3 `ondewei-test-private` — CORS added for `http://localhost` ✅ (confirmed working Jul 20)
- [ ] Cloudflare R2 `ondewei-private` — **MUST add CORS when R2 is set up** (see reminder below)

### ⚠️ REMINDER — When setting up Cloudflare R2 `ondewei-private`:
Add this CORS rule BEFORE deploying presigned uploads to preprod/prod.
R2 dashboard → `ondewei-private` bucket → Settings → CORS policy:
```json
[{
  "AllowedHeaders": ["Content-Type"],
  "AllowedMethods": ["PUT"],
  "AllowedOrigins": [
    "https://ondewei.my",
    "https://preprod.ondewei.my"
  ],
  "MaxAgeSeconds": 3000
}]
```
**Do NOT add localhost here** — prod/preprod only. localhost uses AWS S3 test bucket (separate CORS).
If you forget this, presigned PUT uploads will be blocked by CORS in browser and riders/customers get silent errors.

---

## Phase 3 — Controller Disk Swaps ✅ ALL DONE (commits ff36a06, 12bf1aa)

All 7 controllers updated. Dual-disk pattern: try R2 first, fall back to local disk during migration window.

- [x] MenuItemController → `store('menu-items', 'r2')`, relative path saved to DB
- [x] ProfileController → `store('avatars', 'r2')` + `Storage::disk('r2')->delete()`
- [x] GoogleAuthController avatar → `Storage::disk('r2')->put()` with `Str::uuid()` naming
- [x] GoogleAuthController rider docs → `storeAs('rider_documents/...', 'r2-private')`
- [x] GoogleAuthController outer catch → `Storage::disk('r2')->delete($avatarPath)` on DB rollback
- [x] Rider/ProfileDocumentController → `storeAs('rider_documents/...', 'r2-private')`
- [x] RegisteredUserController → `storeAs('rider_documents/...', 'r2-private')`
- [x] Customer/OrderController pickup proofs → `store('pickup-proofs/{order_id}', 'r2-private')`
- [x] Customer/OrderController track() JSON → uses `storage.pickup-proof` route for pickup orders (security fix)
- [x] Rider/OrderController delivery proofs → `store('delivery_proofs/{order_id}', 'r2-private')`
- [x] DeliveryConversationController → `store('conversation_attachments/{conv_id}', 'r2-private')`

**Serving routes (routes/web.php — ALL buffered, not streamed — Hostinger LiteSpeed QUIC compat):**
- `storage.menu-item` — CDN redirect 301 to `assets.ondewei.my/production/menu-items/...`; local fallback
- `storage.avatar` — CDN redirect 301 to `assets.ondewei.my/production/avatars/...`; local fallback
- `storage.rider-document` — buffered PHP proxy (admin only); local fallback
- `storage.delivery-proof` — buffered PHP proxy (customer+vendor+rider+admin); local fallback
- `storage.pickup-proof` — buffered PHP proxy (customer+admin ONLY); local fallback

**Security bugs fixed during Phase 3 review (Jul 19):**
- `customer/orders/show.blade.php` line 251: was using `storage.delivery-proof` for pickup orders → vendor could view pickup proof
- `Customer/OrderController::track()` line 773: same issue in JSON polling API
- Both fixed: now route to `storage.pickup-proof` when `order_type === 'pickup'`

---

## Phase 4 — File Migration Command ✅ Written (commit 12bf1aa) — run pending

```bash
php artisan storage:migrate-to-r2 [--dry-run] [--chunk=50]
```

- Restart-safe: progress in `storage/app/r2-migration-progress.json`
- `set_time_limit(0)` + `ini_set('memory_limit', '256M')` for Hostinger SSH
- 6 scopes: menu-items, avatars, delivery_proofs, pickup-proofs, rider_documents, conversation_attachments

```bash
php artisan storage:normalise-avatars [--dry-run]
```
- Renames old Google-avatar paths (`{username}_{timestamp}.jpg`) to UUID scheme in R2 and updates DB
- Run AFTER `storage:migrate-to-r2` completes
- Restart-safe: UUID pattern check skips already-renamed rows

**⚠️ IMPORTANT**: Migration command must be run AFTER credentials are added. Do NOT run migration on a bucket that was previously used without the `root=APP_ENV` config — files would land without the `production/` prefix and `exists()` checks would miss them. If that happens, clear `r2-migration-progress.json` and re-run.

---

## Phase 4.5 — Cloudflare R2 Setup ⬜ NOT STARTED (do before production cutover)

**Status (Jul 20):** AWS S3 test buckets working locally. R2 not set up yet.
**Docs verified:** Jul 20, 2026 against live Cloudflare docs via cloudflare-docs MCP. All findings below confirmed.

### ⚠️ Prerequisites (MUST do first)

**`ondewei.my` must be a Cloudflare zone before you can attach a custom domain to R2.**
Cloudflare requires the domain to exist as a zone in the **same account** as the R2 bucket.
- If `ondewei.my` is currently on Hostinger/Namecheap DNS → either transfer DNS fully to Cloudflare (recommended), OR use [partial CNAME setup](https://developers.cloudflare.com/dns/zone-setups/partial-setup/)
- This is a hard blocker for step 5 (custom domain). Do this first.

### API Token — use the correct permission type

For S3-compatible presigned uploads, use **"Object Read & Write"** — NOT "Admin Read & Write" (that's for Data Catalog/Iceberg, wrong scope).
- Scope the token to `ondewei-private` + `ondewei-public` buckets only (principle of least privilege)
- Token gives you `Access Key ID` + `Secret Access Key` — copy both immediately after creation (Secret Key shown once only)

### R2 setup checklist (one-time, do when ready for preprod)

1. [ ] Create Cloudflare account (or use existing)
2. [ ] **⚠️ Add `ondewei.my` as a zone in the same Cloudflare account** (transfer DNS or partial CNAME setup — required for custom domain step)
3. [ ] Go to R2 → Create bucket → `ondewei-public` (leave Block Public Access OFF for CDN)
4. [ ] Go to R2 → Create bucket → `ondewei-private` (Block Public Access: ON — no custom domain EVER)
5. [ ] R2 → Manage API tokens → Create token → **"Object Read & Write"** scoped to both buckets — copy key + secret
6. [ ] `ondewei-public` → Settings → Custom domain → Add `assets.ondewei.my`
   - Domain must already be a Cloudflare zone (step 2) for this to work
   - Cloudflare creates the CNAME record automatically
   - ⚠️ Only add custom domain to PUBLIC bucket — never to private
7. [ ] **⚠️ `ondewei-private` → Settings → CORS policy** → add:
   ```json
   [{
     "AllowedHeaders": ["Content-Type"],
     "AllowedMethods": ["PUT"],
     "AllowedOrigins": [
       "https://ondewei.my",
       "https://preprod.ondewei.my"
     ],
     "ExposeHeaders": ["ETag"],
     "MaxAgeSeconds": 3000
   }]
   ```
   *Note: `ExposeHeaders: ETag` added per Cloudflare S3-compatibility recommendation (Jul 20, 2026 docs check)*
8. [ ] Fill preprod `.env` with R2 values:
   ```
   R2_ACCESS_KEY=<token key>
   R2_SECRET_KEY=<token secret>
   R2_ENDPOINT=https://<account_id>.r2.cloudflarestorage.com
   R2_REGION=auto
   R2_PUBLIC_BUCKET=ondewei-public
   R2_PUBLIC_URL=https://assets.ondewei.my
   R2_PRIVATE_BUCKET=ondewei-private
   ```
9. [ ] `php artisan config:clear` on preprod

**Notes:**
- R2 `account_id` is in the R2 dashboard URL. Format: `https://<32-char-hex>.r2.cloudflarestorage.com`
- R2 region is always `auto` — never use `ap-southeast-1` (that's AWS S3 only)
- If CORS errors appear on custom domain: check for `cf-mitigated` header in browser DevTools — may be WAF blocking, not actual CORS

---

## Phase 5 — Production Cutover ⬜ Pending (after preprod test passes)

**Preprod test steps (on preprod.ondewei.my):**
1. Complete Phase 4.5 R2 setup first
2. `php artisan config:clear && php artisan cache:clear`
3. `php artisan migrate` (runs backfill + any pending)
4. `php artisan storage:migrate-to-r2 --dry-run` → verify counts
5. `php artisan storage:migrate-to-r2` → actual copy
6. `php artisan storage:normalise-avatars --dry-run` → check old-scheme avatars
7. `php artisan storage:normalise-avatars` → rename in R2 + update DB
8. Full regression test (checklist below)

**Production cutover:**
- [ ] `php artisan down` (maintenance mode)
- [ ] Fill `.env` with Cloudflare R2 credentials (same as preprod but prod bucket names)
- [ ] `php artisan config:clear`
- [ ] `php artisan migrate`
- [ ] `php artisan storage:migrate-to-r2`
- [ ] `php artisan storage:normalise-avatars`
- [ ] Spot-check all 6 file types
- [ ] `php artisan up`
- [ ] Monitor error logs for 1 hour
- [ ] Keep Hostinger local files 30 days then delete
- [ ] Merge `feature/s3-r2-storage` → `main`

---

## Regression Test Checklist

- [ ] Menu item photo uploads and displays correctly (vendor panel)
- [ ] Menu item photo updates — old R2 file deleted, new file serves via CDN
- [ ] User avatar upload (profile page) — CDN URL returned
- [ ] Google OAuth avatar saves correctly + old avatar deleted on profile update
- [ ] Rider uploads IC + licence docs during registration
- [ ] Admin can view rider documents (PHP proxy, not raw R2 URL)
- [ ] Delivery proof captured and viewable by customer + admin
- [ ] Pickup proof captured, NOT viewable by vendor/rider (auth check: 403)
- [ ] Chat attachment sends and loads in conversation
- [ ] Chat attachment: ConversationAttachmentController only serves to conversation members
- [ ] `assets.ondewei.my` CDN serves files (200 with cache headers)
- [ ] Old Hostinger `/storage/` URLs return 404 (nothing still pointing there)
- [ ] `storage.delivery-proof` for a pickup order → must 403 (or be unreachable from UI)

---

## Notes
- PHP proxy beats signed URLs (Hostinger): no expiry, no broken links, auth always enforced
- `APP_ENV` root prefix is transparent to app code — Flysystem applies it automatically
- `assets.ondewei.my` CDN must point at bucket ROOT — `production/` is a key prefix inside the bucket
- Post-launch: magic byte validation for PDFs, virus scan queue for rider docs
- Vendor.profile_picture: check `SELECT COUNT(*) FROM vendors WHERE profile_picture IS NOT NULL` before prod migration

---

*Plan authored: Jul 16, 2026 — full review + security audit Jul 19, 2026*
*Team: Reza 🔐, Hana 🌸, Sora ⚡, Davai 🧪, Kai 🏗️*
*12 commits total on branch `feature/s3-r2-storage`*
