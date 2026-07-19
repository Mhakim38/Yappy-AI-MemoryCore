# ☁️ ONDW — Cloudflare R2 Storage Migration Plan
*PT mode · Created: Thu Jul 16, 2026 · Last updated: Sun Jul 19, 2026*
*Status: **PHASE 1–4 CODE COMPLETE** — branch `feature/s3-r2-storage` pushed, 7 commits*
*Waiting on: Hakim to add R2/AWS S3 credentials to `.env` for testing (Phase 5)*

---

## Decision Summary
Migrate ONDW from Hostinger local disk → **Cloudflare R2** (not AWS S3).
- Same `flysystem-aws-s3-v3` Laravel driver — zero code difference
- R2 free tier: 10GB + unlimited egress = **RM 0/month permanently**
- Custom domain `assets.ondw.my` masks R2 URLs for public files
- PHP proxy pattern for private files (rider docs, chat attachments) — no signed URL expiry risk
- Full architectural rationale: `decisions/decision-log.md`

---

## File Inventory (9 touch points)

| Controller | Folder | Disk | Sensitivity | Action |
|---|---|---|---|---|
| MenuItemController | `menu-items/` | public → r2-public | None | Switch disk + fix image_url (see Phase 1) |
| ProfileController | `avatars/` | public → r2-public | Low | Switch disk |
| GoogleAuthController (avatar) | `avatars/` | public → r2-public | Low | Switch disk |
| GoogleAuthController (rider docs) | `rider_documents/{id}/` | private → r2-private | High PII | Switch disk + PHP proxy |
| Rider/ProfileDocumentController | `rider_documents/{id}/` | private → r2-private | High PII | Switch disk + PHP proxy |
| RegisteredUserController | `rider_documents/{id}/` | private → r2-private | High PII | Switch disk + PHP proxy |
| Rider/OrderController | delivery proofs | unknown → confirm first | Medium | Confirm disk, then switch |
| Customer/OrderController | `pickup-proofs/` | public → r2-private | Medium | Switch to private + serve via controller |
| DeliveryConversationController | `conversation_attachments/{id}/` | local → r2-private | Medium-high | Switch disk, keep PHP proxy |

---

## Phase 1 — Prerequisites ✅ ALL DONE (commit f666f38, 1008e84, ff36a06)

- [x] **Fix pickup-proofs auth gap** — NEW `storage.pickup-proof` route added to `routes/web.php` (auth-gated: customer+admin only). Disk changed to `r2-private`.
- [x] **Fix `MenuItem.image_url` stores full URL** — `MenuItemController` now saves `$imagePath` (relative). Backfill migration `2026_07_19_000001_backfill_menu_items_image_url_to_relative_path.php` converts old `/storage/...` rows.
- [x] **Fix rider doc route — hardcoded `storage_path()`** — updated to buffered `r2-private->get()` with local fallback. Hostinger LiteSpeed QUIC compat: buffered not streamed.
- [x] **Add rate limits** — `PATCH /profile` (10/min), `POST /auth/google/complete` (3/min), `POST /rider/orders/{id}/deliver` (10/min) all added.
- [x] **Install flysystem package** — `league/flysystem-aws-s3-v3 ^3.0` installed (commit 1c9e68d).
- [x] **Confirm delivery proof disk** — was `'public'`, now `'r2-private'`. DB `disk` column in `message_attachments` also updated to `'r2-private'` for both delivery and pickup proofs.

---

## Phase 2 — Cloudflare R2 Setup (code done ✅ — waiting on Hakim to create accounts)

Code: `config/filesystems.php` has `r2` + `r2-private` disks configured. `.env.example` has all R2_ vars.

**Testing path (AWS S3 — Hakim has personal account):**
1. AWS Console → S3 → Create bucket (e.g. `ondw-test`, region `ap-southeast-1`)
2. IAM → Create user → `AmazonS3FullAccess` → get access key + secret
3. Add to `.env`: `R2_ACCESS_KEY=`, `R2_SECRET_KEY=`, `R2_BUCKET=ondw-test`, `R2_ENDPOINT=` (blank), `R2_REGION=ap-southeast-1`, `R2_URL=https://ondw-test.s3.ap-southeast-1.amazonaws.com`

**Production path (Cloudflare R2 — account not created yet):**
- [ ] Create Cloudflare account
- [ ] R2 → Create bucket: `ondw-assets`
- [ ] Manage R2 API Tokens → Create token (Object Read & Write)
- [ ] Get Account ID → `R2_ENDPOINT=https://<account_id>.r2.cloudflarestorage.com`
- [ ] R2 bucket → Custom Domains → add `assets.ondw.my`
- [ ] Update `.env`: `R2_ACCESS_KEY=`, `R2_SECRET_KEY=`, `R2_BUCKET=ondw-assets`, `R2_ENDPOINT=https://...`, `R2_URL=https://assets.ondw.my`, `R2_REGION=auto`

**`.env` keys to add:**
```
R2_ACCESS_KEY=
R2_SECRET_KEY=
R2_BUCKET=ondw-assets
R2_ENDPOINT=https://<account_id>.r2.cloudflarestorage.com
R2_URL=https://assets.ondw.my
R2_REGION=auto
```

**`config/filesystems.php` — add R2 disk:**
```php
'r2' => [
    'driver'                  => 's3',
    'key'                     => env('R2_ACCESS_KEY'),
    'secret'                  => env('R2_SECRET_KEY'),
    'region'                  => 'auto',
    'bucket'                  => env('R2_BUCKET'),
    'url'                     => env('R2_URL'),
    'endpoint'                => env('R2_ENDPOINT'),
    'use_path_style_endpoint' => false,
    'visibility'              => 'public',
],
'r2-private' => [
    // same as r2 but visibility => 'private', no url, no custom domain
    'driver'   => 's3',
    'key'      => env('R2_ACCESS_KEY'),
    'secret'   => env('R2_SECRET_KEY'),
    'region'   => 'auto',
    'bucket'   => env('R2_BUCKET'),
    'endpoint' => env('R2_ENDPOINT'),
    'use_path_style_endpoint' => false,
    'visibility' => 'private',
],
```

