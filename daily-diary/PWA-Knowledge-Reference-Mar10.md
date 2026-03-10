# 📚 PWA Knowledge - Wedding Wall Reference

**Recorded**: March 10, 2026 (04:51 AM - Session Start)
**Topic**: Progressive Web App (PWA) Implementation Standards
**Source**: ONDW-Laravel-HAKIM analysis + Wedding Wall planning
**Status**: Knowledge Entry for Wedding Wall development

---

## 🎯 PWA Standards Reference

### What is a PWA?
A Progressive Web App is a web application that works like a native app:
- **Installable**: Add to home screen on mobile/desktop
- **Offline-First**: Service workers cache content
- **Fast**: Quick load times, smooth animations
- **App-like**: Standalone display mode (no browser chrome)
- **Responsive**: Works on any device size

### Key PWA Files Required

#### 1. **manifest.json** (Public Web App Metadata)
Location: `public/manifest.json`

**Essential Properties**:
```json
{
  "name": "App Full Name",
  "short_name": "Short Name",
  "id": "/",
  "description": "App description",
  "start_url": "/pwa-start" OR "/",
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

**ONDW Reference Values**:
- `name`: "OnDeWei - Food Delivery"
- `short_name`: "OnDeWei"
- `theme_color`: "#429AD5" (primary brand color)
- `display`: "standalone" (hides address bar)

#### 2. **service-worker.js** (Offline & Caching Logic)
Location: `public/service-worker.js`

**Core Responsibilities**:
- Cache static assets on install
- Intercept network requests (offline fallback)
- Background sync (queue actions when offline)
- Push notifications (optional)
- Cache versioning & cleanup

**Pattern**:
```javascript
const CACHE_NAME = "v1";
const urlsToCache = ["/", "/offline.html", "/css/style.css"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache)));
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => response || fetch(event.request))
  );
});
```

#### 3. **Icon Set** (App Icons)
Required Sizes (for manifest):
- **32x32px** - Favicon (browser tab)
- **192x192px** - App icon (mobile home screen)
- **512x512px** - App splash screen (largest)

**Maskable Icons**: Design with padding so icon works in any shape (rounded squares, circles, etc.)

#### 4. **meta tags in HTML Head**
```html
<meta name="theme-color" content="#429AD5">
<meta name="description" content="App description">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="manifest" href="/manifest.json">
<link rel="apple-touch-icon" href="/apple-icon.png">
```

---

## 📱 Mobile-First Design Strategy

### Responsive Breakpoints (Standard)
```css
Mobile: 320px - 767px
Tablet: 768px - 1024px
Desktop: 1025px+

Touch-friendly minimum: 44x44px buttons
```

### PWA Mobile Considerations
- **Safe area insets** for notches/rounded corners (iPhone X+)
- **Bottom navigation** (easier thumb access)
- **Full viewport utilization** (no wasted space)
- **Fast interaction** (< 200ms response)

---

## 🔄 ONDW PWA Implementation Details

**ONDW Uses**:
- Laravel backend with Vite frontend bundler
- Manifest at `/public/manifest.json`
- Service worker for offline support
- Tailwind CSS for responsive design
- Custom icons from `favicon-32x32.png`

**For Wedding Wall** (Next.js version):
- Next.js has built-in service worker support (next.js 14+)
- Can use `next-pwa` library for automatic setup
- Or manual implementation similar to ONDW
- Manifest at `public/manifest.json`
- Service worker at `public/service-worker.js`

---

## 💡 PWA Best Practices for Wedding Wall

1. **Install Prompt**: Show "Add to Home Screen" on first visit (optional)
2. **Offline Gallery**: Cache downloaded photos locally
3. **Background Sync**: Queue photo uploads when offline, sync when online
4. **Push Notifications**: Notify users when new photos arrive
5. **Performance**: Lighthouse score > 90

---

## 📝 Key Learnings from ONDW

✅ **What Worked**:
- Standalone display mode (feels like native app)
- Theme color matching brand (UX consistency)
- Icon set for multiple sizes
- Tailwind CSS for mobile-responsive design

⚠️ **Considerations**:
- Manifest needs proper start_url (ONDW uses `/pwa-start`)
- Icons should be optimized (sharp, correct sizes)
- Service worker caching strategy matters
- Test on real devices (not just Chrome DevTools)

---

## 🎯 Wedding Wall PWA Checklist

- [ ] `manifest.json` with correct metadata & icons
- [ ] `service-worker.js` for caching strategy
- [ ] Icon set (32x32, 192x192, 512x512 - maskable)
- [ ] Meta tags in `app/layout.tsx`
- [ ] Mobile-first CSS (Tailwind responsive)
- [ ] Offline fallback page
- [ ] Install prompt component (optional)
- [ ] Lighthouse audit > 90
- [ ] Test on real mobile device

---

**Memory Type**: Knowledge Base  
**Applicable To**: Wedding Wall development  
**Reference System**: Echo-Memory-Recall (searchable via "PWA", "service worker", "manifest")  
**Status**: Ready for implementation in Phase 1

