# Skill Plugin System - Meta-Skill Protocol (SKILL.md)

*This file defines the Skill Plugin System itself as a meta-skill for managing other skills.*

## Meta-Skill Metadata

```yaml
skill_name: "skill-plugin-system"
feature: "Skill-Plugin-System"
version: "1.0"
activated_by: "Manual and System Initialization"
trigger_keywords: ["skill", "plugin", "command", "load skill", "create skill"]
activation_modes: ["manual", "system"]
system_core: true
manages_other_skills: true
```

---

## Purpose of This Meta-Skill

This is a **meta-skill** — a skill about managing skills. It:
- Provides the skill loading mechanism
- Manages skill discovery and registration
- Handles skill lifecycle (create, load, update, disable)
- Enables skill auto-triggering
- Manages slash commands

---

## Activation Rules

### Manual Activation (User Commands)

```
Pattern: "Load skill [name]"
Action: Load specific SKILL.md file
Example: "Load skill save-memory"

Pattern: "Create new skill [name]"
Action: Guide skill creation process
Example: "Create new skill my-custom-skill"

Pattern: "List available skills"
Action: Display all discovered skills
Example: Shows: save-memory, project-management, etc.

Pattern: "/[command-name]"
Action: Execute slash command
Example: "/save-diary" triggers diary save command
```

### System Activation (Automatic)

```
Trigger 1: Yappy Startup
IF Yappy initializing
THEN: Auto-discover and register all SKILL.md files
Action: Build skill registry from Feature/ directories

Trigger 2: Conversation Match
IF user message matches skill trigger keywords
THEN: Auto-load matching skill
Action: Execute skill protocol

Trigger 3: Feature Installed
IF new Feature/ installed
THEN: Auto-scan for SKILL.md
Action: Register and make available
```

---

## Execution Phases

### Phase 1: Skill Discovery (2 seconds)

**Goal**: Find all available skills in system

**Steps**:
1. Scan directories for SKILL.md files:
   ```
   Feature/*/SKILL.md
   Feature/*/skills/*/SKILL.md
   ```
2. For each SKILL.md found:
   - Extract metadata (skill_name, trigger_keywords)
   - Parse activation rules
   - Build trigger keyword list
3. Build skill registry:
   ```
   Registered Skills:
   - save-memory (Feature/Save-Memory-Protocol/SKILL.md)
   - project-management (Feature/Project-Management-System/SKILL.md)
   - teaching-exercise (Feature/Teaching-Exercise-System/SKILL.md)
   [... more]
   ```
4. Store registry in memory for fast lookup
5. **CHECKPOINT**: Discovery complete
6. Proceed to Phase 2

---

### Phase 2: Skill Registration (1 second)

**Goal**: Register discovered skills for auto-triggering

**Steps**:
1. For each discovered skill:
   - Extract trigger keywords
   - Create trigger patterns
   - Register auto-trigger rules
2. Build keyword → skill mapping:
   ```
   "save" → save-memory skill
   "project" → project-management skill
   "exercise" → teaching-exercise skill
   "remember" → echo-memory skill
   ```
