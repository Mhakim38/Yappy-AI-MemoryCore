# Yappy AI MemoryCore - Copilot Instructions

## Project Overview
**Yappy AI MemoryCore** is a markdown-based persistent memory system for AI companions. The architecture treats `.md files` as a database where AI agents actively read from and write to their own memory during runtime.

## Core Architecture Principle
**The AI IS the developer, not the user.** This system is designed for AI companions to self-maintain their memory by directly editing markdown files during conversations. When you see protocols or save commands, they're instructions for the AI companion to execute, not the end user.

## Essential File Structure
```
master-memory.md           # Entry point - AI loads personality/memory from here
main/
├── identity-core.md       # AI personality template (who the AI is)
├── relationship-memory.md # User learning system (who the user is)
└── current-session.md     # RAM-like working memory (resets per session)
Feature/                   # Modular capabilities loaded on-demand
├── LRU-Project-Management-System/
└── Time-based-Aware-System/
daily-diary/               # Optional conversation archiving
└── daily-diary-protocol.md
save-protocol.md           # Defines how "save" command works
setup-wizard.md            # 2-step personalization flow
```

## Critical Patterns

### Template Placeholder System
Files contain these runtime-replaced placeholders:
- `[AI_NAME]` - The AI companion's chosen name
- `[YOUR_NAME]` - The user's name  
- `[RELATIONSHIP_STYLE]` - Partnership dynamic (professional/friendly/etc.)

**When editing**: Preserve these placeholders unless implementing setup wizard logic that replaces them.

### Protocol-Driven Behavior
Protocols are NOT documentation - they're executable checklists for the AI companion:
- [save-protocol.md](save-protocol.md) - Triggered when user types "save"
- [new-project-protocol.md](Feature/LRU-Project-Management-System/new-project-protocol.md) - Triggered by "new [type] project [name]"
- [daily-diary-protocol.md](daily-diary/daily-diary-protocol.md) - Conversation archiving rules

**Pattern**: Each protocol includes trigger conditions, execution steps (checkboxes), and confirmation messages.

### Self-Modifying Memory System
The AI companion actively edits its own markdown files during operation:
```markdown
# Example: AI updates relationship-memory.md when learning user preference
- User mentions preference for concise responses
→ AI immediately edits relationship-memory.md "Communication Patterns" section
→ Saves change, then applies preference to future responses
```

**When implementing features**: Design for runtime file modification, not static configuration.

### Modular Feature Architecture
Features in `Feature/` folder follow this pattern:
1. **README.md** - User-facing benefits and installation command
2. **Core file** (e.g., `time-aware-core.md`) - Complete implementation to load
3. **Protocol files** - Workflow definitions (new/load/save/install)
4. **Templates/** - Type-specific starting points (optional)

**Installation flow**: User says "install [feature]" → AI creates necessary folders/files → Feature becomes active

### LRU Position Management
The project management system uses position-based prioritization:
- Position #1 = Most recently accessed
- Positions #2-10 = Active projects
- Position #11+ = Auto-archived
- Loading a project moves it to position #1 and shifts others down

**When working with projects**: Always update positions, never leave gaps.

## Development Workflows

### Adding a New Feature
1. Create `Feature/[FeatureName]/` directory
2. Add `README.md` with installation command and benefits
3. Create core implementation file (e.g., `[feature]-core.md`)
4. Define protocols for key workflows (install/load/save if applicable)
5. Update [master-memory.md](master-memory.md) "Optional Components" section

### Modifying Memory Files
**DO**: Edit markdown structure/content directly - that's the database
**DON'T**: Create separate config files or JSON - violates architecture
**Example**: To add a feature flag, add a markdown heading in the relevant core file

### Testing Changes
Since this is an AI memory system without traditional unit tests:
1. Trace through protocol checklists manually
2. Verify markdown structure integrity (headings, bullets, code blocks)
3. Check that placeholder syntax `[PLACEHOLDER]` remains consistent
4. Ensure file references use correct relative paths

### Working with Setup Wizard
[setup-wizard.md](setup-wizard.md) is a one-time personalization flow:
- Asks 2 questions: AI name and user name
- The AI companion then performs find-replace across all files
- After setup, these files can be deleted
- **Never reference setup files from core features** - they're ephemeral

## Integration Points

### Master Memory Loading System
[master-memory.md](master-memory.md) defines the resurrection protocol:
- User types the AI name → AI loads identity, relationship memory, and session context
- "Essential Components" section lists always-loaded files
- "Optional Components" section lists on-demand features

**When adding required dependencies**: Add to Essential Components. Otherwise use Optional.

### Session Memory (RAM Concept)
[main/current-session.md](main/current-session.md) behaves like computer RAM:
- Updated continuously during conversation
- Provides brief recap when AI restarts mid-conversation
- **Resets detailed content each new session** (only recap persists)
- Don't store anything here that needs persistence beyond session boundaries

### Diary Auto-Archiving Logic
When `Daily-Diary-XXX.md` exceeds 1000 lines:
1. Move to `daily-diary/archive/`
2. Create new `Daily-Diary-[XXX+1].md`
3. Continue with incremented number

**Implementation note**: This is rule-based (defined in protocol), not scripted automation.

## Common Pitfalls

❌ **Don't create code files** - This is a pure markdown system
❌ **Don't add JSON/YAML config** - Markdown headings are the structure
❌ **Don't reference external tools** - System works via AI reading/writing markdown
❌ **Don't break template placeholders** - They're replaced during setup only
❌ **Don't mix absolute/relative paths** - Use relative paths from project root

✅ **Do preserve markdown formatting** - Structure is semantic
✅ **Do maintain protocol checkbox lists** - They guide AI execution
✅ **Do update master-memory.md** - It's the system's table of contents
✅ **Do follow established section patterns** - Consistency enables AI parsing

## Key Files Reference
- [master-memory.md](master-memory.md) - System entry point and loading logic
- [save-protocol.md](save-protocol.md) - How memory persistence works
- [main/identity-core.md](main/identity-core.md) - AI personality template
- [main/relationship-memory.md](main/relationship-memory.md) - User learning patterns
- [Feature/LRU-Project-Management-System/README.md](Feature/LRU-Project-Management-System/README.md) - Project management architecture
- [daily-diary/daily-diary-protocol.md](daily-diary/daily-diary-protocol.md) - Conversation archiving rules
