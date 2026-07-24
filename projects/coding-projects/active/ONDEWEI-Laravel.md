# ONDEWEI-Laravel
*Coding Project - Created February 14, 2026*

## Description
Laravel 10 food delivery platform with multi-role order management system. Features customer ordering, vendor menu management, rider delivery tracking, and admin oversight with real-time order status transitions and notification system.

## Project Details
- **Type**: Coding Project
- **Status**: Active
- **Created**: February 14, 2026 7:35 PM
- **Last Accessed**: February 14, 2026 7:35 PM
- **Position**: #2
- **Location (WSL)**: ~/holeeshet/ONDEWEI-LARAVEL-HAKIM (hakim@DESKTOP-L52VB9R)
- **Windows Path**: \\wsl$\Ubuntu\home\hakim\holeeshet\ONDEWEI-LARAVEL-HAKIM

## Technical Stack
- **Languages**: PHP 8.1+
- **Framework**: Laravel 10.10
- **Authentication**: Laravel Breeze 1.29, Sanctum 3.3
- **Authorization**: Spatie Laravel-Permission 6.23
- **Frontend**: Tailwind CSS, Alpine.js, Vite
- **Database**: MySQL (migrations for orders, order_items, menu_items, notifications)
- **Additional**: Laravel Socialite 5.23

## Project Structure
```
ONDEWEI-LARAVEL-HAKIM/
├── app/
│   ├── Http/Controllers/
│   │   ├── Customer/OrderController.php
│   │   ├── Vendor/OrderController.php
│   │   ├── Rider/OrderController.php
│   │   └── Admin/OrderController.php
│   ├── Models/
│   │   ├── Order.php
│   │   ├── OrderItem.php
│   │   ├── MenuItem.php
│   │   └── User.php (with Customer, Vendor, Rider, Admin roles)
│   ├── Services/
│   │   ├── OrderService.php
│   │   └── OrderStatusService.php
│   └── Events/
│       ├── OrderPlaced.php
│       └── OrderStatusChanged.php
├── routes/
│   ├── web.php (multi-role routing)
│   ├── api.php
│   └── auth.php
└── database/migrations/
```

## Development Goals
1. Fix critical bugs in order state machine and authorization
2. Complete ready_for_pickup transition implementation
3. Remove exposed debug routes from production
4. Enhance notification system for real-time updates
5. Improve error handling across controllers

## Progress Log
### February 14, 2026 7:35 PM
- Project added to Yappy memory system
- Deep code analysis completed (30+ files analyzed)
- 4 critical bugs identified with exact locations
- Order workflow architecture mapped
- Multi-role authorization system documented

## Code Standards
- **Style Guide**: Laravel PSR-12 standards
- **Testing**: Laravel Feature/Unit tests (to be implemented)
- **Documentation**: Inline docblocks + README
- **Git Workflow**: Feature branch strategy

## Current Tasks
- [x] Fix authorization mismatch between OrderControllers and OrderStatusService
- [x] Replace non-existent \UnauthorizedException with proper Laravel exception
- [x] Implement ready_for_pickup transition trigger (vendor action or timer)
- [x] Secure or remove debug routes (/check-user, /admin-test, /create-admin-profile)
- [x] Add comprehensive order state machine tests
- [x] Fix: Rider document storage - files were going to public instead of private disk (Feb 19 2026)

## Known Issues
### Critical Bugs Identified (Feb 14, 2026)

**1. Authorization Mismatch - Vendor Cancel Bug**
- **Location**: app/Http/Controllers/Vendor/OrderController.php (lines 173-197)
- **Issue**: Controller allows vendor cancel at 'rider_accepted' status, but OrderStatusService validTransitions (lines 28-35) forbids vendor from canceling in that state
- **Impact**: Transaction failures, inconsistent state handling

**2. Authorization Mismatch - Rider Cancel Bug**
- **Location**: app/Http/Controllers/Rider/OrderController.php (lines 318-321)
- **Issue**: Controller allows rider cancel at 'accepted'/'preparing', but OrderStatusService validTransitions (lines 28-47) forbids rider from those states
- **Impact**: Transaction failures

**3. Non-Existent Exception Class**
- **Location**: app/Services/OrderStatusService.php (line 119)
- **Issue**: Throws `\UnauthorizedException` which doesn't exist in PHP/Laravel
- **Fix Needed**: Replace with `\Illuminate\Auth\Access\AuthorizationException`
- **Impact**: Fatal error when unauthorized transitions attempted

**4. Incomplete State Machine - Stuck in Preparing**
- **Location**: app/Services/OrderStatusService.php (lines 36-38, 125-144)
- **Issue**: preparing→ready_for_pickup transition defined as 'system' but no trigger code exists (handleAutoTransitions only covers accepted→preparing)
- **Impact**: Orders get stuck in 'preparing' status indefinitely
- **Clarification Needed**: Should this be vendor action or automatic timer?

**5. Security Issue - Exposed Debug Routes**
- **Location**: routes/web.php (lines 37-93)
- **Issue**: /check-user, /admin-test, /create-admin-profile active in production
- **Impact**: Information disclosure, unauthorized admin creation
- **Fix Needed**: Environment gating or complete removal

### Resolved Issues (Feb 19, 2026)

**Pending Rider Auto-Login Bug**
- **Problem**: After registration, pending riders were auto-logged in and redirected to `/rider/dashboard` even though they should wait for admin approval
- **Root Cause**: RegisteredUserController and GoogleAuthController auto-logged in ALL new riders without checking status
- **Solution Applied** (Feb 19, 2026):
  - Modified RegisteredUserController: Don't auto-login if user status is 'pending', redirect to login page instead
  - Modified GoogleAuthController: Don't auto-login if user status is 'pending', redirect to login page instead
  - LoginRequest already has status checks that will prevent pending users from logging in
- **Files Modified**:
  - `app/Http/Controllers/Auth/RegisteredUserController.php`
  - `app/Http/Controllers/Auth/GoogleAuthController.php`
- **Git Commit**: ff7c45a - "Fix: Prevent pending riders from auto-login after registration - redirect to login page instead"
- **Behavior After Fix**: Pending riders see message "Registration successful! Please wait for admin approval before logging in" and redirect to login page
- **Note**: Currently only checks for 'pending' status. Could be improved to ONLY allow auto-login if status === 'active' to also prevent 'suspended' and 'inactive' users from auto-logging in. LoginRequest already handles these cases if they try to login manually.

**Menu Item Image Cache Configuration**
- **Original Issue**: Images required hard refresh (Ctrl+F5) when uploaded
- **Root Cause**: Cache was set to 1 year (31536000 seconds) - browser cached forever
- **Solution**: Changed to 1 week (604800 seconds) - balance between performance and freshness
- **Attempted Solutions** (reverted):
  - ❌ Cache-busting with timestamp query params (`?v=timestamp`)
  - ❌ ETag validation and complex cache headers
  - ✅ Simple 1-week cache approach chosen
- **Files Modified**:
  - `routes/web.php` - Updated menu item image serving route with `max-age=604800`
- **Git Commit**: 3ceb03c - "Revert: Menu item cache-busting changes - use 1 week cache instead"
- **Behavior**: Images cache for up to 1 week, reasonable tradeoff for performance vs freshness

