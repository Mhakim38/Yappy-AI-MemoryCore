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
- **Database**: Supabase (PostgreSQL managed) + Prisma ORM
- **Storage**: AWS S3 (image originals), optional CloudFront CDN
- **Auth**: NextAuth/Auth.js (Google + email magic link)
- **Backend**: Next.js API routes
- **UI**: shadcn/ui + Radix UI components
- **Tools**: ESLint, npm/node

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

### Selected Strategy: Vercel + Supabase + S3
We have chosen **Vercel** for hosting the Next.js frontend and API routes.
- **Database**: Connects to the existing **Supabase** instance (same data as dev).
- **Storage**: Connects to the existing **AWS S3** bucket (same files as dev).
- **Environment Variables**:
  - `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
  - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `AWS_S3_BUCKET`
  - `NEXT_PUBLIC_APP_NAME`, `NEXT_PUBLIC_APP_DESCRIPTION`

### Architecture Note
Deploying to Vercel does **not** create a new database. It connects to the *same* live production database used in development. Deleting data on the deployed site deletes it from the shared database.

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

### March 10, 2026
- ✅ Phase 1: Next.js + PWA Foundation scaffolded
- ✅ Phase 2: Database setup with Supabase + shadcn/ui + FontAwesome landing page
- ✅ Phase 3-5: API routes, pages, and styling completed
- ✅ Database schema with Photo and UploadToken fields implemented
- ✅ Route restructuring and error handling improvements
- **Last commit**: "Fix: Remove route groups and restructure to correct URLs" (Mar 10, 23:00)

## Code Standards
- **Style Guide**: ESLint configured
- **Testing**: [In progress]
- **Documentation**: [To be added]
- **Git Workflow**: Feature-based commits with descriptive messages

## Current Tasks
- [x] Define MVP feature scope and user flow
- [x] Choose technical stack and hosting approach
- [x] Draft initial database schema for users, events, and photos
- [x] Scaffold Next.js app with auth, Prisma, and upload API
- [x] Create end-to-end flow (events, uploads, gallery)
- [x] Fix remaining bugs and UI refinements (Dark mode, Mobile menu, PWA clipboard)
- [ ] Complete testing coverage
- [x] Finalize deployment strategy (Vercel + Supabase + S3)
- [ ] Execute Vercel deployment

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
