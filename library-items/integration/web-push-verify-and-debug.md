# Web Push: verify, debug and "targeted push" pitfalls (Laravel + minishlink/web-push + PWA)

Proven Oct 14, 2026 (food-delivery PWA): rider-message push to a customer, tapped banner opens the exact chat. Sanitised: no keys, endpoints or user data.

## 1. Split every "push didn't show" into three hops and test each alone
1. **Our server -> push service.** Send from `php artisan tinker` and PRINT the real `MessageSentReport`:
   `isSuccess()`, `isSubscriptionExpired()`, `getResponse()?->getStatusCode()`, `getReason()`, and `parse_url($endpoint, PHP_URL_HOST)` (host only, never the endpoint).
   - `201` from `web.push.apple.com` / FCM = the push service accepted it. Server, VAPID keys, payload and subscription are fine.
   - `403/400` (BadJwtToken etc.) = VAPID subject/key setup. `404/410` / `isSubscriptionExpired` = dead subscription, must re-subscribe.
2. **Push service -> device.** A 201 does NOT mean a banner. iOS: installed Home Screen app only, per-app notification permission, Focus, Scheduled Summary, low power. Prove the chain on a second device (Mac Safari/Chrome) with the same command: banner there = server + service worker are good, remaining issue is that device's settings/install.
3. **Service worker -> screen -> tap.** `push` handler must call `showNotification` inside `event.waitUntil` (iOS drops silent pushes). `notificationclick` must open only same-origin URLs (`new URL(url, location.origin)` check), focus an existing window or `clients.openWindow`.

## 2. Don't trust a green "sent to N devices" toast
An admin "send to user" button that counts `$sent++` whenever no exception is thrown reports success even when the push service refused it. Count only `report->isSuccess()`, log non-expired failures with status + reason, and return honest results ("0 delivered, subscription expired"). One shared send service for every caller; a second hand-copied sender drifts.

## 3. Subscriptions are per (user, endpoint), not per account-on-device
- Unique key (user_id, endpoint) lets ONE phone be stored under many accounts (each account that tapped "allow" on that device). A push for any of them lands on the same phone.
- Logout does not remove the row unless you do it: user A's pushes keep arriving after user B logs in on a shared phone (privacy). Fix: unsubscribe on logout and/or re-bind the endpoint to the logged-in user at subscribe time.
- To see who is linked: tinker listing `id, user_id, user_agent, created_at` (UA shows iPhone vs Macintosh vs Android).

## 4. Rider-message style push (generic text, deep link)
- Payload is a constant title/body (never the message text on a lock screen), `url` = the chat route, `tag` = `chat-<conversation id>` with `renotify` so a burst replaces itself.
- Gates: feature flag (default off), current sender is the order's current rider, recipient has a subscription, recipient is NOT currently viewing the chat (short cache "presence" key + last_read_at), burst throttle (`Cache::add`, ~4 min), urgent messages (photo / "arrived") bypass the burst throttle.
- Queue it (job) so a slow push service never blocks the chat POST; on shared hosting without workers the cron-run `queue:work` still fired within seconds.

## 5. Live tap-test recipe (needs the human's device)
1. Confirm the target account has a subscription row whose user-agent matches the test device.
2. Device: logged in, notifications allowed, chat page CLOSED (open chat suppresses the push on purpose), screen locked.
3. Send exactly ONE message from the sender account, note the exact MYT time, tell the human.
4. Human reports: banner time, text, where the tap opened (chat route vs home vs login).
5. Then 3 more messages (expect no extra push), then one urgent message (expect a push).
Staff rule: the tester sends nothing more until the human reports; close browsers after.
