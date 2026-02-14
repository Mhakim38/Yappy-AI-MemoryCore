# 🧭 LRU Manager
*Rules and behavior for project positioning and archiving*

## Core Rules
1. Position #1 is always the most recently created or loaded project.
2. Positions #2-10 are active projects in descending recency.
3. When a project would move to position #11, it is auto-archived.
4. Each project type (coding, business, research) maintains its own LRU queue.

## Standard Actions

### New Project
- Insert at position #1
- Shift all active projects down
- Auto-archive position #11 if needed

### Load Project
- Move loaded project to position #1
- Shift others down
- Reactivate if it was archived
- Auto-archive position #11 if needed

### Save Project
- Update timestamps and progress log
- Preserve current position (no reordering)

## File Locations
- Active projects: `projects/[type]-projects/active/`
- Archived projects: `projects/[type]-projects/archived/`
- Templates: `projects/templates/`
- Overview: `projects/project-list.md`

---

*LRU Manager v1.0*