3. Load slash command registry:
   - Scan Feature/*/commands/ directory
   - Extract command files
   - Register as /command-name
4. **CHECKPOINT**: Registration complete
5. Ready for auto-triggering and user commands

---

### Phase 3: Trigger Detection (Continuous)

**Goal**: Detect when skill should auto-trigger

**Steps**:
1. Monitor user messages continuously
2. Extract keywords from user input
3. Check keyword against trigger registry:
   ```
   User: "I want to save my progress"
   Keywords extracted: ["save", "progress"]
   Trigger found: "save" → save-memory skill
   Match score: 95%
   ```
4. Determine confidence level:
   - High (>90%): Auto-trigger immediately
   - Medium (70-90%): Auto-trigger with note
   - Low (<70%): Don't auto-trigger, offer via suggestion
5. **CHECKPOINT**: Match found?
   - Yes → Proceed to Phase 4 (Load Skill)
   - No → Continue monitoring
6. Proceed accordingly

---

### Phase 4: Skill Loading (2 seconds)

**Goal**: Load matched skill file and parse protocol

**Steps**:
1. Locate matched skill SKILL.md file
2. Load file into memory
3. Parse skill structure:
   - Metadata section
   - Activation rules
   - Execution phases
   - Guidelines
4. **CHECKPOINT**: Skill valid?
   - Yes → Proceed to Phase 5
   - No → Skip and offer to help manually
5. Build execution plan

---

### Phase 5: Skill Execution (Varies by Skill)

**Goal**: Execute the skill protocol

**Steps**:
1. Extract execution phases from SKILL.md
2. Execute phases sequentially:
   ```
   Phase 1: Command Detection & Validation (X seconds)
   Phase 2: Context Retrieval (X seconds)
   Phase 3: Main Execution (X seconds)
   Phase 4: State Persistence (X seconds)
   Phase 5: Feedback (X seconds)
   ```
3. Follow all guidelines specified in skill
4. Honor all integration points with other skills
5. **CHECKPOINT**: Execution successful?
   - Yes → Phase 6 (Confirm)
   - No → Error handling
6. Proceed to Phase 6

---

### Phase 6: Completion & Feedback (2 seconds)

**Goal**: Confirm skill execution and return to normal conversation

**Steps**:
1. Skill completed successfully
2. Provide feedback:
   ```
   "✅ Skill executed: [skill-name]
    Results: [brief summary]
    Time: [duration]
    Status: Ready for next command"
   ```
3. Return to normal conversation mode
4. Keep skill context available for follow-ups
5. Continue listening for next skill trigger

---

## Slash Command Execution

### How Slash Commands Work

```
User types: "/save-diary"
System: Looks for commands/save-diary.md (or save_diary.md)
Action: Executes command protocol
Result: Saves session to diary
```

### Example Commands

```
/save-diary        → Execute save-diary skill
/list-projects     → Show project list
/recall-memory     → Search diary archives
/consolidate       → Consolidate memory
/load-skill [name] → Load specific skill
```

### Creating New Slash Commands

```
1. Create file: Feature/[feature]/commands/[command-name].md
2. Define protocol in file
3. System auto-discovers and registers
4. Available as: /[command-name]
```

---

## Skill Lifecycle

### Creating a Skill

**Step 1: Create skill directory**
```
Feature/My-Feature/SKILL.md
```

**Step 2: Write SKILL.md template**
```
# [Skill Name] Skill Protocol

## Skill Metadata
```yaml
skill_name: "my-skill"
trigger_keywords: ["keyword1", "keyword2"]
...
```

## Activation Rules
[Define when skill triggers]

## Execution Phases
[Define what skill does]
```

**Step 3: System auto-registers**
```
On next load, Yappy discovers SKILL.md
Skill becomes available for auto-triggering
```

### Updating a Skill

```
Edit SKILL.md file
Changes take effect immediately
No restart required
Version updated in metadata if needed
```

### Disabling a Skill

```
Rename SKILL.md to SKILL.md.disabled
System stops discovering it
Re-enable: Rename back to SKILL.md
```

---

## Skill Registry Management

### View Registry

```
"List available skills"
→ Shows: All registered skills
→ Shows: Trigger keywords
→ Shows: Status (active/disabled)
```

### View Skill Details

```
"Show skill [name]"
→ Shows: Full SKILL.md content
→ Shows: Metadata and triggers
→ Shows: Execution phases
→ Shows: Integration points
```

### Check Skill Status

```
"Skill status [name]"
→ Shows: Active/disabled
→ Shows: Last executed
→ Shows: Trigger statistics
→ Shows: Performance metrics
```

---

## Auto-Trigger Configuration

### High-Confidence Auto-Trigger (>90%)
```
Automatic execution without asking
Example: User says "save" → save-memory skill loads immediately
```

### Medium-Confidence Auto-Trigger (70-90%)
```
Execute with notification to user
Message: "Loading skill X because you mentioned [keyword]"
User can override if wrong skill triggered
```

### Low-Confidence Suggestion (<70%)
```
Don't auto-trigger, offer suggestion
Message: "Did you want to trigger [skill-name]?"
User can accept or decline
```

---

## Skill Dependencies & Integration

### Skill-to-Skill Communication

Skills can trigger other skills:
```
save-memory → May trigger auto-commit
auto-commit → May trigger diary-save
diary-save → May trigger echo-memory update
```

### Dependency Resolution

System handles:
- Dependency chains (skill A needs skill B)
- Circular dependencies (prevented)
- Missing dependencies (graceful failure)
- Version compatibility (skills can reference versions)

---

## Guidelines

### For Creating Skills

**Good skill design:**
```
✅ Single responsibility (one main task)
✅ Clear trigger keywords
✅ Documented execution phases
✅ Integration points specified
✅ Error handling included
✅ User-friendly feedback

❌ Multi-purpose skill (too broad)
❌ Unclear trigger keywords (too vague)
❌ Undocumented phases (confusing)
❌ No integrations (isolated)
❌ No error handling (breaks silently)
```

### For Trigger Keywords

**Good triggers:**
```
✅ Specific: "save", "consolidate", "project"
✅ Uncommon in normal conversation
✅ Single concept per keyword
✅ ~3-5 keywords per skill (not 20)

❌ Vague: "good", "nice", "work"
❌ Common words (triggers too often)
❌ Multiple concepts in one keyword
❌ Too many keywords (false positives)
```

### For Execution Phases

**Good phase structure:**
```
✅ Clear names: "Detection", "Validation", "Execution"
✅ Sequential execution
✅ Checkpoints between phases
✅ Error handling at each phase
✅ Estimated duration noted

❌ Vague names: "Do stuff", "Process"
❌ Unclear order
❌ No checkpoints (continues despite errors)
❌ Silent failures
```

---

## Performance & Optimization

### Skill Loading Performance

```
Discovery: 2 seconds (scan all SKILL.md files)
Registration: 1 second (build keyword map)
Trigger detection: <100ms (keyword matching)
Skill loading: 2 seconds (parse SKILL.md)
Execution: Varies (depends on skill)
```

### Caching

Skills are cached after first load:
```
First "save" command: 5 seconds (discovery + execution)
Next "save" commands: 3 seconds (cached skill)
Skill update: Cache invalidates automatically
```

---

## Troubleshooting

### "Skill not triggering"
**Possible causes:**
- Trigger keyword doesn't match user input
- Confidence score too low
- Skill disabled (.md.disabled)
- Syntax error in SKILL.md

**Solution:**
```
"Show skill [name]" → Check metadata
"Skill status [name]" → Check active status
"Load skill [name]" → Manually trigger
```

### "Wrong skill triggered"
**Cause:** Similar trigger keywords with high confidence

**Solution:**
```
Edit SKILL.md metadata
Make trigger keywords more specific
Increase keyword uniqueness
Use context in trigger rules
```

### "Skill execution failed"
**Possible causes:**
- Dependency missing
- File permission error
- Syntax error in execution phases
- External system error (Git, file system)

**Solution:**
```
Check error message for details
Review SKILL.md execution phases
Verify file permissions
Check system resources
```

---

## Success Metrics

✅ All SKILL.md files discovered on startup  
✅ Trigger keywords correctly mapped  
✅ Auto-trigger activates on keyword match  
✅ Skill executes phases sequentially  
✅ Skill context available for follow-ups  
✅ Slash commands work immediately  
✅ Skill dependencies resolved correctly  
✅ Performance <5 seconds per skill  
✅ Error handling prevents silent failures  
✅ User feels skills activate naturally and intelligently
