# Project Management System - Auto-Trigger Protocol (SKILL.md)

*This file enables the Skill Plugin System to auto-trigger project management workflows.*

## Skill Metadata

```yaml
skill_name: "project-management"
feature: "Project-Management-System"
version: "1.0"
activated_by: "Skill Plugin System"
trigger_keywords: ["new", "project", "load", "save", "archive", "list projects"]
activation_modes: ["manual", "context-aware"]
```

---

## Activation Rules

### Manual Activation (User Types Command)

```
Pattern: "new [TYPE] project [NAME]"
Action: Execute new-project-protocol.md
Example: "new coding project Web-Dashboard"

Pattern: "load project [NAME]"
Action: Execute load-project-protocol.md
Example: "load project Wedding-Wall"

Pattern: "save project"
Action: Execute save-project-protocol.md
Example: "save project"

Pattern: "list projects"
Action: Display current LRU queue with status
Example: "list projects"

Pattern: "archive project [NAME]"
Action: Move project to archive, remove from active
Example: "archive project Old-Idea"
```

### Context-Aware Activation (Automatic)

```
Trigger 1: Project Mention
IF user mentions existing project name in conversation
THEN: Load project context in background (don't interrupt)

Trigger 2: Project Switch Signal
IF user says: "switch to", "move to", "work on", "focus on [PROJECT]"
THEN: Execute load-project-protocol with mentioned project

Trigger 3: Session End
IF session is ending AND user was working on a project
THEN: Suggest "save project" to persist progress
```

---

## Execution Phases

### Phase 1: Command Detection & Validation (5 seconds)

**Goal**: Parse user input and validate it's a project management command

**Steps**:
1. Extract command keyword: `new` / `load` / `save` / `archive` / `list`
2. Parse arguments: `[type]`, `[name]`
3. Validate command structure:
   - Is project type valid? (coding/writing/research/business)
   - Does project name exist or should be created?
   - Is user in a project context already?
4. **CHECKPOINT**: If invalid command, ask for clarification
5. Proceed to Phase 2 only if valid

**Error Handling**:
- Invalid type → List available types and ask to retry
- Invalid syntax → Show command format and example
- Missing arguments → Ask for required info

---

### Phase 2: Project Context Retrieval (10 seconds)

**Goal**: Load relevant project information from storage

**Steps**:
1. Load `projects/project-list.md` — Current LRU queue
2. Load `projects/lru-manager.md` — State of LRU system
3. Load `projects/[type]-projects/active/[name].md` — Project file (if exists)
4. Check timestamp on last access
5. **CHECKPOINT**: Verify project file is valid and not corrupted
6. Extract current state: goals, progress, status, technical stack

**What Gets Loaded**:
```
- Project Title & Type
- Description
- Status (Active/Paused/Blocked/Complete)
- Created Date
- Last Accessed Date
- Current Goals (next 3-5 items)
- Progress (recent milestones)
- Technical Stack (tools, languages, frameworks)
- Key Decisions (architecture choices)
- Blockers or Challenges (if any)
- Next Steps (planned work)
- Session Notes (free-form project notes)
```

---

### Phase 3: Workflow Execution (varies by command)