**Document Storage Issue Investigation** (Documented for Reference)
- **Problem**: When riders registered via Google, document uploads created DB records but files weren't actually stored to disk
- **Root Cause**: `$file->storeAs(..., 'private')` was not respecting the 'private' disk parameter - files went to `storage/app/public/` instead of `storage/app/private/`
- **Solution Attempted** (Feb 19, 2026):
  - Changed from `storeAs()` to explicit `Storage::disk('private')->put()` calls
  - Added verification checks: only create DB record if file exists
  - Added logging for diagnostic purposes
  - Git Commit: 872a3f6 - "Fix: Ensure rider documents stored to private disk using Storage facade"
  - ❌ Later Reverted: 7924017 - "Revert: Reverted storage fix changes - back to original storeAs() implementation"
- **Status**: Reverted - keeping original implementation for now, but fix documented for future reference
- **Technical Note**: Issue may be environment-specific. Original storeAs() method observed working in production environment
- **Problem**: After registration, pending riders were auto-logged in and redirected to `/rider/dashboard` even though they should wait for admin approval
- **Root Cause**: RegisteredUserController and GoogleAuthController auto-logged in ALL new riders without checking status
- **Solution Applied** (Feb 19, 2026):
  - Modified RegisteredUserController: Don't auto-login if user status is 'pending', redirect to login page instead
  - Modified GoogleAuthController: Don't auto-login if user status is 'pending', redirect to login page instead
  - LoginRequest already has status checks that will prevent pending users from logging in
- **Files Modified**:
  - `app/Http/Controllers/Auth/RegisteredUserController.php`
  - `app/Http/Controllers/Auth/GoogleAuthController.php`
- **Git Commit**: ff7c45a - "Fix: Prevent pending riders from auto-login after registration - redirect to login page instead"
- **Behavior After Fix**: Pending riders see message "Registration successful! Please wait for admin approval before logging in" and redirect to login page
- **Note**: Currently only checks for 'pending' status. Could be improved to ONLY allow auto-login if status === 'active' to also prevent 'suspended' and 'inactive' users from auto-logging in. LoginRequest already handles these cases if they try to login manually.
- **Problem**: When riders registered via Google auth or normal registration, document uploads created DB records but files weren't actually stored to disk
  - Files were saved to `storage/app/public/` instead of `storage/app/private/`
  - Later admin viewing would get 404 ("Document not found")
- **Root Cause**: `$file->storeAs(..., 'private')` was not respecting the 'private' disk parameter
- **Solution Applied** (Feb 19, 2026):
  - Changed from `storeAs()` to explicit `Storage::disk('private')->put()` calls
  - Updated **RegisteredUserController.php** document upload loop
  - Updated **GoogleAuthController.php** document upload loop
  - Added verification checks: only create DB record if file actually exists on disk
  - Added logging for diagnostic purposes
- **Files Modified**:
  - `app/Http/Controllers/Auth/RegisteredUserController.php`
  - `app/Http/Controllers/Auth/GoogleAuthController.php`
- **Git Commit**: 872a3f6 - "Fix: Ensure rider documents stored to private disk using Storage facade"
- **Testing**: Need to verify with new Rider registration (both paths) that files store correctly
- **Note**: May be reverted - this documents the fix for future reference

## Resources & References
- Laravel 10 Documentation: https://laravel.com/docs/10.x
- Spatie Permissions: https://spatie.be/docs/laravel-permission
- Order State Machine Flow: pending → rider_accepted → accepted → preparing → ready_for_pickup → on_delivery → delivered

## Session Notes
*Space for working notes during active sessions*

### Architecture Overview
- **Multi-Role System**: Customer, Vendor, Rider, Admin with role-based middleware
- **Order Workflow**: 8-status state machine with role-specific transitions
- **Service Layer**: OrderService (creation), OrderStatusService (transitions + events)
- **Event-Driven**: OrderPlaced, OrderStatusChanged for notifications
- **Locking**: OrderStatusService uses database locks for concurrent safety (line 87-121)

### State Machine Rules
```php
validTransitions = [
    'pending' => ['rider_accepted', 'cancelled'],  // system, vendor/customer
    'rider_accepted' => ['accepted', 'cancelled'], // vendor, system
    'accepted' => ['preparing', 'cancelled'],      // vendor
    'preparing' => ['ready_for_pickup'],           // system (NOT IMPLEMENTED)
    'ready_for_pickup' => ['on_delivery'],         // rider
    'on_delivery' => ['delivered'],                // rider
]
```

## Memory Patterns
- **Authorization Pattern**: Always validate transitions through OrderStatusService before controller level checks
- **State Transitions**: Use $order->transitionTo($newStatus, $role) for all status changes
- **Event Broadcasting**: OrderStatusChanged fires on every transition for real-time updates
- **Error Handling**: Wrap status changes in try-catch for transaction rollback

---

## ChatBox Integration (May 2, 2026 - 8:38 PM) 💜

### Critical Clarifications

#### 🔴 PARTICIPANTS: Only Rider ↔ Customer (NOT Vendor!)
- Chat is EXCLUSIVELY between **Rider** and **Customer**
- Vendor is NOT a chat participant
- This simplifies the conversation participants to 2 roles only
- Update plan: Remove vendor from auto-spawned participants

#### ⚙️ source_app Field Explanation
- **Purpose**: ChatBox is designed as a **MULTI-APP system**
- `source_app='ondewei'` tags which application this conversation originates from
- Allows single ChatBox database to handle conversations from multiple different apps
- **Example Scenario**: If you build another app (food delivery v2, wedding planning, etc.), it could reuse same ChatBox with `source_app='another-app'`
- **Benefits**:
  - Namespace isolation (easily identify which app owns which conversation)
  - Query filtering (search only ONDW conversations, not cross-app noise)
  - Future multi-tenancy ready
- **For ONDW**: Always use `source_app='ondewei'`

#### 🔗 context_id ↔ order_id Relationship
- `context_id` stores the `order_id` value
- **Should have FK constraint** to `orders.order_id`
- Database schema: `context_id` VARCHAR(255) with FK relationship
- **Cascade behavior**: When order deleted, conversation should either:
  - Option A: Soft delete (mark as archived, preserve historical records)
  - Option B: Hard delete cascade (remove all messages, participants)
  - **Recommendation**: Soft delete (use `deleted_at` timestamp on conversations table)

#### 💾 Message DB Storage - YES, Every Message!
- **Every message MUST be stored to DB immediately on creation**
- **Why**: 
  1. Polling mechanism needs persistence source (fetches new messages from DB)
  2. Message history for future access
  3. Read receipts tracking (last_read_at per participant)
  4. Audit trail for support/disputes

- **Flow**:
  ```
  User sends message
  → POST /api/conversations/{id}/messages
  → Controller validates + stores to DB instantly
  → Event emitted (MessageCreated)
  → Response returned to client
  → Next poll cycle (3-5 sec) fetches from DB
  → All participants see message
  ```

- **No caching optimization for messages** (unlike vendor/rider order polling)
  - Direct DB queries on each poll are acceptable
  - Can add pagination (latest 25 messages) to reduce payload
  - Consider query optimization: `->latest('created_at')->paginate(25)`

- **Storage Detail**:
  ```sql
  INSERT INTO messages (
    uuid, 
    conversation_id, 
    sender_user_id,
    type,
    body, 
    delivered_at,
    created_at
  ) VALUES (...) -- immediate, synchronous
  ```

### Updated Participant Model
```php
// For each order conversation, add:
- Customer (role='customer')
- Rider (role='rider')
// REMOVE: Vendor

// ConversationParticipant::create([
//     'conversation_id' => $conversation_id,
//     'user_id' => $customer->user_id, // or $rider->user_id
//     'role' => 'customer', // or 'rider'
//     'joined_at' => now(),
// ])
```

