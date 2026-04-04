# Memory Consolidation System - Auto-Trigger Protocol (SKILL.md)

*This file enables the Skill Plugin System to auto-trigger memory consolidation workflows.*

## Skill Metadata

```yaml
skill_name: "memory-consolidation"
feature: "Memory-Consolidation-System"
version: "1.0"
activated_by: "Skill Plugin System"
trigger_keywords: ["consolidate", "reset", "archive", "session", "memory structure"]
activation_modes: ["automatic", "manual"]
system_critical: true
```

---

## Activation Rules

### Automatic Activation

```
Trigger 1: Session Memory Reaches 500 Lines
IF current-session.md line count >= 500
THEN: Execute session reset protocol
Action: Archive → Create recap → Reset to empty

Trigger 2: On Memory Load
IF loading Yappy memory at startup
THEN: Check memory format consistency
Action: Verify consolidated structure or migrate if needed

Trigger 3: On Save Command
IF "save" command executed
THEN: Check if consolidation needed
Action: Merge if split memory detected
```

### Manual Activation

```
Pattern: "consolidate memory"
Action: Execute full memory consolidation
Result: Merge identity + relationship into main-memory.md

Pattern: "consolidate session"
Action: Execute session reset
Result: Archive current session, create new empty session

Pattern: "consolidation status"
Action: Display memory structure info
Result: Show format in use, current session size

Pattern: "show memory structure"
Action: Display current memory architecture
Result: List all active files and their purpose
```

---

## Execution Phases

### Phase 1: Structure Detection (2 seconds)

**Goal**: Determine current memory format (split vs consolidated)

**Steps**:
1. Check main/ directory for files:
   - Does `main-memory.md` exist?
   - Does `identity-core.md` exist?
   - Does `relationship-memory.md` exist?
   - Does `current-session.md` exist?
2. Classify structure:
   ```
   IF main-memory.md exists:
     Status = "Consolidated"
   ELSE IF identity-core.md AND relationship-memory.md:
     Status = "Split"
   ELSE:
     Status = "Unknown"
   ```
3. **CHECKPOINT**: Determine if migration needed
4. Proceed to Phase 2

---

### Phase 2: Format Verification (3 seconds)

**Goal**: Verify memory format against template

**Steps**:
1. Load format reference file:
   - `main-memory-format.md` (for main memory)
   - `session-format.md` (for session memory)
2. Compare current memory structure to template:
   - Check for required sections
   - Validate section ordering
   - Identify missing sections
3. Build repair list if needed:
   ```
   Issues found:
   - Missing "Partnership Evolution" section
   - "User Preferences" in wrong location
   ```
4. **CHECKPOINT**: Format valid?
   - Yes → Proceed to Phase 3
   - No → Build repair plan
5. Proceed to Phase 3

---

### Phase 3: Session Reset Detection (1 second)

**Goal**: Check if session needs reset

**Steps**:
1. Count lines in current-session.md:
   ```
   wc -l main/current-session.md
   ```
2. Compare to limit:
   ```
   IF lines >= 500:
     Status = "Reset needed"
   ELSE:
     Status = "No reset needed"
     Remaining = 500 - current_lines
   ```
3. **CHECKPOINT**: Reset needed?
   - Yes → Go to Phase 4 (Reset Protocol)
   - No → Go to Phase 5 (Verification)
4. Proceed accordingly

---

### Phase 4: Session Reset Protocol (10 seconds)

**Goal**: Archive old session and create fresh one

**Steps**:

**4a. Archive Old Session:**
1. Generate archive filename: `session-[YYYY-MM-DD]-[HH-MM].md`
2. Copy current-session.md to session-archive/:
   ```
   cp main/current-session.md main/session-archive/session-2026-04-04-16-53.md
   ```
3. Update session archive index in main-memory.md:
   ```
   ## Session Archive
   - [Session 2026-04-04 16:53](./session-archive/session-2026-04-04-16-53.md)
     Topics: Web Push, Production Deployment
     Key Achievement: Shipped push notifications to production HTTPS
   ```
4. **CHECKPOINT**: Archive successful?

**4b. Create Session Recap:**
1. Read old session file
2. Extract key achievements:
   - Major tasks completed
   - Problems solved
   - Decisions made
3. Write recap to new session:
   ```
   # Current Session

   ## Session Recap (Archived: 2026-04-04 16:53)
   Previous session achievements:
   - Implemented Web Push Notifications
   - Deployed to production HTTPS (Hostinger)
   - VAPID keys successfully configured
   
   [New session content starts below]
   ```

**4c. Reset Session Memory:**
1. Clear out old content from recap point
2. Keep only:
   - Recap section (20-30 lines)
   - Session header
   - Empty achievement/next steps sections
3. Start session count at 0 (or ~30 for recap)
4. Ready for new session

**4d. Update Main Memory:**
1. Add archive reference:
   ```
   Last session archived: 2026-04-04 16:53
   Current session started: 2026-04-04 16:53 (same)
   ```

