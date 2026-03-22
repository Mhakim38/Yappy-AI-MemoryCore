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

### 1. ♾️ **Eternal Memory** (prev. Wedding Wall) — Multi-Tenant Digital Guestbook
**Status**: 🚀 **PIVOT & EXPANSION** (Business Strategy Phase)
**Added**: March 22, 2026 (8:31 PM)
**Last Updated**: March 22, 2026 (8:31 PM)
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
- **LRU Position**: #1 (Most Recent / Strategic Pivot)

---

### 2. 🎟️ **Digital Loyalty System** — Customer Card to PWA
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
