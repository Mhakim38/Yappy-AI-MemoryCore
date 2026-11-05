# Social Posting Protocol (Hakim's accounts), set Nov 5, 2026

**Trigger:** Hakim says anything like "post it", "post on our platforms", "daily update post", "share what I did".
Private detail (his voice analysis, platform handles, drafts) lives in `secret_information/projects/personal-portfolio/social-voice-guide-2026-11-05.md`. This file is the public-safe protocol only.

## Run it like this, every time
1. **List ALL platforms first** (registry in the private guide; today: Threads and LinkedIn, ask if Hakim wants others added: Instagram, X, Facebook). Say which are in scope this run.
2. **Write one draft per platform from the day's real work** (read the notes in secret_information). Use his voice guide. Threads = his casual Bahasa/English voice. LinkedIn = professional English conversion (hook, short paragraphs, 3 to 5 bullets, one lesson, one question, max 3 hashtags, no emoji or dashes).
3. **Sanitise.** FT client projects: skills and lessons only, never client names, systems, data, screenshots, IPs, credentials. ONDW and personal projects: only name them with his OK per post. No invented numbers.
4. **Show the exact text and wait for "post it".** A public post is outward-facing and cannot be fully taken back.
5. **Run each platform in its own Playwright Chrome window** (own persistent profile folder per platform, remote-debugging port, attach with connectOverCDP). Human pace: type with a delay, no loops, no scheduling, a few posts a day. Take a screenshot of the typed draft, click Post only after approval, screenshot the result.
6. **Login, email code, 2FA, captcha, checkpoint page:** STOP and tell Hakim to enter it himself in that window. Never type passwords or codes. Never repeat a code he pastes.
7. Report what was posted where, with a short summary, and clean up (offer to delete profile folders; they hold session cookies).

Related: [[anti-slop writing rules]] (no dashes, human tone), [[announce repo target before save]].
