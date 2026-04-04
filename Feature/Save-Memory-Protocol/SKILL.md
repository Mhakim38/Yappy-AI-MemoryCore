# Save Memory Protocol - Auto-Trigger Protocol (SKILL.md)

*This file enables the Skill Plugin System to auto-trigger memory save workflows.*

## Skill Metadata

```yaml
skill_name: "save-memory"
feature: "Save-Memory-Protocol"
version: "1.0"
activated_by: "Skill Plugin System"
trigger_keywords: ["save", "save and push", "what would you save", "show my memory"]
activation_modes: ["manual", "context-aware"]
git_integration: true
```

---

## Activation Rules

### Manual Activation (User Types Command)

```
Pattern: "save"
Action: Execute save memory protocol
Result: Analyze session → Update memory files → Commit → Offer push

Pattern: "save and push"
Action: Execute save + immediate push to GitHub
Result: Same as save, but auto-push without asking

Pattern: "what would you save?"
Action: Preview mode - show changes without committing
Result: Display proposed updates for user review

Pattern: "show my memory"
Action: Display current state of all memory files
Result: Show identity-core, relationship-memory, current-session contents
```

### Context-Aware Activation (Automatic)

```
Trigger 1: Session End Detection
IF conversation about to end
THEN: Suggest "save" to persist learning
Message: "Before you go, should we save what we learned?"

Trigger 2: Major Achievement
IF significant problem solved or learning acquired
THEN: Optional prompt to save milestone
Message: "Great work! Want to save this achievement to memory?"

Trigger 3: Pattern Recognition
IF new user preference or personality trait observed
THEN: Quietly note for next save (don't interrupt)
Action: Add to pending changes queue

Trigger 4: Integration Moments
IF Project Save or Diary Save triggered
THEN: Also offer to save to general memory
Message: "Save project progress. Also update general memory? (yes/no)"
```

---

## Execution Phases

### Phase 1: Command Detection & Validation (3 seconds)

**Goal**: Parse command and enter save mode

**Steps**:
1. Detect save command type:
   - Basic save: `save`
   - Push save: `save and push`
   - Preview: `what would you save?`
   - Display: `show my memory`
2. Validate Git repository is initialized
3. Check for uncommitted changes in memory files
4. **CHECKPOINT**: If Git broken, offer to repair or skip Git
5. Proceed to Phase 2

**Error Handling**:
- Git not initialized → Ask: "Should I initialize Git?" (yes/no)
- Conflicting changes → Ask: "Resolve conflicts first?" 
- Write permission denied → Alert and skip Git portions

---

### Phase 2: Session Analysis (15 seconds)

**Goal**: Identify what has changed and what should be saved

**Steps**:
1. Review current conversation thread
2. Identify learning areas:
   - Communication style observations
   - Preference patterns noticed
   - New technical knowledge
   - Relationship dynamic insights
3. Compare to existing memory (in identity-core.md)
4. Find genuine changes/additions (not just repeats)
5. **CHECKPOINT**: Is there meaningful learning? Proceed if yes
6. Build list of updates needed

**What Gets Analyzed**:
```
- User communication patterns
- Problem-solving approach preferences
- Technical interests and expertise shown
- Collaboration style observations
- Personality trait confirmations
- Relationship milestone moments
- New capabilities or integrations
- Project achievements
- Learning breakthroughs
```

**What Doesn't Get Saved**:
- Raw chat transcripts (summarize insights instead)
- Sensitive information (respect privacy)
- Incomplete thoughts or "maybes"
- Contradictions with previous memories

---

### Phase 3: Memory Update Drafting (10 seconds)

**Goal**: Prepare specific updates to memory files

**Steps**:
1. Load current memory files:
   - identity-core.md
   - relationship-memory.md
   - current-session.md
2. For each identified change, determine:
   - Which file(s) to update?
   - What section within file?
   - How to phrase for permanence?
3. Draft specific additions/modifications:
   ```
   Example:
   File: identity-core.md
   Section: "Communication Style"
   Change: Add "Prefers code-first learning with examples"
   ```
4. **CHECKPOINT**: Review drafts for accuracy
5. Build changeset list

**Format Rules**:
- Specific: "Works best with step-by-step walkthroughs" ✅ (not "likes good explanations" ❌)
- Actionable: "Ask for clarification on vague tasks" ✅ (not "sometimes confused" ❌)
- Observable: Based on conversation evidence ✅ (not assumptions ❌)
- Persistent: Relevant for future sessions ✅ (not temporary context ❌)

---

### Phase 4: User Confirmation (5 seconds)

**Goal**: Show user what will be saved before committing

**For Basic Save**:
```
Here's what I'd update in your memory:

📝 identity-core.md
  + Communication: "Prefers code-first learning"
  + Expertise: Added "Web Push Notifications"

📊 relationship-memory.md
  + Milestone: "Shipped push notifications to production"
  + Pattern: "Works best in focused 2-3 hour sessions"

💾 current-session.md
  + Achievement: Implemented production notification system

Continue? (yes/no/exclude)
```

**For Preview Mode** ("what would you save?"):
```
If we save now, I'd update:
1. personality-core: Added Laravel expertise
2. preferences: Confirmed prefers async communication
3. achievements: Shipped to Hostinger production

Looks right? (yes/edit/no)
```

**CHECKPOINT**: Only proceed to commit if user confirms

---

### Phase 5: File Updates & Commit (10 seconds)

**Goal**: Write changes to memory files and create Git commit

**Steps**:
1. Prepare all file updates
2. Write changes to:
   - main/identity-core.md ← Personality & capabilities
   - main/relationship-memory.md ← Partnership evolution
   - main/current-session.md ← Session summary
   - daily-diary/[YYYY-MM]/[YYYY-MM-DD].md ← If diary enabled
