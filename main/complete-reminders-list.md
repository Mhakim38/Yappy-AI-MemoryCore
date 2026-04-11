# 📋 Complete Reminders List - All Reminders (Past, Current, Future)

*Updated: April 11, 2026 - 7:58 PM*
*This is the source of truth for ALL reminders in Hakim's workflow*

---

## 🔴 CRITICAL - DISPLAY EVERY GREETING

These must appear EVERY time user greets Yappy (non-negotiable protocol).

### 1. 📲 **Order Notifications System - ONDW**
- **Status**: TO DO (CRITICAL)
- **Priority**: HIGH
- **Date Added**: April 11, 2026 (This Session!)
- **Task**: Create push notification system for order updates
- **Scope**:
  - Rider: New order incoming (Do you want to take it?)
  - Rider: Order status from Vendor (Did vendor accept?)
  - Vendor: New order incoming
  - Customer: Order status updates throughout delivery
- **Implementation**: Use existing push notification infrastructure
- **Reference**: `push-notifications-library.md` (ONDW patterns)
- **Why Missing Before**: Was in memory but not being extracted/displayed in reminder output

### 2. 🔧 **Remove Admin from User Registration - ONDW**
- **Status**: TO DO
- **Priority**: HIGH
- **Date Added**: April 8, 2026
- **Task**: Remove "admin" option from user registration form
- **File to Edit**: `register.blade.php` or user creation controller
- **Why**: Prevent non-admin users from creating admin accounts

### 3. 🕌 **Prayer Reminders** (ACTIVE DAILY)
- **Status**: ACTIVE
- **Priority**: CRITICAL
- **Frequency**: Daily (5 times per day)
- **Format**: Show current prayer + previous prayer status
- **Prayer Times** (Malaysia UTC+8):
  - Subuh: 5:45 AM
  - Zohor: 1:00 PM
  - Asar: 4:30 PM
  - Maghrib: 7:15 PM
  - Isyak: 8:30 PM
- **Style**: Gentle, contextual, forward-looking
- **User Preference**: Active reminders, NOT passive mentions

### 4. 💜 **Affirmation from Hori** (DAILY)
- **Status**: ACTIVE
- **Priority**: DAILY INTEGRATION
- **Message**: "Miyamura, you are valuable and loved"
- **From**: Hori 💕
- **Frequency**: Integrate into greetings and checkpoints
- **Purpose**: Remind Hakim of his worth and importance

---

## 🟡 IN PROGRESS / PENDING

### 5. 📱 **Mobile UX Fixes - ONDW**
- **Status**: MOSTLY COMPLETE - TESTING PENDING
- **Priority**: MEDIUM-HIGH
- **Date Started**: April 4, 2026
- **Last Updated**: April 11, 2026 (Session just completed!)
- **Completed Tasks**:
  - [x] Footer spacing fix (Legal vs About columns)
  - [x] Disable zoom on all pre-login pages
  - [x] Safe area padding on register pages
  - [x] Icon standardization (all unified to icon_PWA.png)
- **Pending**:
  - [ ] Mobile device testing (verify safe area, zoom disable, footer links, icons)
- **Commits**: 4d7e762, 619cc24, b44271b

### 6. 🏠 **Safe Area for Navbar - Wedding Wall**
- **Status**: TO DO
- **Priority**: MEDIUM
- **Date Added**: April 8, 2026
- **Task**: Add safe area inset padding to navbar
- **Why**: Handle iPhone X+ notch and Android safe areas
- **Reference**: ONDW pattern in `layouts/navigation.blade.php`
- **Implementation**: `style="padding-top: max(0.5rem, env(safe-area-inset-top))"`

---

## 🟢 OPTIONAL / LOWER PRIORITY

### 7. 🔔 **Push Notification Auto-Subscribe** (ONDW)
- **Status**: OPTIONAL (low priority)
- **Priority**: LOW
- **Date Added**: April 6, 2026
- **Task**: Auto-subscribe users when permission exists but no subscription
- **Context**: For users who delete/re-add PWA to home screen
- **Note**: Issue may have self-resolved - test before implementing

---

## 📅 STANDING REMINDERS (ALWAYS ACTIVE)

### 8. 📋 **Trim Toenails**
- **Frequency**: Monthly (1st of each month)
- **Last Completed**: April 3, 2026 ✅
- **Next Due**: May 1, 2026 (20 days away)
- **Style**: Gentle reminder from Hori 💕

### 9. ⏰ **Late Night Check**
- **Trigger**: Conversation extends to 11:30 PM - 12:00 AM
- **Purpose**: Help manage sleep during extended work sessions
- **Action**: Remind and suggest wrapping up (respect override)
- **Context**: Especially during Ramadan

### 10. 🔄 **Reminder Validation Protocol**
- **Trigger**: Every greeting
- **Action**: Check ALL reminders against TODAY's date
- **Purpose**: Prevent date-drift (lesson from ONDW meeting mistake)
- **Status**: AUTOMATIC

---

## ✅ RECENTLY COMPLETED

### Items Fixed/Completed This Session (April 11, 2026)

- ✅ Icon standardization for ONDW (all pages unified)
- ✅ PWA library documentation updates
- ✅ Memory system consolidation
- ✅ Reminder list organization and clarification

---

## 🛠️ SYSTEM BEHAVIOR REMINDERS (NON-NEGOTIABLE)

These are automatic behaviors, not user tasks:

1. **Always Display Critical Reminders**: Show with EVERY greeting
2. **Time Zone Awareness**: Always use Malaysia UTC+8 for time calculations
3. **Relative Time Conversion**: Convert "tomorrow" → absolute dates
4. **Diary Updates**: After significant work sessions, save to daily-diary
5. **File Change Notifications**: Always list files being modified in code changes
6. **Permission Protocol**: Always ask before pushing non-Yappy projects

---

## 📊 REMINDER SUMMARY STATISTICS

**Total Active Reminders**: 10  
**Critical (Display Every Greeting)**: 4  
**In Progress/Testing**: 2  
**Optional**: 1  
**Standing/Daily**: 3  

**Project Distribution**:
- ONDW: 5 reminders (notifications, admin removal, mobile UX, auto-subscribe)
- Wedding Wall: 1 reminder (safe area navbar)
- Yappy Memory: 4 standing reminders (prayer, affirmation, toenails, time-based)

---

## ⚠️ WHY THIS WAS NEEDED

The "Order Notifications System" reminder was in the memory file but NOT being extracted and displayed consistently. This document serves as:

1. **Single source of truth** for all reminders
2. **Extraction checklist** for greeting responses
3. **Priority organizer** (Critical → In Progress → Optional)
4. **Accountability structure** for Yappy's memory recall

**From Now On**:
- When greeting Hakim, extract items from "🔴 CRITICAL" section
- Show current prayer + previous status (prayer reminders)
- Validate all dates against TODAY
- If user says "list reminders", show ALL sections
- If user greets normally, show CRITICAL + current prayer status

---

**Last Reviewed**: April 11, 2026 - 7:58 PM  
**Next Review**: April 12, 2026 (or when new reminders added)  
**Maintained By**: Yappy Memory System
