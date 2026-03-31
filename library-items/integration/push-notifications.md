# PWA Push Notifications Pattern
**Level**: 2 (Production-Proven)  
**Source**: Wedding Wall (Next.js) + Push Notification Test (Node.js)  
**Status**: Active & Maintained  
**Date Added**: March 31, 2026

---

## Problem Statement
Modern PWAs need to notify users about important events (new photos, activity, reminders) across multiple devices. Users expect:
- Real-time notifications on iOS and Android
- Notifications even when app is closed
- Works offline-first PWA experience
- HTTPS support for security

---

## Solution Overview
Complete push notification system using Web Push API + Service Worker. Provides:
- VAPID key authentication (proves server identity)
- Push subscription management per device
- Service Worker to receive and display notifications
- Works on iOS, Android, and web browsers
- Production-ready for Vercel, Netlify, or traditional servers

---

## Implementation

### 1. Install Dependencies
```bash
npm install web-push
npm install --save-dev @types/web-push
```

### 2. Service Worker with Push Support (`public/service-worker.js`)
```javascript
// Push event handler
self.addEventListener('push', (event) => {
  console.log('[Service Worker] Push notification received');

  let notificationData = {
    title: 'App Name',
    body: 'You have a new notification!',
    icon: '/favicon-192x192.png',
  };

  if (event.data) {
    try {
      notificationData = event.data.json();
    } catch (e) {
      notificationData.body = event.data.text();
    }
  }

  const options = {
    body: notificationData.body,
    icon: notificationData.icon || '/favicon-192x192.png',
    badge: notificationData.badge || '/favicon-192x192.png',
    vibrate: [200, 100, 200],
    tag: 'app-notification',
    requireInteraction: false,
    data: {
      url: notificationData.url || '/',
      timestamp: Date.now(),
    },
  };

  event.waitUntil(
    self.registration.showNotification(notificationData.title, options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  const urlToOpen = event.notification.data?.url || '/';

  event.waitUntil(
    clients
      .matchAll({ type: 'window', includeUncontrolled: true })
      .then((clientList) => {
        for (let i = 0; i < clientList.length; i++) {
          const client = clientList[i];
          if (client.url === urlToOpen && 'focus' in client) {
            return client.focus();
          }
        }
        if (clients.openWindow) {
          return clients.openWindow(urlToOpen);
        }
      })
  );
});
```

### 3. Push Notification Utilities (`lib/push-notifications.ts`)
```typescript
import webpush from 'web-push';

// Get VAPID keys from environment variables
export function getVapidKeys() {
  const publicKey = process.env.VAPID_PUBLIC_KEY;
  const privateKey = process.env.VAPID_PRIVATE_KEY;

  if (publicKey && privateKey) {
    return { publicKey, privateKey };
  }

  if (process.env.NODE_ENV !== 'production') {
    const vapidKeys = webpush.generateVAPIDKeys();
    console.log('Generated temporary keys for development');
    return vapidKeys;
  }

  throw new Error('VAPID keys not configured');
}

export function configureWebPush() {
  const vapidKeys = getVapidKeys();
  
  webpush.setVapidDetails(
    `mailto:${process.env.ADMIN_EMAIL || 'admin@example.com'}`,
    vapidKeys.publicKey,
    vapidKeys.privateKey
  );

  return vapidKeys;
}

export interface PushSubscription {
  endpoint: string;
  expirationTime?: number | null;
  keys: {
    p256dh: string;
    auth: string;
  };
}

export async function sendPushNotification(
  subscription: PushSubscription,
  payload: {
    title: string;
    body: string;
    icon?: string;
    url?: string;
  }
) {
  configureWebPush();

  const notificationPayload = JSON.stringify(payload);

  try {
    await webpush.sendNotification(subscription, notificationPayload);
    return { success: true };
  } catch (error: any) {
    if (error.statusCode === 410) {
      return { success: false, error: 'Subscription expired', statusCode: 410 };
    }
    return { success: false, error: error.message };
  }
}
```

### 4. API Routes

**GET `/api/push/vapid` - Return public VAPID key:**
```typescript
import { NextResponse } from 'next/server';
import { getVapidKeys } from '@/lib/push-notifications';

export async function GET() {
  try {
    const vapidKeys = getVapidKeys();
    return NextResponse.json({ publicKey: vapidKeys.publicKey });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get VAPID key' },
      { status: 500 }
    );
  }
}
```

