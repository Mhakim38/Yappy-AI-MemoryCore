# PWA Offline-First Pattern
**Level**: 2 (Production-Proven)  
**Source**: OnDeWei Food Delivery (Laravel) - 2+ years production  
**Status**: Active & Maintained  

---

## Problem Statement
Modern web apps need offline functionality, home screen installation, and native-like experience. Users expect:
- Works when network is down
- Installable as app on home screen
- Push notifications support
- Auto-update capability

---

## Solution Overview
Complete PWA setup with manifest.json + service worker registration pattern. Provides:
- Service Worker for offline caching
- Web App Manifest for installation
- Install prompt handling (beforeinstallprompt)
- Graceful fallbacks for unsupported browsers

---

## Implementation

### 1. Web App Manifest (`public/manifest.json`)
```json
{
  "name": "App Name - Full Description",
  "short_name": "AppName",
  "id": "/",
  "description": "Brief description of your app",
  "start_url": "/pwa-start",
  "scope": "/",
  "display": "standalone",
  "background_color": "#FBFBFB",
  "theme_color": "#429AD5",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/favicon-32x32.png",
      "sizes": "32x32",
      "type": "image/png"
    },
    {
      "src": "/favicon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/favicon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
```

**Key Fields**:
- `display: "standalone"` - Removes browser UI, feels native
- `start_url` - Initial page when installed (can track pwa installs)
- `theme_color` - Mobile browser chrome color
- `purpose: "maskable"` - Icons on devices that crop/mask them
- Sizes needed: 32px, 192px, 512px minimum

---

### 2. Service Worker Registration (`public/pwa.js`)
```javascript
// Service Worker registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
                console.log('Service Worker registered:', registration.scope);
            })
            .catch((error) => {
                console.log('Service Worker registration failed:', error);
            });
    });
}

// Install prompt handling
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    console.log('PWA install prompt available');
    // Show custom install button here
});

// Track installation
window.addEventListener('appinstalled', () => {
    console.log('PWA was installed');
    deferredPrompt = null;
});
```

---

### 3. Service Worker (`public/sw.js`)
```javascript
const CACHE_NAME = 'app-v1';
const urlsToCache = [
  '/',
  '/manifest.json',
  '/favicon-32x32.png',
  '/favicon-192x192.png',
  '/favicon-512x512.png'
];

// Install - cache essential files
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
      .catch((error) => console.log('Cache addAll failed:', error))
  );
  self.skipWaiting();
});

// Fetch - serve from cache, fallback to network (cache-first)
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) return response;
        return fetch(event.request).then((response) => {
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
          return response;
        });
      })
      .catch(() => caches.match(event.request))
  );
});

// Activate - clean up old caches
self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});
```

---

### 4. HTML Head Configuration
```html
<head>
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#429AD5">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <script src="/customJS/pwa.js"></script>
</head>
```

---

## Adaptation Guide

### For Next.js 16+
1. Place manifest in `public/manifest.json`
2. Place service worker in `public/sw.js`
3. Add script loading in layout root:
   ```tsx
   useEffect(() => {
     const script = document.createElement('script');
     script.src = '/pwa.js';
     document.head.appendChild(script);
   }, []);
   ```
4. Link manifest in `app/layout.tsx`:
   ```tsx
   <link rel="manifest" href="/manifest.json" />
   <meta name="theme-color" content="#429AD5" />
   ```

### For Laravel/Blade
1. Place in `public/` directory
2. Reference in main layout blade:
   ```blade
   <link rel="manifest" href="{{ asset('manifest.json') }}">
   <script src="{{ asset('customJS/pwa.js') }}"></script>
   ```

### For Other Frameworks
- Manifest always in `public/` or `static/`
- Service worker registration in main script
- Link manifest in document `<head>`
- Same service worker logic applies universally

---

## Decision Matrix

| Decision | Reasoning |
|----------|-----------|
| Cache-first strategy | Fast repeat visits, works offline |
| beforeinstallprompt | Triggers install flow on supported browsers |
| maskable icons | Better appearance on modern Android devices |
| start_url redirect | Track PWA installations vs web visits |
| skipWaiting() | Newer SW versions activate immediately |
| claim() in activate | Take control of all clients immediately |

---

## Pros & Cons

### ✅ Advantages
- **Offline Access**: Works completely offline after first load
- **Native Feel**: Standalone display removes browser chrome
- **Installable**: Home screen icon just like native app
- **Faster Loading**: Cache-first strategy blazingly fast
- **Push Ready**: Foundation for push notifications
- **Auto-Update**: Service Worker can check for updates

### ❌ Limitations
- **Cache Management**: Stale content if cache invalidation not handled
- **Browser Support**: Older devices may not support full PWA
- **iOS Limitations**: Limited PWA support compared to Android
- **Storage Quota**: Limited cache size per domain (~50MB typical)
- **HTTPS Only**: Service Workers require secure context
- **Complexity**: Debugging offline behavior can be tricky

---

## Critical Sections
- **Lines 1-10**: Manifest configuration (customize app name, colors)
- **Lines 24-35**: Install prompt detection (customize UI trigger)
- **Lines 50-65**: Service Worker caching strategy (adjust CACHE_NAME for updates)
- **Lines 75-90**: Activate event (cleanup old caches after update)

---

## Validation Checklist
- [ ] `manifest.json` linked in HTML head
- [ ] Icon sizes: 32px, 192px, 512px created
- [ ] Service Worker file at `/sw.js`
- [ ] `pwa.js` or equivalent loaded in page
- [ ] App tested offline (DevTools Network → Offline)
- [ ] Install prompt shows on first visit (Chrome/Android)
- [ ] Theme color matches brand (browser chrome)
- [ ] `start_url` distinct from normal entry (to track PWA installs)

---

## Testing Strategy

```javascript
// Test offline capability
1. Open DevTools → Application → Service Workers
2. Check "Offline" checkbox
3. Refresh page - should still work
4. Check DevTools → Application → Cache Storage
5. Verify cached resources are listed

// Test installation
1. Open on Android/Chrome
2. Wait 3+ seconds
3. Install prompt should appear
4. Install and check home screen
5. Launch from home screen - should load without browser UI

// Test update
1. Modify sw.js
2. Change CACHE_NAME to 'app-v2'
3. Reload page
4. Old cache should be cleaned up
5. New cache should be populated
```

---

## Common Pitfalls
1. **Forgetting HTTPS** - Service Workers require secure context
2. **Cache Poisoning** - Old cache not cleared on update (use versioning)
3. **Stale Content** - Cache-first can serve outdated pages (use skip-waiting)
4. **Icon Size Mismatch** - Wrong sizes cause installation failures
5. **Scope Issues** - Service Worker scope must match app structure

---

## Future Enhancements
- Push notifications API integration
- Background sync for offline forms
- Periodic sync for auto-updates
- Cache quota monitoring
- Dynamic route caching based on usage patterns

---

## Source Context
- **Maturity**: Production-tested in OnDeWei (2+ years)
- **Scale**: Serves thousands of daily active users
- **Framework**: Originally Laravel, pattern is framework-agnostic
- **Last Updated**: Checkpoint Phase 6 (Wedding Wall completion)

**Reuse Status**: ✅ Ready to extract and implement in Next.js, Vue, React, or any framework.