### Updated Database Schema Requirement
```sql
ALTER TABLE conversations ADD CONSTRAINT fk_context_id
  FOREIGN KEY (context_id) REFERENCES orders(order_id);
  
-- Optional: Soft deletes to preserve history
ALTER TABLE conversations ADD deleted_at TIMESTAMP NULL;
```

### Migration Strategy Revision
- Legacy `order_chat` migration: Only migrate messages for rider ↔ customer (ignore vendor if present)
- Resolve legacy sender_id mapping: Must match to correct rider or customer

### Git Deployment Strategy (May 2, 2026 - 8:48 PM)
- **Feature Branch**: `feature/chatbox-integration` (created, local)
- **Workflow**:
  1. Develop & test locally on `feature/chatbox-integration`
  2. Push to origin/feature/chatbox-integration
  3. Merge to origin/preprod (staging) for double-check
  4. After preprod verified, merge to origin/main (production)
- **Docker Status**: All 4 containers running (mysql, redis, app, nginx)
- **Redis Note**: Access via Docker network (`redis:6379` from container), NOT `127.0.0.1` from host
- **Docker Fix** (May 2, 2026 - 8:53 PM): Fixed `.env` REDIS_HOST from `127.0.0.1` → `redis`
  - Restarted docker-compose
  - App now loads successfully at http://localhost ✅
  - Ready for ChatBox implementation

---
*Yappy AI Project Entry - ChatBox Integration Planning & Deployment Setup (May 2, 2026)*

---

## 🆕 Major Update — Jun 2026 (Last Updated: Jun 16, 2026 · 03:00 MYT)

### Environment Change
- **No longer WSL** — Hakim now on macOS
- **Local path**: `/Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM`
- **Local dev**: Docker (`docker-compose exec app php artisan ...`)
- **Service name**: `app` (NOT `php`) in docker-compose

### Branch Structure (Jun 2026)
| Branch | Purpose |
|---|---|
| `feature/push-notification` | **Preprod deploy branch** — Hostinger pulls this |
| `main` | Production (`ondewei.my`) |
| `origin/AI-integration` | Aiman's dev branch — merged into feature/push-notification Jun 16 |
| `preprod` | DEAD — 150+ commits behind, ignore |

**Important**: Hostinger shared hosting has NO Node.js. Vite build artifacts must be committed to git (`git add -f public/build/`).

### Team (Jun 2026)
- **Hakim** — lead / owner (PT mode alongside FT job at 2Q Alliance)
- **AimanDhaifullah** — team dev. Handles AI features + admin overhaul.

---

### ✅ Payment Integration — COMPLETE (Jun 7–16, 2026)

#### BillPlz (fully live on preprod)
- **V3 bills** — customer checkout. `POST /api/v3/bills`, form-encoded.
- **V5 Payment Orders** — vendor/rider disbursements (weekly batch + manual)
- **X-Signature fix** (Jun 8, commit `7780573`): `ksort` → `uksort` comparator. See `library-items/integration/billplz-integration.md` for full details.
- **`PAYMENT_GATEWAY_ENABLED`** master switch: `false` = demo mode (instant settlement, no BillPlz call). Must be `true` on preprod/prod.

#### PERKESO (fully integrated Jun 14)
- 1.25% of `delivery_fee` per order, per rider
- Annual cap: RM 157.20 / rider / year
- Fires at BillPlz webhook (`paid=true`) — not at delivery, not at PO payout
- Retries via `SubmitPerkesoDeductionJob` if API fails
- See `library-items/integration/perkeso-gig-api.md` for full details.

#### Order Lifecycle (updated)
```
pending_payment → (BillPlz webhook paid=true) → pending → (rider accepts) → processing → delivered
```
- Delivery chat created AFTER payment confirmed
- `scopeActive()` excludes `pending_payment` — riders/vendors never see unpaid orders
- Weekly disbursement: Monday 09:00 MYT (`disbursements:process-weekly`)

---

### ✅ AI Chat-Ordering (Aiman, Jun 14, commit `f699549`)
- Customer orders via AI chat using OpenAI
- `CHAT_ORDER_AI_ENABLED`, `OPENAI_API_KEY`, `CHAT_ORDER_AI_MODEL=gpt-5.4-mini`
- Chat messages auto-pruned every 24 hours (`chat-order:prune` at 03:30 MYT)
- Keep `CHAT_ORDER_AI_ENABLED=false` on preprod until ready to enable

---

### ✅ Push Notifications (complete, earlier 2026)
- VAPID web push — working across all roles
- Latency fixed, dead subscription pruning active (HTTP 404/410)
- `feature/push-notification` branch name is from this feature

---

### 🔴 Pre-Launch Outstanding
1. E2E test on preprod: checkout → BillPlz → webhook → `pending` → riders notified → `perkeso_deductions` populated
2. Run `php artisan migrate` on preprod (`create_chat_order_ai_usage_table`)
3. Add 3 keys to preprod `.env`: `PAYMENT_GATEWAY_ENABLED=true`, `CHAT_ORDER_AI_ENABLED=false`, `OPENAI_API_KEY=`
4. Clear test order data from PROD (overdue since Jun 5)
5. Email BillPlz for e-wallet activation (SSM + KYC docs)
6. Enable all payment channels in admin
7. Run legacy data migration on PROD at launch
8. Merge `feature/push-notification` → `main`

---

### Key Commits (Jun 2026)
| Commit | Date | What |
|---|---|---|
| `7780573` | Jun 8 | X-Signature uksort fix (BillplzService.php) |
| `f699549` | Jun 14 | Aiman: AI chat + admin overhaul + BillPlz/PERKESO (162 files) |
| `caf06b2` | Jun 16 | Merge AI-integration → feature/push-notification (7 conflicts resolved) |
| `dda7e4f` | Jun 16 | Vite build artifacts committed (fixed preprod 500) |
| `6012c64` | Jun 21 | fix(location): skip modal if flag set; fix button label "Picked Up" → "Pick Up" |
| `3da6862` | Jun 21 | fix(pickup): GPS on all 4 pickup surfaces, localStorage-first, no repeated modal |
| `1e11d1d` | Jun 21 | fix(pickup): eliminate 422 race on available page; pill shape fix in chat (display:contents) |
| `f83e613` | Jun 21 | feat(deliver): proof modal on available page — photo + GPS like chat deliver |
| `6e7f862` | Jun 21 | fix(available): static Delivered button + pickup AJAX (2 missed bugs) |
| `022d0e7` | Jun 21 | fix(ios): replace .flat() with [].concat.apply() for iOS 11 compat |
| `bb71d71` | Jun 22 | fix(deliver): submit interceptor for cached old form + filemtime cache-busting |
| `79400a3` | Jun 22 | fix(pickup): 422 root cause (type=submit in Blade) + pickup submit interceptor + flicker HTML-diff fix |
| `192c993` | Jun 22 | feat(chat-order): remove ORDER TEMPLATE pre-fill, add Load Template pill button |
| `bd9eb39` | Jun 22 | fix(vendor): pending_payment filter, status polling, call button, Preparing pill sync |
| `ac2431c` | Jun 22 | fix(pickup+deliver): replace ondwForcePoll with page reload — eliminates requestInFlight race |

---

### ✅ Rider GPS + Delivery Proof Flow — COMPLETE (Jun 21–22, 2026)

**Branch**: `feature/push-notification` | All commits pushed to origin.

