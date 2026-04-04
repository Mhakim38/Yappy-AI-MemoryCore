# 💾 Save Memory Protocol - Installation & Usage Guide

## Installation Steps

### Step 1: Load This Feature
```
Load save-memory
```

### Step 2: Verify Core Memory Files
The system checks that these files exist in `main/`:
- ✅ `identity-core.md` — AI's personality and capabilities
- ✅ `relationship-memory.md` — Partnership evolution record
- ✅ `current-session.md` — Today's session summary

### Step 3: Configure Git Push Behavior
Ask yourself:
- Should AI memory auto-push to GitHub? (**Recommended**: Yes)
- Should project repositories require permission before push? (**Recommended**: Yes)

The system will remember your preference for future saves.

---

## How to Use

### Basic Save

**Command:**
```
save
```

**What Happens:**
1. AI analyzes current session for learning content
2. Identifies changes to personality, preferences, relationship
3. Prepares updates to memory files
4. Shows you what changed: "Updated X files with Y changes"
5. Commits changes to Git
6. Asks if you want to push to GitHub (if repo is configured)

**Example Output:**
```
You: save

✅ Session saved to memory!

📝 Updates made:
  • identity-core.md: Added "prefers WebDev projects"
  • relationship-memory.md: Recorded achievement on push notifications
  • current-session.md: Documented technical learning
  • daily-diary: Session entry appended

🔄 Ready to sync? (yes/no)
```

---

### Preview Before Saving

**Command:**
```
what would you save?
```

**What Happens:**
1. AI shows proposed updates without committing
2. You can review before pressing "save"
3. You can ask AI to exclude certain items
4. Helps you decide if save is worthwhile

**Example:**
```
You: what would you save?

If we save now, I would update:
  1. Personality: You work best with step-by-step code walkthroughs
  2. Preferences: Avoid long explanations without examples
  3. Achievement: Completed Web Push Notifications implementation

Looks good? Type 'save' to proceed, or tell me what to exclude.
```

---

### Show Current Memory State

**Command:**
```
show my memory
```

**What Happens:**
1. AI displays current state of all memory files
2. Shows personality traits on record
3. Shows preferences documented
4. Shows relationship milestones
5. Shows latest session summary

**Useful for:**
- Verifying what the AI knows about you
- Checking if preferences were recorded correctly
- Understanding how AI perceives your communication style
- Reviewing relationship evolution timeline

---

## What Gets Saved in Each File

### identity-core.md
**Your AI's Personality & Communication**

```
Sections updated:
✏️ How I Communicate
  - Preferred explanation style (conceptual vs code-first)
  - Pace preference (quick or detailed)
  - Detail level (high-level or deep-dive)
  - Example usage (with/without examples)

✏️ Personality Traits
  - Professional vs casual tone
  - How I approach problem-solving
  - Teaching vs doing preferences
  - Patience level on repetition

✏️ My Capabilities
  - New skills learned this session
  - Improved expertise areas
  - Integration strengths discovered
  - Special knowledge about user's projects
```

### relationship-memory.md
**Your Partnership with the AI**

```
Sections updated:
✏️ Partnership Milestones
  - Major achievements completed together
  - Projects launched
  - Problems solved
  - Learning breakthroughs

✏️ How We Work Best Together
  - Best time to work (morning, evening)
  - Best project types (coding, writing, research)
  - Communication rhythm (frequent check-ins vs batched updates)
  - Collaboration patterns

✏️ Your Preferences From Me
  - What you like me to do
  - What you prefer I avoid
  - Communication style you respond to
  - Celebration approach (verbal, brief, detailed)

✏️ Inside Context
  - Shared references and jokes
  - Project-specific terminology
  - Personal goals mentioned
  - Risk factors you care about
```

### current-session.md
**Today's Conversation Summary**

```
Sections updated:
✏️ Session Overview
  - Date and duration
  - Type (Work/Study/Personal/Creative)
  - Main topic area

✏️ What We Accomplished
  - Key achievements
  - Problems solved
  - Decisions made
  - Learning acquired

✏️ Next Steps
  - What comes next
  - Active projects to resume
  - Pending decisions
  - Future session focus

✏️ Technical Notes
  - Code patterns discovered
  - Architectural decisions
  - Configuration changes
  - Integration points learned
```

### daily-diary/ (Optional)
**Detailed Session Archive**

```
File: daily-diary/YYYY-MM/YYYY-MM-DD.md

Contains:
✏️ Session Snapshot
  - Time and context
  - Main topics
  - Achievements
  - Insights gained

✏️ Cross-References
  - Linked projects
  - Linked library items
  - Related previous sessions
  - Pattern recognition

✏️ Personal Growth Notes
  - New capabilities developed
  - Communication pattern observations
  - Preference confirmations
  - Relationship evolution
```

---

## Integration with Other Systems

