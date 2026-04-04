# 📊 Project Management System - Installation & Usage Guide

## Installation Steps

### Step 1: Load This Feature
```
Load project-management
```

### Step 2: Verify Project Structure
The system checks that these files/folders exist in `projects/`:
- ✅ `project-list.md` — Master project registry
- ✅ `lru-manager.md` — LRU queue state
- ✅ `templates/` directory with project templates
- ✅ Type-based subdirectories: `coding-projects/`, `writing-projects/`, etc.

### Step 3: Initialize If Empty
If `project-list.md` is empty, run:
```
init projects
```

This scaffolds:
- Project list with no active projects yet
- LRU manager (initially empty)
- Empty active and archived folders for each type

---

## How to Use

### Creating a New Project

**Trigger:**
```
new [type] project [name]
```

**Examples:**
```
new coding project API-Dashboard
new writing project Chapter-5
new research project AI-Trends
new business project Q1-Strategy
```

**What Happens:**
1. AI extracts type and name from command
2. Asks for brief description (1-2 sentences)
3. Creates project file from appropriate template
4. Adds to `projects/[type]-projects/active/[name].md`
5. Updates project list (position #1)
6. If 11 projects exist, archives the oldest one

**File Created:**
- Location: `projects/[type]-projects/active/[ProjectName].md`
- Format: Pre-filled template with your description, created date, status=Active

---

### Loading an Existing Project

**Trigger:**
```
load project [name]
```

**Examples:**
```
load project API-Dashboard
load project Chapter-5
load project Wedding-Wall
```

**What Happens:**
1. AI searches for project in active and archived lists
2. Loads project file and reads current state
3. Extracts key context: goals, progress, technical stack
4. Updates "Last Accessed" to today
5. Moves to position #1 in LRU queue
6. Shifts other projects down; if 11+, archives lowest

**Result:**
- AI now focused on this project
- Ready to discuss next steps, continue work, etc.
- Context persists until you switch projects or end session

---

### Saving Project Progress

**Trigger:**
```
save project
```

**What Happens:**
1. AI reviews current session work on this project
2. Updates project file with:
   - New achievements and milestones completed
   - Technical decisions made this session
   - Current blockers or challenges
   - Updated "Last Accessed" date
   - New status if changed (Active → Paused, etc.)
3. Saves updated project file
4. Optionally updates project list with new info

**Before & After:**
```
BEFORE:
  Last Accessed: 2026-04-01
  Progress: [old status]
  Next Steps: [old tasks]

AFTER:
  Last Accessed: 2026-04-04
  Progress: [includes new session achievements]
  Next Steps: [updated based on today's work]
```

---

### Listing Projects

**Trigger:**
```
list projects
```

**Shows:**
- **Position 1-10**: Active projects (LRU order)
- **Recent**: Last 3 accessed projects
- **Archived**: How many projects in archive
- **Type Breakdown**: Count by type (coding, writing, research, business)

---

### Archiving a Project

**Trigger:**
```
archive project [name]
```

**What Happens:**
1. Moves project from `active/` to `archived/`
2. Updates status to "Archived (manual)"
3. Removes from active project list
4. Stays in memory for later retrieval

**To Reactivate:**
```
load project [name]
```
(Automatically moves from archived back to active)

---

## Project Types & Templates

### Available Types

| Type | Purpose | Template | Location |
|------|---------|----------|----------|
| **coding** | Software projects, features, fixes | coding-template.md | `projects/templates/` |
| **writing** | Articles, blogs, chapters, docs | writing-template.md | `projects/templates/` |
| **research** | Learning projects, investigations | research-template.md | `projects/templates/` |
| **business** | Business plans, strategy | business-template.md | `projects/templates/` |

Each template pre-fills sections appropriate for that project type.

---

## Advanced Usage

### Switching Between Projects
```
You: "load project Wedding-Wall"
→ AI switches context to Wedding-Wall project

You: "What's the status?"
→ AI responds with Wedding-Wall's current state

You: "load project API-Dashboard"
→ AI switches context to API-Dashboard project
```

### Project + Other Systems

#### With Auto-Commit-System
```
save project
→ Also auto-commits project changes to Git
```

#### With Save-Diary-System
```
save project
→ Adds session achievements to today's diary
→ Creates diary entry documenting progress
```

#### With Library-System
```
While working on project: "add to library [snippet]"
→ Code pattern saved to library for reuse in future projects
```

#### With Memory-Consolidation-System
```
archive project [name]
→ Automatically extracts learning and key insights
→ Creates consolidated memory entry for future reference
```

---

## Troubleshooting

### "Project not found"
- Check spelling of project name
- Run `list projects` to see available projects
- If in archived, run `load project [name]` to reactivate

### "Can't create more projects"
- You have 10 active projects (LRU limit reached)
- Oldest project automatically moves to archive
- Or manually `archive project [name]` first

### "Lost project data"
- Check `projects/[type]-projects/archived/` folder
- Archived projects are preserved, just not active
- Load with `load project [name]` to restore

---

## Protocol References

For detailed workflows, see in `projects/`:
- **new-project-protocol.md** — Detailed creation steps
- **load-project-protocol.md** — Detailed loading steps
- **save-project-protocol.md** — Detailed saving steps
- **lru-manager.md** — LRU queue implementation details