#### New Files Created
| File | Purpose |
|---|---|
| `public/customJS/ondw-pickup-gps.js` | Shared GPS utility for ALL pickup surfaces. MutationObserver + localStorage-first + AJAX submit. |
| `public/customJS/ondw-deliver-proof.js` | Delivery proof modal driver. Photo + GPS capture + AJAX. Delegated click + submit interceptor. |
| `resources/views/partials/_rider-proof-modal.blade.php` | Proof modal HTML (photo input, GPS status, confirm). IDs: `ondw-proof-*`. |

#### Key Architecture Decisions
- **iOS Permissions API is broken** — `navigator.permissions.query({name:'geolocation'})` always returns `'prompt'` on iOS Safari, even after user grants. NEVER use as a gate. Use `localStorage.getItem('ondw_location_granted')` instead (set on profile page first grant).
- **`getCurrentPosition()` must be synchronous inside click handler** — not inside a Promise/async chain. iOS/Android won't count it as a user gesture otherwise — system dialog won't appear.
- **`display:contents` on pickup form** — `<form>` is block-level and breaks the inline-flex rounded-full pill in chat. `class="contents"` makes the form invisible to flex layout.
- **`rider-orders-realtime.js` re-renders every 1200ms** — any GPS inputs injected by JS get wiped on next poll. Solution: AJAX submit (not `form.submit()`), GPS captured in the click handler payload sent immediately.
- **Pickup form: `type="button"` in JS template** — prevents native form submit racing MutationObserver on injection.
- **Deliver form: `data-ondw-deliver-btn` + `data-deliver-url`** — replaces the old plain `<form POST>` in both static Blade and JS-rendered templates. Delegated click on `document` catches dynamically injected buttons.
- **Submit interceptor (defensive)** — capture-phase `submit` listener in `ondw-deliver-proof.js` catches old cached `rider-orders-realtime.js` (Hostinger server-side HTTP cache) that might still inject old form POST. Any form matching `/orders/{id}/deliver` is hijacked → proof modal.
- **`filemtime()` cache-busting** — `?v=<unix_mtime>` on all three `customJS/` script URLs. Forces new URL on file change → bypasses both browser cache and Hostinger's HTTP layer cache.
- **`[].concat.apply([], Object.values(errors))` NOT `.flat()`** — `.flat()` is ES2019 and fails on iOS 11/Chrome 68 and below.
- **`ondwForcePoll()`** — exposed as `window.ondwForcePoll = checkForNewOrders` in `rider-orders-realtime.js`. Lets GPS/deliver handlers trigger immediate re-render without page reload.

#### 4 Pickup Surfaces — All Fixed
1. **Chat page** (`conversations/show.blade.php` + `delivery-conversation-realtime.js`) — `wireRiderActions()` intercepts submit, `requestPickupGPS()` localStorage-first
2. **Available page static Blade** (`rider/orders/available.blade.php`) — `class="ondw-pickup-form"`, wired by `ondw-pickup-gps.js` MutationObserver
3. **Available page JS-render** (`rider-orders-realtime.js` `activeActionsHtml()`) — `class="ondw-pickup-form"`, `type="button"` at birth, wired by MutationObserver
4. **Order detail page** (`rider/orders/show.blade.php` + `order-status-detail-realtime.js`) — `ondw-pickup-form` class, `ondw-pickup-gps.js` included

#### PERKESO Status
- `perkeso_deductions` table shows `status=pending` on preprod
- Root cause NOT yet investigated (was pre-existing before this session)
- `last_error` column migration not yet run on preprod — run `php artisan migrate`

#### Jun 22 2026 — Second Session (2 AM MYT)

**Additional fixes committed this session:**
- Vendor orders page — 4 bugs fixed:
  - `pending_payment` orders now filtered from vendor API response
  - `processPendingOrders()` re-renders card when status changes (e.g. → `rider_accepted`)
  - `initializeOrderStatuses()` reads real status from `data-order-status` attribute
  - `buildOrderCardHTML()` now has `isCooking` branch + call button (rider phone) on both pending+cooking cards
  - `updateHeaderPills()` syncs Pending/Preparing pill counts live after every card change
- Rider available page — pickup + deliver stuck "Locating…" fixed:
  - Root cause: `requestInFlight` guard in `checkForNewOrders()` silently dropped both `ondwForcePoll()` calls if a poll was mid-flight
  - Fix: `window.location.reload()` after 800ms on pickup success and deliver success — reliable, no race conditions
- Deliver button flicker — definitive fix:
  - HTML string comparison always failed (browser normalises whitespace differently from template literals)
  - Fix: `lastRenderedStatus{}` object tracks per-order status; DOM only updated on actual status transition
- Chat page — ORDER TEMPLATE removed from textarea pre-fill; "Load template" pill button added (same row as "Repeat last")

**CEO confirmation pending (do not implement until confirmed):**
- "Terima Order" call button: confirm with CEO whether to call RIDER or CUSTOMER

#### Still Pending (Pre-Launch)
1. Add `PERKESO_EMPLOYER_CODE` + `PERKESO_EMPLOYER_NAME=ONDW` to preprod `.env` + `php artisan config:cache`
2. Retry PERKESO deduction from `/admin/integrations/perkeso` — verify `last_error` clears
3. E2E test: checkout → BillPlz → webhook → rider pickup (GPS) → deliver (GPS + photo) → confirm PERKESO fires
4. Clear test order data from PROD (overdue since Jun 5)
5. Email BillPlz for e-wallet activation (SSM + KYC)
6. CEO confirmation: "Terima Order" call button — rider or customer?
7. Run `billplz:sync-fpx-banks` on preprod/prod
8. Merge `feature/push-notification` → `main`

---

## Jun 24, 2026 — Bug Fix + UX Session (commits 2fe7554, f05e841, e20ab24)

### Bugs Fixed
| Bug | Root Cause | Fix |
|---|---|---|
| All orders cancelled after payment | `PaymentTransaction.amount_sen` missing platform fee → webhook mismatch | Added `+ PLATFORM_FEE_SEN` to stored amount |
| Rider Pick Up button stuck | `lastRenderedStatus[orderId]` — `orderId` was undefined, wrote `"undefined"` key, never re-rendered | Fixed to `order.order_id` in `rider-orders-realtime.js` |
| Proof delivery 404 | Disk mismatch — saved to `'public'`, served from `'local'` | `Storage::disk('local')` → `'public'` in `routes/web.php` (3 occurrences) |
| Proof modal under navbar | Modal inside `@section('content')` → inside `<main overflow-y:auto>` → iOS clips fixed children | Moved to `@push('modals')` stack, `@stack('modals')` added to `app.blade.php` |
| PERKESO never auto-retried | `markFailed()` set `next_retry_at` but never re-dispatched job; no scheduled sweep | `markFailed()` now re-dispatches job; 10-min Kernel sweep via `pendingRetry` scope |
| PERKESO missing API fields | `transacted_at`, `end_date`, `employer_name`, `employer_code` all absent from payload | All fields added to `PerkesoDeductionService::attemptSubmit()` payload |

### New Feature
- **Customer orders infinite scroll** — `OrderController::index()` JSON branch + `customer-orders-infinite.js` (IntersectionObserver, 200px early trigger, paginate 20 per load)

### Key Commits
| Commit | What |
|---|---|
| `2fe7554` | PERKESO missing fields fix (transacted_at + employer fields) |
| `f05e841` | Rider polling, proof 404, modal body-append, onerror on dynamic img |
| `e20ab24` | Drawer @stack('modals') fix, PERKESO auto-retry, customer orders infinite scroll |

---

## Jun 26, 2026 — BillPlz Payment Order (Payout) Deep Dive (03:00+ MYT)