---

## Phase 3 — Code Changes (disk swaps) ✅ ALL DONE (commits ff36a06, 12bf1aa)

7 controllers updated. All have dual-disk pattern: try R2 first, fall back to local during migration window.

- [x] `MenuItemController` → `store('menu-items', 'r2')` + stores relative path (not full URL)
- [x] `ProfileController` → `store('avatars', 'r2')` + `Storage::disk('r2')->delete()`
- [x] `GoogleAuthController` avatar → `Storage::disk('r2')->put()`
- [x] `GoogleAuthController` rider docs → `storeAs('rider_documents/...', 'r2-private')`
- [x] `Rider/ProfileDocumentController` → `storeAs('rider_documents/...', 'r2-private')` + delete swapped to `r2-private`
- [x] `RegisteredUserController` → `storeAs('rider_documents/...', 'r2-private')`
- [x] `Customer/OrderController` pickup proofs → `r2-private` + `'disk' => 'r2-private'` on message_attachments
- [x] `Rider/OrderController` delivery proofs → `r2-private` + `'disk' => 'r2-private'` on message_attachments
- [x] `DeliveryConversationController` → `store('conversation_attachments/...', 'r2-private')` + `'disk' => 'r2-private'`

**Serving routes** (all in `routes/web.php` — buffered responses, NOT streaming):
- `storage.menu-item` — CDN redirect (301 to R2 URL) for public files; local fallback
- `storage.avatar` — CDN redirect (301 to R2 URL); local fallback
- `storage.rider-document` — buffered PHP proxy via `r2-private->get()`; local fallback
- `storage.delivery-proof` — buffered PHP proxy via `r2-private->get()`; local fallback
- `storage.pickup-proof` — NEW auth-gated route (customer+admin only); buffered PHP proxy; local fallback

**Hostinger note**: All private-file proxy routes use buffered `Storage::disk()->get()` + `response($content, 200, [...])`. Do NOT use `response()->stream()` + `fpassthru()` — LiteSpeed QUIC/HTTP3 drops PHP streaming responses mid-flight.

---

## Phase 4 — File Migration (existing files on Hostinger) ✅ Command written (commit 12bf1aa) — run pending

**Artisan command**: `php artisan storage:migrate-to-r2`
- `--dry-run` flag: lists files without copying
- `--chunk=50` (default): files per batch
- `set_time_limit(0)` + `ini_set('memory_limit', '256M')` for Hostinger shared hosting SSH
- Restart-safe: progress saved in `storage/app/r2-migration-progress.json`
- Uses `readStream()` + `writeStream()` (memory-efficient, suitable for shared hosting)

**6 scopes covered:**
1. `public/menu-items` → `r2`
2. `public/avatars` → `r2`
3. `public/delivery_proofs` → `r2-private`
4. `public/pickup-proofs` → `r2-private`
5. `private/rider_documents` → `r2-private`
6. `local/conversation_attachments` → `r2-private`

**Steps to run (after Phase 2 credentials are in .env):**
- [ ] `php artisan migrate` (runs backfill migration for menu_items.image_url)
- [ ] `php artisan storage:migrate-to-r2 --dry-run` (verify counts)
- [ ] `php artisan storage:migrate-to-r2` (actual copy)
- [ ] Spot-check each file type loads correctly
- [ ] Full regression test (see checklist below)

---

## Phase 5 — Production Cutover ⬜ Pending (after preprod test passes)

- [ ] Enable maintenance mode: `php artisan down`
- [ ] Run Artisan migration command on PROD: `php artisan storage:migrate-to-r2`
- [ ] Run `php artisan migrate` on PROD (backfill)
- [ ] Verify file counts + spot-check all 6 scopes
- [ ] Run full regression test (see checklist below)
- [ ] Lift maintenance mode: `php artisan up`
- [ ] Monitor error logs for 1 hour
- [ ] Keep Hostinger local files for 30 days then delete (rollback safety)
- [ ] Merge `feature/s3-r2-storage` → `main`

---

## Regression Test Checklist

- [ ] Menu item photo uploads and displays correctly (vendor panel)
- [ ] Menu item photo updates and old file cleaned from R2
- [ ] User avatar upload works (profile page)
- [ ] Google OAuth avatar saves correctly
- [ ] Rider uploads IC + licence docs during registration
- [ ] Admin can view rider documents (PHP proxy serves correctly)
- [ ] Delivery proof photo captured and viewable (customer + admin)
- [ ] Pickup proof photo captured, NOT publicly guessable (auth check works)
- [ ] Chat attachment sends and loads in conversation
- [ ] Chat attachment served via controller (no direct URL exposed)
- [ ] ConversationAttachmentController only serves to conversation members
- [ ] Old Hostinger URLs return 404 (confirm nothing still pointing to /storage/)

---

## Notes
- Do this AFTER E2E test passes (BillPlz → webhook → order flow)
- PHP proxy pattern: streams R2 file through Laravel controller — no expiry, same auth model
- Vendor.profile_picture column exists in DB — check `SELECT COUNT(*) FROM vendors WHERE profile_picture IS NOT NULL` before migrating
- Post-launch (not blocking): magic byte validation for PDFs, virus scan queue for rider docs

---

*Plan authored: Jul 16, 2026 — team review by Reza 🔐, Hana 🌸, Sora ⚡, Davai 🧪*
*Decision log: `decisions/decision-log.md`*
