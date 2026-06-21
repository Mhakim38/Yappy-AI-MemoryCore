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
1. Run `php artisan migrate` on preprod (`last_error` column + AI chat table)
2. Set preprod `.env`: `PAYMENT_GATEWAY_ENABLED=true`, `CHAT_ORDER_AI_ENABLED=false`
3. PERKESO pending root cause investigation
4. E2E test: checkout → BillPlz → webhook → rider pickup (GPS) → deliver (GPS + photo) → confirm PERKESO fires
5. Clear test order data from PROD
6. Email BillPlz for e-wallet activation (SSM + KYC)
7. CEO confirmation: "Terima Order" call button — rider or customer?
8. Merge `feature/push-notification` → `main`
