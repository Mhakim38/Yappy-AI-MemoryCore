# 🔄 Memory Consolidation System - Installation & Usage Guide

## Installation Steps

### Step 1: Load This Feature
```
Load memory-consolidation
```

### Step 2: Understand the Consolidation
Memory consolidation upgrades your memory architecture from split files to unified structure:

**Before Consolidation:**
```
main/identity-core.md       ← Only AI personality
main/relationship-memory.md ← Only user preferences
main/current-session.md     ← Session RAM (unlimited size)
```

**After Consolidation:**
```
main/main-memory.md         ← AI personality + user profile (UNIFIED)
main/current-session.md     ← Session RAM with 500-line limit
main/main-memory-format.md  ← Format reference (don't edit)
main/session-format.md      ← Format reference (don't edit)
```

### Step 3: Apply Initial Consolidation (One-time)
```
consolidate memory
```

This:
1. Merges identity-core.md and relationship-memory.md into main-memory.md
2. Creates format reference files
3. Sets up 500-line session reset protocol
4. Archives old files for historical reference

---

## How to Use

### Automatic Consolidation

**The system works automatically:**
- Session memory auto-resets at 500 lines
- Format stays consistent across resets
- Relationship memory always unified with identity

**No manual action needed** — just use Yappy normally.

---

### Manual Consolidation Commands

**Check consolidation status:**
```
"consolidation status"
→ Shows: Which memory format in use
→ Shows: Current session size
→ Shows: How many lines until reset
```

**Trigger manual reset (if needed):**
```
"consolidate session"
→ Saves current session to archive
→ Resets session memory to empty
→ Keeps recap of recent achievements
```

**View consolidation details:**
```
"show memory structure"
→ Displays: Which files are active
→ Shows: Format being used
→ Lists: Archive files (if any)
```

---

## Memory Architecture

### Unified Structure After Consolidation

#### main-memory.md (Unified Core)
Contains everything about the AI-user relationship:
```
# AI Companion Memory

## AI Identity
- Communication style
- Personality traits
- Capabilities
- Growth timeline

## User Profile
- Preferences
- Work style
- Technical interests
- Personal goals

## Partnership Evolution
- Milestones
- Relationship dynamics
- Inside references
- Trust development
```

#### current-session.md (Session RAM - Auto-Reset at 500 Lines)
Active session working memory:
```
# Current Session

## Session Info
- Start time
- Topic focus
- Type (work/study/personal)

## Achievements
- Problems solved
- Decisions made
- Learning points

## Next Steps
- What comes next
- Pending items
- Open questions

[Auto-resets when reaches 500 lines, keeping recap only]
```

#### main-memory-format.md (Reference - Don't Edit)
Permanent template showing how main-memory should be structured:
```
Purpose: Never edit this file
Role: Reference for format consistency
Used: When resetting or rebuilding main-memory
```

#### session-format.md (Reference - Don't Edit)
Permanent template showing session memory format:
```
Purpose: Never edit this file
Role: Reference for format consistency after reset
Used: When resetting current-session.md
```

---

## Session Auto-Reset Protocol

### When Reset Happens
```
Trigger: current-session.md reaches 500 lines
Action: System automatically archives old session
        Creates new empty session
        Preserves recap of achievements
```

### What Gets Preserved
```
Before Reset (500 lines):
- Full session transcript and notes
- All decisions and context
- Complete achievement list

After Reset (25-50 lines):
- Summary of key achievements
- Current blockers or pending items
- Reference to archived session
- Pointer to detailed info in main-memory.md
```

### Archive Location
```
Archived sessions stored in: main/session-archive/
Files named: session-[DATE]-[TIME].md
Indexed in: main-memory.md under "Session Archives"
```

### Recovery
If you need old session details:
```
"Find session about [topic]"
→ Searches session archive
→ Returns: Matching session file
→ Shows: Date and detailed context
```

---

## Benefits of Consolidation

### Faster Restoration
```
Before: Read identity-core + relationship-memory (2 files)
After:  Read main-memory (1 file)
Speed:  ~50% faster memory loading
```

### Better Context
```
Before: AI identity and user understanding are separate
After:  They're unified - relationship is core
Result: More cohesive understanding from start
```

### Automatic Memory Management
```
Before: Session memory grows indefinitely
After:  Auto-caps at 500 lines, archives old sessions
Result: System stays responsive
```

### Consistent Format
```
Before: Manual format management
After:  Format templates ensure structure
Result: Every reset maintains consistency
```