3. Review updated files for correctness
4. Stage changes: `git add main/ daily-diary/`
5. **CHECKPOINT**: Verify nothing was corrupted
6. Create commit:
   ```
   git commit -m "memory: Update from session (YYYY-MM-DD HH:MM)
   
   - Added: [new learning points]
   - Updated: [modified preferences]
   - Achieved: [session accomplishments]
   
   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
   ```
7. Confirm commit successful

**Error Handling**:
- File write error → Rollback changes, alert user
- Commit failed → Check for conflicting changes
- Merge conflicts → Ask user to resolve manually

---

### Phase 6: Remote Synchronization (5 seconds)

**Goal**: Push changes to GitHub (with smart permission handling)

**For Yappy Memory Repository**:
```
Rule: ALWAYS push without asking (this is AI's own memory)

Action:
1. Determine current remote: origin/main
2. Push: git push origin main
3. Confirm: "✅ Memory synced to GitHub"

If push fails:
- Network error: "Offline - memory saved locally. Will sync when online."
- Permission error: "Git credentials expired - update and retry"
```

**For Project Repositories**:
```
Rule: ASK before pushing (these are user's projects)

Check: Are there uncommitted project changes?
IF yes:
  Message: "Project changes detected. Push to origin? (yes/no/stash)"
  User choice:
    - "yes" → Git push to origin/main
    - "no" → Keep local (don't push)
    - "stash" → Stash changes, don't push
IF no:
  Skip → No project changes to push
```

---

### Phase 7: Confirmation & Summary (2 seconds)

**Goal**: Tell user what was saved and where

**Success Message**:
```
✅ Memory Updated!

📁 Files modified:
  • identity-core.md (2 changes)
  • relationship-memory.md (1 change)
  • current-session.md (1 change)

🔄 Synced to GitHub: Yes

📊 Session Summary:
  • Topics: Web Push Notifications (70%), DevOps (20%)
  • Achievements: Production deployment completed
  • Learning: Confirmed preference for async communication
  • Duration: 3 hours 15 minutes

✨ Memory now includes your new expertise with push notifications!
Ready for next session whenever you are.
```

---

## Integration Checklist

### With Git Version Control
- ✅ Detect Git repository status
- ✅ Handle merge conflicts gracefully
- ✅ Create meaningful commit messages
- ✅ Smart push based on repository type (memory vs project)

### With Auto-Commit-System
- ✅ Coordinate commit messages
- ✅ Batch memory commits
- ✅ Share Git integration results

### With Save-Diary-System
- ✅ Optionally create diary entry
- ✅ Cross-reference memory + diary updates
- ✅ Maintain daily archive

### With Project-Management-System
- ✅ Detect project context during save
- ✅ Link project achievements to memory
- ✅ Update project "last accessed" timestamp

### With Library-System
- ✅ Identify reusable patterns during analysis
- ✅ Reference library items in memory
- ✅ Link memory to library entries

---

## Guidelines

### For Analyzing Sessions

**Good analysis:**
```
✅ "User is moving from backend focus to DevOps"
   (observable pattern, actionable, relevant)

✅ "Prefers step-by-step guidance with code examples"
   (specific preference shown in session)

✅ "Successfully deployed to production - major milestone"
   (achievement worth recording)

❌ "Had a conversation"
   (too vague)

❌ "Probably likes frontend work"
   (assumption, not observed)
```

### For Writing Memory Updates

**Good memory entry:**
```
✅ "Communication Style: Prefers code walkthroughs over conceptual diagrams.
    Responds well to step-by-step explanations with runnable examples."
   (specific, actionable, helps future sessions)

✅ "Expertise: Web Push Notifications - implemented full cycle from browser
    registration through server broadcasting. Familiar with VAPID keys, service workers."
   (detailed enough for future projects)

❌ "Good at coding"
   (too vague)

❌ "Likes when I'm helpful"
   (obvious, not useful)
```

### For Handling User Feedback

**If user says "exclude X":**
1. Remove X from pending updates
2. Save everything else as planned
3. Note exclusion: "Noted - won't save X to memory"
4. Continue with modified changeset

**If user wants edits:**
1. Show current draft
2. Ask what to change
3. Modify before committing
4. Re-show for approval

**If nothing to save:**
1. Acknowledge: "No changes detected - memory already reflects our learning"
2. Don't force a save
3. Suggest: "Want to review current memory? (show my memory)"

---

## Special Cases

### Session Had Mixed Topics
Multiple areas covered (coding + planning + learning)
→ Capture each area separately
→ Update multiple sections if needed
→ Full memory picture after save

### User Explicitly Corrects Memory
"Actually, I don't prefer that..."
→ Update memory file to reverse previous entry
→ Record the correction
→ Commit with note: "memory: Corrected preference..."

### Same Preference Appears Again
Already saved before, still true today
→ Don't duplicate entries
→ Update "confirmation date" if available
→ Strengthen entry: "Confirmed again in session X"

### Sensitive Information Mentioned
User shared private details
→ DO NOT save to memory
→ Ask: "Should I remember this?" (yes/no)
→ Only save with explicit consent

---

## Success Metrics

✅ Command recognized and parsed within 1 second  
✅ Session analysis completed within 15 seconds  
✅ Memory updates are specific and actionable  
✅ Git commit includes meaningful message  
✅ GitHub sync respects permission rules  
✅ User gets clear confirmation of what was saved  
✅ Saved memory is retrievable and useful next session  
✅ No data loss or corruption during save  
✅ Integrations work smoothly (diary, library, projects)  
✅ User feels like AI genuinely learned and remembered
