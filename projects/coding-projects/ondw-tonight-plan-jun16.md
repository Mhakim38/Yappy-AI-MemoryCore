# 🛠️ ONDW Tonight's Plan — Jun 16, 2026
*Analyzed by Reza + Hana. Final verdict by Yappy. DO NOT CODE until this session.*
*Status: PLAN ONLY — no code changed yet*

---

## Issue 1 — "Complete Payment" button redirects to waiting screen instead of BillPlz

### Root Cause
`PaymentController::pending()` renders the waiting/polling screen every time it's called — it never loads `PaymentTransaction` or checks for `bill_url`. The `bill_url` IS correctly saved to DB on checkout (confirmed in `OrderController::createBillForOrder()` line 232).

### Current Flow (broken)
```
Customer revisits /customer/orders/88
  → clicks "Complete Payment"
  → route('customer.payment.pending', $orderId)
  → PaymentController::pending() → renders waiting screen (no BillPlz URL)
```

### Correct Flow (after fix)
```
Customer revisits /customer/orders/88
  → clicks "Complete Payment"
  → route('customer.payment.pending', $orderId)
  → PaymentController::pending()
      → load PaymentTransaction WHERE order_id = $orderId AND status = 'pending' AND bill_url NOT NULL
      → redirect($transaction->bill_url)  ← back to BillPlz payment page
      → customer pays → BillPlz redirects to /customer/payment/88/pending (the return route)
```

### Fix Required
**File**: `app/Http/Controllers/Customer/PaymentController.php` — `pending()` method (lines 18–35)

Add `PaymentTransaction` lookup before rendering the view:
```php
use App\Models\PaymentTransaction;

public function pending(int $orderId)
{
    $order = Order::where('order_id', $orderId)
        ->where('customer_id', Auth::user()->customer->customer_id)
        ->firstOrFail();

    if ($order->status !== 'pending_payment') {
        $conversation = $order->deliveryConversation;
        if ($conversation) {
            return redirect()->route('conversations.delivery.show', $conversation)
                ->with('success', 'Payment confirmed! Riders are being notified.');
        }
        return redirect()->route('customer.orders.show', $orderId);
    }

    // Redirect to actual BillPlz payment page
    $transaction = PaymentTransaction::where('order_id', $orderId)
        ->where('status', 'pending')
        ->whereNotNull('bill_url')
        ->latest()
        ->first();

    if ($transaction?->bill_url) {
        return redirect($transaction->bill_url);
    }

    // Fallback: no bill_url found — show waiting screen
    return response()->view('customer.payment.pending', compact('order'));
}
```

**No change needed** to `show.blade.php` — the button route is already correct.

---

## Issue 2 — PERKESO deduction never fires (empty perkeso_deductions table)

### Root Cause
PERKESO is triggered inside `BillplzWebhookController::callback()` at the `pending_payment → pending` transition. But the guard at line 134 is:
```php
if ($order && $order->rider_id) {
```
At payment time, `rider_id` is **NULL** — no rider has accepted yet. The entire PERKESO block is silently skipped.

Additionally, PERKESO requires `end_latitude`/`end_longitude` (`delivery_proof_lat/lng`) which are only set when the rider submits delivery proof. So PERKESO literally cannot fire at payment time.

### Order Lifecycle Context
```
pending_payment → (BillPlz webhook) → pending     ← rider_id = NULL, proof_lat = NULL
     → (rider accepts) → rider_accepted           ← rider_id SET, proof_lat = NULL
     → accepted → processing → on_delivery
     → (rider delivers) → delivered               ← rider_id SET, proof_lat/lng SET ✅
```

### Fix Required
**Move PERKESO deduction from `BillplzWebhookController` → `delivered` transition**

**Option A (Recommended): Hook into `OrderController::deliver()`**
- `deliver()` already sets `delivery_proof_lat/lng` (lines 403–408)
- After the status update to `delivered`, call `perkesoDeduction->submitForOrder($order)` in a try/catch
- All required data available: `rider_id`, `rider->ic_no`, `delivery_proof_lat`, `delivery_proof_lng`, `delivery_fee`

**Option B: Hook into `OrderStatusService` on `delivered` transition**
- Cleaner architecture long-term
- Add a post-transition hook in `updateStatus()` when `$newStatus === 'delivered'`

**Recommended: Option A** (simpler, less risk, faster to ship tonight)

**Files to change:**
1. `app/Http/Controllers/Rider/OrderController.php` — `deliver()` method — add PERKESO call after `delivered` status update
2. `app/Http/Controllers/Webhooks/BillplzWebhookController.php` — remove the dead PERKESO block (lines 130–150) since it will never fire anyway

---

## Issue 3 — Rider history shows customer's total_amount instead of delivery_fee

### Root Cause
`resources/views/rider/orders/history.blade.php` lines 64 and 115 both use:
```php
RM {{ number_format($order->total_amount, 2) }}
```
This shows the customer's full food order value (e.g. RM 18.00). The rider should see their `delivery_fee` (e.g. RM 3.50).

### Fix Required

**File 1**: `resources/views/rider/orders/history.blade.php`
- Line 64: change `$order->total_amount` → `$order->delivery_fee`
- Line 115: change `$order->total_amount` → `$order->delivery_fee`
- Consider: label change from just "RM X.XX" to "Delivery: RM X.XX" for clarity
- Consider: make the delivery_fee text larger (`text-2xl` instead of `text-xl`) since this is the primary number riders care about

**File 2**: `resources/views/rider/orders/available.blade.php`
- "Today RM" widget at lines 34–37 is currently `text-sm` (14px) — increase to `text-base` or `text-lg` for better visibility
- Functionally correct (already uses `delivery_fee`) — just a visual tweak

**File 3 (optional)**: `app/Http/Controllers/Rider/OrderController.php` — `history()` method
- Could add total earnings summary (sum of `delivery_fee` for all delivered orders) passed to view as `$totalEarnings`

---

## Tonight's Execution Order

1. **Issue 1** (bill_url) — `PaymentController::pending()` — quick fix, ~10 lines
2. **Issue 3** (rider history amount) — blade files, 2 lines + visual tweak
3. **Issue 2** (PERKESO lifecycle) — move call to `deliver()`, remove dead block — needs careful testing

---

## Files Involved Tonight

| File | Change |
|---|---|
| `app/Http/Controllers/Customer/PaymentController.php` | Add PaymentTransaction lookup in `pending()` |
| `app/Http/Controllers/Webhooks/BillplzWebhookController.php` | Remove dead PERKESO block |
| `app/Http/Controllers/Rider/OrderController.php` | Add PERKESO call in `deliver()` |
| `resources/views/rider/orders/history.blade.php` | Fix lines 64 + 115: `total_amount` → `delivery_fee` |
| `resources/views/rider/orders/available.blade.php` | Visual: make Today earnings widget larger |