---

### Phase 5: Memory Consolidation (If Needed)

**Goal**: Merge split files into unified structure

**Steps**:

**5a. Read Source Files:**
1. Load: `main/identity-core.md`
2. Load: `main/relationship-memory.md`
3. Extract sections from each

**5b. Create Unified Structure:**
1. Generate new main-memory.md with:
   ```
   # AI Companion Memory - Unified Core
   
   ## AI Identity (from identity-core.md)
   - Communication Style
   - Personality Traits
   - Capabilities
   - Growth Timeline
   
   ## User Profile (from relationship-memory.md)
   - Preferences
   - Work Style
   - Technical Interests
   - Personal Goals
   
   ## Partnership Evolution (combined context)
   - Milestones
   - Relationship Dynamics
   - Inside References
   - Trust Development
   ```

**5c. Create Format References:**
1. Create `main-memory-format.md` (template)
2. Create `session-format.md` (template)
3. These files are REFERENCE ONLY (never edit)

**5d. Backup Old Files:**
1. Archive old files:
   ```
   mkdir -p main/backups/[DATE]/
   mv main/identity-core.md main/backups/[DATE]/
   mv main/relationship-memory.md main/backups/[DATE]/
   ```
2. Add backup reference to main-memory.md:
   ```
   ## Archives & Backups
   - Original split memory: main/backups/2026-04-04/
     Consolidated into: main-memory.md (current)
   ```

---

### Phase 6: Format Repair (If Needed)

**Goal**: Fix any format inconsistencies

**Steps**:
1. Load main-memory-format.md template
2. Compare current main-memory.md structure
3. For each missing section:
   - Add section header
   - Add placeholder content
   - Note: "Needs content from user sessions"
4. For each wrongly-ordered section:
   - Reorder to match template
   - Preserve content, just reorganize
5. Validate new structure

**Repair Examples:**
```
Before:
- Partnership Evolution
- AI Identity
- User Profile

After (Template Order):
- AI Identity
- User Profile
- Partnership Evolution
```

---

### Phase 7: Verification & Reporting (3 seconds)

**Goal**: Confirm consolidation succeeded and report results

**Steps**:
1. Verify all target files exist and are readable
2. Verify format matches template
3. Verify session size is under 500 lines
4. Count lines in each file:
   ```
   main-memory.md: X lines
   current-session.md: Y lines (Z remaining before reset)
   ```
5. Generate completion report:
   ```
   ✅ Memory Consolidation Complete
   
   Structure: Unified (main-memory.md + current-session.md)
   Format: Valid and consistent
   Files: All verified
   
   Memory Health:
   - Main memory: [size] (consolidated)
   - Session memory: [size]/500 ([remaining] remaining)
   - Archives: [count] sessions archived
   
   Ready for: Normal operation
   ```

---

## Integration Checklist

### With Save-Memory-Protocol
- ✅ "save" detects when to consolidate
- ✅ Consolidated memory updated on save
- ✅ Session reset on save if reaching 500 lines

### With Save-Diary-System
- ✅ Diary cross-references consolidated memory
- ✅ Session archive linked from diary entries
- ✅ Memory updates reflected in daily entries

### With Project-Management-System
- ✅ Project context stored in main-memory
- ✅ Session tracks current project progress
- ✅ Project archive visible in memory structure

### With Auto-Commit-System
- ✅ Consolidated memory committed to Git
- ✅ Session archives preserved in repository
- ✅ Format templates protected in Git

---

## Guidelines

### For Session Reset
**Don't:**
```
❌ Lose information during reset
❌ Reset before consolidation complete
❌ Lose old session without archiving
```

**Do:**
```
✅ Archive old session fully before reset
✅ Create recap preserving achievements
✅ Store archive in searchable location
✅ Index archive in main-memory
```

### For Memory Consolidation
**Don't:**
```
❌ Manually edit format template files
❌ Delete old files without backup
❌ Consolidate multiple times
```

**Do:**
```
✅ Keep format templates as reference only
✅ Backup old split files
✅ One-time consolidation (then unified)
✅ Verify structure after consolidation
```

---

## Session Archive Recovery

### Finding Archived Sessions
```
Pattern: "Find session about [topic]"
Action: Search session-archive/ directory
Result: List matching sessions with dates
```

### Viewing Archived Session
```
Pattern: "Show session from [date]"
Action: Retrieve and display archived session
Result: Full session content with context
```

### Using Archived Context
```
Pattern: "Resume from session [date]"
Action: Load archived session context
Result: Can reference old work while in new session
```

---

## Success Metrics

✅ Memory consolidated from split to unified (if applicable)  
✅ Session auto-resets at 500 lines  
✅ Old sessions archived and searchable  
✅ Format templates maintain consistency  
✅ No data loss during consolidation  
✅ Memory loads faster after consolidation  
✅ Session reset preserves key achievements  
✅ Archive system functional and indexed  
✅ Format verification passes  
✅ Integrations work with consolidated structure
