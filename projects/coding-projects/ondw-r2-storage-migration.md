# ☁️ ONDW — Cloudflare R2 Storage Migration Plan
*PT mode · Created: Thu Jul 16, 2026 · Last updated: Sun Jul 19, 2026*
*Status: **ALL CODE COMPLETE — 12 commits on `feature/s3-r2-storage`***
*Waiting on: Hakim to create AWS S3 test buckets + fill `.env` credentials*

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

## Phase 5 — Production Cutover ⬜ Pending (after preprod test passes)

**Preprod test steps (on preprod.ondewei.my):**
1. Fill `.env` on preprod with AWS S3 test credentials (two buckets)
2. `php artisan config:clear && php artisan cache:clear`
3. `php artisan migrate` (runs backfill + any pending)
4. `php artisan storage:migrate-to-r2 --dry-run` → verify counts
5. `php artisan storage:migrate-to-r2` → actual copy
6. `php artisan storage:normalise-avatars --dry-run` → check old-scheme avatars
7. `php artisan storage:normalise-avatars` → rename in R2 + update DB
8. Full regression test (checklist below)

**Production cutover:**
- [ ] `php artisan down` (maintenance mode)
- [ ] Fill `.env` with Cloudflare R2 credentials
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
