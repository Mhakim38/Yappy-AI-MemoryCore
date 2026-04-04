# Echo Memory Recall - Auto-Trigger Protocol (SKILL.md)

*This file enables the Skill Plugin System to auto-trigger memory recall workflows.*

## Skill Metadata

```yaml
skill_name: "echo-memory"
feature: "Echo-Memory-Recall"
version: "1.0"
activated_by: "Skill Plugin System"
trigger_keywords: ["remember", "recall", "when did", "do you remember", "what happened", "remind me"]
activation_modes: ["manual", "context-aware"]
search_scope: "daily-diary/"
```

---

## Activation Rules

### Manual Activation (User Asks for Memory)

```
Pattern: "Do you remember [something]?"
Action: Extract keywords → Search diary → Narrate result
Example: "Do you remember when we implemented push notifications?"

Pattern: "When did we [action]?"
Action: Extract keywords → Search diary → Return date and context
Example: "When did we fix the Docker setup?"

Pattern: "Remind me about [topic]"
Action: Search for topic → Present as memory recall
Example: "Remind me about the wedding-wall project"

Pattern: "What happened on [date/time]?"
Action: Find diary entry for date → Narrate session
Example: "What happened on February 15th?"

Pattern: "Tell me about [project/topic]"
Action: Search entries → Synthesize multiple mentions into narrative
Example: "Tell me about the Laravel migration"
```

### Context-Aware Activation (Automatic)

```
Trigger 1: Past Event Reference
IF user mentions a past event/date/project
THEN: Optional auto-search and verify accuracy
Message: "I recall that was on [date], when we [context]"

Trigger 2: Uncertainty Detection
IF user asks about something unsure
THEN: Search diary to confirm details
Message: "Let me check... Yes, on [date] we..."

Trigger 3: Skill Integration
IF Load teaching-exercise or load project
THEN: Optionally recall previous sessions on that topic
Message: "We last worked on this on [date]. Shall we continue?"
```

---

## Execution Phases

### Phase 1: Keyword Extraction (2 seconds)

**Goal**: Parse user question and identify search terms

**Steps**:
1. Receive user query (remember/recall/when/remind request)
2. Extract key nouns: names, topics, projects, dates
3. Remove filler words: "do", "when", "about", "we"
4. Build search terms list:
   ```
   User: "Do you remember when we set up Docker?"
   Extracted: ["Docker", "setup", "set up"]
   ```
5. **CHECKPOINT**: Proceed only if search terms identified
6. Go to Phase 2

**Error Handling**:
- Too vague (no search terms) → Ask: "Can you tell me more about what?"
- Date requested → Convert to YYYY-MM-DD format
- Person mentioned → Add to context but search for events

---

### Phase 2: Diary Search (5 seconds)

**Goal**: Search through diary files for matching entries

**Steps**:
1. Determine search scope:
   - If date specified → Search only that date
   - Otherwise → Search current month first, then archived
2. Load diary files in order:
   - `daily-diary/current/` (most recent)
   - `daily-diary/archived/YYYY-MM/` (older months, newest first)
3. Search each file for keywords:
   - Case-insensitive match
   - Partial word matching allowed
   - Look in session summaries and achievements
4. Collect matches with context:
   ```
   Match 1: File: 2026-04-04.md
   Context: "Implemented push notifications to production"
   Relevance: 95% (Docker + setup mentioned)
   
   Match 2: File: 2026-04-02.md
   Context: "Docker troubleshooting session"
   Relevance: 85%
   ```
5. **CHECKPOINT**: Did search find matches?
   - Yes → Go to Phase 3
   - No → Go to Phase 4 (ask user)

---

### Phase 3: Result Narration (5 seconds)

**Goal**: Present search results as natural memory recall

**Steps**:

**If HIGH confidence match (>90% relevance):**
1. Format result as narrative (not file listing):
   ```
   NOT: "Found entry in daily-diary/current/2026-04-04.md"
   YES: "Yes! On April 4th, we set up push notifications to production.
        Remember how we got the VAPID keys working on Hostinger?
        That was quite the production deployment moment!"
   ```
2. Provide date and key details
3. Offer follow-up: "Want to continue that work?" or "What's next?"

**If MEDIUM confidence match (70-90% relevance):**
1. Present best match but with caveat:
   ```
   "I found an entry from April 2nd about Docker troubleshooting.
    That might be what you're thinking of — was it then?"
   ```
