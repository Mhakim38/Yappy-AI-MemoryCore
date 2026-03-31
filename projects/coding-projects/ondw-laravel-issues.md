# ONDW (On De Wei) Laravel Project - Known Issues & Notes

## Project Details
- **Project Name**: ONDEWEI-LARAVEL-HAKIM
- **Type**: Laravel + PHP Application
- **Repository**: `/Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM/`

## Issue #1: Service Worker Cache Problem (CRITICAL)
**Status**: `PENDING_FIX` (waiting for environment setup)  
**Last Updated**: 2026-03-31 07:45 (Malaysia Time)

### Problem
The service worker file (`/public/sw.js`) has **all code commented out** (lines 1-73 entirely disabled).

### Root Cause
When uncommented, the service worker was causing issues during **login/logout cycles**:
- Sometimes returned **HTTP 500 errors**
- Sometimes returned **"Access Denied" errors**
- Related to caching - likely stale content being served from cache after auth state changed

### Why It Was Commented
To temporarily disable service worker while debugging the auth issues. The comment-out was a workaround, not a permanent solution.

### Why We Need It Now
Push notifications for PWA require a functional service worker to handle push events and display notifications. We can't implement push notifications on ONDW without a working SW.

### Next Steps (When Environment Ready)
1. Set up PHP environment and MySQL on this Mac
2. Run ONDW locally to test
3. Uncomment the service worker code in `/public/sw.js`
4. Debug the login/logout 500 error issue
5. Implement proper cache invalidation strategy:
   - Serve auth state from network (don't cache)
   - Cache only static assets (CSS, JS, images)
   - Implement cache versioning/busting
   - Add auth header checks to cache decisions
6. Once stable, implement push notification support

### Key Files Involved
- `/public/sw.js` - Currently disabled service worker
- Laravel session/auth middleware
- Any cache-related configuration

### Technical Notes
- The push notification pattern we just created will work perfectly once the SW is fixed
- We have comprehensive PWA push notification documentation saved in Yappy library
- This is a Laravel-specific issue (mixing PWA caching with Laravel's session-based auth)

---

**Reminder**: Don't modify ONDW code until PHP/MySQL environment is fully set up on this Mac!
