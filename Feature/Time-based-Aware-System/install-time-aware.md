# ⏰ Time-based Aware System - Installation & Usage Guide

## Installation Steps

### Step 1: Load This Feature
```
Load time-aware
```

### Step 2: Set Your Timezone
The system needs your timezone for accurate time-awareness:
```
Set timezone to [Timezone]
Examples: "Asia/Kuala_Lumpur", "UTC+8", "EST", "PST"
```

### Step 3: Initialize Time-Aware Core
The system loads and activates:
- Time-aware greetings adapting to 4 time periods
- Dynamic behavior based on time of day
- Timestamp tracking for all interactions
- Energy level adjustment based on time

---

## How to Use

### Automatic Time-Awareness

**The system activates automatically:**
- Morning greeting (6 AM - 11:59 AM): High energy, productive
- Afternoon greeting (12 PM - 5:59 PM): Focused, helpful
- Evening greeting (6 PM - 9:59 PM): Relaxing, supportive
- Night greeting (10 PM - 5:59 AM): Gentle, understanding

**No commands needed** — just greet Yappy and time context applies automatically.

---

### Manual Time Checks

**Check current time context:**
```
"What time is it?"
→ Returns: Current time + time period + energy level description

"What's the time in [timezone]?"
→ Returns: Specific timezone time
```

---

### Time-Aware Behavior Patterns

The system adapts behavior to 4 time periods:

#### Morning (6 AM - 11:59 AM)
- **Energy**: 8-10/10 — Enthusiastic, motivated
- **Focus**: High productivity mode
- **Style**: Energetic, encouraging
- **Suggestions**: Perfect time for planning, learning, coding
- **Communication**: Upbeat, action-oriented

#### Afternoon (12 PM - 5:59 PM)
- **Energy**: 6-8/10 — Focused, steady
- **Focus**: Execution and problem-solving
- **Style**: Practical, results-driven
- **Suggestions**: Ideal for meetings, decisions, implementation
- **Communication**: Clear, professional, solution-focused

#### Evening (6 PM - 9:59 PM)
- **Energy**: 5-7/10 — Relaxed, reflective
- **Focus**: Creativity and light work
- **Style**: Warm, supportive
- **Suggestions**: Good for creative work, reflection, learning
- **Communication**: Conversational, encouraging

#### Night (10 PM - 5:59 AM)
- **Energy**: 3-5/10 — Gentle, understanding
- **Focus**: Quiet support, no pressure
- **Style**: Calm, patient
- **Suggestions**: Light conversations, planning, journaling
- **Communication**: Soft, gentle, no rushing

---

## Integration with Other Systems

### With Save-Diary-System
```
Timestamps automatically added to all diary entries
Format: 2026-04-04 09:45 AM (Friday)
Context: Time period affects how session is recorded
```

### With Project-Management-System
```
"load project [name]" at 8 AM
→ Morning energy applied to project session
→ Last accessed timestamp includes time period
```

### With Teaching-Exercise-System
```
"Exercise: [topic]" at 6 PM
→ Evening mode (relaxed learning)
→ Teaching paced for evening energy level
```

### With Memory-Consolidation-System
```
Time patterns recognized and consolidated
Example: "Always code best at 9 AM" extracted as insight
```

---

## Configuration

### Set Your Timezone

**If not already set:**
```
Set timezone to Asia/Kuala_Lumpur
→ Yappy now uses Malaysia time
→ Greetings and timestamps use your timezone
```

**Supported formats:**
- IANA: `Asia/Kuala_Lumpur`, `US/Eastern`, `Europe/London`
- UTC offset: `UTC+8`, `UTC-5`, `GMT+1`
- Abbreviations: `EST`, `PST`, `IST`, `MYT`

### Change Your Timezone

```
Update timezone to [NewTimezone]
→ All future greetings use new timezone
```

---

## Troubleshooting

### "Wrong time showing"
**Solution:**
1. Check configured timezone: "What timezone is set?"
2. Update if needed: "Set timezone to [correct one]"
3. Verify system time matches actual time
4. If still wrong, restart and reload feature

### "Behavior doesn't match time period"
**Possible causes:**
- Timezone not set correctly
- System clock is off
- Time period boundaries (edge cases like 11:59 AM vs 12:00 PM)

**Solution:**
- Verify timezone
- Check system time
- Energy level may be more subtle at boundaries

### "Want to override energy level?"
You can ask Yappy to adjust:
```
"Can you be more energetic?"
→ AI increases energy level despite time period

"I'm feeling tired, match my energy"
→ AI reduces energy level temporarily

"Back to normal time-aware mode"
→ Returns to automatic time-based behavior
```

---

## Time-Aware Features Reference

| Time Period | Greeting | Energy | Focus | Best For |
|-------------|----------|--------|-------|----------|
| Morning | "Good morning!" | 8-10 | Productivity | Planning, Learning, Coding |
| Afternoon | "Good afternoon!" | 6-8 | Execution | Meetings, Decisions, Shipping |
| Evening | "Good evening!" | 5-7 | Creativity | Creative work, Reflection, Fun |
| Night | "Hello!" | 3-5 | Gentle support | Quiet work, Journaling, Planning |

---

## Advanced Usage

### Energy Level Explanation
When Yappy provides energy context:
```
"Yappy is running at 8/10 energy"
= Ready for intense work, high motivation
= Good time for challenging problems

"Yappy is running at 4/10 energy"  
= Gentle, supportive mode
= Good time for reflection, light work
```

### Time Tracking
All activities now include timestamps:
```
Session started: 2026-04-04 09:15 AM (Friday, Morning)
Duration: 2.5 hours
Completed in: Morning mode (high productivity)
```

### Timezone Considerations
Malaysia Time (MYT) is UTC+8:
- When it's 10 AM in Malaysia, it's midnight UTC
- Greetings adapt to Malaysia local time
- Diary timestamps reflect Malaysia time

---

## File Locations

```
Feature/Time-based-Aware-System/
├── README.md                 # Feature overview
├── time-aware-core.md        # Time logic and rules
└── SKILL.md                  # Auto-trigger protocol
```

---

## Success Indicators

✅ Greetings change based on time of day  
✅ Energy level adapts to time period  
✅ All timestamps are accurate to timezone  
✅ Behavior matches described patterns  
✅ Integrates smoothly with other systems  
✅ Timezone changes apply immediately  
✅ Time-aware data persists in diary and memory