### 🔑 Critical BillPlz PO Knowledge (hard-won tonight)

#### Sandbox Testing
- **`bank_code: DUMMYBANKVERIFIED`** — the ONLY bank_code that produces a successful PO in BillPlz sandbox. Every other code (real SWIFT, TEST0021, ABB0234, BP-FKR01) results in transaction failure or rejection.
- Staging FPX codes (`BP-FKR01`, `TEST0021` etc.) are for FPX bill payment (`reference_1`), NOT for Payment Order `bank_code`. These are completely different fields.
- BillPlz sandbox does NOT reliably fire PO callbacks. Status stays `processing` forever unless callback URL is configured AND BillPlz sandbox actually sends it.

#### PO Callback URL
- Must be set on the **Payment Order Collection** (not main account settings)
- BillPlz Dashboard → Payment Orders → your collection → Edit/Settings → Callback URL
- Our endpoint: `POST /webhooks/billplz/po` (CSRF-exempt, X-Signature verified)
- Checksum field order (strict): `[id, bank_account_number, status, total, reference_id, epoch]`
- BillPlz retries once after 1 hour on failure. 2 failures = permanently removed. Account rank degraded per failed callback.

#### Create PO — Required Fields
```
payment_order_collection_id, bank_code, bank_account_number, name,
description (ASCII only, max 200 chars, NO special chars), total (sen),
epoch (unix), checksum
```
- Checksum order for creation: `[payment_order_collection_id, bank_account_number, total, epoch]`
- Our implementation in `BillplzService::createPaymentOrder()` ✅ matches exactly

#### SWIFT Bank Codes (production po_bank_code) — Corrected Jun 26
| Bank | Correct SWIFT |
|---|---|
| Maybank | `MBBEMYKL` |
| CIMB | `CIBBMYKL` ← was `CIMBCLKL` (wrong) |
| Hong Leong | `HLBBMYKL` |
| RHB | `RHBBMYKL` |
| Affin | `PHBMMYKL` ← was `AFBQMYKL` (wrong) |
| Alliance | `MFBBMYKL` ← was `ABMB0212` (FPX code used by mistake) |
| AmBank | `ARBKMYKL` ← was `AMMBKLKL` (wrong) |
| Bank Islam | `BIMBMYKL` |
| Bank Rakyat | `BKRMMYKL` |
| BSN | `BSNAMYK1` ← digit 1 NOT letter L (official BillPlz doc confirmed) |
| Agrobank | `AGOBMYKL` (added) |
| Bank Muamalat | `BMMBMYKL` (added) |
| HSBC | `HBMBMYKL` (added) |
| Citibank | `CITIMYKL` (added) |
| Kuwait Finance House | `KFHOMYKL` (added) |
| OCBC | `OCBCMYKL` |
| Public Bank | `PBBEMYKL` |
| Standard Chartered | `SCBLMYKX` |
| UOB | `UOVBMYKL` |

### Bugs Fixed Tonight (all on `feature/push-notification`)

| Commit | Bug | Fix |
|---|---|---|
| `51de36c` | BillPlz PO 422 "invalid characters" | Em dash `—` in description → ASCII hyphen `-` |
| `03dc0a6` | Wrong SWIFT codes in seeder, 5 banks missing | Full `BillplzPaymentChannelSeeder` rewrite from official docs |
| `fcbab2f` | Same-day retry blocked by DB unique constraint | `disburseManual()` cleans `failed`/`refunded` records before retry |
| `fb0a6da` | Payout button dead — no network request | Browser silently blocking `confirm()` → replaced with inline 2-click amber confirm pattern |
| `86c446a` | Orders reappear in pending balance after payout | Flawed `disbursements.created_at >= orders.updated_at` timestamp join → 30-day window instead |
| `78d69b3` | "Reference ID already taken" on retry | BillPlz permanently holds reference_ids → added `HHmmss` to `manual-YmdHis-type-id` batch_ref |

### Architecture Notes — DisbursementService
- **Pending balance query**: `whereNotExists` with 30-day window on `processing`/`completed` disbursements
- **Manual batch_ref**: `manual-YmdHis-vendor-3` (timestamp in seconds, unique per attempt)
- **Weekly batch_ref**: `week-2026-26-vendor-3` (date-week, idempotent per week)
- **Retry safety**: failed/refunded records auto-deleted before new attempt; processing records block new attempts via pending balance = 0
- **Double-pay protection**: `processing` status blocks pending balance → no second payout possible while first is in flight

### Still Pending
1. Set `DUMMYBANKVERIFIED` on staging vendor/rider for sandbox E2E test
2. Configure PO callback URL on BillPlz sandbox PO collection
3. Verify webhook fires and local status flips `processing` → `completed`
4. On production: use real SWIFT codes (corrected in seeder) + real vendor/rider bank details

---

## Jun 27, 2026 — FIUU DuitNow QR Integration (COMPLETE + Security Hardened)

### Branch
`feature/push-notification` — committed (`fe86ee4`) + pushed to `origin/feature/push-notification` (preprod)

### What Was Built
Full FIUU DuitNow QR payment gateway integration — replaces BillPlz as the **customer checkout gateway** (BillPlz kept for rider/vendor disbursements only).

#### New Files
| File | Purpose |
|---|---|
| `app/Services/Fiuu/FiuuService.php` | Core FIUU service — vcode, skey, `normalizePayload()`, `buildPaymentParams()`, `getPaymentUrl()` |
| `app/Http/Controllers/Webhooks/FiuuWebhookController.php` | `notify()` (webhook), `redirect()` (return URL), `cancel()` (cancel URL) |
| `resources/views/customer/payment/fiuu-redirect.blade.php` | Auto-submit hidden form page — "Redirecting to DuitNow QR…" |
| `app/Console/Commands/ExpirePendingPayments.php` | Expire orders stuck in `pending_payment` for >30 min; schedule: every 15 min |

#### Modified Files
| File | What Changed |
|---|---|
| `config/services.php` | Added `fiuu` config block (merchant_id, verify_key, secret_key, env, channel) |
| `app/Http/Middleware/VerifyCsrfToken.php` | Added `webhooks/fiuu` to `$except` |
| `routes/web.php` | FIUU webhook route + customer auth group: launch, return, cancel |
| `app/Http/Controllers/Customer/PaymentController.php` | `fiuuLaunch()` + `pending()` now checks `from_fiuu_redirect` |
| `app/Http/Controllers/Customer/OrderController.php` | `placeOrder()` + `placeFromChatContext()` route to FIUU/BillPlz based on `FIUU_ENABLED` flag |
| `resources/views/customer/checkout.blade.php` | Payment method pills (DuitNow QR default / FPX Online Banking) + hidden input |
| `app/Console/Kernel.php` | `payments:expire-pending` every 15 min |

### Critical Architecture Notes

#### FIUU field naming — two conventions
FIUU's API has legacy field names (`amount`, `tranID`, `orderid`, `status`, `domain`) used in the skey formula, AND new API names (`TxnAmount`, `TransactionID`, `ReferenceNo`, `TxnStatus`, `MerchantID`). **Always call `$fiuuService->normalizePayload($request->all())` first** in every handler — maps both to legacy names. Signature formula and amount check use normalised keys.

#### skey formula
```
pre_skey = md5(tranID + orderid + status + domain + amount + currency)
skey     = md5(paydate + domain + pre_skey + appcode + secret_key)
```
- `hash_equals()` used for timing-safe comparison ✅
- Paydate freshness check: reject if >300 seconds old (anti-replay) ✅