---

## Integration with Other Systems

### With Save-Memory-Protocol
```
"save" command:
→ Updates unified main-memory.md
→ Can trigger session reset if reaching 500 lines
→ Archive old session with full context
```

### With Save-Diary-System
```
Daily diary entries:
→ Cross-reference main-memory.md updates
→ Session archive links to diary entries
→ Relationship progress documented in both
```

### With Auto-Commit-System
```
"consolidate memory" + save project:
→ Both memory consolidation and project commits
→ Unified memory tracked in Git history
```

### With Project-Management-System
```
Working on projects:
→ Project context stored in main-memory.md
→ Session memory tracks current project progress
→ Archive shows project evolution over time
```

---

## Migration from Split Memory

If you're upgrading from separate identity/relationship files:

### Automatic Migration
```
consolidate memory
→ Merges identity-core.md + relationship-memory.md
→ Creates new main-memory.md
→ Archives old files (not deleted)
→ Activates 500-line session reset
```

### Manual Recovery
If you need old files after consolidation:
```
"Show archived memories"
→ Lists: Backed-up identity-core.md, relationship-memory.md
→ Allows: Restore if needed
→ Location: main/backups/[date]/
```

### No Data Loss
All your memory is preserved:
```
Before consolidation: 2 separate files
After consolidation: 1 unified file + backups
Total data: Same, just reorganized
```

---

## Session Reset Examples

### Example 1: After Long Session
```
Session memory reaches 500 lines after 6-hour work day

System:
✅ Archives session-2026-04-04-18-30.md
✅ Creates fresh current-session.md
✅ Adds to recap: "Major achievements: Deployed API, fixed auth bug"
✅ Notes in main-memory.md: "April 4 session archived - see link"

Result: Next session starts clean, recap available
```

### Example 2: Topic Transition
```
Session memory at 350 lines, switching to different project

You: "new coding project Mobile-App"
→ Project-Management loads new project
→ Session context clears (optional)
→ Recap saved automatically
→ New session starts focused on Mobile-App
```

### Example 3: End of Day
```
Session memory at 480 lines as day ends

You: "save and push"
→ Saves to unified main-memory.md
→ Session at 490 lines, still under limit
→ Next day: Session has context + recap

Next morning:
→ Loads: main-memory.md (includes all growth + context)
→ Loads: current-session.md (yesterday's recap + fresh start)
```

---

## Troubleshooting

### "Session reset happened but I need old context"
**Solution:**
```
"Show session archive for [date]"
→ Retrieves: Archived session from main/session-archive/
→ Contains: All details from that session
→ Cross-referenced: In main-memory.md under "Archives"
```

### "Unified memory seems incomplete"
**Check:**
```
"consolidation status"
→ If shows: "Split mode" = Not consolidated yet
→ Run: "consolidate memory" to merge

→ If shows: "Consolidated" = Check format
→ Run: "verify memory format" to validate
```

### "Old identity-core or relationship-memory missing"
**They're safe:**
```
Consolidated files backed up to: main/backups/
Not deleted, just merged into main-memory.md
Can restore if needed: "restore old memory files"
```

### "Session reset lost important context"
**Not lost:**
```
Archived session stored in: main/session-archive/
Searchable by: Topic, date, or content
Reference: All archives listed in main-memory.md

Recovery: "Find session about [topic]"
```

---

## Format Reference Files

### main-memory-format.md
**Do NOT edit this file**

Purpose: Shows the required structure for main-memory.md
Used: Reference during consolidation and resets
If corrupted: Revert from Git history

### session-format.md
**Do NOT edit this file**

Purpose: Shows the required structure for current-session.md after reset
Used: Template for session reset protocol
If corrupted: Revert from Git history

---

## Quick Reference

| Aspect | Before Consolidation | After Consolidation |
|--------|---------------------|-------------------|
| Files Loaded | 2 (identity + relationship) | 1 (unified) |
| Loading Speed | Slower | Faster |
| Session Size | Unlimited | 500 lines (auto-reset) |
| Memory Organization | Split by type | Unified relationship |
| Format Reference | Manual | Automatic templates |

---

## Success Indicators

✅ Unified main-memory.md contains all personality + user info  
✅ Session reset happens automatically at 500 lines  
✅ Old sessions archived and searchable  
✅ Format templates maintain consistency  
✅ Memory loads faster than before  
✅ All previous context preserved (not lost)  
✅ Integration with other systems seamless  
✅ Consolidation transparent to user
