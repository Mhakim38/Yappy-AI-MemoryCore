# Social Posting Protocol (Hakim's accounts), set Nov 5, 2026

**Trigger:** Hakim says anything like "post it", "post on our platforms", "daily update post", "share what I did".
Private detail (his voice analysis, platform handles, drafts) lives in `secret_information/projects/personal-portfolio/social-voice-guide-2026-11-05.md`. This file is the public-safe protocol only.

## Run it like this, every time
1. **List ALL platforms first** (registry in the private guide; today: Threads and LinkedIn, ask if Hakim wants others added: Instagram, X, Facebook). Say which are in scope this run.
2. **Write one draft per platform from the day's real work** (read the notes in secret_information). Use his voice guide. Threads = his casual Bahasa/English voice. LinkedIn = professional English conversion (hook, short paragraphs, 3 to 5 bullets, one lesson, one question, max 3 hashtags, no emoji or dashes).
3. **Content scope (Hakim, Nov 5, 2026): PT mode work ONLY** (ONDW and his personal projects). Never post about FT mode (2Q Alliance) work. Never client names, systems, data, screenshots, IPs, credentials. No invented numbers.
4. **Show the exact text in chat.** Hakim reviews it, and HE clicks the Post button himself on each platform. Yappy never clicks Post.
5. **Run each platform in its own Playwright Chrome window** (own persistent profile folder per platform, remote-debugging port, attach with connectOverCDP). Human pace: type with a delay, no loops, no scheduling, a few posts a day. Type the draft into the composer, screenshot it, and STOP. Leave the composer open for Hakim to review and press Post himself.
6. **Login, email code, 2FA, captcha, checkpoint page:** STOP and tell Hakim to enter it himself in that window. Never type passwords or codes. Never repeat a code he pastes.
7. Tell Hakim which windows hold a ready draft, then clean up after he has posted (offer to delete profile folders; they hold session cookies).

Related: [[anti-slop writing rules]] (no dashes, human tone), [[announce repo target before save]].

## Scheduling and edits (Nov 5, 2026)
- Use each platform's built-in scheduler (LinkedIn clock icon, Threads "..." menu > Schedule...). Set date and time, then STOP before the confirm button; Hakim clicks it.
- Hakim edits drafts in the composer. Before touching a window, read the composer text, diff it against what was typed, and record his edits in the private guide; apply them to later drafts (full company names, technical terms named in brackets).
- Keep each window script alive for hours and never kill a window that holds his draft.

## Tags, screenshots, who clicks (Nov 5, 2026)
- Ondewei posts always tag the Ondewei account on every platform (only that account). Check the mention picker before selecting.
- Save screenshots of each draft, scheduled and posted state under Sweet/OnDeWei/Postings/<Platform>/.
- The final Post/Schedule/Confirm click is Hakim's. The auto-mode classifier blocks Yappy clicking publish buttons; never work around it.
