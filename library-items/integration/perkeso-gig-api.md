# PERKESO GIG Workers API Integration (Laravel)
**Level**: 1 (Emerging — testing harness live & working on preprod; deduction automation pending)
**Source**: ONDW (Laravel food-delivery PWA)
**Status**: 🚧 In progress
**Date Added**: May 27, 2026

---

## Problem Statement
Integrate a Malaysian government API (PERKESO **GIG Workers API v2.1**, ACT 789) into a gig platform to submit **1.25% of each completed job** as a rider's social-security contribution. The API is REST/JSON, HTTPS-only, Bearer-authenticated, follows JSend (`success`/`fail`/`error`), **and is IP-whitelisted**.

## ⚠️ The #1 Gotcha: IP Whitelisting
PERKESO whitelists your server's egress IP. Requests from a non-whitelisted IP are **silently dropped → "Request Timeout"** (NOT a 403/401).
- ❌ Postman / curl from a laptop → times out forever.
- ✅ `curl` ON the server (or any server-side call) → 200 + JSON.
- **Implication**: the integration MUST be server-side, and you test it on the server (or via a server-side route), never from your machine.
- Give PERKESO your **egress** IP (`curl ifconfig.me` on the server) — it can differ from the domain's DNS A-record.

## Solution Overview
1. **Server-side `PerkesoService`** (Laravel `Http` client) — one method per endpoint; base URL + token from `config/services.php`; sandbox|production switch.
2. **Admin testing harness** — one controller method per endpoint + a jQuery UI (form per endpoint, live JSON viewer) to exercise every endpoint from the whitelisted server before automating.
3. **CSRF-exempt public callback** route for PERKESO's async results.

## Implementation

### config/services.php
```php
'perkeso' => [
    'env'            => env('PERKESO_ENV', 'sandbox'),   // sandbox | production
    'sandbox_url'    => env('PERKESO_SANDBOX_URL', 'https://gig-sandbox.perkeso.gov.my'),
    'production_url' => env('PERKESO_PRODUCTION_URL', 'https://gig-connector.perkeso.gov.my'),
    'token'          => env('PERKESO_TOKEN'),
],
```

### Service — one method per endpoint, correct HTTP verb
```php
protected function client() {
    return Http::withToken($this->token)->acceptJson()->asJson()->timeout(30);
    // NOTE: docs say "form-encoded request bodies" — if a POST/PATCH returns 400/422,
    // swap ->asJson() for ->asForm().
}
public function checkUser(string $ic): Response {
    return $this->client()->get("{$this->baseUrl}/api/v1/obs/".rawurlencode($ic));
}
public function submitDeduction(string $requestId, array $deductions): Response {
    return $this->client()->post("{$this->baseUrl}/api/v1/deductions",
        ['request_id'=>$requestId, 'deductions'=>$deductions]);
}
// ...one method per endpoint (checkIcBatch, getSectors, getStates, getContributions,
//    registerUser, registerBatch, updateUser, updateBatch, cancelDeduction, generateToken)
```

### Controller + routes — "1 function = 1 endpoint" (Hakim's preference)
- One controller method per endpoint, all in one controller; a shared private `respond()` only shapes the JSON.
- Internal routes mirror the API's **real verb** (GET reads, PATCH updates, PUT cancel, POST creates) so the harness reflects the docs.
- ⚠️ After adding routes, run **`php artisan optimize:clear`** — a stale route cache throws `Route [...] not defined` (500) on every page that references the new route.

### Testing UI — the deferred-jQuery trap
If jQuery is loaded with `defer`, an inline `<script>` parses BEFORE jQuery exists → **`$ is not defined`**. `@push('scripts')` placement does NOT fix it (inline scripts run before deferred ones). Wrap in **native** `DOMContentLoaded` (fires *after* deferred scripts), NOT `$(document).ready` (which itself needs `$` defined):
```js
document.addEventListener('DOMContentLoaded', function () {
    // $ / jQuery is guaranteed available here
});
```

### Public callback (CSRF-exempt)
```php
// routes/web.php (outside the auth group)
Route::post('/integrations/perkeso/callback', [PerkesoCallbackController::class, 'handle']);
// app/Http/Middleware/VerifyCsrfToken.php → protected $except = ['integrations/perkeso/callback'];
```

## Endpoint Catalog (v2.1)
| Endpoint | Verb | Path |
|---|---|---|
| Check User | GET | `/api/v1/obs/{ic_no}` |
| Check IC (batch) | GET | `/api/v1/check-ic?ic_no=` |
| Get Sectors | GET | `/api/v1/sectors` |
| Get States & Cities | GET | `/api/v1/states` |
| Get Contributions | GET | `/api/v1/obs/{ic_no}/contributions` |
| Register User | POST | `/api/v1/obs` |
| Register (batch) | POST | `/api/v1/signup` |
| Update User | PATCH | `/api/v1/obs/{ic_no}` |
| Update (batch) | PATCH | `/api/v1/user-details` |
| **Submit Deduction** ⭐ | POST | `/api/v1/deductions` (success = 202) |
| Cancel Deduction | PUT | `/api/v1/deductions/{transaction_id}` |
| Generate Token | POST | `/oauth/token` (client_credentials) |

**Callbacks (PERKESO → your URL):** batch-registration result, deduction result (ACCEPTED/PARTIAL/REJECTED/DUPLICATE), monthly contribution confirmation.

## Deduction Flow (the actual integration)
1. **Register rider once**: Check User → Register User → Update User Details. Store status on the rider.
2. **Submit deduction per delivered order**: 1.25% × job amount. Payload `{request_id, deductions[]{ic_no, transaction_id, transacted_at, sector_code, amount, start/end lat-long}}`. **Daily batch cron** recommended (the API takes an array); use a **stable, idempotent `transaction_id`** (e.g. `ONDW-{order_id}`).
3. **Handle callbacks**: mark each transaction accepted/rejected; record monthly contributions.
4. **Cancel** deduction on refund/cancel (`PUT /deductions/{transaction_id}`).

## Data You Must Have (common gaps)
- Rider **`ic_no` + `ic_type`** (often only an IC *document image* is stored, not the number).
- Per-order **pickup/delivery GPS** — Submit Deduction lists start/end lat-long as **mandatory**.
- Rider **demographics + address + next-of-kin** (for registration).
- The right **`sector_code`** (run Get Sectors).
- A `*_deductions` table for idempotency + reconciliation.

## Reusable Lessons (any IP-whitelisted / government REST API)
- Whitelisted API → **server-side only**; a *timeout* (not 403) from a client tool = wrong source IP.
- Config-driven sandbox|prod switch; token via `config()`, **never `env()` outside `config/`** (breaks under `config:cache`).
- **One service method per endpoint** = clean + debuggable; an admin testing harness (one controller method per endpoint) lets you validate every call before automating.
- Adding routes → `optimize:clear`. Deferred jQuery → wrap inline JS in `DOMContentLoaded`.

---
**Reusable For**: Any Laravel integration with a government / IP-whitelisted third-party REST API that needs a server-side client + admin testing harness.
**ONDW refs**: branch `feature/push-notification`, commits `4adcf4a`→`d4f4ec6`. Testing UI at `/admin/integrations/perkeso`.
