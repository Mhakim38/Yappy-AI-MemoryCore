# 🏛️ MPAJ iComm — Project Reference
*First analyzed: Jun 16, 2026 by Sora + Yappy*
*Status: 🟢 Active maintenance — Hakim is maintainer*

---

## 📌 What Is This System?

**MPAJ iComm** — Integrated citizen-service and internal management platform for **Majlis Perbandaran Ampang Jaya (MPAJ)**, a Malaysian local authority (Pihak Berkuasa Tempatan / PBT).

Two audiences:
- **Public/Resident-facing**: Rate (cukai taksiran) account management, bill payment, facility bookings, ownership transfer applications, tenders/procurement, klinik panel registration
- **Staff/Internal**: HR (Personalia), task tracking (Itask), enforcement (kompaun/saman), clinic admin, procurement evaluation workflow

**Live domains**: `icomm2.mpaj.gov.my` (web) · `icommapp.mpaj.gov.my:3100` (mobile app)
**Repo**: `/Users/hakim/holeeMonth/2qa_projects/mpaj-icomm`

---

## 🛠️ Tech Stack

| Layer | Detail |
|---|---|
| Framework | Laravel 10.x (`^10.10`) |
| PHP | `^8.1` |
| Frontend | Blade + **Livewire 2.x** (heavily — almost all pages are Livewire components) |
| Build tool | Vite 4 |
| CSS | Bootstrap (Monster Admin Template by WrapPixel) |
| Icons | MDI (Material Design Icons) |
| Auth | Custom Livewire `Login.php` + Laravel Auth + Sanctum (for mobile API) |
| Charts | `asantibanez/livewire-charts`, `mediconesystems/livewire-datatables` |
| RBAC | Spatie Laravel Permission v5 + custom `KawalanPaparan` feature flags |
| Audit | `spatie/laravel-activitylog` + `owen-it/laravel-auditing` |
| PDF | Custom `PdfController` + `PdfHelper.php` (DomPDF) |

---

## 🗄️ Database — 4 Connections

| Connection | Purpose |
|---|---|
| `mysql` | Main app DB (default) |
| `mysql2`, `mysql3` | Secondary MySQL (legacy/ekiosk mirror tables) |
| `oracle` | Legacy ORAGIS/ISMET Oracle DB (read via `yajra/laravel-oci8`) |
| `sgis` | SGIS Oracle (spatial/GIS data) |

### Key Table Groups

**Payment/Finance (cryptic legacy Oracle names):**
- `tvabaki` — Outstanding assessment bill balances per account
- `kmvndk` — Vehicle/compound-related accounts
- `xpymnt` — Payment transaction records (inserted after successful payment)
- `ypymnt` — Another payment type
- `elpnyt` — Licence payment-related
- `payment_collections` — Pre-payment staging (one row per bill item before SenangPay redirect)
- `senangpay_transactions` — SenangPay gateway transaction log
- `mass_payment_account` — Mapping of bil codes to bank accounts for split settlement
- `Old*` tables — Historical records from BillPlz, iPay88, RaudhahPay (decommissioned gateways)

**Assessment/Taksiran**: `ismet_data`, `pminduk`
**Facility Booking**: `fasiliti`, `fasiliti_tempahan`, `fasiliti_*` (12+ tables)
**Cagaran (Security Deposit)**: `cagaran_*` tables
**Enforcement (Misys)**: `misys_kompaun`, `misys_*` tables
**Procurement**: `procure_*` (30+ tables)
**HR/Personalia**: `intranet_*` (30+ tables)
**Klinik Panel**: `klinik_*` tables
**Ekiosk mirrors**: `ekiosk_*` variants of most financial tables (synced by Cron)
**System**: `users`, `kawalan_paparan`, `activity_log`, `hebahan`, `notifications`

> ⚠️ Core financial table names (`tvabaki`, `kmvndk`, `xpymnt`, etc.) are cryptic — inherited from the legacy Oracle ISMET/ORAGIS system.

---

