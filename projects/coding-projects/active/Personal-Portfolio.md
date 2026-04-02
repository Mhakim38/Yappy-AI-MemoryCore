# Personal Website Portfolio
*Coding Project - Created April 2, 2026*

## Description
Professional portfolio website showcasing Hakim's coding projects with modern UI/UX, PWA functionality, smooth animations, and push notifications. Displays Wedding Wall, ONDW, Booking Bus System, and other projects.

## Project Details
- **Type**: Coding Project
- **Status**: Planning → Ready for Development
- **Created**: April 2, 2026 6:39 PM
- **Last Updated**: April 2, 2026 6:44 PM
- **Position**: #1 (Most Recent)
- **Collaboration**: With Hori 💕

## Technical Stack
- **Languages**: TypeScript (frontend + backend)
- **Framework**: Next.js (App Router, full-stack)
- **Styling**: Tailwind CSS
- **Animations**: Anime.js
- **UI Components**: Custom glassmorphic components + shadcn/ui patterns
- **PWA**: Service Worker + Web Push API (VAPID keys)
- **Push Notifications**: Web Push API (localStorage for subscriptions, no DB required)
- **SEO**: Next.js generateMetadata() + JSON-LD structured data
- **Images**: Next.js Image optimization
- **Deployment**: Vercel
- **Version Control**: Git + GitHub

## Project Structure
```
portfolio/
├── app/
│   ├── api/
│   │   └── push/
│   │       ├── vapid.ts
│   │       ├── subscribe.ts
│   │       └── send.ts
│   ├── components/
│   │   ├── Navbar.tsx (glassmorphic)
│   │   ├── NotificationPopup.tsx (first-visit permission)
│   │   ├── NotificationToggle.tsx (subscribe button)
│   │   ├── ProjectCard.tsx
│   │   └── animations/
│   ├── projects/
│   │   ├── page.tsx
│   │   └── [slug]/page.tsx
│   ├── layout.tsx (SEO metadata)
│   └── page.tsx (home)
├── lib/
│   ├── push-notifications.ts
│   ├── projects-data.ts
│   └── seo.ts
├── public/
│   ├── service-worker.js
│   ├── manifest.json
│   └── robots.txt
├── styles/
│   └── globals.css (Anime.js animation definitions)
└── README.md
```

## Development Goals
1. ✅ Plan comprehensive architecture with all features
2. Set up Next.js project with TypeScript
3. Implement glassmorphic navbar with Anime.js animations
4. Build PWA with service worker and offline support
5. Create push notification system with first-visit pop-up
6. Implement SEO (meta tags, structured data, sitemap)
7. Build project showcase with infinite scroll
8. Test on desktop, mobile, and iOS
9. Deploy to Vercel and go live

## Feature Specifications

### 1. SEO Implementation ✅ (Verified)
- **Meta Tags**: Dynamic titles, descriptions per page
- **Open Graph**: Social media sharing (Facebook, LinkedIn)
- **Twitter Cards**: Twitter-specific metadata
- **Structured Data**: JSON-LD (Person, Project, Organization schemas)
- **Sitemap**: Auto-generated sitemap.xml
- **robots.txt**: Search engine crawling rules
- **Canonical URLs**: Prevent duplicate content issues
- **Image Optimization**: Next.js Image component with lazy loading
- **Core Web Vitals**: Performance-focused implementation
- **Mobile-first**: Responsive design from start

### 2. Push Notifications ✅ (NO DATABASE REQUIRED)
- **Type**: Web Push API + VAPID keys (industry standard)
- **Storage**: Browser localStorage (no server database needed!)
- **Per-device**: Each device gets unique subscription endpoint
- **HTTPS**: Automatic on Vercel
- **User Flow**:
  1. First-visit pop-up requests permission
  2. Subscribe/unsubscribe toggle button in navbar
  3. Test notification button (for demo)
  4. Notifications work when app is closed
- **Service Worker**: Handles push events and offline notifications
- **Error Handling**: Graceful handling of expired subscriptions (410 errors)

#### Components to Build
- `NotificationPopup.tsx`: First-time permission request modal
- `NotificationToggle.tsx`: Subscribe/unsubscribe button
- `NotificationTester.tsx`: Send test notification (dev/demo)
- `service-worker.js`: Push event listener and notification display
- `/api/push/vapid`: GET public VAPID key
- `/api/push/subscribe`: POST save subscription to localStorage
- `/api/push/send`: POST send test notification

### 3. Glassmorphic Navbar
- **From Library**: `library-items/wedding-wall-patterns/PATTERN_LIBRARY.md`
- **Style**: Glass effect with backdrop blur + border/transparency
- **Responsive**: Sticky on desktop, hamburger menu on mobile
- **Animation**: Scroll-based height shrinking with Anime.js
- **Interactive**: Smooth transitions and hover effects
- **Mobile**: Touch-friendly navigation menu

### 4. Anime.js Animations
- **Animation Style**: Mix of subtle + bold effects
- **Use Cases**:
  - Navbar scroll animations
  - Project card hover effects
  - Page transitions
  - Scroll-triggered animations
  - Button interactions
  - Load animations
- **Performance**: Optimized for 60fps on mobile

