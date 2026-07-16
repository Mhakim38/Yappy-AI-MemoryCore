# PERKESO GIG Workers API Integration (Laravel)
**Level**: 2 (Working — deduction submission confirmed on sandbox Jul 4, 2026)
**Source**: ONDW (Laravel food-delivery PWA)
**Status**: ✅ Sandbox working; production pending IP whitelist
**Date Added**: May 27, 2026 | **Last Updated**: Jul 4, 2026

---

## Problem Statement
Integrate a Malaysian government API (PERKESO **GIG Workers API v2.1**, ACT 789) into a gig platform to submit **1.25% of each completed job** as a rider's social-security contribution. REST/JSON, HTTPS-only, Bearer-authenticated, JSend (`success`/`fail`/`error`), **IP-whitelisted**.

## ⚠️ The #1 Gotcha: IP Whitelisting
PERKESO whitelists your server's egress IP. Requests from a non-whitelisted IP are **silently dropped → "Request Timeout"** (NOT a 403/401).
- ❌ Postman / curl from a laptop → times out forever.
- ✅ `curl` ON the server → 200 + JSON.
- Give PERKESO your **egress** IP (`curl ifconfig.me` on the server) — may differ from DNS A-record.

---

## Solution Overview
1. **`PerkesoService`** — thin HTTP wrapper, one method per endpoint, base URL + token from config.
2. **`PerkesoDeductionService`** — orchestrates cap logic, registration check, deduction submission, retry scheduling.
3. **Admin testing harness** — one controller method per endpoint + jQuery UI to exercise every endpoint server-side before automating.

---

## config/services.php
```php
'perkeso' => [
    'env'            => env('PERKESO_ENV', 'sandbox'),
    'sandbox_url'    => env('PERKESO_SANDBOX_URL', 'https://gig-sandbox.perkeso.gov.my'),
    'production_url' => env('PERKESO_PRODUCTION_URL', 'https://gig-connector.perkeso.gov.my'),
    'token'          => env('PERKESO_TOKEN'),
    'client_id'      => env('PERKESO_CLIENT_ID'),
    'client_secret'  => env('PERKESO_CLIENT_SECRET'),
    'sector_code'    => env('PERKESO_SECTOR_CODE'), // letters only — G = Goods & Foods Transport
    'employer_name'  => env('PERKESO_EMPLOYER_NAME', 'ONDW'),
    'employer_code'  => env('PERKESO_EMPLOYER_CODE'), // optional — omit from payload if null
],
```

---

## Endpoint Catalog (v2.1)
| Endpoint | Verb | Path |
|---|---|---|
| Check User | GET | `/api/v1/obs/{ic_no}` |
| Check IC (batch) | GET | `/api/v1/check-ic?ic_no=` |
| Get Sectors | GET | `/api/v1/sectors` |
| Get States & Cities | GET | `/api/v1/states` |
| Get Contributions | GET | `/api/v1/obs/{ic_no}/contributions` |
| **Register User** | POST | `/api/v1/obs` |
| Register (batch) | POST | `/api/v1/signup` |
| Update User | PATCH | `/api/v1/obs/{ic_no}` |
| Update (batch) | PATCH | `/api/v1/user-details` |
| **Submit Deduction** ⭐ | POST | `/api/v1/deductions` (success = 202) |
| Cancel Deduction | PUT | `/api/v1/deductions/{transaction_id}` |
| Generate Token | POST | `/oauth/token` (client_credentials) |

**Sector codes**: letters only (no numbers). ONDW uses `G` = "GOODS AND FOODS TRANSPORT". Run `getSectors` to list all. `FS001` is WRONG (fails API validation).

---

## ⭐ Correct Deduction Payload (6.8 Submit Deduction)
```json
{
  "request_id": "ONDW-{order_id}-{deduction_id}",
  "deductions": [
    {
      "transaction_id": "ONDW-{order_id}-{deduction_id}",
      "ic_no": "010101010011",
      "amount": 1.25,
      "sector_code": "G",
      "transacted_at": "2026-07-04 12:10:45",
      "start_point_latitude": 3.139,
      "start_point_longitude": 101.6869,
      "end_point_latitude": 3.142,
      "end_point_longitude": 101.69
    }
  ]
}
```
**GPS is optional** — only include when captured. Success = HTTP 202.