## 💳 Payment Integration — SenangPay (ONLY ACTIVE GATEWAY)

Old gateways (BillPlz, iPay88, RaudhahPay) exist only as `Old*` models from previous iComm. SenangPay is the ONLY live gateway.

### Key Files

| File | Purpose |
|---|---|
| `app/Helpers/Helper.php` | **Core payment logic** — 1,519 lines. SenangPay pre-payment, verify, notify, SMS |
| `app/Http/Controllers/PembayaranController.php` | Payment controller — redirect, semak, berjaya, gagal |

### ENV Keys
```
SENANGPAY_URL=https://app.senangpay.my/
SENANGPAY_MERCHANT_ID=377169224545019
SENANGPAY_SECRET_KEY=<secret>
SENANGPAY_ENDOWMENT_MERCHANT_ID=<separate merchant for endowment split settlement>
SENANGPAY_ENDOWMENT_SECRET_KEY=<secret>
EKIOSK_CHANNEL=<terminal/operator code inserted into xpymnt records>
```

### Payment Flow
```
1. User selects bills → Livewire calls Helper::prePaymentSenangpay() with Crypt::encryptString() payload
2. payment_collections rows created (one per bill item)
3. User redirected to SenangPay via encrypted URL
4. SenangPay calls back /api/pembayaran/semak-pembayaran
5. Helper::semakPembayaranSenangpay() → calls SenangPay apiv1/query_order_status → verifies → updates all related tables → inserts xpymnt records (for Oracle ekiosk sync)
```

### Hash Generation
HMAC-SHA256: `hash_hmac('sha256', MERCHANT_ID . SECRET_KEY . ORDER_ID . AMOUNT . CALLBACK_URL, SECRET_KEY)`

---

## 🏗️ Architecture Notes

- **No `app/Services/` folder** — all business logic is in `Helper.php` or directly inside Livewire component `mount()`/action methods. The Helper is the de-facto service layer.
- **Livewire 2.x** (not 3.x) — `wire:model`, `wire:click`, `$emit` syntax (not `dispatch`)
- **150+ Livewire components** in `app/Http/Livewire/` organized by feature domain
- **80+ Artisan commands** in `app/Console/Commands/` — SenangPay cron reconciliation, Oracle/Ekiosk sync, data migration
- **Mobile app** served via `/api/mobile/*` with Sanctum token auth

### Custom Middleware
- `SKBMiddleware` (`skb`) — Gates facility booking behind Sijil Kelayakan Bangunan check
- `KawalanPaparanMiddleware` (`kawalan_paparan`) — Feature-flag middleware; `kawalan_paparan` table controls which UI sections are visible

### Submodules (4 active)
- `Epelesenan` — E-Lesen (business licensing)
- `Etempahan` — E-Tempahan (event/ticket booking)
- `Poslite` — Postal lite (document delivery)
- `Stla` — STLA form/application system

---

## 🔴 Known Bugs & Issues

### BUG #1 — FIXED Jun 16, 2026: `network_info` undefined — 500 after SenangPay FPX/Touch N Go payment
**File**: `app/Helpers/Helper.php` lines 165–179
**Trigger**: FPX and Touch N Go payments via SenangPay — API response does not include `network_info` key for these payment modes. The redirect block tries to access `$dataSenangPay['network_info']['referer']` → undefined array key crash.
**Root cause**: `$redirectInfo` was already an empty array (all redirect entries commented out lines 50–72) making the entire redirect block dead code. The crash was still happening because the array key access happens before the `->count() != 0` check.
**Fix applied by Hakim**: Entire redirect block commented out (lines 165–179):
```php
//redirect here, if from other platform
// $redirectInfo = collect($redirectInfo);
// if($redirectInfo->where('url',$dataSenangPay['network_info']['referer'])->count() != 0)
// { ... }
// end redirect
```
**Status**: Fix applied, NOT committed (FT mode). Payment now completes successfully without 500 error.