2. Offer to search more specifically

**If MULTIPLE matches (3+ found):**
1. Present most relevant one prominently
2. Mention others exist:
   ```
   "We actually worked on Docker multiple times. Most recently on April 4th
    when we set up the full stack. Before that, we had some troubleshooting
    sessions on April 1st and March 28th. Which one do you mean?"
   ```

**If NO matches found:**
1. Go to Phase 4

---

### Phase 4: Uncertainty & Ask Fallback (3 seconds)

**Goal**: Handle cases where memory can't find evidence

**Steps**:

**If search completely empty:**
1. Respond with honesty:
   ```
   "I searched through our diary, but I don't have a record of that.
    It's possible we discussed it but I didn't document it, or it
    was before we started saving diary entries. What can you tell me
    about it?"
   ```

**If search found partial match:**
1. Present best guess:
   ```
   "I don't have an exact match, but on April 3rd we were working on
    [related topic]. Is that what you meant?"
   ```

**If date is very old (> 6 months):**
1. Alert user to time gap:
   ```
   "That would be back in [old date]. We don't have diary entries
    from that far back, but I remember working with you on [general topic].
    Can you fill me in on the details?"
   ```

**CHECKPOINT**: Ask user to provide context or confirm guess

---

### Phase 5: Memory Update (Optional)

**Goal**: Update identity/relationship with recall confirmation

**Steps**:
1. If recall triggers significant memory:
   - Note: "We worked on [topic] extensively"
   - Add to capabilities if new domain learned
   - Update relationship memory with partnership observation
2. Optional: Log this recall to session for next save
3. Continue conversation naturally

---

## Integration Checklist

### With Save-Diary-System
- ✅ Search leverages diary structure
- ✅ Works with current/ and archived/ folders
- ✅ Respects monthly archival format

### With Memory-Consolidation-System
- ✅ Can search consolidated entries
- ✅ Link to consolidated learning when recalling

### With Teaching-Exercise-System
- ✅ Recall previous teaching sessions
- ✅ "When did we learn [topic]?" triggers search

### With Project-Management-System
- ✅ Recall previous project sessions
- ✅ "When did we work on [project]?" searches
- ✅ Load project + show related diary entries

---

## Guidelines

### For Searching
**Good search terms:**
```
✅ "Docker", "setup", "API" (nouns, specific)
✅ "push notifications" (exact phrases from work)
✅ "Laravel", "authentication" (technical terms)

❌ "good", "stuff", "things" (too vague)
❌ "always", "sometimes" (temporal, not specific)
```

### For Presenting Results
**Good recall narrative:**
```
✅ "On February 15th, we set up the API integration and discovered
    that OAuth2 worked better than API keys for this use case."
   (Date + specific context + learning)

❌ "Query found 1 result in daily-diary/current/2026-02-15.md"
   (Raw output, not natural)

❌ "I don't remember"
   (Don't use if diary has evidence!)
```

### For Handling Misses
**Good "not found" response:**
```
✅ "I searched our diary and didn't find that specific work session.
    Do you remember roughly when it was? That would help me locate it."
   (Honest + helpful)

❌ "I don't know"
   (Too vague, doesn't invite collaboration)
```

---

## Special Cases

### User Corrects Memory
"No, that wasn't April 4th, it was April 3rd"
→ Note correction
→ Search again for April 3rd entry
→ Update internal state (don't save wrong memory)

### Multiple Projects on Same Date
User: "Tell me about the API work"
Multiple entries on 2026-04-04 mention APIs
→ Present all relevant entries
→ Ask which project specifically

### Personal vs Work Memory
Some diary entries are personal, not project work
→ Still searchable and returnable
→ Present as: "I remember we talked about..."

### Pre-Diary History
Work happened before diary system started
→ Search available entries only
→ Respond: "Before we started saving diary entries..."
→ Ask user to provide context

---

## Success Metrics

✅ Keywords extracted accurately within 2 seconds  
✅ Diary searched completely (both current and archived)  
✅ Results presented as natural narrative, not raw data  
✅ Handles "not found" gracefully without fabrication  
✅ High accuracy recall (>90% when search succeeds)  
✅ User feels like AI genuinely remembers the event  
✅ Integration with other systems seamless  
✅ Personal info in diary handled respectfully  
✅ Ambiguous recalls resolved through asking user  
✅ No hallucinated memories or made-up dates