#### vcode formula (request)
```
vcode = md5(amount + merchantID + orderid + verify_key)
```

#### Order reference
`ONDW-{orderId}` (max 40 chars, alphanumeric). Parse back with `FiuuService::parseOrderId()`.

#### Status codes
- `00` = success → settle
- `11` = failed → cancel
- `22` = pending (bank processing) → hold, wait for another notify

#### Payment flow
```
Checkout → placeOrder() → createFiuuPaymentForOrder()
  → stores params in session("fiuu_params.{orderId}")
  → creates PaymentTransaction (provider='fiuu', status='pending')
  → redirects to /customer/payment/fiuu/pay/{orderId}
→ fiuuLaunch() → pulls session params (one-time pull, deleted) → renders auto-submit form
→ Customer browser POSTs to FIUU hosted page
→ FIUU fires notify() → verifies skey + paydate → checks idempotency → DB::transaction + lockForUpdate → settles order → fires OrderPlaced
→ Customer browser returns to redirect() → if settled, go to conversation; else pending screen
```

#### Cancel flows
- **Customer cancels on FIUU page** → `cancel()` → marks order `cancelled`, transaction `failed/customer_cancelled`
- **Customer manual cancel** → `OrderController::cancel()` — now accepts `pending_payment` status, marks transaction `failed/customer_cancelled`
- **Auto-expiry** → `ExpirePendingPayments` artisan command every 15 min — marks transaction `expired/session_timeout`, order `cancelled`

### .env Variables Required (Hakim adds manually to preprod/prod)
```
FIUU_MERCHANT_ID=
FIUU_VERIFY_KEY=
FIUU_SECRET_KEY=
FIUU_ENV=sandbox
FIUU_ENABLED=true
FIUU_CHANNEL=DQR
```
After adding: `php artisan config:cache && php artisan route:cache`

### Davai 🧪 Test Findings — 9 Bugs Found, 3 Critical Fixed

| Bug | Severity | Status | Description |
|---|---|---|---|
| BUG-01 | High | ✅ Fixed | `verifyCallbackSignature` used `$payload['amount']` but FIUU sends `TxnAmount` → fixed by `normalizePayload()` |
| BUG-09 | Medium | ✅ Fixed | `PaymentController::pending()` only checked `from_billplz_redirect`, not `from_fiuu_redirect` |
| BUG-05 | Medium | ✅ Fixed | `placeFromChatContext()` always called `createBillForOrder()`, bypassing FIUU routing |
| BUG-02 | Low | Open | Session expiry UX gap on cancel URL when no orderid |
| BUG-03 | Low | Open | Session expiry UX gap on return URL when no orderid |
| BUG-06 | Medium | Open | `ExpirePendingPayments` may cancel status-22 in-flight transactions |

### Reza 🔐 Security Audit — All Mediums Fixed

| ID | Severity | Status | Finding |
|---|---|---|---|
| SEC-01 | Medium | ✅ Fixed | Full raw payload logged on unknown orderid — now logs only orderid/status/tranID |
| SEC-02 | Medium | ✅ Fixed | No paydate freshness check — added 300s window, rejects stale callbacks |
| SEC-03 | Low | Open | No payload size cap (mitigated by shared hosting php.ini) |
| SEC-04 | Low | ✅ Fixed | `payment_method` not in validation allowlist — added `Rule::in(['fiuu','billplz'])` |
| SEC-05 | Info | N/A | MD5 used per FIUU spec — cannot change |

**Security properties verified green:**
- Keys env-only, never hardcoded ✅
- Amount server-computed, never from browser ✅
- `hash_equals()` for timing-safe signature comparison ✅
- DB transaction + `lockForUpdate()` on settlement ✅
- Idempotency guard prevents double-settlement ✅
- Webhook always returns HTTP 200 ✅
- CSRF exemption scoped to webhook only ✅
- IDOR: `firstOrFail()` scoped to `customer_id` on all routes ✅

### New Staff
- **Davai 🧪** — Software Tester. Tests end-to-end flows, reports bugs with root cause. Onboarded Jun 27.
- **Zara ⚡🎛️** — already on staff (confirmed earlier)

### Still Pending Before Going Live
1. Hakim adds FIUU `.env` vars to preprod server
2. Run `php artisan config:cache && php artisan route:cache` on preprod
3. E2E sandbox test: checkout → DuitNow QR → webhook → conversation (Davai task)
4. Set `FIUU_ENV=production` + real credentials when going live
5. Later: remove payment method selector from checkout, hardcode FIUU only
6. CEO confirmation: "Terima Order" call button — rider or customer?

---

## Jul 4–5, 2026 — PERKESO + FIUU + Session Fix

### PERKESO ensureRiderRegistered() — Multiple Bugs Fixed ✅
- `checkUser` response: `status:"success"` means API call worked, NOT that user is registered. Real answer in `data.result`
- Registered result string is `"REGISTERED_USER"` (not `"USER_REGISTERED"`) — confirmed from real API response
- `"already been registered"` fail from registerUser → treat as registered, update flag, proceed
- All deduction paths covered: admin raw form has its own `checkRegistration()` method that uses same logic

### ic_type Selector — Added to All Rider Entry Points ✅ (commit e6c35e3)
- `register.blade.php`, `google-complete.blade.php`, `profile/edit.blade.php`
- `RegisteredUserController`, `GoogleAuthController`, `ProfileUpdateRequest`, `ProfileController`
- Mapping: `mykad/mykid → 'B'`, `passport → 'PR'` (PERKESO API format)

### Non-Blocking PERKESO on Deliver — `app()->terminating()` Applied ✅
- PERKESO deduction moved out of synchronous deliver() path
- `app()->terminating(fn() => ...)` — Laravel fires AFTER `$response->send()` flushes to rider's browser
- Rider sees "Delivered" immediately; PERKESO HTTP calls happen in background
- No queue worker needed — works on Hostinger shared hosting

### FIUU Post-Payment Logout Bug — Fixed ✅ (tested on preprod)
- Root cause: FIUU redirects customer back via POST form → SameSite=Lax blocks session cookie → `auth()->user()` null
- Fix: `SESSION_SAME_SITE=none` + `SESSION_SECURE_COOKIE=true` in .env
- `config/session.php` now env-driven: `env('SESSION_SAME_SITE', 'lax')`
- BillPlz not affected (uses GET redirect — Lax allows cookies on GET)
- **Prod .env reminder**: add `SESSION_SAME_SITE=none` + `SESSION_SECURE_COOKIE=true`

### FIUU Refund isQueued Fix ✅
- `initiateRefund()` wrongly returned `success=true` when FIUU served an HTML 404 page (HTTP 200)
- Fix: `$isQueued = $response->successful() && !$hasError && $response->json() !== null`

---

## Jul 6, 2026 — Pickup Feature Architecture Analysis (00:00–01:00 MYT)

### Context
Miyamura wants pickup order type alongside delivery. Team (Hana/Sora/Mira) did parallel codebase audit. Full analysis produced — no code written yet, planning only.

### Proposed Flows
- **Delivery** (existing): `Customer → payment → Rider accepts → Vendor prepares → Rider delivers → Customer`
- **Pickup** (new): `Customer → payment → Vendor prepares → Customer collects` (no rider)

---

### Confirmed Breakpoints

#### 🔴 Critical — Hard Failures

**1. No `order_type` column** — zero migration, zero model field. Everything else depends on this.
- Fix: `ALTER TABLE orders ADD order_type ENUM('delivery','pickup') DEFAULT 'delivery'`