**For "new project [type] [name]":**
1. Load template: `projects/templates/[type]-template.md`
2. Ask user for description (1-2 sentences)
3. Create project file with template + description
4. Update LRU queue (position #1)
5. Check if 11 projects exist → archive oldest if yes
6. Save updated project-list.md and lru-manager.md
7. Confirm creation message

**For "load project [name]":**
1. Find project in active or archived list
2. Load project file and extract full context
3. Update "Last Accessed" to today
4. Reorder LRU queue (move to #1)
5. If 11+ projects, archive lowest ranked
6. Set AI context to this project
7. Provide brief status summary to user

**For "save project":**
1. Confirm active project exists (must be loaded)
2. Review current session work
3. Update project file with:
   - Session achievements
   - Technical decisions made
   - Blockers identified
   - Updated "Last Accessed"
   - New status if changed
4. Save updated project file
5. Update "Last Accessed" in project-list.md
6. Optional: Also save to diary if Save-Diary-System active

**For "list projects":**
1. Load project-list.md and lru-manager.md
2. Display positions 1-10 (active projects)
3. Show type breakdown
4. Show archived count
5. Show last 3 accessed dates

**For "archive project [name]":**
1. Locate project in active list
2. Move file from `active/` to `archived/`
3. Update status to "Archived (manual)"
4. Remove from active project-list
5. Update lru-manager.md
6. Confirm archival

---

### Phase 4: State Persistence (5 seconds)

**Goal**: Save all changes to persistent files

**Files Updated**:
- `projects/project-list.md` — New positions, counts
- `projects/lru-manager.md` — Updated LRU queue state
- `projects/[type]-projects/active/[name].md` — Project details
- `projects/[type]-projects/archived/[name].md` — If archived

**Commit Strategy**:
1. If Auto-Commit-System active: Auto-commit changes
2. If not: Changes persist but require manual Git push
3. Always sync to GitHub when user types "save"

---

### Phase 5: Feedback & Context Setup (2 seconds)

**Goal**: Confirm action and prepare for next user request

**For Create**:
```
"✅ Project created: [Name]
📁 Location: projects/[type]-projects/active/[Name].md
🎯 Let's start working on it! What's the first goal?"
```

**For Load**:
```
"✅ Loaded: [Name] (Position #1 in LRU)
📊 Status: [Status]
🎯 Last worked on: [Date]
💡 Next Steps: [Current next steps]

Ready to continue?"
```

**For Save**:
```
"✅ Project saved!
📝 Achievements this session: [List]
🔄 Status: [New status if changed]
⏰ Last accessed: Today

Great work!"
```

**For Archive**:
```
"✅ Archived: [Name]
📚 Now in: projects/[type]-projects/archived/
🔄 Can reload anytime with 'load project [name]'"
```

---

## Integration Checklist

### With Auto-Commit-System
- ✅ When project saved → auto-commit to Git
- ✅ Commit message includes project name and session summary
- ✅ Respects user's Git branch preferences

### With Save-Diary-System
- ✅ When "save project" runs → also add achievement to today's diary
- ✅ Links project name and milestone in diary entry
- ✅ Creates cross-reference: project ↔ diary

### With Library-System
- ✅ User can save reusable code/patterns while working on project
- ✅ Library items reference project origin
- ✅ Can suggest library patterns when creating new project

### With Memory-Consolidation-System
- ✅ When project archived → extract key learnings
- ✅ Create consolidated memory entry with project insights
- ✅ Link consolidated entry to project for future reference

---

## Guidelines

### For Project Creation
- Always ask for description (don't assume)
- Validate type exists before creating
- Use templates to maintain consistency
- Welcome user to project explicitly

### For Project Loading
- Provide concise status summary (3-5 lines max)
- Always show "last accessed" date for context
- Ask what user wants to do next
- Be ready to switch context smoothly

### For Project Saving
- Review achievements (don't just save empty state)
- Ask if status changed or new challenges arose
- Optionally create diary entry
- Confirm what was saved

### For LRU Management
- Keep top 10 projects active (no exceptions)
- Archive automatically when 11 reached
- Always preserve archived projects
- Never lose project data

---

## Troubleshooting During Execution

### Project File Corrupted
1. Try loading from backup
2. If no backup, ask user to recreate
3. Log incident to memory for prevention

### LRU Queue Desynchronized
1. Rebuild queue from project files
2. Verify all projects still exist
3. Re-sort by "Last Accessed" date

### Conflicting Project Name
1. Ask if user meant different project
2. Show list of similar names
3. Use full path to disambiguate

---

## Success Metrics

✅ Command recognized within 1 second  
✅ Project created/loaded within 5 seconds  
✅ Project context accurate and usable  
✅ All state changes persist to files  
✅ LRU queue maintains 10 active limit  
✅ No project data lost on archive  
✅ Auto-integrations (diary, commit) work seamlessly
