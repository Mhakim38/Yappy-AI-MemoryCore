# 📍 Mobile Geolocation — Allow System Pattern (PWA / Laravel)

**Project**: ONDW Food Delivery PWA  
**Settled**: Jun 21, 2026 (commit `baeecf7`)  
**Context**: PERKESO EIS compliance requires GPS pickup + delivery coordinates per order

---

## The Core Problem

iOS and Android require a **direct user gesture** (a real button click, not a JS timeout or async wrapper) to show the system location permission dialog. Any async layer between the user tap and `getCurrentPosition()` breaks the gesture chain — the system dialog never appears, the call fails silently.

The system permission dialog fires ONCE per origin. After the user grants, `getCurrentPosition()` resolves without a dialog. After the user denies, re-asking requires them to go into device Settings.

---

## What Doesn't Work

```js
// ❌ Async pre-check breaks gesture chain on iOS
navigator.permissions.query({ name: 'geolocation' }).then(result => {
    if (result.state === 'prompt') {
        navigator.geolocation.getCurrentPosition(...) // too late — gesture consumed
    }
})

// ❌ Form submit event — iOS doesn't reliably fire submit inside fixed containers
form.addEventListener('submit', () => navigator.geolocation.getCurrentPosition(...))

// ❌ External JS file delegation — window.Foo.requestLocation() called via click
// if the actual getCurrentPosition() is inside a method, iOS may not see it as gesture-direct
```

---

## What Works — The Pattern (confirmed on iOS + Android)

**Step 1**: Show a custom ONDW modal explaining WHY location is needed (PERKESO compliance).  
**Step 2**: The "Allow Location" button in that modal calls `getCurrentPosition()` via a **direct `addEventListener` click handler** — no async, no wrapper, no delegation.  
**Step 3**: On success → fill hidden form inputs → submit form. On fail → show error + Retry button.

```js
// ✅ Direct addEventListener on the button element — this IS the user gesture
document.getElementById('allow-btn').addEventListener('click', function () {
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            document.getElementById('lat-input').value = pos.coords.latitude.toFixed(7);
            document.getElementById('lng-input').value = pos.coords.longitude.toFixed(7);
            form.submit();
        },
        (err) => {
            // Show error + Retry button; do NOT submit form
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
});
```

**Key rule**: `getCurrentPosition()` must be called SYNCHRONOUSLY inside a click event listener. No `.then()`, no `setTimeout`, no async/await between click and the call.

---

## iOS Safari Permissions API Bug

iOS Safari returns `navigator.permissions.query({ name: 'geolocation' })` → `state: 'prompt'` even after the user has already granted location. This means:
- Never use the Permissions API to decide whether to skip the modal
- Always show the modal — if permission is already granted, `getCurrentPosition()` resolves instantly without showing a system dialog

**Workaround for profile status display**: Persist grant in `localStorage` key `ondw_location_granted = '1'` after first successful `getCurrentPosition()`. Read from localStorage (not Permissions API) to show green "Allowed" status in the rider's profile page.

---

## Race Condition (delivery proof modal)

**Problem**: Modal opens → `captureLocation()` starts async → user selects photo → submit button enables → user submits BEFORE GPS resolves → empty coords saved.

**Fix**: Two-flag pattern. Submit only enables when BOTH flags are true.

```js
let photoReady    = false;
let locationReady = false;

function enableSubmitIfReady() {
    submitBtn.disabled = !(photoReady && locationReady);
}

// On modal open:
captureLocation(); // async — sets locationReady when done

// GPS success:
locationReady = true; enableSubmitIfReady();

// GPS failure (location REQUIRED — do NOT set locationReady):
retryBtn.classList.remove('hidden'); // show Retry, submit stays disabled

// Photo selected:
photoReady = true; enableSubmitIfReady();
```

If location is **optional** (original design): set `locationReady = true` on both success and error paths — submit unlocks after photo regardless. If location is **required** (current ONDW design): only set `locationReady = true` on success; error path shows Retry button.

---

## Laravel Backend — Required Validation

```php
$validated = request()->validate([
    'pickup_lat' => ['required', 'numeric', 'between:-90,90'],
    'pickup_lng' => ['required', 'numeric', 'between:-180,180'],
], [
    'pickup_lat.required' => 'Location is required to confirm pickup.',
    'pickup_lng.required' => 'Location is required to confirm pickup.',
]);

// Then always save — no conditional:
$order->update([
    'pickup_lat'         => $validated['pickup_lat'],
    'pickup_lng'         => $validated['pickup_lng'],
    'pickup_captured_at' => now(),
]);
```

**Critical**: Add GPS columns to `$fillable` AND `$casts` in the model. Missing `$fillable` = silent mass-assignment block — Laravel ignores the field with NO error. This is what caused pickup GPS to never save even when JS sent correct coords.

```php
// Order.php
protected $fillable = [
    // ...
    'pickup_lat',
    'pickup_lng',
    'pickup_captured_at',
    'delivery_proof_lat',
    'delivery_proof_lng',
    'delivery_proof_captured_at',
];

protected $casts = [
    'pickup_lat'                 => 'decimal:7',
    'pickup_lng'                 => 'decimal:7',
    'pickup_captured_at'         => 'datetime',
    'delivery_proof_lat'         => 'decimal:7',
    'delivery_proof_lng'         => 'decimal:7',
    'delivery_proof_captured_at' => 'datetime',
];
```

---

## Silent Failure Traps Summary

| Trap | Symptom | Fix |
|---|---|---|
| GPS columns not in `$fillable` | Coords sent from browser, silently ignored by Laravel, null in DB | Add to `$fillable` + `$casts` |
| `getCurrentPosition()` not in direct gesture | System dialog never appears, call fails immediately | Move call to direct `addEventListener click` handler |
| iOS Permissions API returns 'prompt' after grant | Profile shows wrong state, code thinks permission not granted | Use localStorage flag, not Permissions API |
| Race condition (async GPS + early submit) | GPS resolves after form submits, null stored | Two-flag pattern: `photoReady` + `locationReady` |
| `form submit` event used instead of button click | iOS fixed-container forms don't reliably fire submit | Use `type="button"` + click handler |

---

## Admin Debug Page Pattern

Built `/admin/integrations/location` (commit `980881e`) — a standalone page with a direct button → `getCurrentPosition()` → shows lat/lng result. Use this to verify location permission works on a device before debugging the actual flow. Same pattern confirmed working = the issue is in the flow, not the permission.

---

## Files in ONDW

| File | Role |
|---|---|
| `resources/views/conversations/show.blade.php` | Pickup modal (inline script) + delivery proof modal |
| `public/customJS/location-permission.js` | `window.LocationPermissionManager` (jQuery modal — legacy, not used in pickup inline) |
| `app/Http/Controllers/Rider/OrderController.php` | `pickup()` + `deliver()` — validation + DB save |
| `app/Models/Order.php` | `$fillable` + `$casts` for GPS columns |
| `resources/views/admin/integrations/location-test.blade.php` | Admin debug test page |