**2. `delivery_location` fields are `required` + `NOT NULL`**
- `app/Http/Controllers/Customer/OrderController.php` lines 109–124
- Will 422 on every pickup order placement.
- Fix: nullable migration + `required_if:order_type,delivery` validation

**3. Status machine has no pickup path**
- `app/Services/OrderStatusService.php` lines 24–57
- Current: `pending → rider_accepted → accepted → preparing → ready_for_pickup → on_delivery → delivered`
- Pickup needs: `pending → accepted (vendor direct) → preparing → ready_for_pickup → collected`

**4. Vendor portal blind to pickup orders**
- `Vendor/OrderController::accept()` guards on `status !== 'rider_accepted'`
- `$vendorRelevantStatuses` starts at `rider_accepted` — pickup `pending` orders invisible

**5. Rider push notifications fire for pickup orders**
- `SendOrderNotifications` — no order_type guard; all riders notified

**6. Rider available pool shows pickup orders**
- `Rider/OrderController::available()` — no `order_type` filter; pickup appears in rider queue

#### 🟡 Medium — New Flow Needed
**7. Pickup confirmation** — no endpoint exists. Simplest: vendor "Mark Collected" button. Alt: QR/PIN.

#### 🟢 Safe — No Changes
| Area | Why |
|---|---|
| PERKESO | `if ($order->rider)` guard; pickup never reaches deliver() |
| Disbursements | delivery_fee = 0, no rider → auto-excluded |
| Payment gateway | Just pass delivery_fee = 0 — gateway charges correctly |
| Delivery chat | null rider_id in meta is benign |

---

### Recommended Build Order (When Ready to Implement)

```
1 ↓ Migration — add order_type ENUM('delivery','pickup') DEFAULT 'delivery'
2 ↓ Make delivery_location_* nullable + conditional validation
3 ↓ Status machine — add pickup transition path in OrderStatusService
4 ↓ Vendor portal — accept 'pending' pickup orders; add to vendorRelevantStatuses
5 ↓ Rider notification guard — skip OrderPlaced blast for pickup
6 ↓ Rider available pool — exclude pickup from query
7 ↓ Pickup confirmation endpoint — vendor "Mark Collected" button (simplest)
8 ↓ Checkout UI — order type toggle, conditional delivery section, fee logic
9 ↓ Customer order show — pickup progress steps + hide rider panel
10 ↓ Vendor/admin views — conditional copy, hide rider card for pickup
```

Steps 1–6 = system skeleton (orders flow end to end). Steps 7–10 = UX layer.

---

### Sunmi Companion App — ON HOLD
- Plan: Android `.apk` — polls print queue API, auto-accepts, prints via Sunmi AIDL SDK
- Components: BootReceiver, PrinterService, SunmiPrinterHelper, MainActivity
- **Status**: ON HOLD until Aiman's Sunmi device arrives. Will revisit once in hand.

---

## Outstanding Tasks (as of Jul 6, 2026)

### Pre-Launch Must-Do
1. ⬜ FIUU refund ONDW-158 — stuck at `refund_pending`; FIUU sandbox won't send callback. Manual DB reset → `captured`, retry on prod
2. ⬜ `verifyRefundNotifySignature()` — confirm formula when real prod callback arrives
3. ⬜ Attachment image bug — remove `Content-Length` in `ConversationAttachmentController::show()`
4. ⬜ Proof modal drawer — pull preprod + test on mobile
5. ⬜ End-to-end preprod test (full order flow: checkout → payment → rider pickup GPS → deliver proof → PERKESO)
6. ⬜ Email BillPlz for e-wallet activation (SSM + KYC docs)
7. ⬜ Run `billplz:sync-fpx-banks` on preprod/prod
8. ⬜ Test payout flow end-to-end on preprod
9. ⬜ Legacy data migration on prod at launch
10. ⬜ CEO confirmation: "Terima Order" call button — rider or customer?
11. ⬜ Ask Aiman: KK distances (KM) + ETA (minutes) for rider available orders page
12. ⬜ Chat order UI improvement (Hakim not satisfied with current design)
13. ⬜ Merge `feature/push-notification` → `main`

### New Features (Planned)
14. ⬜ Pickup feature — analysis done, 10-step build plan above
15. ⬜ Sunmi companion app — ON HOLD until device arrives

### Prod .env Checklist (before going live)
```
SESSION_SAME_SITE=none
SESSION_SECURE_COOKIE=true
PERKESO_ENV=production
PERKESO_SECTOR_CODE=G
PERKESO_EMPLOYER_NAME=ONDW
PERKESO_EMPLOYER_CODE=
PERKESO_TOKEN=
PERKESO_CLIENT_ID=
PERKESO_CLIENT_SECRET=
FIUU_ENV=production
FIUU_MERCHANT_ID=
FIUU_VERIFY_KEY=
FIUU_SECRET_KEY=
FIUU_CHANNEL=RPP_DuitNowQR
php artisan migrate
php artisan db:seed --class=DeliveryLocationsSeeder
php artisan db:seed --class=BillplzPaymentChannelSeeder
php artisan config:cache
php artisan route:cache
```

---

## Jul 12, 2026 — Pickup Feature COMPLETE + Reports/Fees Fixed

### Branch: `feature/push-notification` — 9 commits pushed, latest: `ad755f3`

### What Was Built & Fixed (9 commits)

**Root cause of "same bug three rounds in a row":**
1. `resources/js/delivery-conversation-realtime.js` is Vite-compiled → `public/build/assets/app-*.js`. The committed bundle was 10 days stale (built Jul 2) — pickup JS was never in the deployed bundle. All JS fixes for chat were committing to source but never reaching the browser.
2. `public/build` is git-tracked. Preprod has no Node.js. ANY edit to `resources/js/*` MUST be followed by `npm run build` locally + commit the new bundle + push. MANDATORY RULE from this session forward.
3. JS assets in vendor blade had no cache-busting — PWA kept serving old pre-pickup JS forever. Fixed with `?v={filemtime()}`.

**Commit `0cad105`** — Vendor polling: `VendorOrderController::getOrdersStatusUpdates()` was including ALL terminal orders from last 24h in `other` payload. Now: terminal orders only sent if `updated_at >= now()->subMinutes(10)` (JS needs one terminal event to remove the card, then they drop off). Added `sweepStaleCards()` to remove rendered cards absent from both lists.

**Commit `7d32c5c`** — Rebuilt Vite bundle (10-day stale). `DeliveryChatService::statusPillFor/statusLabelFor` made pickup-aware — polling was overwriting the blade-rendered pill with "Waiting for rider" on every tick.

**Commit `c5722b6`** — Vendor history/stats/earnings: `whereIn(['delivered','collected'])` for all revenue/completed queries; "Dipungut" green label; blank location → "Ambil sendiri"; Pickup badge on server-rendered cards; stat cards renamed "Delivered" → "Completed".

**Commit `7c9404b`** — `DisbursementService::pendingBalances()`: `where('status','delivered')` → `whereIn('status', ['delivered','collected'])`. Vendors were silently never getting paid for pickup orders via BillPlz disbursement.

**Commit `c13f64d`** — Customer/Rider/Admin reports: collected in all completed counts; rider feeds sealed from pickup (`order_type=delivery`); customer history card "Waiting for rider" → "Pickup" badge; admin cancel guard fixed (collected is terminal now); `OrderController@repeatLast` now includes collected.

