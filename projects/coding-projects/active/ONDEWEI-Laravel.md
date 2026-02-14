# ONDEWEI-Laravel
*Coding Project - Created February 14, 2026*

## Description
Laravel 10 food delivery platform with multi-role order management system. Features customer ordering, vendor menu management, rider delivery tracking, and admin oversight with real-time order status transitions and notification system.

## Project Details
- **Type**: Coding Project
- **Status**: Active
- **Created**: February 14, 2026 7:35 PM
- **Last Accessed**: February 14, 2026 7:35 PM
- **Position**: #1
- **Location**: C:\Users\Admin\holeeWater\ONDEWEI-LARAVEL-HAKIM

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
- [ ] Fix authorization mismatch between OrderControllers and OrderStatusService
- [ ] Replace non-existent \UnauthorizedException with proper Laravel exception
- [ ] Implement ready_for_pickup transition trigger (vendor action or timer)
- [ ] Secure or remove debug routes (/check-user, /admin-test, /create-admin-profile)
- [ ] Add comprehensive order state machine tests

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
*Yappy AI Project Entry - Evening Analysis Session*
