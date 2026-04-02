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

### 1. 🌐 **Personal Website Portfolio** — Developer Portfolio Site
**Status**: 💡 **NEW IDEA** (Added Apr 2, 2026)
**Added**: April 2, 2026 (6:09 PM)
**Concept**: Build a personal website portfolio to showcase Hakim's projects and skills

**Details**:
- **Purpose**: Professional portfolio site for Hakim
- **Projects to Showcase**: Wedding Wall, ONDW, Booking Bus System, and other coding projects
- **Features**: Project showcase, about section, skills, contact information
- **Tech Stack**: [To be determined - personal choice]
- **Design**: Modern, responsive, clean interface
- **Deployment**: [To be determined]
- **LRU Position**: #1 (Most Recent - Just Added)

---

### 2. ♾️ **Eternal Memory** (prev. Wedding Wall) — Multi-Tenant Digital Guestbook
**Status**: 🚀 **PIVOT & EXPANSION** (Business Strategy Phase)
**Added**: March 22, 2026 (8:31 PM)
**Last Updated**: March 25, 2026 (11:25 AM)
**Concept**: Rebranding "Wedding Wall" into a universal digital guestbook for Cafes, Events, and Photography Studios.

**Details**:
- **Core Value**: "Live Review Wall" — Customers upload photos/reviews, displayed instantly on a screen.
- **Business Model**: Network effect ("Mouth to Mouth") → Ads revenue.
- **Target Clients**: 
  - **Cafes**: Interactive customer review display.
  - **Events**: Weddings, birthdays, corporate events.
  - **Photography Studios**: Instant portfolio/client showcase.
- **Key Feature**: Customizable naming/theming per client (e.g., "Cafe Memories" vs "Wedding Wall").
- **Current Task**: Creating sales pitch & feedback questions.
- **Tech Pivot**: Needs multi-tenant architecture or configurable modes.
- **Hardware Challenge**: Cafes often lack large screens/TVs. Need creative display solutions (Tablets? Projectors? "BYOD" mode?).
- **Pivot Strategy**: Focus on "Counter-Top" displays (iPad/Tablet stands) instead of wall-mounted TVs. Easier adoption.
- **Feature Note**: **Infinite Scroll** (Lazy Loading) implemented in base Wedding Wall. **Auto-Scroll** (Marquee) rejected.
- **Future Enhancement**: **Mini-Game Integration** (Phase 2).
  - Gamify the wait: Play game → Win → Reward = "Feature on the Wall".
  - Solves "boredom" and incentivizes interaction.
- **LRU Position**: #1 (Most Recent / Strategic Pivot)

---

### 2. 🔧 **ONDW Pre-Production Environment** — Docker Local + Hostinger Staging
**Status**: 🚀 **IN PROGRESS** (Docker Local Pre-Prod Strategy)
**Added**: March 31, 2026 (9:05 AM)
**Last Updated**: March 31, 2026 (10:40 AM)
**Concept**: Set up pre-prod environment using Docker locally on Mac for safe testing, then deploy to Hostinger staging when proven stable

**Details**:
- **Domain**: `onewei.my`
- **Current Hosting**: Hostinger (Shared Hosting)
- **Access Method**: SSH
- **Current Environment**: Production only (no pre-prod)
- **Primary Goal**: Test service worker fixes + push notifications safely before production
- **Related Issue**: Service worker (`sw.js`) currently disabled due to cache conflicts with Laravel auth
- **Push Notifications**: PWA pattern ready (documented in library), needs SW working first
- **Action Items**:
  1. SSH into Hostinger and document current setup (PHP version, MySQL, Redis, directory structure)
  2. Create pre-prod subdomain/directory (e.g., `staging.ondw-domain.com`)
  3. Set up separate MySQL database for pre-prod
  4. Configure separate `.env` for pre-prod (different API keys, debug settings)
  5. Deploy code to pre-prod via Git or FTP
  6. Test service worker uncommenting and cache strategy fixes
  7. Test push notifications end-to-end
  8. Document deployment process for future use
- **Technical Notes**:
  - Hostinger shared hosting has file system limits
  - May need to coordinate with hosting provider for additional domains/databases
  - Pre-prod `.env` should mirror production but with test credentials
- **Risk**: Service worker cache issues caused production problems before - pre-prod testing critical
- **LRU Position**: #2 (Most Recent / Active Deployment)

---

### 3. 🎟️ **Digital Loyalty System** — Customer Card to PWA
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

### 4. 🎨 **Photobooth WebApp** — Cloud-Based Remote Shutter
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