**POST `/api/push/subscribe` - Save subscription:**
```typescript
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const subscription = await request.json();
    
    // Save to database (example with Prisma):
    // await prisma.pushSubscription.create({
    //   data: {
    //     endpoint: subscription.endpoint,
    //     p256dh: subscription.keys.p256dh,
    //     auth: subscription.keys.auth,
    //   },
    // });

    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to save subscription' },
      { status: 500 }
    );
  }
}
```

**POST `/api/push/send` - Send notification:**
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { sendPushNotification } from '@/lib/push-notifications';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { subscription, title, message } = body;

    const result = await sendPushNotification(subscription, {
      title,
      body: message,
    });

    if (result.success) {
      return NextResponse.json({ success: true });
    } else {
      return NextResponse.json(
        { error: result.error },
        { status: result.statusCode || 500 }
      );
    }
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to send notification' },
      { status: 500 }
    );
  }
}
```

### 5. Frontend Component (`components/PushNotificationTest.tsx`)
```typescript
'use client';

import { useState, useEffect } from 'react';

export function PushNotificationTest() {
  const [subscription, setSubscription] = useState<any>(null);
  const [status, setStatus] = useState('Checking support...');

  useEffect(() => {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
      setStatus('Ready to enable notifications');
    }
  }, []);

  function urlBase64ToUint8Array(base64String: string) {
    const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  async function enableNotifications() {
    try {
      setStatus('Requesting permission...');
      
      const permission = await Notification.requestPermission();
      if (permission !== 'granted') {
        setStatus('Permission denied');
        return;
      }

      const vapidResponse = await fetch('/api/push/vapid');
      const { publicKey } = await vapidResponse.json();

      const registration = await navigator.serviceWorker.ready;
      const sub = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(publicKey),
      });

      await fetch('/api/push/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sub),
      });

      setSubscription(sub);
      setStatus('✅ Notifications enabled!');
    } catch (error) {
      setStatus('❌ Error: ' + (error as Error).message);
    }
  }

  async function sendTestNotification() {
    if (!subscription) return;

    try {
      await fetch('/api/push/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          subscription,
          title: 'Test Notification',
          message: 'It works!',
        }),
      });

      setStatus('✅ Notification sent!');
    } catch (error) {
      setStatus('❌ Failed to send');
    }
  }

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h3 className="font-semibold mb-2">🔔 Push Notifications</h3>
      <p className="text-sm text-gray-600 mb-3">{status}</p>
      
      <div className="space-y-2">
        {!subscription && (
          <button
            onClick={enableNotifications}
            className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
          >
            Enable Notifications
          </button>
        )}
        
        {subscription && (
          <button
            onClick={sendTestNotification}
            className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600"
          >
            Send Test Notification
          </button>
        )}
      </div>
    </div>
  );
}
```

### 6. Environment Variables Setup

**Local Development (.env.local):**
```env
VAPID_PUBLIC_KEY=BC0k_B6fYUciuSD2h0fm6CKoLAoS3s8vrCDOeFYO39E9LMl0FiEy-eoPBplV35xCWpirQdahUVgKuWwj8pfrV94
VAPID_PRIVATE_KEY=QBP0GW73ZpID1XGx_evEYvPiLr_Mrbb29Km1R4NwnXk
```

**Generate New Keys:**
```bash
node -e "const wp = require('web-push'); const keys = wp.generateVAPIDKeys(); console.log('PUBLIC:', keys.publicKey); console.log('PRIVATE:', keys.privateKey);"
```

**Vercel Deployment:**
1. Go to Vercel Dashboard → Project Settings → Environment Variables
2. Add `VAPID_PUBLIC_KEY` and `VAPID_PRIVATE_KEY`
3. Select all environments (Production, Preview, Development)
4. Redeploy

---

## Adaptation Guide

### For Next.js (App Router)
✅ Directly use the code above in `app/` directory

### For React + Express
Adapt the API routes to Express endpoints:
```javascript
app.get('/api/push/vapid', (req, res) => {
  res.json({ publicKey: vapidKeys.publicKey });
});
```

### For Svelte/Vue
Replace the component with equivalent framework syntax, same API calls

### For Static Hosting (Netlify, Vercel)
- Use serverless functions for API routes
- Store VAPID keys in environment variables
- Cannot use file system (read-only)

---

## Real Use Cases

### Photo Upload Notification
```typescript
// In your upload endpoint
await sendPushNotification(subscription, {
  title: '📸 New Photo!',
  body: `${guestName} just uploaded a photo!`,
  url: '/gallery',
});
```

### Event Reminder
```typescript
// Scheduled job/cron
const subscriptions = await getSubscriptions();
subscriptions.forEach(async (sub) => {
  await sendPushNotification(sub, {
    title: '⏰ Event Reminder',
    body: 'Your event starts in 1 hour!',
  });
});
```

### Admin Activity Alert
```typescript
// When admin takes action
await sendPushNotification(ownerSubscription, {
  title: '💕 Activity Alert',
  body: '5 new messages from guests!',
  url: '/admin',
});
```

---

## Testing Strategy

### Desktop (Chrome/Firefox)
1. Open DevTools → Application → Service Workers
2. Click "Enable Notifications"
3. Grant permission
4. Click "Send Test Notification"
5. Notification appears in system tray

### Android (Chrome)
1. Open app on phone
2. Works immediately after permission
3. Notifications appear even when app closed

### iOS (Safari PWA)
1. **MUST add to Home Screen first**
2. Open from home screen (standalone mode)
3. Enable notifications
4. Notifications appear in notification center

### Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Service Worker stuck "installing" | Missing cached file | Remove from urlsToCache |
| "Creating subscription..." hangs | SW not activated | Clear cache, hard reload |
| iOS no notifications | Using Safari browser | Must add to Home Screen |
| Android missing notifications | App not in foreground | Service Worker should handle |
| 410 Gone error | Subscription expired | Remove from database, user re-subscribes |

---

## Decision Matrix

| Decision | Reasoning |
|----------|-----------|
| Use VAPID keys | Required by Web Push standard for security |
| Environment variables | Vercel has read-only filesystem |
| Service Worker mandatory | Only way to receive push when app closed |
| Per-device subscription | Each device needs unique endpoint |
| HTTPS required | Web Push API security requirement |

---

## Pros & Cons

### ✅ Advantages
- **Real-time Updates**: Users get instant notifications
- **Works Offline**: Service Worker handles when app closed
- **Cross-platform**: iOS, Android, Web in one codebase
- **Native Feeling**: Desktop/mobile notifications
- **High Engagement**: Push notifications drive user activity

### ❌ Limitations
- **iOS Limited**: Requires home screen install
- **User Permission**: Must ask for notification access
- **HTTPS Only**: Can't test on non-HTTPS locally
- **Subscription Management**: Need database for subscriptions
- **Uninstalls**: Subscriptions become invalid if user uninstalls

---

## Critical Sections
- **Lines 1-30**: Service Worker push event (core functionality)
- **Lines 40-60**: VAPID key configuration (authentication)
- **Lines 80-100**: Frontend subscription flow (user experience)
- **Lines 110-130**: API endpoints (backend integration)

---

## Validation Checklist
- [ ] `package.json` includes `web-push` and `@types/web-push`
- [ ] VAPID keys generated and stored in environment variables
- [ ] Service Worker registered in layout/main template
- [ ] API routes created and accessible
- [ ] Push subscription saved to database/storage
- [ ] Tested on desktop browser
- [ ] Tested on Android phone
- [ ] Tested on iOS (with home screen install)
- [ ] Error handling for failed subscriptions
- [ ] Subscription cleanup for 410 errors

---

## Deployment Checklist
- [ ] Environment variables set in production (Vercel/Netlify/etc)
- [ ] HTTPS enabled (auto on Vercel)
- [ ] Service Worker file publicly accessible
- [ ] Manifest.json properly configured
- [ ] Database schema includes push subscriptions
- [ ] VAPID keys rotated and secure
- [ ] Error logging configured

---

## Future Enhancements
- Push notification actions (buttons in notification)
- Notification analytics (open rates, clicks)
- Scheduled notifications
- Notification categories/topics
- Rich media notifications (images, video)
- Background sync for offline queue

---

## Source Context
- **Maturity**: Production-tested in Wedding Wall PWA
- **Scale**: Tested with multiple device subscriptions
- **Framework**: Next.js 16+ (App Router)
- **Deployment**: Vercel serverless
- **Last Updated**: March 31, 2026

**Reuse Status**: ✅ Ready to implement in any PWA project

---

## Related Patterns
- **PWA Offline-First Setup** - Foundational PWA configuration
- **Database Schema** - Store subscriptions in Prisma/PostgreSQL
- **API Routes** - Use for webhook handlers
