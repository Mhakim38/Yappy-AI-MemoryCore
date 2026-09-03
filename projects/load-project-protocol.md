# 📂 Load Project Protocol
*Step-by-step protocol for loading existing projects with LRU management*

## Trigger Command
```
"load project [name]"
```
Alternative: "load [type] project [name]" for type-specific search

## 📋 Execution Steps

### Step 1: Search for Project (pointer index)
- [ ] Resolve the project's canonical location from the MemoryCore pointer index (`projects/project-list.md`) — project files live in `secret_information/projects/[name]/`
- [ ] Fuzzy-match against the pointer list if the exact name isn't found
- [ ] If not indexed but a `secret_information/projects/[name]/` dir exists, load from there and add the pointer

### Step 2: Load Project Data (from secret_information)
- [ ] Read `secret_information/projects/[name]/overview.md` first (what/stack/repo/branch/mode/status)
- [ ] Then load `changelog.md` (recent progress) and `known-bugs.md` / topic files as the task needs
- [ ] Extract key information:
  - [ ] Project type
  - [ ] Description
  - [ ] Current status
  - [ ] Recent progress (last changelog entries)
- [ ] Load associated memory patterns for project type

### Step 4: Display Project Summary
- [ ] Show confirmation:
  ```markdown
  ✅ Project Loaded: [name]
  📁 Detail: secret_information/projects/[name]/
  ⏰ Last worked: [date]
  📝 Description: [description]

  Recent Activity:
  - [Last changelog entry]

  Ready to continue where you left off!
  ```

## 🔍 Smart Search Features
1. **Fuzzy Matching**: Finds "API-Dash" when searching "api dashboard"
2. **Type Priority**: Coding projects checked first for "load project api"
3. **Recent First**: Active projects searched before archived
4. **Partial Names**: "dash" finds "API-Dashboard" project

## 📊 Memory Pattern Loading

### Coding Projects Load:
- Technical terminology preferences
- Code style patterns
- Recent error solutions
- Development workflow

### Writing Projects Load:
- Writing style consistency
- Character/plot notes
- Tone and voice settings
- Chapter progression

### Research Projects Load:
- Source citations
- Key findings
- Research methodology
- Fact connections

### Business Projects Load:
- Client communication style
- Project constraints
- Stakeholder notes
- Timeline awareness

## Error Handling
- Project not found: Show available projects and suggest alternatives
- Multiple matches: Display list with types and last-worked dates
- Corrupted file: Attempt recovery from backup or recreate from template

---

*Load Project Protocol v1.0*
*Part of LRU Project Management System*
