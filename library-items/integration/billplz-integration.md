# BillPlz Payment Gateway Integration (Laravel)
**Level**: 2 (Proven — live on ONDW preprod, webhook fully verified)
**Source**: ONDW (Laravel food-delivery PWA)
**Status**: ✅ Working
**Date Added**: June 9, 2026

---

## Overview
BillPlz is a Malaysian payment gateway supporting FPX, e-wallets, and credit cards.
- V3: Bill creation + X Signature callbacks
- V4: V3-compatible + split payments, card tokenization
- V5: Payment Order (disbursements to bank accounts, HMAC-SHA512)
- Auth: HTTPS Basic Auth — API Secret Key as username, blank password

---

## ⚠️ #1 Gotcha: The X Signature Sort Bug

**The single biggest trap.** BillPlz's X Signature uses HMAC-SHA256, but the fields must be sorted with a **custom comparator** — NOT PHP's `ksort`.

### Why `ksort` silently breaks it

When two keys share a prefix (like `paid`, `paid_at`, `paid_amount`), PHP `ksort` puts the **shorter** key first. BillPlz's official PHP gist puts the **longer** key first.

```php
// ❌ WRONG — standard PHP sort
ksort($payload, SORT_STRING | SORT_FLAG_CASE);
// Produces: paid → paid_amount → paid_at

// ✅ CORRECT — BillPlz's comparator (longer key wins prefix ties)
uksort($payload, function (string $a, string $b): int {
    $result = strncasecmp($a, $b, min(strlen($a), strlen($b)));
    return $result === 0 ? strlen($b) - strlen($a) : $result;
});
// Produces: paid_amount → paid_at → paid
```

Different sort order → different source string → **HMAC always fails regardless of key or format**.

This bug is invisible in testing unless your payload happens to have prefix-sharing keys — which BillPlz callbacks always do (`paid`, `paid_at`, `paid_amount`).

---

## Config (`config/services.php`)

```php
'billplz' => [
    'env'              => env('BILLPLZ_ENV', 'sandbox'),
    'sandbox_url'      => env('BILLPLZ_SANDBOX_URL', 'https://www.billplz-sandbox.com'),
    'production_url'   => env('BILLPLZ_PRODUCTION_URL', 'https://www.billplz.com'),
    'secret_key'       => env('BILLPLZ_SECRET_KEY'),       // Basic Auth username
    'x_signature_key'  => env('BILLPLZ_X_SIGNATURE_KEY'),  // For HMAC-SHA256 + SHA512
    'collection_id'    => env('BILLPLZ_COLLECTION_ID'),    // Bill collection
    'po_collection_id' => env('BILLPLZ_PO_COLLECTION_ID'), // Payment Order collection
],
```

⚠️ Sandbox and production each have their **own** API Secret Key, Collection ID, and X Signature Key. Mixing them = signature mismatch. Confirm with `Log::info()` that env + collection_id match before debugging signatures.

---

## BillplzService — Core Methods

### HTTP Client
```php
protected function client()
{
    return Http::withBasicAuth($this->apiSecretKey, '')
        ->acceptJson()
        ->asForm()       // BillPlz expects application/x-www-form-urlencoded
        ->timeout(30);
}
```

### Create Bill (V3)
```php
// POST /api/v3/bills
$payload = [
    'collection_id'     => $this->collectionId,
    'email'             => $data['email'],
    'mobile'            => $data['mobile'] ?? null,
    'name'              => $data['name'],
    'amount'            => $data['amount_sen'],     // in sen (cents)
    'description'       => $data['description'],
    'callback_url'      => $data['callback_url'],
    'redirect_url'      => $data['redirect_url'],
    'reference_1_label' => 'Order ID',
    'reference_1'       => (string) $data['order_id'],
];
```

### X Signature — POST Callback Verification
```php
public function verifyCallbackSignature(array $payload): bool
{
    if (! isset($payload['x_signature'])) return false;

    $received = $payload['x_signature'];
    unset($payload['x_signature']);

    // ⚠️ Must use BillPlz's custom sort — NOT ksort
    uksort($payload, function (string $a, string $b): int {
        $result = strncasecmp($a, $b, min(strlen($a), strlen($b)));
        return $result === 0 ? strlen($b) - strlen($a) : $result;
    });

    $parts = [];
    foreach ($payload as $key => $value) {
        $parts[] = $key . $value;   // key+value, no separator between them
    }
    $source   = implode('|', $parts);  // | between pairs
    $computed = hash_hmac('sha256', $source, $this->xSignatureKey);

    return hash_equals($computed, $received);  // timing-safe
}
```

