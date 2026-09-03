# 🆕 New Project Protocol
*Step-by-step protocol for creating and managing new projects with LRU*

## Trigger Command
```
"new [type] project [name]"
```
Examples: "new coding project API-Dashboard", "new writing project Chapter-5"

## 📋 Execution Steps

### Step 1: Parse Command
- [ ] Extract project type from command (coding/writing/research/business)
- [ ] Extract project name from command
- [ ] Validate project type exists in system
- [ ] Check if project name already exists

### Step 2: Gather Project Details
- [ ] Ask user for brief description (1-2 sentences)
- [ ] Capture current date and time
- [ ] Note any initial requirements or goals
- [ ] Identify primary technologies/tools (if coding project)

### Step 3: Create Project Files (in secret_information)
- [ ] Create `secret_information/projects/[name]/` with:
  - [ ] `overview.md` — what it is, type, description, tech stack, repo/branch, mode (FT/PT), status, created date
  - [ ] `changelog.md` — empty, dated session history starts here
  - [ ] `known-bugs.md` — empty
  - [ ] Topic files as needed (features.md, infrastructure.md, integrations)
- [ ] Record a **pointer only** in MemoryCore `projects/project-list.md` (`[name] → secret_information/projects/[name]/`)
- [ ] Note in current-session.md: active project = pointer to secret_information (no content copy)

### Step 5: Confirm Creation
- [ ] Display success message:
  ```markdown
  ✅ Project Created: [name]
  📁 Type: [type]
  📍 Location: secret_information/projects/[name]/
  📝 Description: [description]

  Project files created — detail lives in secret_information, pointer added to MemoryCore.
  ```

## 📊 LRU Rules
1. Project detail always lives in secret_information (never removed by LRU)
2. MemoryCore pointer list is capped; archiving a pointer never deletes the project
3. Archived projects can be reloaded anytime from secret_information

## 🗂️ Project File Structure (in secret_information)
```text
secret_information/projects/[name]/
├── overview.md      what it is, stack, repo/branch, mode (FT/PT), status
├── changelog.md     dated session history (all work log)
├── known-bugs.md    open/fixed bugs
└── <topic>.md       features, infrastructure, integrations (as needed)

MemoryCore pointer (only): [Project content moved to secret_information —
                             see projects/[name]/overview.md]
```

## Error Handling
- If project name exists: Suggest alternative or ask to load existing
- If type invalid: Show available types and ask again

---

*New Project Protocol v1.1 (Sep 3, 2026 — project files created in secret_information; MemoryCore holds pointer only)*
*Part of Project Management System*