**Commit `3f090d8`** — Platform fee display fixed. `MoneyHelper::platformFeeSen()` is TIERED (RM 0.50 → RM 1.80+, not flat RM 1.00). Old blades had hardcoded `+ 1` or omitted fee. Fixed: order detail, list card, payment pending, checkout initial paint. Fee is NEVER stored in DB — always computed at display time.

**Commit `c505ca5`** — Chat: confirmation message pickup-aware ("Self pickup at the stall."); "Collect my order" button moved above chat composer (matches rider pattern, `data-pickup-collect-section` + `data-pickup-trigger` attributes unchanged so polling JS works without Vite rebuild); pickup drawer converted to AJAX with photo compression (mirrors rider drawer: fetch + FormData + AbortController 45s timeout + `ondwCompressImage`). `collect()` returns JSON when `expectsJson()`.

**Commit `285ea3e`** — Chat receipt: "Platform support" fee row added (tiered); `DeliveryChatService::conversationPayload()` `total_amount_formatted` now includes tiered fee so JS polling can't regress the header. Label unified to **"Platform support"** (exact checkout.blade.php label) across all customer-facing breakdowns.

**Commit `ad755f3`** — About page: "RM1 system fee" → "RM0.50+ platform support, from"; count-up JS made decimal-safe (was `parseInt`, now `parseFloat` with `toFixed(decimals)`).

### Architecture Decisions — Locked
- `MessageAttachment.attachment_type` = computed accessor (NOT DB column). `uploaded_by_user_id` IS DB NOT NULL — must always be set on `attachments()->create()`.
- Platform fee: NEVER stored in DB. `MoneyHelper::platformFeeRm($total)` at display time, `MoneyHelper::platformFeeSen($total)` at charge time. Never hardcode RM 1.00.
- `DeliveryChatService::ensureForOrder()` (not `forOrder()`) must be used in `collect()` — creates conversation + guarantees customer is a participant so `sendMessage()` doesn't 403.
- Vendor disbursement: `whereIn('status', ['delivered', 'collected'])` — both terminal types paid out.

### Updated Outstanding Tasks (as of Jul 12, 2026)
1. ⬜ FIUU refund ONDW-158 — stuck at refund_pending; manually reset DB + retry on prod
2. ⬜ Chat order UI improvement — Hakim wants polish (future session)
3. ⬜ Attachment image bug — remove `Content-Length` from `ConversationAttachmentController::show()`
4. ⬜ End-to-end preprod test: checkout → payment → pickup flow end-to-end
5. ⬜ Clear test order data from PROD
6. ⬜ Email BillPlz for e-wallet activation (SSM + KYC docs)
7. ⬜ Run `billplz:sync-fpx-banks` on preprod/prod
8. ⬜ Test payout flow end-to-end on preprod
9. ⬜ Legacy data migration on prod at launch
10. ⬜ CEO confirmation: "Terima Order" call button — rider or customer?
11. ⬜ Ask Aiman: KK distances + ETA for rider available orders page
12. ⬜ Merge `feature/push-notification` → `main`
13. ⬜ Sunmi companion app — ON HOLD until Aiman's device arrives

---

## Jul 22–24, 2026 — Liquid Glass Nav + Chat Composer Redesign + Figma-CLI Exploration

### Branch: `feature/push-notification`, commits `41b6d52`..`9b268a0`

### Liquid glass nav (Jul 22)
- `feature/liquid-glass-nav` merged in. Full SVG-displacement refraction effect is **Chromium-only** — Safari, Firefox, and every iOS browser (Chrome-for-iOS, Arc-for-iOS included, since Apple mandates the WebKit engine for all iOS browsers outside the EU) fall back to a plain frosted `backdrop-filter: blur()`. Confirmed with Hakim as expected/permanent, not a bug — closed.
- Fixed a real WebKit bug: `position:fixed` + `backdrop-filter` + `transform` stacked on one element kills backdrop-filter rendering in Safari. Fix: moved the scroll-shrink `transform` to a separate `.mobile-glass-nav-wrap` outer element, kept `backdrop-filter` on the untransformed inner `.mobile-glass-nav`.
- Fixed: mobile bottom pill nav had zero `dark:` classes at all — added, matching `#main-nav`'s existing dark-glass convention.
- Fixed: scroll-shrink was completely dead for customer/rider/vendor (worked only for admin). Root cause: the nav's scroll script is `@include`d in `app.blade.php` *above* `<main>`, and ran synchronously before `<main>` existed in the DOM — `document.querySelector('body.ow-app-shell > main')` always returned null on the locked-shell roles. Admin isn't in the locked-shell list so its plain `window` scroller never hit this. Fixed by wrapping in `DOMContentLoaded`.

### Chat composer redesign (Jul 24)
- First pass: composer became its own floating glass card (rounded-28px, translucent, same recipe as nav) sitting above the pill nav.
- Hakim asked to simplify further: removed the outer card entirely. The input pill itself now carries the glass styling directly and sits right against the top of the nav — no more "card containing a pill" double-box look. Desktop keeps the original flat full-width bar (no pill nav there to match).
- Nav shrink/full-size state now persists across full page navigations via `sessionStorage` (`ow-nav-compact` key), restored synchronously before paint. Previously every fresh page load always started full-size regardless of scroll position on the prior page — visible "pop" when navigating while scrolled down. Fixed.

### Figma-CLI exploration (Jul 24, in progress)
- Dispatched a design-focused subagent to research `github.com/silships/figma-cli` (a third-party CLI, NOT Figma's official Dev Mode MCP) and propose design options for the nav+composer pairing.
- **Key fact about figma-cli**: connects to Figma **Desktop** directly via Chrome DevTools Protocol (port 9222), not Figma's cloud REST API — this is why it needs Figma Desktop open, unlike token-based MCP servers. No API key, no rate limits, runs fully local.
- Two connection modes: **Yolo** (default) patches a single string inside Figma Desktop's `app.asar` (`removeSwitch("remote-debugging-port")` → harmless variant) to unblock Electron's own standard remote-debugging flag — genuinely small/reversible at the byte level, but requires macOS **"App Management"** permission for the terminal, which is a broader ongoing grant than the "one file patch" framing suggests. **Safe Mode** avoids this entirely via a real Figma plugin (Plugins → Development → FigCli) instead, no binary touched.
- Hakim chose Yolo. First attempt failed: `EPERM` — terminal lacked App Management permission. Hakim has since granted the permission via System Settings and needs to fully quit + reopen the terminal for it to take effect — **that's where this left off**, resume with `node src/index.js` (or `figma-cli connect`) from `/private/tmp/claude-501/-Users-hakim/dafc432b-6956-493a-b25c-7d8a01bdc993/scratchpad/figma-cli-check/figma-cli` (session scratchpad — may not exist in a future session; re-clone `https://github.com/silships/figma-cli.git` if so) once the terminal's been restarted.
- Three design options already proposed for the nav+composer pairing (grounded in existing tokens — `#d8e8f4` border, `rgba(255,255,255,.72)`/`.85` bg, `--ow-bottom-nav-h` var, `inset-x-3`): (1) refined stacked cluster — tighten gap, sync with scroll-shrink var — lowest risk, ~90% already built; (2) merged single capsule with internal seam — more novel, needs real iOS-vs-Chromium testing; (3) nav auto-hides on composer focus, composer drops to nav's resting position — best if keyboard-covering-composer is a real complaint. Recommended starting with (1). Also flagged: send button is 40×40px, just under the 44px touch-target minimum — worth bumping regardless of which option ships.
- Next step once reconnected: actually build the picked option(s) live in Figma via plain-language commands, per the CLI's design.