### LATENT BUG #2: `explode('?', $request->fullUrl())[1]` — Helper.php:174
Crashes if URL has no query string. Currently unreachable (blocked by empty `$redirectInfo`). Fix when re-enabling redirect block.

### CODE SMELL: Hardcoded SMS credentials — Helper.php ~line 967
`->withBasicAuth('mpaj', 'MP@j1723')` — SMS API credentials hardcoded. Should be moved to `.env`.

### REPO SMELL: `config/database.php.save`
Backup file in config/. Should be removed from repo.

### DUPLICATE ROUTE BLOCK: `/klinik-panel/*` in web.php
Defined twice (lines 628–658 and 641–658). Second block is superset. Functional but messy.

### ⚪ DISCARDED — SFTP file-routing gap (found + Phase 1 implemented 28 Jul 2026, discarded 29 Jul 2026)
Hakim asked to fully discard this work on 29 Jul — someone else ("she") already made her own separate SFTP-related changes. Confirmed via `git status` the tracked-file edits were already reverted before I checked; removed the 2 leftover untracked new files to complete the discard. **Nothing of this remains in the working tree as of 29 Jul.** Keeping the write-up below purely as historical reference of the diagnosis (the underlying "sftp disk configured but never wired into upload code" problem is still real and still there) — if this comes up again, treat it as a fresh investigation, don't assume any of the below is still applied.

Diagnosed why local disk storage keeps filling up despite a working, tested `sftp` disk (`config/filesystems.php`): every file-upload call in the app hardcodes `'public'`/`'upload'` (local disks) as the explicit disk argument — sftp was configured but never actually wired into upload code. Real scope, confirmed by reading the code (not estimated): 34 files, 167 write call sites across 6 shapes, dozens of read call sites with no sftp-awareness at all, no DB column anywhere tracks which disk a file lives on.

Hakim chose to phase it: **reads first → writes → migrate existing files last**, verifying each phase before the next. **Phase 1 (reads) fully implemented** across 26 files:
- New `app/Helpers/StorageHelper.php` (follows the existing `PdfHelper.php` precedent) — one `resolveDisk()`/`respond()`/`download()` helper used everywhere instead of each call site hand-rolling its own disk probe.
- Fixed `file.view` route (`routes/web.php`) — the single highest-leverage change, since dozens of blade files hardcode `route('file.view', ['disk' => ...])`. Also found and fixed 3 more broken raw-`storage_path()` routes beyond the ones originally spotted (`view.file`, `view.proposal.file`, `view.relevant.file`) — same bug, a shape the first grep pass missed.
- Refactored all ~20 files using the "check upload, then check public" read-probe pattern (~30 call sites) to use `StorageHelper` instead.
- **2 extra bugs found and fixed along the way, unrelated to the original ask**: (1) `NotifyPegawaiForPetenderOffer.php` + `KontraktorAppointmentNotification.php` built mail attachments via a raw local file path derived from `Storage::disk($x)->path(...)` — would silently break for any sftp-stored file; switched to Laravel's `Attachment::fromStorageDisk()`, which is disk-agnostic. (2) `TawaranPegawai.php`'s download button was already broken independent of sftp — its stored `file_path` was never prefixed with `upload/`, so `storage_path('app/'.$file->file_path)` was looking in the wrong place regardless.
- 9 of 13 files hardcoding public-disk URLs fixed (routed through `file.view`). 3 left alone on purpose (`GeneratesProcureEnvelopePdf.php`, `SenaraiDokumenPelawaanTender.php`, `SenaraiIklan.php`) — they generate+write a PDF from scratch bypassing `Storage::` entirely, which is real Phase 2 (write-side) work, not a read fix.
- `tests/Feature/StorageHelperTest.php` added (7 tests, `Storage::fake()` only — deliberately no `RefreshDatabase`, since this repo's `phpunit.xml` has no isolated test database configured and the local dev DB isn't safe to let a test suite touch).

**Status: DISCARDED 29 Jul 2026, working tree clean.** If SFTP routing is picked up again later, it needs a fresh investigation — check what "she" actually changed first, don't assume this write-up still matches reality.