### 5. Project Showcase
- **Projects to Display**:
  1. Wedding Wall (primary showcase - live on Vercel)
  2. ONDW (food delivery platform)
  3. Booking Bus System
  4. Other coding projects (as added)
- **Features**:
  - Project cards with images
  - Infinite scroll implementation
  - Detailed project pages
  - GitHub links
  - Live demo links (where applicable)
  - Technology tags
  - Project descriptions

### 6. PWA Features
- **Offline Support**: Service worker caching strategy
- **Installable**: Add to home screen on mobile
- **Manifest**: Web app metadata
- **Icons**: Multiple sizes for different devices
- **Splash Screen**: Custom loading screen

## Implementation Plan (6 Phases)

### Phase 1: Setup & Skills Integration
- [ ] Create Next.js project with TypeScript
- [ ] Extract UI/UX skills from emilkowalski/skill
- [ ] Set up Tailwind CSS configuration
- [ ] Configure SEO base setup (meta tags, structured data template)
- [ ] Initialize git repository

### Phase 2: Core UI Components
- [ ] Build glassmorphic navbar (from Library pattern)
- [ ] Integrate Anime.js library
- [ ] Create responsive layout with mobile breakpoints
- [ ] Set up SEO metadata template in layout.tsx
- [ ] Add basic routing

### Phase 3: PWA & Notifications
- [ ] Create service worker with push support
- [ ] Build NotificationPopup component (first-visit)
- [ ] Build NotificationToggle component
- [ ] Create API routes (/api/push/*)
- [ ] Implement localStorage subscription storage
- [ ] Test on device

### Phase 4: Project Showcase
- [ ] Design project card component with animations
- [ ] Implement infinite scroll (reuse Wedding Wall pattern)
- [ ] Create project detail pages
- [ ] Add project data structure
- [ ] Optimize project images

### Phase 5: SEO Optimization
- [ ] Generate sitemap.xml dynamically
- [ ] Create robots.txt
- [ ] Add canonical URLs
- [ ] Implement breadcrumb schema
- [ ] Configure Open Graph tags
- [ ] Add Twitter Card metadata

### Phase 6: Polish & Deployment
- [ ] Optimize Anime.js animations
- [ ] Performance audit (Vercel analytics)
- [ ] Mobile responsiveness testing
- [ ] Push notification end-to-end testing
- [ ] iOS home screen app testing
- [ ] Final SEO audit
- [ ] Deploy to Vercel
- [ ] Monitor and iterate

## Knowledge Sources (From Yappy's Library)
1. **Push Notifications**: `library-items/integration/push-notifications.md`
   - Complete Web Push API implementation
   - Service Worker with push event handler
   - VAPID key configuration (auto-generated in dev)
   - API routes for subscription management
   
2. **Glassmorphic Navbar**: `library-items/wedding-wall-patterns/PATTERN_LIBRARY.md`
   - React component with Tailwind CSS
   - Scroll-responsive behavior
   - Mobile menu support

3. **UI/UX Skills**: From emilkowalski/skill repo (`npx skills add emilkowalski/skill`)
   - Design patterns for interfaces
   - Designer + engineer friendly guidance

## Key Decisions (Confirmed April 2, 2026)
1. **Framework**: Next.js (full-stack capability)
2. **Deployment**: Vercel (optimized for Next.js + auto-HTTPS)
3. **Animations**: Mix of subtle (professional) + bold (impressive)
4. **Push Notifications**: Web Push API (no database required!)
5. **SEO**: Full implementation with Next.js
6. **Storage**: Browser localStorage for subscriptions (no backend DB)

## Important Notes
- **No Database for Push**: Subscriptions stored in browser localStorage
- **VAPID Keys Auto-Generated**: Development auto-generates, production uses .env
- **HTTPS Required**: Automatic on Vercel
- **iOS Limitation**: Push notifications work when app added to home screen
- **Service Worker**: Critical for PWA and push functionality
- **Offline-First**: Service worker handles all offline scenarios

## Estimated Timeline
- Phase 1: 1 session
- Phase 2: 1-2 sessions
- Phase 3: 1-2 sessions
- Phase 4: 1-2 sessions
- Phase 5: 1 session
- Phase 6: 1-2 sessions

**Total**: 6-10 sessions (depends on implementation pace)

## Success Criteria
- [ ] Deployed to Vercel with custom domain
- [ ] SEO optimized (Google Search Console verification)
- [ ] PWA installable on mobile and desktop
- [ ] Push notifications working on desktop + mobile
- [ ] Project showcase displaying all 4+ projects
- [ ] Performance score >90 on Lighthouse
- [ ] Mobile responsiveness perfect on all devices
- [ ] Animations smooth at 60fps
- [ ] Zero console errors or warnings

## Related Projects
- **Wedding Wall**: Referenced as primary showcase project
- **ONDW**: Food delivery platform (showcase project)
- **Booking Bus**: Transportation system (showcase project)
- **Yappy Memory System**: Self-updating during development

---

**Version**: Portfolio Project v1.0  
**Status**: Planning Complete → Development Ready  
**Created**: April 2, 2026 (Evening)  
**Owner**: Hakim (with Hori collaboration 💕)

*Ready to build an amazing portfolio with modern tech and smooth animations! Let's make Hakim's projects shine! 💜*
