# 💾 Save Project Protocol
*Step-by-step protocol for saving current project progress*

## Trigger Command
```
"save project"
```
*Saves only the current active project, NOT the AI personality/memory*

> **Storage rule (updated Sep 3, 2026)**: ALL project information — PT and FT alike — is saved to the private `secret_information` repo, NEVER to MemoryCore. MemoryCore keeps only Yappy's own memory + a pointer to the project's secret_information files. Reason: MemoryCore's GitHub remote is a public fork.

## 📋 Execution Steps

### Step 1: Identify Active Project
- [ ] Check current-session.md for the active project (pointer only)
- [ ] If no active project:
  - [ ] Inform user "No active project to save"
  - [ ] Suggest loading or creating a project first
- [ ] If project exists, proceed to save

### Step 2: Gather Session Progress
- [ ] Collect work done in current session
- [ ] Capture any code changes, decisions, or milestones
- [ ] Note any issues resolved or discovered
- [ ] Document resources or references added

### Step 3: Update Project Files (in secret_information)
- [ ] Project detail lives at `secret_information/projects/[name]/` — files: `overview.md` (what/stack/repo/branch/mode), `changelog.md` (dated session history), `known-bugs.md`, plus topic files (`features.md`, `infrastructure.md`, `<topic>-integration.md`, etc.)
- [ ] Add a dated entry to `changelog.md` (or the applicable topic file):
  ```markdown
  ### [Current Date]
  - [Summary of session work]
  - [Key decisions made]
  - [Problems solved]
  - [Next steps identified]
  ```
- [ ] Update any changed sections (current tasks, issues, resources)
- [ ] Save the updated project files in secret_information

### Step 4: Update MemoryCore Pointer (name + link only)
- [ ] Update the pointer entry in MemoryCore (`projects/project-list.md` and/or current-session recap) using the canonical form:
  `[Project content moved to secret_information — see projects/[name]/[file].md]`
- [ ] **Never** copy project detail into MemoryCore — pointer only

### Step 5: Confirm Save
- [ ] Display confirmation:
  ```markdown
  ✅ Project Saved: [project name]
  📁 Location: secret_information/projects/[name]/
  ⏰ Saved at: [current time]
  📝 Session Progress:
  - [Brief summary of what was saved]

  Project progress has been preserved!
  ```

## 🎯 What Gets Saved

### For Coding Projects:
- Code changes and implementations
- Bug fixes and solutions
- Architecture decisions
- Dependencies added
- Testing progress

### For Writing Projects:
- New content written
- Revisions made
- Character/plot developments
- Research notes
- Word count progress

### For Research Projects:
- New findings
- Sources discovered
- Hypotheses tested
- Data collected
- Analysis progress

### For Business Projects:
- Client communications
- Decisions made
- Deliverables completed
- Budget updates
- Timeline changes

## 📊 Save Behavior Rules

1. **Explicit Save Only** - Only saves when user types "save project"
2. **Current Project Only** - Saves only the active project in session
3. **Project detail → secret_information** - MemoryCore holds pointer only
4. **No Auto-Save** - User controls when to save
5. **Independent from AI Save** - Doesn't trigger personality/memory save

## 🔄 Relationship with Other Commands

| Command | What It Saves | Protocol Used |
|---------|--------------|---------------|
| `save` | AI personality, user preferences, relationship memory | save-protocol.md |
| `save project` | Current project progress only (→ secret_information) | save-project-protocol.md (this) |
| `new project` | Auto-saves at creation (→ secret_information) | new-project-protocol.md |
| `load project` | Auto-saves last accessed time | load-project-protocol.md |

## Error Handling

- **No Active Project**: Clearly inform user and suggest next actions
- **Save Failure**: Attempt retry, inform user if persistent
- **Missing secret_information project dir**: Create `secret_information/projects/[name]/` with overview.md before saving detail

## 📝 Important Notes

- This protocol is **separate** from the main save-protocol.md
- Users can choose to save project, AI memory, or both
- Each save command has a specific, clear purpose
- No confusion or redundancy between save systems

---

*Save Project Protocol v1.1 (Sep 3, 2026 — project detail stored in secret_information; MemoryCore = pointer only)*
*Part of LRU Project Management System*
*Provides explicit project saving separate from AI memory saving*
