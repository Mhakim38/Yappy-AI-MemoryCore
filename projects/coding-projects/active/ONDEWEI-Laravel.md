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

### Figma-CLI — WORKING PROTOCOL (Jul 24, connection solved ✅)
- `github.com/silships/figma-cli` (third-party CLI, NOT Figma's official Dev Mode MCP). Connects to Figma **Desktop** via Chrome DevTools Protocol (port 9222) — needs Figma Desktop open, no API key, fully local.
- **Yolo mode is set up and working**: App Management permission granted to terminal + full terminal restart = `EPERM` gone. Run `node src/index.js connect` from the clone (session scratchpad `/private/tmp/claude-501/-Users-hakim/dafc432b-6956-493a-b25c-7d8a01bdc993/scratchpad/figma-cli-check/figma-cli` — re-clone `https://github.com/silships/figma-cli.git` + `npm install` if gone). `status` shows connected file; `files` lists open tabs. A file must be OPEN in Figma Desktop (blank Figma = `files` returns `[]`; File → New Tab, ⌘T, to create one — CLI cannot create files itself, plugin API limitation).
- **Renderer gotchas (all confirmed by painful experience)**: rgba() string fills CRASH — use hex8 alpha (`#ffffffB8`); `blur` prop = layer blur (blurs icons too — wrong), `bgBlur` = real backdrop blur; `canvas next` and `set pos` both ETIMEDOUT and silently fail — position via `eval` wrapped in IIFE `(function(){...})()` (top-level `const` in eval collides with daemon scope); input rows need `w="fill"` on textarea container or send button overlaps; several small render calls > one giant render-batch (a giant one stalled a whole agent once); icons are Lucide-only via Iconify (closest matches to app's Font Awesome).

### Design exploration gallery (Jul 24 evening — Figma file "ONDW")
- **18 frames after final round** (4 rows): Original + Original-Suggested-Improvements (8:938); first trio Option 1/2/3 (Option 3 = auto-hide, 4 sub-states pickup/delivery × idle/focused); rejected warm-palette trio A/B/C (off-brand orange, kept on canvas); round-3 D/E/F + R1/R2/R3 (y≈832); round-4 G/H/I + R4/R5/R6 (y=1100); round-5 J/K/L + R7/R8/R9 (y=1600, final round, built Jul 24 ~8:30 PM).
- **Hakim's favorite: OVERHAUL D — Split Dock (12:1127)** — 4-tab glass pill + detached 56px circular Chat island with unread dot, capsule composer, rounded-full green Collect. Runner-up: **G — Twin Orbit (13:1496)** — Chat island left + green Collect FAB island right, 3-tab pill (Cart dropped — tradeoff). He loves the "refreshing ideas" energy of the island language.
- All rounds after A/B/C use STRICT original palette only: glass `#ffffffB8`+bgBlur, borders `#d8e8f4`/`#cfe5f7`, blue `#2167AD`, green `#2F7D5C`, tint `#EAF5FF`, textarea `#F8F6F1`, bg `#EEF1F4`, inactive `#64748b`. Differentiation via structure/elevation (scale: `0 4 6` / `0 8 16` / `0 20 40`, one top-elevated element per frame). Nav always pill-shaped (Hakim's hard constraint).
- QA pass (Davai) found + fixed: F's broken waist seam, R2's chip overflow + lost corner radii. D verified untouched/clean 3×.
- **Implementation scope (Hakim confirmed)**: winning design applies ONLY to the two pages with a message input — delivery chat (`conversations/show.blade.php`) + AI chat-order (`chat-order/index.blade.php`). Bonus: unifies their currently-inconsistent composers. Nav elsewhere unchanged.
- **Already shipped to code (commit `a807237`, pushed to `feature/push-notification`)**: Option 3 auto-hide behavior — composer focus adds `body.ow-composer-focused`, fades out `#mobile-nav-wrap` (opacity/pointer-events only, Safari-safe), composer shell locally zeroes `--ow-bottom-nav-h`. Pickup Collect button stays visible, shifts with composer. NOT yet browser-tested — Davai E2E test still pending.
- **Design gallery grew to 24 frames** (Cart-solution round added, y=2782): 6 variants answering "where does Cart go in island layouts" — CART-1 Compressed Five, CART-2 Orders Merge, CART-3 Cart Satellite, CART-4 Context Swap (contextual FAB, blue Cart / green Collect), CART-5 Cart in Composer, CART-6 Expandable More. All build on D/G's island language.
- **DECIDED (Jul 24 night): Hakim picked OVERHAUL D — Split Dock (12:1127)** as the final design direction. Cart-tab question still technically open (which CART-1..6 treatment pairs with it) but NOT YET IMPLEMENTED IN CODE — a same-night feature request (Unofficial Vendor) took priority and consumed the rest of the session. **Next session: resume here** — either finalize the Cart pairing then dispatch Zara to implement D on the two chat pages (delivery chat + AI chat-order, on top of the already-shipped Option 3 auto-hide), or ask Hakim if priorities shifted.
- Option 3 auto-hide (commit `a807237`) **still not browser-tested** — carried over, still pending.

---

## Jul 24 night → Jul 25 early morning — Unofficial Vendor + Rider Credit (FULL FEATURE SHIPPED)

### Branch: `feature/s3-r2-storage` (Hakim's explicit choice — a side branch, NOT the preprod deploy branch `feature/push-notification`; synced with latest preprod + pushed before work started, HEAD `8585ed1`)

### The problem
Some real vendors refuse to onboard onto ONDW. **Unofficial Vendor** = admin-created vendor account, indistinguishable to customers. Customer still pays in full online (FIUU/BillPlz: food + delivery fee + platform fee). Since the vendor has no real platform relationship, the **rider pays the vendor cash at the counter** like a walk-up customer — funded by a **Credit** float that admins manually bank-transfer to riders and track in a new ledger.

### Locked business rules (owner-confirmed via AskUserQuestion, do not revisit without him) — SUPERSEDED, see corrections below
1. Credit deducts **food subtotal only** (`total_amount − delivery_fee`) — platform fee NOT deducted, ONDW already keeps that from the customer charge. **Still true.**
2. ~~Negative credit auto-heals from future earnings~~ — **REMOVED Jul 25, see "Debt-direction correction" below.**
3. **Rider accept = vendor accept** — no admin/vendor override needed; rider accepting auto-advances the phantom vendor's accept step. **Still true.**
4. Unofficial vendors are **delivery-only** — self-pickup hidden + server-rejected (nobody could hand off a pickup, vendor never sees the order). **Still true.**
5. Unofficial vendors **fully excluded** from vendor weekly payouts (rider already paid cash, no bank details stored). **Still true.**

### What shipped (initial pass — 10 commits, `ad1192e`..`fae3b2e`, all pushed)
1. **Schema**: `vendor_type` on `vendor_profiles`; new `credit_transactions` ledger (types: topup/food_payment/earnings_refill/reversal/adjustment, signed `amount_sen`, `unique(order_id, type)` for hard idempotency, **no cached balance column** — always `SUM()`, avoids drift).
2. **`CreditService`**: balance/topup/adjust/recordFoodPayment (idempotent)/divertEarningsIfNegative (partial math)/reverseFoodPaymentIfAny. Plus `Vendor::isUnofficial()`, `Order::isUnofficialVendorOrder()/foodSubtotalSen()`.
3. **Checkout guard**: pickup blocked for unofficial vendors, both UI (`customer/checkout.blade.php`) and server (`OrderService::createOrder`).
4. **Rider accept chain**: new `OrderStatusService::systemTransition()` (proper lock/validate/history, not a raw bypass) — `Rider/OrderController::accept` auto-advances unofficial orders straight to `accepted`→auto-`preparing`.
5. **Pickup cash step**: server `recordFoodPayment()` in `pickup()` (try/catch, never blocks — negative allowed); rider-facing cash-confirm modal in `ondw-pickup-gps.js` (all pickup surfaces funnel through it) showing "Pay counter RM X cash · credit RM Y → RM Z", red when going negative. **Chat page needed its own mirrored modal** (`delivery-conversation-realtime.js` has a separate `wireRiderActions()` path, doesn't use `ondw-pickup-gps.js` — forced an `npm run build`, only JS rebuild needed all night).
6. **Diversion + payout exclusion**: diversion runs in `deliver()`'s terminating callback after PERKESO submission; `DisbursementService::pendingBalances` subtracts diverted amounts from rider payout and fully excludes unofficial vendors (`vendor_type='official'` whereExists) from vendor payouts.
7. **Rider UI**: 3rd "Credit" header card on `available.blade.php` (exact sibling of PERKESO/Earnings cards, red when negative, **hidden entirely for riders with an empty ledger**); new `rider.credits` history page; amber "Cash at counter · RM X" chips everywhere a rider sees an order card. **Security note**: `conversationPayload()` is shared with customers — unofficial-vendor fields gated to `Auth::id() === rider.user_id` so customers never see the flag even in dev tools.
8. **Admin UI**: `Admin/UnofficialVendorController` (create vendor, one-time credential flash — "save these now, shown once"; MVP menu management = admin logs into the vendor account directly, no separate admin menu CRUD built); `Admin/RiderCreditController` (balances list negatives-first, per-rider ledger, topup + adjustment forms, adjustment note mandatory for audit trail).
9. **Cancel-after-pickup reversal**: new `ReverseUnofficialFoodPaymentOnCancel` listener on `OrderStatusChanged` (manually registered — `EventServiceProvider` has event discovery OFF) — rider's cash auto-credited back if order cancelled post-pickup. Cancel-before-pickup: no-op. **ONDW absorbs the counter cash on cancel-after-pickup — accepted risk, flagged to Hakim, not a bug.**
10. **Tests + verification**: 19 new tests (`CreditServiceTest` unit, `UnofficialVendorOrderFlowTest` feature — deliberately service-level, sidestepping this env's pre-existing CSRF/302 HTTP-test trap) + full E2E tinker walkthrough of the money flow (vendor→order→accept→pickup→deliver→diversion→cancel-reversal), all inside a rolled-back DB transaction. **Verified independently twice** — once by Davai (agent), once by Yappy directly re-running the suite herself as a manager check. Both got identical **78 failed / 58 passed** (78 = pre-existing unrelated env failures, unchanged; +19 genuinely new passing tests, zero regressions).

### Environment facts discovered this session (save — will bite again otherwise)
- Host only has the **standalone `docker-compose` binary**, not the `docker compose` plugin — every artisan command must be `docker-compose exec app php artisan ...`.
- The local Docker MySQL has **no persistent volume** — it's a fresh schema-only scaffold, never seeded with real data. Confirmed 0 rows before AND after tonight's work; nothing was wiped, there was just never anything there. Real ONDW data lives on the Hostinger preprod/production server, untouched by local Docker work.
- `phpunit.xml` points tests at a **separate** `ondw_testing` database specifically so `RefreshDatabase` can never touch the dev DB — comment in the file confirms this was deliberate.

### Jul 25 — five follow-up hardening passes (all on the same branch, same session continued into the night)

Hakim kept using the feature conceptually after the initial ship and found real gaps by reasoning through concrete numbers with Yappy — this is the value of walking through scenarios out loud, not just shipping and moving on.

1. **Rider eligibility gate** (`7549a6a`) — the initial ship had ZERO restriction on which riders could see/take unofficial-vendor orders (real gap, not hypothetical — confirmed via codebase research before building). New `rider_profiles.can_fulfill_unofficial_orders` boolean + `enabled_by`/`enabled_at` audit trail, admin toggle on the existing rider approval page. Gates 6 touchpoints: `available()`, AJAX polling, `accept()` (defense-in-depth), `show()`, `track()`, badge count — plus the push-notification listener (`SendOrderNotifications`) so ineligible riders don't even get pinged about orders they can't take.

2. **−RM5.00 credit floor** (`1f92c91`) — composes with #1 via `Rider::isEligibleForUnofficialVendors()` (trust flag AND above floor). Blocks accepting **new** unofficial orders once balance ≤ −500 sen; in-flight orders completely unaffected (a real bug was caught and fixed while building this — the eligibility scope would have 404'd a rider's own already-assigned order the moment they crossed the floor mid-delivery).

3. **Photo proof at pickup** (`fafb87e`) — replaced the honor-system "I've paid" tap with a required photo, reusing the app's existing delivery-proof-drawer pattern exactly (same compression, same AJAX upload). New `credit_transactions.proof_photo_path` column. Closes the "rider could just lie about paying" gap.

4. **Debt-direction correction — the important one** (`52312a8`) — Hakim identified via first-principles reasoning (not a bug report, a live Socratic back-and-forth) that the original "negative credit auto-heals from future delivery earnings" design had the debt direction backwards. The rider always fronts real cash first for a customer who already paid ONDW in full — so a negative balance means **ONDW owes the rider**, not the reverse. The old mechanic "repaid" this by withholding the rider's *unrelated, already-earned* delivery pay (traced concretely: a small −RM5 gap self-healed almost invisibly within the same order's own delivery fee, but a −RM45 gap meant ~9-10 completely separate deliveries paid at RM0 before clearing). **Removed entirely** — `divertEarningsIfNegative()` deleted, riders now get paid their full delivery fee unconditionally, every delivery, no exceptions. Negative credit became a plain debt resolvable only by admin topup (as of this commit).

5. **Auto-settlement via payout** (`d7e7ee0`) — Hakim's own follow-up improvement on #4: instead of relying on an admin to remember to top up, fold any owed debt into the rider's next scheduled/manual payout automatically, funded by ONDW as an addition on top of earnings (never subtracted). Works even for riders with zero orders that cycle (settlement-only payout, `order_count=0` — the existing skip-if-zero batch logic needed the calculation itself extended, not the eligibility list). New `disbursements.credit_settlement_sen` column for audit breakdown (earnings vs. debt, per Hakim's explicit ask so Aiman/admins can see why a payout was bigger than that week's deliveries suggest); new `credit_transactions` `auto_settlement` type. Row-locked (mirrors the existing `PerkesoAnnualCap` pattern) to prevent the Friday cron and a manual disburse double-settling the same rider.

### CEO-facing documentation delivered
Built a full scenario-reference document (14 distinct situations, business language not code) as both a published Artifact and a matching PDF for Hakim to send his CEO Aiman — covers every negative-credit scenario, the debt-direction principle, and a live-vs-in-development status table. Republished once already (auto-settlement flipped from "in development" to "Live" the moment `d7e7ee0` landed and was independently verified). Artifact URL: `https://claude.ai/code/artifact/a26e2591-b53e-4ed5-b356-e9ccd3085d63`.

### Full test count as of Jul 25 late night
**55 new tests** across 6 files (`CreditServiceTest`, `UnofficialVendorOrderFlowTest`, `RiderEligibilityGateTest`, `RiderCreditFloorGateTest`, `UnofficialVendorPickupProofTest`, `CreditSettlementDisbursementTest`) — all independently confirmed passing via a filtered run, not just trusted from agent reports. Full suite: **78 failed / 94 passed**. The 78 are 100% pre-existing, unrelated to any of tonight's work (traced one sample failure back to a Dec 2025 Laravel boilerplate scaffold test — `VendorOrderTest::test_example()` hitting `/` expecting 200, gets 302 — never cleaned up, not a regression).

### Leftover/cleanup audit (Jul 25, post-session)
Ran a full sweep after Hakim asked "any leftover from last session?" — genuinely useful habit, do this after any long multi-agent session: git working tree clean + fully pushed, all 62 migrations run with none pending, **zero leftover rows** in any table touched by tonight's tinker/verification work (rollback discipline held, verified by direct query not assumption), Docker containers healthy with no orphans, no stray scratch files inside the actual repo, `php -l` clean across all 44 files touched since the branch's merge-base. Only genuine gap found: **MemoryCore itself was stale** — this file hadn't been updated since the initial 10-commit pass, missing all 5 follow-up hardening commits. Fixed by this edit.

### Genuinely still pending (not done, not glossed over)
- **Real browser/device testing** — everything is verified at code + DB-transaction level, nobody has clicked through the actual UI yet (admin creating a vendor, rider seeing the cash modal or photo-proof drawer live in a browser).
- **Merge decision** — all 15 commits live on `feature/s3-r2-storage` only; not yet merged into `feature/push-notification` (preprod) or `main`. Hakim's call, after browser testing.
- Pre-existing (unrelated) bug flagged, NOT fixed (out of scope): `available.blade.php`'s earnings card never subtracted PERKESO from displayed pending earnings even before tonight.
- **Figma design decision (OVERHAUL D — Split Dock)** from earlier the same evening — picked, 24-frame gallery complete, but NOT YET implemented in code on the two chat pages. This got deprioritized when the Unofficial Vendor feature request came in; resume next session if Hakim wants it.

---

## Jul 26 evening → Jul 27 early morning — R2 Storage Actually Set Up + Domain Migrated to Cloudflare

### The starting problem
The branch is literally named `feature/s3-r2-storage` and the app's whole config (`config/filesystems.php`) was already built for Cloudflare R2 — but R2 had **never actually been set up**. `.env` pointed at a real but placeholder AWS S3 test bucket (`ondewei-test-public`/`ondewei-test-private`, region `ap-southeast-1`, blank `R2_ENDPOINT`) — confirmed via the giveaway that real R2 uses `region=auto`, not an AWS region code. Root cause of "forgot to add R2 credentials": the buckets themselves didn't exist yet, not just missing env values.

### 🟢 CRITICAL SECURITY ISSUE — FOUND AND FIXED SAME SESSION
Hakim mistakenly attached the custom domain to **`ondewei-private`** instead of `ondewei-public` — a custom domain on the private bucket exposes the entire bucket publicly (Cloudflare's own documented R2 behavior, also explicitly warned about in this app's `.env.example` comments), and that bucket holds rider IC/license documents, delivery/pickup proof photos, and chat attachments. Caught and fixed same session: domain removed from `ondewei-private` (confirmed empty), correctly reattached to `ondewei-public` (confirmed Active). Exposure window was short, domain was brand new/unindexed/never linked publicly — real-world risk assessed as low, but flagging the history here in case it's ever relevant. **Lesson for next time**: always double-check which bucket a custom domain lands on before moving to the next step — the R2 UI doesn't strongly warn you if you pick the wrong one.

### Domain migration: `ondewei.my` moved from Exabyte/Hostinger DNS to Cloudflare
Domain registration stayed at Exabyte (registrar unchanged) — only DNS management moved to Cloudflare (nameservers `bart.ns.cloudflare.com` / `savanna.ns.cloudflare.com`). Real DNS content was actually being served by **Hostinger**, not Exabyte, despite Exabyte being the registrar — confirmed because Cloudflare's live scan matched Hostinger's hPanel DNS records exactly, not Exabyte's (which turned out to be a stale/legacy zone with old `byet.org` nameservers, a different IP, and a broken self-referential MX — safe to ignore).

**Two near-misses caught before flipping nameservers** (both would have caused real outages):
1. Cloudflare's auto-scan defaulted 5 mail-related CNAMEs (`autoconfig`, `autodiscover`, 3× `hostingermail-*._domainkey` DKIM records) to **Proxied** — these are looked up by mail servers/clients directly, not browsers; proxying them would have broken DKIM verification and mail autodiscovery. Fixed to **DNS only** before cutover.
2. `preprod.ondewei.my` was **completely missing** from Cloudflare's auto-scan — it exists in Hostinger's real panel as an `ALIAS` record (`preprod → preprod.ondewei.my.cdn.hstgr.net`) that the scanner simply didn't pick up. Added manually as a CNAME (set to DNS only, since it's an active staging environment that shouldn't be cached) before switching nameservers — without this, the entire preprod deploy target would have gone dark (NXDOMAIN) the moment nameservers changed.

DNSSEC was checked and confirmed never enabled at Exabyte — non-issue. Nameservers switched, zone went Active (took a few hours to fully propagate; WHOIS/registry updated near-instantly but individual resolvers lagged behind, which is normal).

### 🔴 MAJOR GOTCHA — `.env` is NOT what this app's Docker setup actually reads
Spent real debugging time on this: `.env` was edited correctly multiple times (R2 keys, endpoint, region=auto, public URL) and `config:clear`/`cache:clear` were run — but Laravel kept resolving stale values. Root cause: **`docker-compose.yml`'s `app` service uses `env_file: .env.docker`**, a completely separate file. Docker bakes `env_file` values into the container's real OS environment **at container startup** — and Laravel's dotenv loader never overrides variables already present in the real environment. Two consequences to remember:
1. **Any future env change for local dev must go into `.env.docker`, not `.env`.**
2. Editing `.env.docker` alone isn't enough either — since values are baked in at startup, the container needs a full recreate: `docker-compose up -d --force-recreate app` (a restart may not be sufficient; recreate is what worked).

### R2 architecture — confirmed, worth remembering exactly
Two completely different upload+view patterns exist, and they're intentionally mirror images of each other based on public vs. private:
- **Public files (avatars, menu images)**: upload goes **browser → Laravel server → server writes to R2** (traditional multipart upload, no CORS involved ever). Viewing does a 301 redirect straight to the public custom domain (`assets.ondewei.my`) — no server involvement in serving the actual bytes.
- **Private files (rider docs, delivery/pickup proofs, chat attachments)**: upload goes **browser → R2 directly**, via a presigned PUT URL from `PresignedUploadController::generate()` (`Storage::disk('r2-private')->temporaryUploadUrl()`, 15-min TTL) — bypasses the server entirely for the actual bytes, which is exactly why this needed CORS configured on the bucket (R2 has none by default). Viewing is proxied through routes like `/storage/rider-documents/{id}` — the server fetches from R2 server-side and streams it back, because there's no public URL to redirect to (private bucket has no custom domain by design) and because an authorization check has to happen before the file is served.
- **CORS fix applied**: added a policy to `ondewei-private` only (public bucket doesn't need one — `<img>` tag loads aren't subject to CORS at all, and public uploads don't use presigned URLs):
  ```json
  [{"AllowedOrigins": ["http://localhost", "https://preprod.ondewei.my", "https://ondewei.my"], "AllowedMethods": ["PUT","GET","HEAD"], "AllowedHeaders": ["*"], "MaxAgeSeconds": 3600}]
  ```

### `storage:migrate-to-r2` artisan command (pre-existing, not written this session)
Copies (not moves — originals untouched) local files to R2 across 6 scopes (menu-items, avatars → `r2`; delivery_proofs, pickup-proofs, rider_documents, conversation_attachments → `r2-private`). Resumable via a progress JSON file, supports `--dry-run`. **Only migrates files on whatever server it's run on** — needs to run via SSH directly on the Hostinger production server (with that server's own real `.env` populated with R2 creds — no `.env.docker` complexity there since Hostinger doesn't use Docker) to actually migrate the real production files. Not yet run against production.

### R2 confirmed fully working end-to-end on local — 27 Jul 2026
Avatar (public) and rider-document (private) upload + view both verified working live in browser after the DNS-resolver switch and the custom-domain fix. Session closed with two artifacts: an updated QA checklist (`https://claude.ai/code/artifact/a23f70b5-5c80-4206-a003-d93f1d1f3bf3`, now includes a gotchas callout at the top) and a new architecture diagram (`https://claude.ai/code/artifact/ff1e0c29-f686-49be-8671-2043a390c8d2`) showing exactly why public vs private files take mirror-image upload/view paths.

### 🔴 GOTCHA — `php artisan test` wipes the local dev database (27 Jul 2026)
`phpunit.xml` explicitly configures a separate `DB_DATABASE=ondw_testing` specifically so `RefreshDatabase` "never wipes a dev database" (its own comment says so) — but in practice, running `php artisan test` (both filtered and full-suite) wiped the real local dev DB twice in the same session. Root cause traced to the same env_file-baked-at-container-startup gotcha already documented above: `docker-compose exec app printenv` showed the container's REAL live `DB_DATABASE` as `if0_38066807_ondewei` (Hakim confirmed this is just his local dev DB, not real production data — despite the alarming name match to the `.gitignore`-flagged production dump filename), not `ondewei_local` like the current `.env.docker` file on disk claims. phpunit.xml's `ondw_testing` override apparently doesn't hold against whatever's actually causing this mismatch, so the test run's database refresh lands on the real running dev database instead of the intended isolated one.
**Fix needed (not done yet)**: figure out why phpunit's env override isn't taking effect — likely needs the container force-recreated (`docker-compose up -d --force-recreate app`) so its baked env matches current `.env.docker`, then re-verify `php artisan test` actually targets `ondw_testing` afterward. Until fixed: **assume any `php artisan test` run will wipe local dev data** — reseed after via `php artisan db:seed` (full seeder chain: `DeliveryLocationsSeeder`, `UserSeeder`, `MenuSeeder`, `OrderSeeder` — restores 19 users/5 riders/10 orders/3 vendors). Caught this immediately both times by checking `docker ps` uptime (container never restarted, so data loss wasn't from a volume reset) and `php artisan migrate:status` (every migration showing the same batch number confirms a full fresh rebuild happened).

### 11-item rider-side punch list, all shipped (27-28 Jul 2026)
Hakim's list had two "6"s and two "7"s — renumbered into 11 distinct items, researched with 3 parallel Explore agents + 1 Plan agent before touching code, then implemented in 7 commits on `feature/s3-r2-storage` (not yet pushed to preprod as of this note):
1. Rider nav "Order food" → "Hungry?" (`d1898d7`)
2. Star badge for unofficial-vendor-eligible riders in admin lists + stricter push-notification filter (`d1898d7`) — the push filter turned out to already be correctly scoped, just used the weaker of two eligibility checks
3. Boxed-background removed from rider Pickup/Cash-at-counter block + quick-reply pills hidden for riders (`efebc3a`) — same anti-pattern already fixed once on the composer (`213220d`), just never applied to these sibling blocks
4. Rider delivery-chat page brought to Split Dock parity with customer (4-tab pill + detached Chat island) (`9da236f`)
5. R2 orphan-file fixes: delivery-proof and pickup-proof photos weren't deleting the old file on retry/resubmit (avatar/menu-item uploads already did this correctly) (`fe82637`)
6. Unofficial vendor creation now redirects straight to the hours-setup page instead of the vendor index — confirmed a new vendor is genuinely invisible/unorderable (`is_online=false`, no `business_hours`) until hours are set, not just a nice-to-have (`250e746`)
7. **Real bug found**: `OrderStatusService::handleAutoTransitions()` mutates the shared `$order` object to `'preparing'` and fires its own event BEFORE the caller's own event dispatch reads the status — so `'accepted'`-flavored notifications never fired correctly anywhere in the app (official-vendor accept included, not just unofficial), and `'preparing'` fired twice. Fixed by dispatching before `handleAutoTransitions()` in both `updateStatus()`/`systemTransition()`. Added Accept-button spinner/disable too (`73cf91e`)
8. **Real bug found**: 9 routes (`profile.update`, `upload.presigned`, both customer status polls, `rider.orders.deliver`, `rider.orders.status`, all 3 `conversations.*` routes) shared ONE rate-limit counter because Laravel's raw `throttle:N,1` keys by user-id alone, not per-route. Delivery chat's background polling (~50-60/min) silently exhausted the shared bucket before a rider even took their delivery photo — this was the exact cause of the live `429` on order #181. Fixed with named `RateLimiter::for()` closures giving each route its own bucket (same numeric limits, just isolated). Proved it with a real before/after repro: reverted to old syntax → 429 reproduced; restored fix → 200 (`e03d1c3`)

Every fix verified live (Playwright screenshots/measurements for UI, real HTTP repro + targeted test runs for the two bugs) before committing — not just code review.

QA checklist artifact for this batch: `https://claude.ai/code/artifact/bf46225b-1b13-414e-a8e3-4ad76a2801f2` (interactive, localStorage-persisted, per the QA Checklist Artifact Protocol).

### 🔴 GOTCHA — `php artisan test` wipes the local dev database, recurs even without running tests
Happened 3 times in one session (documented above), including once with no `php artisan test` in between at all — just `php -l`/`route:clear`/`route:list`/tinker commands. Root cause not fully pinned down beyond the known env_file-baked-at-startup mismatch (`if0_38066807_ondewei` vs `.env.docker`'s `ondewei_local`) — something is periodically triggering a fresh migration/reseed-worthy wipe on this exact local setup, more often than just "when tests run." Reseed via `php artisan db:seed` restores it (19 users/5 riders/10 orders/3 vendors) — confirmed safe to do freely, Hakim confirmed this DB is just local dev data, not anything sensitive.

### Still pending from this session
- Push this 7-commit batch to preprod when Hakim asks (same pattern as always — merge `feature/s3-r2-storage` into `feature/push-notification`).
- Actually root-cause (not just work around) the recurring DB-wipe gotcha above.
- Fix the `php artisan test` DB-wipe gotcha above — currently just working around it by reseeding after every test run.
- Hakim confirmed preprod pulled + running fine (27 Jul 2026, after the Profile-nav + earlier composer/PHP-8.3 + gitignore fixes all shipped to `feature/push-notification`, latest `bb98ec1`).
- Run `storage:migrate-to-r2 --dry-run` then for real on the actual Hostinger production server once its `.env` has real R2 credentials (no `.env.docker` complexity there — Hostinger doesn't use Docker).
- Finish the rest of the QA checklist (Section A remaining items, all of Section B — the actual Unofficial Vendor + Credit flow has still never been clicked through live).
- Confirm on preprod/prod later: same `.env` vs `.env.docker`-style gotcha shouldn't exist there (no Docker), but worth a sanity check that R2 env vars are actually present before assuming they work.

### `ERR_NAME_NOT_RESOLVED` on `assets.ondewei.my` — expected propagation lag, not a real bug (27 Jul 2026)
Hakim reported avatar upload/upload confirmed present in `ondewei-public` bucket, but browser threw `ERR_NAME_NOT_RESOLVED` loading it from `assets.ondewei.my`. Rider-doc (private, server-proxied) path confirmed working fine at the same time — that alone narrows it to the public redirect path specifically, since that's the only R2 path where the *client's own DNS* resolves the hostname directly (private files never touch `assets.ondewei.my` at all).

Diagnosed directly: `dig assets.ondewei.my` against the sandbox's default resolver returned nothing (SOA still showed `ns1.dns-parking.com`), but the exact same query against `1.1.1.1` and `8.8.8.8` directly resolved correctly to Cloudflare's anycast IPs. Zone/custom-domain config on Cloudflare's side is confirmed correct — this is a resolver that hasn't picked up the nameserver delegation change yet, consistent with what's already documented above ("WHOIS/registry updated near-instantly but individual resolvers lagged behind, which is normal"). Not a bucket, upload, or R2-config problem.
**Fix**: nothing to fix — resolves itself as caches expire (typically within a few hours, up to ~24-48h worst case for stubborn ISP resolvers). If Hakim wants to confirm it's *only* propagation and not something else: point his device's DNS at `1.1.1.1` temporarily, or just retry the same image URL again later today.

---

## Jul 27 morning — Split Dock live-built, BillPlz local creds fixed, preprod deployed twice, critical `.gitignore` bug found

### Split Dock (OVERHAUL D) implemented for real
Picked up the Figma decision from Jul 24 night and actually built it — 6 commits (`d4f8bf1` through `78c3839`) on `feature/s3-r2-storage`, on top of the same two pages as the earlier auto-hide work: `conversations/show.blade.php` (delivery chat) + `chat-order/index.blade.php` (AI order chat).
- Chat pulled out of the 5-tab pill into its own detached 56px circular island; remaining 4 tabs (Search/Cart/Orders/Profile) reused verbatim from the existing nav — no new icons/routes invented.
- Capsule composer (rounded-full, matching nav's glass tokens exactly).
- New: manual tap-toggle on the Chat island to fully collapse/expand the composer (additive to the existing focus-based auto-hide, not a replacement — confirmed by Hakim explicitly). `body.ow-composer-collapsed` class + `display:none` (genuinely non-interactable, not just faded).
- **5 real bugs found + fixed via live testing, in order**: (1) leftover white card-wrap on delivery-chat composer — same "card behind pill" anti-pattern already fixed once before for the other page, just never carried over; (2) blue background falling short of viewport on keyboard-open (`100vh` doesn't track keyboard, switched to `100dvh`); (3) Chat island moved from left to right per Hakim's request (now beside Profile); (4) same bg gap persisting in the NON-focused idle state too (`h-full` added, still insufficient); (5) **the actual root cause of the bg gap, proven with a real headless-browser screenshot + `getBoundingClientRect()` measurements** — `h-full` resolves against the parent's content-box, excluding the parent's own `pb-28` padding (reserved exactly where the nav sits) — fixed by putting the blue directly on `<body>` for this route instead of fighting the height chain a third time. Also a separate composer-overlapping-nav bug on chat-order specifically (zero bottom-padding buffer, unlike its sibling — brought in line with the established safe-area convention).
- **Lesson**: after 2 "should be fixed now" claims that weren't, the 3rd attempt was required to get real visual proof (actual rendered screenshot + measured box heights) before being trusted — pure code-reasoning had already failed twice on this exact bug. Worth demanding this proof bar earlier next time a background/layout bug survives one fix attempt.

### BillPlz local sandbox creds — same `.env.docker` gotcha, twice more
Checkout was failing locally with `collection_id: ""` → 401. Root cause identical to the R2 gotcha two nights ago: `.env.docker` was **completely missing** `BILLPLZ_*`, `FIUU_*` (the actual default gateway!), `OPENAI_API_KEY`, and `PERKESO_*` — not just wrong values, just absent. Fixed by diffing `.env` vs `.env.docker` var names directly (`diff <(grep -oE ... .env) <(grep -oE ... .env.docker)`) and syncing everything at once rather than waiting for each one to bite separately. Second round: the BillPlz secret key itself was stale/wrong even with correct env-loading — confirmed by curling BillPlz's sandbox API directly with the configured key (bypassing Laravel entirely) before touching any code, proving it was a credentials problem, not a code bug. Hakim rotated the key + collection ID in the BillPlz dashboard; re-verified via the same direct curl before declaring it fixed.

### 🔴 Critical, long-standing bug found: `public/build` was gitignored
`.gitignore` had Laravel's **stock default** `/public/build` exclusion (assumes server-side/CI build, which this Hostinger-shared-hosting deploy has never had). `manifest.json` was tracked and updated correctly on every rebuild, but the actual hashed `.js`/`.css` files it pointed to were silently git-ignored — so preprod would 404 on `app-*.js`/`app-*.css` every time the main bundle got a new content hash, going all the way back to whenever this `.gitignore` line was added (not something introduced this session — just finally surfaced when Hakim pulled to preprod and hit it live). Fixed: removed the `/public/build` line, committed the two files that were actually missing at time of discovery (`app-CmuJS765.js`, `app-BqGFzx0w.css`), pushed to both branches. **This should not recur** now that the directory is properly tracked — but worth double-checking after any future `npm run build` that the new hashed files actually show up in `git status` before pushing, as a habit.

### Preprod deployed twice this session
`feature/s3-r2-storage` → `feature/push-notification`, both times a clean fast-forward merge (no conflicts): first at 22 commits (the whole Unofficial Vendor + Credit + R2 + admin-nav body of work), second at +6 more (Split Dock + the gitignore fix). Both pushed to GitHub. **Important distinction Hakim needs to keep acting on**: pushing to GitHub ≠ live on the server — Hostinger needs an actual `git pull` (manual, no auto-deploy hook known) plus `php artisan migrate` for the first batch's 6 new migrations. Not yet confirmed whether Hakim has actually pulled+migrated on the real server as of this save — check next session.

### Admin nav redesign also shipped (not yet mentioned above)
Separate from Split Dock — desktop admin bar regrouped from 9 flat items into 4 standalone (Dashboard/Orders/Disbursements/Users) + 3 dropdowns (Rider Management, Vendor Management, System Tools); mobile bottom bar cut 5→4 tabs; FAB rebuilt into an accordion speed-dial; the orphaned "More" panel and dead hamburger entries removed entirely. One real gap owned by Yappy (not the builder): **Reports never made it into the new structure** — was in the old dead panel, got dropped when the plan was written, not yet resolved with Hakim on where it should live now.

### Genuinely still pending
- **Confirm Reports' new home** in the admin nav (flagged to Hakim, no answer yet as of this save).
- **Confirm preprod server actually pulled + migrated** — GitHub is updated, unclear if Hostinger itself is caught up.
- `storage:migrate-to-r2` still not run against real production data.
- Full QA checklist Section B (Credit flow) still never fully clicked through live end-to-end.

---

## Jul 29 evening — Credit balance display fix (post-live-QA of Unofficial Vendor + Credit)

Hakim clicked through the full Credit + Unofficial Vendor flow live end-to-end for the first time (closes the Section B QA gap above) and reported: "Earnings bug not tally with payout." Real bug was purely a DISPLAY problem, not a money problem — confirmed by reading `DisbursementService::pendingBalances()`/`settleCreditIfIncluded()` directly first: the actual bank payout already correctly folds negative credit balance into the real BillPlz PO amount (Hakim's own point #1 confirmed this). The gap: riders/admins saw a scary raw negative ledger number with no clear "already handled" framing, and the Earnings page's "Pending Payout" total was already correct but never broke down *why* it was bigger than plain delivery earnings.

**Fix, commit `867686c`, `feature/push-notification`** (7 files):
- `CreditService::displayBalanceSenFor()` / `pendingSettlementSenFor()` — two new PURE DISPLAY-ONLY derived methods (`max(0, balance)` / `abs(min(0, balance))`). Deliberately did NOT touch `balanceSenFor()` itself — that's what drives the real −RM5 floor gate and the real disbursement settlement math, both of which must never see a fake-zeroed balance or the floor gate stops gating and the real payout stops topping up.
- Wired into `Rider\CreditController`, `Admin\RiderCreditController` (both `index()` and `show()`), and 4 blade views (`rider/credits/index`, `admin/rider-credits/index`, `admin/rider-credits/show`, `rider/earnings/index`) — balance never shows negative anymore, replaced with a non-alarming "pending payout, folded into next payout automatically" callout in both rider and admin views. Rider Earnings page now shows an explicit delivery-earnings + credit-settlement = total breakdown instead of one unexplained lump sum.
- **Verified before committing**: 35/35 tests passing across `CreditServiceTest`, `RiderCreditFloorGateTest`, `CreditSettlementDisbursementTest`, `UnofficialVendorOrderFlowTest` — specifically re-ran the floor-gate and settlement suites as the two things most at risk of a silent regression, both fully green, confirming the real (non-display) balance logic is provably unchanged.
- Tests must run via `docker exec ondw-app php artisan test ...` — running from the host hits the known `.env`-points-to-`mysql`-hostname gotcha (`getaddrinfo for mysql failed`), not a real failure. Reseeded (`db:seed`) after, per the known test-wipes-local-DB gotcha.