### ❌ Fields that cause 422 validation errors (do NOT send):
- `job_amount` (wrong name — use `amount`)
- `ic_type`, `name`, `start_date`, `end_date`, `employer_name`, `employer_code`
- GPS without `_point_` prefix (`start_latitude` → wrong, use `start_point_latitude`)

---

## ⭐ Registration Payload (6.3 Register User)
Must register rider with PERKESO before first deduction submission.
```json
{
  "ic_type": "B",
  "ic_no": "010101010011",
  "name": "Full Name As Per IC",
  "email": "rider@example.com",
  "mobile_no": "60123456789"
}
```
- `ic_type`: `B` = New IC (MyKad/MyKid), `L` = Old IC, `PR` = Permanent Resident
- `mobile_no`: must have country code 60 prefix — normalize at send time: `'60' . ltrim($phone, '0')`
- ONDW DB stores `ic_type` as `mykad/mykid/passport` → map: `mykad/mykid → B`, `passport → PR`
- Email comes from `users.email` (not in `rider_profiles`) via `$rider->user->email`

**Success response:**
```json
{
  "status": "success",
  "data": { "user": { "ic_type": "B", "ic_no": "...", "name": "...", ... } }
}
```

---

## Full Deduction Flow (implemented in PerkesoDeductionService)
```
submitForOrder(Order)
  └─ guard: rider has ic_no?
  └─ DB transaction: cap check + create deduction record
  └─ attemptSubmit()
       └─ ensureRiderRegistered()          ← NEW
            ├─ perkeso_registered flag? → fast pass
            ├─ checkUser(ic_no) → success? → update flag, proceed
            ├─ not found → registerUser() → success? → update flag, proceed
            └─ register fail → store error, return false (no retry)
       └─ submitDeduction(payload)
            └─ 202 → update status=submitted, store perkeso_transaction_id
            └─ fail → markFailed() → exponential backoff (15m → 1h → 6h → 24h, max 5 attempts)
```

### perkeso_registered flag on rider_profiles
- `perkeso_registered` (boolean, default false) — skip API check when true
- `perkeso_registered_at` (timestamp) — when registration was confirmed
- **Must be in `$fillable`** on the Rider model (was missing, now fixed Jul 4, 2026)

---

## Data Gaps (ONDW-specific)
| Field | Status | Note |
|---|---|---|
| `ic_no` | ⚠️ Partial | Nullable — guard exists, skips if null |
| `ic_type` | 🔴 Never collected | No form asks for it. Every rider defaults to `mykad`. Add selector to registration/profile forms. |
| `email` | ✅ Via user | `$rider->user->email` — always present |
| `name` | ✅ | `rider_profiles.full_name` |
| `mobile_no` | ⚠️ Prefix | Stored without `60` — normalize at send time |

---

## Non-Blocking Webhook Pattern
```php
// Outside/after the BillPlz DB::transaction():
try {
    $deduction = $this->perkesoDeduction->submitForOrder($order);
    // markFailed() inside the service handles retry scheduling
} catch (\Throwable $e) {
    Log::error('PERKESO deduction error (non-blocking)', ['error' => $e->getMessage()]);
    // Never rethrow — BillPlz must still get 200
}
```

---

## Admin Integration & Retry
- UI at `/admin/integrations/perkeso` — one form per endpoint, live JSON response viewer
- Pending/failed deductions shown with Force Retry button (bypasses backoff)
- Artisan: `php artisan perkeso:retry-pending --force` (or `--id=N` for one)

---

## Reusable Lessons
- IP-whitelisted API → server-side only; timeout (not 403) = wrong source IP.
- Config-driven sandbox|prod switch; token via `config()`, never `env()` outside config files.
- One service method per endpoint; admin harness validates before automating.
- Adding routes → `php artisan optimize:clear` (stale cache = 500).
- Registration check before deduction: use a local DB flag (`perkeso_registered`) to avoid hitting the check API on every deduction.

---

**ONDW refs**: branch `feature/push-notification`. Admin UI at `/admin/integrations/perkeso`.
**Commits**: payload fix + registration flow added Jul 4, 2026.