### X Signature — GET Redirect Verification
```php
public function verifyRedirectSignature(array $query): bool
{
    $billplz  = $query['billplz'] ?? [];
    if (! isset($billplz['x_signature'])) return false;

    $received = $billplz['x_signature'];
    unset($billplz['x_signature']);

    // Flatten: billplz[id] → 'billplzid'
    $pairs = [];
    foreach ($billplz as $key => $value) {
        $pairs['billplz' . $key] = $value;
    }

    // Same custom sort applies here too
    uksort($pairs, function (string $a, string $b): int {
        $result = strncasecmp($a, $b, min(strlen($a), strlen($b)));
        return $result === 0 ? strlen($b) - strlen($a) : $result;
    });

    $parts = [];
    foreach ($pairs as $k => $v) { $parts[] = $k . $v; }
    $computed = hash_hmac('sha256', implode('|', $parts), $this->xSignatureKey);

    return hash_equals($computed, $received);
}
```

### Payment Order V5 Checksum (Disbursement)
```php
// Strict field order: [po_collection_id, bank_account_number, total, epoch]
// Uses HMAC-SHA512 (NOT SHA256)
$epoch    = (string) time();
$source   = $poCollectionId . $bankAccountNumber . $totalSen . $epoch;
$checksum = hash_hmac('sha512', $source, $this->xSignatureKey);

// POST /api/v5/payment_orders
```

### Payment Order Callback Verification
```php
// Callback checksum order: [id, bank_account_number, status, total, reference_id, epoch]
$source = $payload['id'] . $payload['bank_account_number'] . $payload['status']
        . $payload['total'] . $payload['reference_id'] . $payload['epoch'];
$computed = hash_hmac('sha512', $source, $this->xSignatureKey);
return hash_equals($computed, $payload['checksum']);
```

---

## Webhook Controller Pattern

```php
// 1. Verify FIRST — before any DB write
$payload = $request->all();
if (! $this->billplz->verifyCallbackSignature($payload)) {
    return response('Unauthorized', 401);
}

// 2. Idempotency guard
$existing = PaymentTransaction::where('bill_id', $billId)->where('status', 'paid')->first();
if ($existing) return response('OK', 200);  // BillPlz must get 200

// 3. Settlement check (paid=true, state=paid, amount matches)
$paid         = filter_var($payload['paid'] ?? false, FILTER_VALIDATE_BOOLEAN);
$amountFromGw = (int) ($payload['amount'] ?? 0);
if (! $paid || $payload['state'] !== 'paid' || $amountFromGw !== $transaction->amount_sen) {
    // handle failed payment
    return response('OK', 200);
}

// 4. Settle inside DB transaction
DB::transaction(fn() => ...);

// 5. Return 200 — BillPlz retries up to 5× if it doesn't get 200
return response('OK', 200);
```

### CSRF Exemption (required)
```php
// app/Http/Middleware/VerifyCsrfToken.php
protected $except = [
    'webhooks/billplz',
    'webhooks/billplz/po',
];
```

---

## Callback Fields (what BillPlz POSTs)
`amount`, `collection_id`, `due_at`, `email`, `id`, `mobile`, `name`, `paid`,
`paid_amount`, `paid_at`, `state`, `transaction_id`, `transaction_status`, `url`,
and any `reference_1`/`reference_1_label` you sent during bill creation.

All of these are included in the X Signature computation.

---

## Redirect GET Fields
`billplz[id]`, `billplz[paid]`, `billplz[paid_at]`, `billplz[transaction_id]` (optional),
`billplz[transaction_status]` (optional), `billplz[x_signature]`

---

## Webhook Retry Schedule
| Attempt | Timing |
|---------|--------|
| 1st | Immediate |
| 2nd | +15s + random(0–300s) |
| 3rd/4th | +15min + random |
| 5th | +24hrs after 4th |

Each failed attempt degrades your account's callback rank — respond 200 fast.

---

## Reusable Lessons
- **Never use `ksort`** for X Signature — always use the custom `uksort` comparator above.
- **X Signature Key is environment-specific** — sandbox key ≠ production key. Collection ID too.
- Verify X Signature **before** any database write. Never after.
- Webhook + redirect can arrive in **any order** — make handlers idempotent.
- `redirect_url` is UX only — **never settle from redirect**, always wait for webhook.
- BillPlz expects `application/x-www-form-urlencoded` (`asForm()`), not JSON.
- Return `200` even for duplicate/failed webhooks — returning 4xx triggers retries.

---

## V5 Checksum Field Orders (reference)
| Endpoint | Values — strict order |
|---|---|
| Create Payment Order | `[po_collection_id, bank_account_number, total, epoch]` |
| Get Payment Order | `[payment_order_id, epoch]` |
| Payment Order Callback | `[id, bank_account_number, status, total, reference_id, epoch]` |

---

**Reusable For**: Any Laravel app needing Malaysian FPX / e-wallet checkout + vendor disbursement.
**ONDW refs**: `app/Services/Billplz/BillplzService.php`, `app/Http/Controllers/Webhooks/BillplzWebhookController.php`, branch `feature/push-notification`, fix commit `7780573`.
