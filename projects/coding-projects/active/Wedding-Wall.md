# Wedding Wall
*Coding Project - Created March 9, 2026*

## Description
Web app for wedding photo stories where users upload image-only moments and guests can browse shared pictures from other attendees.

## Project Details
- **Type**: Coding Project
- **Status**: Active
- **Created**: March 9, 2026 2:32 AM
- **Last Accessed**: March 9, 2026 2:32 AM
- **Position**: #1

## Technical Stack
- **Languages**: TypeScript (frontend + backend)
- **Frameworks**: React + Next.js (App Router), Tailwind CSS
- **Database**: PostgreSQL (managed)
- **Storage**: AWS S3 (image originals), optional CloudFront CDN
- **Auth**: NextAuth/Auth.js (Google + email magic link)
- **Backend**: Next.js API routes for MVP, optional NestJS service later if scale grows
- **Tools**: Prisma ORM, Zod validation, React Query, Sentry, GitHub Actions

## Project Structure
```
Wedding-Wall/
├── src/
├── tests/
├── docs/
└── README.md
```

## Development Goals
1. Build image upload and gallery flow for wedding guests
2. Implement authentication and event-based access control
3. Optimize mobile-first browsing and upload performance
4. Ship MVP in 2-3 weeks with reliable image delivery

## Architecture Draft (MVP)

### Product Scope
- Event-based public/private wedding photo wall
- Guests upload image-only stories (no video)
- Feed/gallery view with simple engagement (like or comment optional for v2)

### Backend Recommendation
- **Recommended now**: Next.js full-stack backend (server actions + API routes)
- **Why**: Faster delivery, one deploy target, less DevOps overhead for MVP
- **When to split backend**: Move to NestJS/Express service after traffic or feature complexity increases (admin analytics, moderation queue, background jobs)

### Core Data Model (v1)
- `users` (id, name, email, avatar_url)
- `events` (id, slug, title, date, owner_user_id, privacy)
- `event_members` (event_id, user_id, role)
- `photos` (id, event_id, user_id, s3_key, thumbnail_key, caption, created_at)
- `reactions` (id, photo_id, user_id, type)

### Upload Flow
1. User selects image
2. Frontend requests pre-signed upload URL from backend
3. Browser uploads directly to S3
4. Backend stores metadata in PostgreSQL
5. Gallery reads from DB and serves optimized image URLs

### Security & Moderation (v1)
- File type whitelist: jpeg/png/webp only
- Max file size limit (for example: 10MB)
- Event-scoped access control checks on every read/write
- Basic report/remove flow for inappropriate uploads

## Hosting Decision

### Option A: Hostinger
- **Pros**: Lower cost, familiar environment
- **Cons**: Can be limiting for modern Node full-stack apps and background workers
- **Best for**: Static sites or simple PHP/Laravel workflows

### Option B: DigitalOcean
- **Pros**: Better control for Node/Next.js, App Platform simplicity, managed Postgres available
- **Cons**: Slightly more setup cost and infra decisions
- **Best for**: Production-ready Next.js + API growth path

### Option C: Vercel (strong alternative)
- **Pros**: Easiest for Next.js deployment, CDN and edge delivery out of the box
- **Cons**: Can get expensive at scale depending on usage patterns
- **Best for**: Fastest MVP launch with minimal ops

### Recommendation
- **MVP**: `Next.js + S3 + Managed Postgres` on **Vercel** or **DigitalOcean App Platform**
- **If you want one choice now**: choose **DigitalOcean** for better long-term cost/control balance
- **Keep S3 regardless of host**: storage stays portable if hosting changes later

## Progress Log
### March 9, 2026
- Project initialized
- Core concept captured (image-only wedding stories)
- Added to LRU project list at position #1
- Architecture draft completed (frontend, backend, storage, hosting)

## Code Standards
- **Style Guide**: [Project style]
- **Testing**: [Testing approach]
- **Documentation**: [Doc standards]
- **Git Workflow**: [Branch strategy]

## Current Tasks
- [x] Define MVP feature scope and user flow
- [x] Choose technical stack and hosting approach
- [x] Draft initial database schema for users, events, and photos
- [ ] Finalize deployment target: DigitalOcean or Vercel
- [ ] Scaffold Next.js app with auth, Prisma, and upload API
- [ ] Create first event + upload + gallery end-to-end flow

## Known Issues
- None yet

## Resources & References
- [Documentation links]
- [API references]
- [Related projects]

## Session Notes
*Space for working notes during active sessions*

## Memory Patterns
- Error solutions discovered
- Performance optimizations
- Architecture decisions
- Code snippets to remember

---
*Yappy AI Project Entry - March 9, 2026*