---

### 🟢 FIXED (29 Jul 2026, not yet committed) — CronCheckPaymentSenangPay lock timeout
Real production incident, root-caused via live log correlation rather than guessed: `SQLSTATE[HY000]: General error: 1205 Lock wait timeout exceeded` on the hourly payment-reconciliation cron. The failing `UPDATE payment_collections ... WHERE rp_productID = X` sat blocked for **exactly 50 seconds** — matches MySQL's default `innodb_lock_wait_timeout` precisely (`updated_at` value being written showed `15:59:31`, error logged `16:00:21`).

Two compounding causes:
1. `payment_collections` (15,772+ rows) has **no index** on `rp_productID`, `paid`, or `timestamp` — confirmed by reading every migration; the table's only index (`description`+`myID`) is unused by this cron. Every query is a full table scan, and InnoDB's default isolation can lock rows merely examined during a scan, not just the one matched.
2. `CronCheckPaymentSenangPay.php` wrapped its entire daily batch loop in one outer transaction (`DB::beginTransaction()` before the loop, `commit()` only after every order that day finished) — so any lock taken processing order #1 stayed held until the last order in the batch was done.

**Fix** (both in the local working tree, not committed — FT mode, Hakim commits):
- New migration `database/migrations/2026_07_29_000001_add_indexes_to_payment_collections_table.php` — adds the two missing indexes. Verified locally (ran, checked via `SHOW INDEX`, rolled back cleanly, re-applied).
- `app/Console/Commands/CronCheckPaymentSenangPay.php` — removed the outer `DB::beginTransaction()`/`commit()`/`rollback()` (each order's real writes already have their own transaction handling inside `Helper::semakPembayaranSenangpay()`). Verified via a real local run — hit an unrelated pre-existing local-only gap (the `Epelesenan` submodule isn't even registered in this checkout's `.gitmodules`), but confirmed the fix itself behaves correctly: exception caught cleanly, no dangling transaction.

Diagnosis process worth remembering: this took several rounds of Hakim running real commands on staging/production and pasting back actual logs (not me guessing) — including catching that my first hypothesis (a mixed-format `timestamp` column silently breaking date-range queries) was **wrong**, disproven by a real test returning 22 rows instead of the predicted 0. Left that as a known code smell, not a bug, once disproven.

**Not yet done**: deploy + verify on staging/production — needs Hakim, no direct server access from here.

---

## 📁 Route Structure (web.php — 1,674 lines)

| URL Prefix | Purpose |
|---|---|
| `/` — public | Login, register, forgot-password, news, barcode |
| `/dashboard` | Main dashboard |
| `/akaun-saya/*` | Resident bill accounts, statements, payment |
| `/permohonan/*` | Assessment applications (pindaan, pindah milik) |
| `/perkhidmatan/*` | Facility bookings (behind `skb` middleware) |
| `/perolehan/*` | Procurement/tender portal |
| `/admin/*` | Full admin panel (Kutipan, Fasiliti, Perolehan, Cagaran, Tetapan, Log) |
| `/staff/*` | Staff modules (Klinik, Itask) |
| `/admin-klinik/*` | Klinik admin panel |
| `/pdf/*` | 40+ PDF generation endpoints |
| `/api/pembayaran/*` | SenangPay callbacks |
| `/api/mobile/*` | Mobile app API (Sanctum) |
| `/api/misys/*` | Misys enforcement system REST |

---

## 🔑 RBAC

- **Spatie Laravel Permission v5** — string-based permissions per route middleware
- Example: `->middleware('permission:Kutipan')`, `->middleware('permission:Perolehan-Semakan Urussetia')`
- Roles: Super Admin, Admin, HR, Staff, Klinik Panel company, Contractor (Perolehan)
- `FasilitiKategori::permissionName()` — dynamically generates permission strings per facility category
- `kawalan_paparan` table — feature-flag system for showing/hiding UI sections

---

## 💻 Local Dev Setup (Jun 16, 2026)

### Prerequisites
- ONDW Docker MySQL (`ondw-mysql` container) must be running: `docker start ondw-mysql`
- Database `mpaj_icomm2` exists inside it (created Jun 16, 2026)

### .env (local overrides)
```
APP_ENV=local                  # IMPORTANT: must be local, NOT prod (prod loads submodule Blade views)
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=mpaj_icomm2
DB_USERNAME=root
DB_PASSWORD=root_password
```

### To run locally
```bash
cd ~/holeeMonth/2qa_projects/mpaj-icomm
php artisan serve
# Opens at http://127.0.0.1:8000
```

### Local-only code changes (DO NOT deploy these)
These are workarounds for fresh local install — they are fine on staging/prod:

1. **`app/Models/FasilitiKategori.php`** — `Schema::hasTable()` guard at top of `scopePermissionName()`. Prevents boot crash when `fasiliti_kategori` table doesn't exist yet.

2. **`app/Providers/AppServiceProvider.php`** — Doctrine DBAL `geometry` type mapping registered in `boot()`. Required because `misys_kompaun` has a `geometry` column that Doctrine doesn't understand when doing `renameColumn`.

3. **`config/app.php`** — `Oci8ServiceProvider` + all 4 submodule providers commented out:
   - `Yajra\Oci8\Oci8ServiceProvider` (ext-oci8 not installed locally)
   - `Epelesenan`, `Etempahan`, `Poslite`, `Stla` service providers (submodule dirs are empty)

4. **6 migration files** — Added `Schema::hasTable()`/`hasColumn()` guards to migrations that assume tables exist (true on staging, not on fresh local install). Migrations affected: jabatan_unit, procure_allocation_form, intranet_kursus, rename_statuses, rename_forms, and 4 stla_* migrations.

5. **`app/Http/Livewire/Login.php` line 78** — Null check on `Attribute::kategoryTempatMenarik()`. On empty local DB, scope returns null which would crash when accessing `->ref_attributeValue`.

---

## 📋 Pending Tasks

### TASK #1 — MyDigital ID Login Endpoint
*Added: Jun 23, 2026 | Status: ⬜ Pending — spec sent to backend team*

**Endpoint:** `POST /api/mobile/loginMyDigital`
**Auth input:** `Authorization: Bearer <MyDigital access token>` (header only)

#### Backend Requirements

1. **Token validation** — validate using Keycloak OIDC issuer:
   `https://sso.digital-id.my/realms/mpaj`

2. **NRIC extraction** — retrieve from `preferred_username` claim in the verified token.
   > 🔴 **Security**: Do NOT accept NRIC sent separately by the app. Only use identity claims from the verified MyDigital token.

3. **Account lookup** — find corresponding MPAJ account by NRIC.

4. **Success response** — return the same `token` + `userData` structure as `/api/mobile/loginMobile`.

5. **Not found response** — return HTTP 404:
```json
{
  "code": "MPAJ_ACCOUNT_NOT_FOUND",
  "message": "Akaun MPAJ tidak dijumpai",
  "mydigital_user": {
    "ic": "...",
    "name": "...",
    "email": "..."
  }
}
```

#### Open Questions for Backend Team
- [ ] Token expiry — how is it handled? Does the app need to refresh?
- [ ] Logout — should this endpoint invalidate the MyDigital token or just the local Sanctum token?
- [ ] Refresh-token behavior — does MyDigital SSO support refresh tokens?
- [ ] Account registration/linking — if MPAJ account not found, is there a registration flow, or just 404?

#### Flutter App Data Requirements
The app needs to store from the success response:
`token` · `entryID` · `IC` · `name` · `email` · `phone` · `citizenship` · `last name`

> Request a **sample successful JSON response** from backend so Flutter team can map fields correctly.

---

## 📜 Key Commits (Jun 2026)

| Date | What |
|---|---|
| Jun 16, 2026 | Bug fix: `network_info` null guard in Helper.php:168 (FPX SenangPay 500 error) |
