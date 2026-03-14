# 💡 Project Ideas Pipeline
*Emerging concepts and brainstorm backlog - managed with LRU-style ordering*

## Trigger Commands
```
"show ideas" → Display all project ideas
"add project idea: [concept]" → Add new idea to pipeline
"project ideas" → Display all ideas
```

---

## Active Ideas (Ordered by Recency)

### 1. 🎟️ **Digital Loyalty System** — Customer Card to PWA
**Status**: 💡 **BRAINSTORM** (Idea Captured)
**Added**: March 14, 2026 (5:56 PM)
**Last Updated**: March 14, 2026 (5:56 PM)
**Concept**: Replace physical punch/loyalty cards with digital PWA-based system

**Details**:
- **Use Case**: Generic (adaptable to any business)
- **Platform**: PWA (Progressive Web App)
- **Customer Experience**: QR code scanning to track checkpoint progress
- **Checkpoint System**: 
  - Default: 10 checkpoints per loyalty cycle
  - Admin customizable rewards at each checkpoint
  - Auto-reset or one-time loyalty cycles
- **Admin Dashboard**: Create programs, customize rewards, track customer progress
- **Key Features**: Real-time progress tracking, reward notifications, mobile-optimized
- **Tech Stack**: [To be determined during planning]
- **LRU Position**: #1 (Most Recent / Brainstorm Phase)

---

### 2. 💒 **Wedding Wall** — Instagram-Story Photo Sharing Platform
**Status**: 🔄 **ONGOING** (Active Development)
**Added**: March 9, 2026 (2:32 AM)
**Last Updated**: March 9, 2026 (12:26 AM)
**Concept**: Wedding guests upload picture-only moments to a shared visual feed (like Instagram stories)

**Details**:
- **Main Feature**: Photo upload wall where guests browse shared wedding photos in real-time
- **Architecture**:
  - Frontend: React with Next.js
  - Storage: AWS S3 (direct browser upload with pre-signed URLs)
  - Backend: Next.js API routes/server actions for MVP
  - Database: PostgreSQL + Prisma
  - Hosting: DigitalOcean (or Vercel as fastest-launch alternative)
- **Current Status**: Architecture drafted, ready for implementation kickoff
- **LRU Position**: #2

---

### 3. 🎨 **Photobooth WebApp** — Cloud-Based Remote Shutter
**Status**: 💭 **CONCEPT** (Planning Phase)
**Added**: March 9, 2026 (12:19 PM)
**Last Updated**: March 9, 2026 (12:26 AM)
**Concept**: Two-device photobooth system with cloud sync

**Details**:
- **Main Device**: Camera interface with capture logic
- **Remote Device**: WebApp with simple wireless shutter button (press → photo captured on main device)
- **Architecture Decision**: Cloud-based (not local WiFi)
- **Photo Handling**: Email delivery OR download link, then auto-discard session (clean state)
- **Future Enhancement**: Live preview on remote (possible, not priority)
- **Stack**: [To be determined during planning]
- **LRU Position**: #3

---

### 4. [Empty]
### 5. [Empty]
### 6. [Empty]
### 7. [Empty]
### 8. [Empty]
### 9. [Empty]
### 10. [Empty]

---

## 📊 Ideas Management Rules

1. **Position #1** = Most recently added or updated idea
2. **Positions #2-10** = Active ideas in pipeline
3. **Maximum 10 ideas** before auto-archival
4. **Promotion**: Ideas move to active projects when development starts
5. **Archival**: Ideas pushed to position #11 auto-archive to `project-ideas-archived.md`

## File Location
- **Active Ideas**: `projects/project-ideas.md` (this file)
- **Archived Ideas**: `projects/project-ideas-archived.md` (older backlog)
- **Reference**: `main/relationship-memory.md` (triggers + display logic)

---

*Project Ideas v1.0 - Emerging concepts managed with LRU ordering*