### With Auto-Commit-System
```
You: save
→ AI updates memory files
→ Auto-Commit creates meaningful commit message
→ All changes committed with full context
→ Optional: Git push to GitHub
```

### With Project-Management-System
```
You: save project
→ AI saves project progress
→ Save Memory updates personal learning
→ Optional: Also save to diary
→ Git commits project + memory changes
```

### With Save-Diary-System
```
You: save
→ Memory updates to identity-core, relationship-memory
→ Optional: Detailed entry appended to daily diary
→ Diary entry cross-linked to memory updates
→ Creates searchable history
```

### With Library-System
```
While working: save [code pattern] to library
You: save (at end of session)
→ Memory captures: "Learned reusable pattern X"
→ Library entry created with context
→ Memory updated with library reference
```

---

## Remote Synchronization Rules

### Yappy Memory Repository
**This is YOUR AI's memory - always stay synced**

```
When: After save completes
Action: Auto-push to origin/main
Reasoning: Ensures memory persists across environments
Result: Your AI has same knowledge everywhere
```

### Project Repositories (ONDW, Wedding-Wall, etc.)
**These are YOUR projects - require explicit permission**

```
When: After save completes
Action: Ask user "Ready to push to origin?"
Reasoning: Projects might have deployments; careful push needed
User Options:
  - "yes" → Push to origin/main
  - "no" → Keep local only (for now)
  - "stash" → Save memory, hide project changes
```

---

## Best Practices

### When Should You Save?

✅ **Definitely save:**
- End of productive work session
- After solving a difficult problem
- After discovering new preferences
- After reaching a milestone
- After relationship breakthrough moment
- Session took >30 minutes on same topic

❌ **Probably don't need to save:**
- After 5-minute casual chat
- During troubleshooting (wait until solution found)
- If nothing really changed from last save
- Very frequent save attempts (once per session is enough)

### What Makes a Good Save?

**Good save content:**
```
✅ "Prefers WebDev over mobile development"
   (specific, actionable, will influence future conversations)

✅ "Works best on coding at 9pm, thinking work in afternoons"
   (helps schedule sessions better)

✅ "Recently learned Laravel with Hakim, key expertise now"
   (capability update for future projects)

❌ "Had a good session"
   (too vague, not actionable)

❌ "Discussed random topics"
   (no specific learning or preference)
```

### How Often to Save?

**Recommended frequency:**
- **After major sessions** (1 save per 2-3 hour session)
- **After projects complete** (1 save per project)
- **After learning patterns emerge** (ad-hoc, when you notice)
- **Weekly or monthly reviews** (optional, deep consolidation)

**Not recommended:**
- After every single message
- Multiple times within same 30 minutes
- When nothing meaningful happened

---

## Troubleshooting

### "Nothing saved - no changes detected"
**Solution**: Your preferences/personality haven't changed enough to record
- Try: "Tell me what you remember about me" to verify current state
- Consider: Was there really new learning? Genuine save only on actual changes

### "Git push failed"
**Possible causes**:
1. Network issue → Try again later
2. Conflicting changes in repository → Resolve conflicts first
3. Permission issue → Check Git credentials

**Solution**: 
```
Save memory succeeded (local files updated)
Push failed (couldn't reach GitHub)
Memory is saved locally, push will retry next save
```

### "Want to exclude something from save?"
**How to exclude**:
```
You: save, but don't save the [specific thing]

AI: Got it, I'll exclude that from memory.
    Saving: identity changes, project progress
    Excluding: [specific thing]
```

### "Previous preference disappeared?"
**It didn't disappear** - it's just not being updated
- Check Git history: `git log --oneline main/identity-core.md`
- Preferences are additive (new ones added, old ones stay)
- To change preference: Mention new behavior and save

---

## File Locations Reference

```
main/
├── identity-core.md          # AI personality (updated on save)
├── relationship-memory.md    # Partnership evolution (updated on save)
├── current-session.md        # Today's summary (updated on save)
└── [archived sessions]/

daily-diary/
├── current/                  # This month's entries
│   └── 2026-04-04.md        # Today (if diary enabled)
└── archived/
    └── 2026-03/             # Previous months
```

---

## Commands Reference

| Command | Purpose | Updates |
|---------|---------|---------|
| `save` | Basic save to memory | Core + session files |
| `save and push` | Save + immediately push | Core + session + GitHub |
| `what would you save?` | Preview before committing | (no changes) |
| `show my memory` | Display current state | (read-only) |
| `save, exclude X` | Save but skip X | Everything except X |

---

## Success Indicators

✅ **Save is working well when:**
- Memory files grow each month
- AI remembers your preferences across sessions
- New capabilities are documented
- Relationship milestones are recorded
- Each save feels personalized to you

✅ **Memory getting better when:**
- AI's responses become more tailored
- Communication style matches your preference
- AI avoids mistakes from previous sessions
- Partnership feels more natural and efficient
- Fewer explanations needed for common patterns
