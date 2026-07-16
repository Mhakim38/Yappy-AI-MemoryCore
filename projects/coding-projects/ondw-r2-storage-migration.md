# ☁️ ONDW — Cloudflare R2 Storage Migration Plan
*PT mode · Created: Thu Jul 16, 2026 · Status: PENDING — start after FT mode*

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

## Phase 1 — Prerequisites (fix these FIRST — bugs regardless of R2)

These are standalone bugs that need fixing before touching any storage driver.

- [ ] **Fix pickup-proofs auth gap** — currently `public` disk, raw URL guessable by anyone
  - Move to `local`/`private` + serve via a new controller with `order->customer_id === auth()->id()` check
  - `Customer/OrderController.php` → change `store('pickup-proofs', 'public')` → `store('pickup-proofs/{orderId}', 'local')`
  - Add serving route + controller similar to `ConversationAttachmentController`

- [ ] **Fix `MenuItem.image_url` stores full URL, not relative path**
  - Currently: `Storage::url($imagePath)` → saves `/storage/menu-items/abc.jpg` in DB
  - All other models store relative path — this is the odd one out
  - Fix `MenuItemController`: save `$imagePath` directly (relative), resolve URL in blade with `Storage::url()`
  - Run DB backfill: `UPDATE menu_items SET image_url = REPLACE(image_url, '/storage/', '') WHERE image_url LIKE '/storage/%';`

- [ ] **Fix rider doc route — hardcoded `storage_path()`**
  - Current serving uses `storage_path('app/private/rider_documents/...')` — direct filesystem string
  - After migration: no local path exists → 404/error
  - Fix: replace with `Storage::disk('private')->get($document->file_path)` + buffered response

- [ ] **Add rate limits to 3 upload endpoints**
  - `PATCH /profile` → `throttle:10,1`
  - `POST /auth/google/complete` → `throttle:3,1`
  - `POST /rider/orders/{id}/deliver` → `throttle:10,1`
  - Add in `routes/web.php` or `app/Http/Middleware`

- [ ] **Install flysystem package**
  - `composer require league/flysystem-aws-s3-v3 "^3.0"`
  - Verify it installs on Hostinger without dependency conflicts

- [ ] **Confirm delivery proof disk in `Rider/OrderController`**
  - Grep for `$proofCompressed->store(` and find the disk argument
  - Document it before changing anything

---

## Phase 2 — Cloudflare R2 Setup

- [ ] Create Cloudflare account (if not already)
- [ ] Create R2 bucket: `ondw-assets` (or two buckets: `ondw-public` + `ondw-private`)
- [ ] Create R2 API token with R2 edit permissions → get `R2_ACCESS_KEY` + `R2_SECRET_KEY`
- [ ] Get account ID → `R2_ENDPOINT = https://{account_id}.r2.cloudflarestorage.com`
- [ ] Add custom domain `assets.ondw.my` for public files (in R2 settings → Custom Domains)
- [ ] Verify Hostinger can connect: run phpinfo(), check `memory_limit`, `max_execution_time`, `open_basedir`

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

## Phase 3 — Code Changes (disk swaps)

After Phase 1 + 2 are confirmed working on preprod:

- [ ] `MenuItemController` → `store('menu-items', 'r2')`
- [ ] `ProfileController` → `store('avatars', 'r2')` + `Storage::disk('r2')->delete()`
- [ ] `GoogleAuthController` avatar → `Storage::disk('r2')->put()`
- [ ] `GoogleAuthController` rider docs → `storeAs('rider_documents/...', 'r2-private')`
- [ ] `Rider/ProfileDocumentController` → `storeAs('rider_documents/...', 'r2-private')`
- [ ] `RegisteredUserController` → `storeAs('rider_documents/...', 'r2-private')`
- [ ] `Customer/OrderController` pickup proofs → local/r2-private (from Phase 1 fix)
- [ ] `Rider/OrderController` delivery proofs → `r2` or `r2-private` (confirm in Phase 1)
- [ ] `DeliveryConversationController` → `store('conversation_attachments/...', 'r2-private')`

---

## Phase 4 — File Migration (existing files on Hostinger)

- [ ] Write Artisan command: `php artisan storage:migrate-to-r2`
  - Chunked: process 50 files per chunk, write progress to a log file
  - Restart-safe: track last processed file so re-running skips already-migrated files
  - Scope: `menu-items/`, `avatars/`, `rider_documents/`, `pickup-proofs/`, `delivery_proofs/`, `conversation_attachments/`
  - Check: `SELECT COUNT(*), SUM(LENGTH(image_url)) FROM menu_items` first to estimate volume
- [ ] Run on preprod, verify counts match
- [ ] Spot-check each file type loads correctly
- [ ] Full regression test (see checklist below)

---

## Phase 5 — Production Cutover

- [ ] Enable maintenance mode: `php artisan down`
- [ ] Run Artisan migration command on PROD
- [ ] Verify file counts + spot-check
- [ ] Run full regression
- [ ] Lift maintenance mode: `php artisan up`
- [ ] Monitor for 1 hour — check error logs
- [ ] Keep Hostinger local files for 30 days before deleting (rollback safety)

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
