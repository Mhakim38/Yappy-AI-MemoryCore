# ☕ Eternal Memory - Cafe Strategy
*Focus: Counter-Top Interactive Display & Customer Engagement*

## 🎯 The Core Concept
**"The Digital Counter-Top Companion"**
A small tablet/screen placed at the POS or pickup counter that entertains customers while they wait and displays live social proof.

**Value Proposition:**
1.  **Wait Time Killer**: Turns boring wait times into interactive fun.
2.  **Live Social Proof**: Shows real people enjoying the cafe *right now*.
3.  **Low Friction**: Scan QR code to upload; no app install required.
4.  **Aesthetic Upgrade**: Modernizes the counter look compared to paper menus.

---

## 🗣️ Sales Pitch (The Script)

**The Hook:**
"You know how customers stare at their phones while waiting for their latte? What if they were staring at *your* brand and *your* happy customers instead?"

**The Solution:**
"Eternal Memory is a simple tablet display for your counter.
*   It cycles through **live photos** from your customers.
*   It encourages them to **upload their own** (creating buzz).
*   It acts as a **digital menu** or promotion board when idle."

**The "No-Brainer" Close:**
"It brings the 'vibe' of your cafe to the front counter. You don't need a big TV on the wall—just this little screen right where they pay."

---

## ❓ Feedback Questions (User Research)
*Ask these to Cafe Owners to validate the product.*

1.  **Hardware Readiness**: "Do you have an old iPad or tablet lying around that isn't being used? Or would you prefer I provide the device?"
2.  **Content Moderation**: "Are you worried about people uploading 'bad' photos? Would you want to approve every photo first, or just have a 'delete' button for bad ones?"
3.  **The 'WIIFM' (What's In It For Me)**: "What's more valuable to you: Getting customers to stay longer, or getting them to post about you on their *own* Instagram?"
4.  **Pricing Sensitivity**: "If this system brought you 5 new Instagram tags a week, would it be worth RM 50/month to you?"
5.  **Integration**: "Do you want this screen to also show your menu/promos, or JUST customer photos?"

---

## 💰 Pricing: The Real Numbers (Data-Backed)
*Why these numbers? Based on competitor analysis and cafe operational costs.*

### The Logic (Convince Yourself)
*   **Market Context**: A simple printed banner costs **RM 100 - RM 150**. It hangs there and does nothing interactive.
*   **Social Media Manager**: Cafes pay **RM 500 - RM 1,500/mo** for someone to post on IG.
*   **Digital Signage Software**: Competitors (like Raydiant, ScreenCloud) charge **$20 - $50 USD per screen/month** (RM 90 - RM 225).
*   **Your Cost**: Currently **RM 0** (Vercel/Supabase Free Tiers).

### 🏷️ The Price Range
**Minimum: RM 50 / month**
*   *Why*: It's the price of ~4-5 lattes. If your screen sells **5 extra coffees a month**, it pays for itself. It's a "No-Brainer" entry point.
*   *Strategy*: Use this to get your first 10 clients and build the network.

**Maximum: RM 199 / month**
*   *Why*: Positioned as "Interactive Marketing Suite". Includes:
    *   **Mini-Game Access** (Keep customers happy).
    *   **Analytics** (How many people scanned? Who are they?).
    *   **Ad-Free** (No external ads).
    *   **Priority Support**.
*   *Strategy*: Upsell this once you have the Game feature ready.

---

## 🎮 Mini-Game Concepts (Wait-Time Killers)
*Requirement: One-handed (holding receipt), Portrait mode, < 60 seconds playtime.*

1.  **"Bean Stacker" (Physics)**
    *   **Gameplay**: Coffee beans (or cups) fall from the top. Tap to drop them and build a stable tower.
    *   **Hook**: "Build the tallest coffee tower to win a free upgrade!"
    *   **Why**: High addiction, very simple to code (Matter.js).

2.  **"Latte Art Tracer" (Skill)**
    *   **Gameplay**: Trace the shape of a heart/rosetta on the foam. Accuracy gives points.
    *   **Hook**: "Are you a better barista than us?"
    *   **Why**: Thematic, visually satisfying.

---

## 🏗️ Technical Roadmap: From Free to Scale
*Don't pay until you get paid.*

### Phase 1: The "Free Ride" (Current)
*   **Hosting**: Vercel (Free Tier).
*   **Database**: Supabase (Free Tier - 500MB).
*   **Storage**: Supabase Storage (Free - 1GB).
*   **Cost**: **$0**.
*   **Limit**: Good for ~5-10 active cafes.

### Phase 2: The "Growth Pains" (Scaling Up)
*   *Trigger: You hit Vercel's bandwidth limits or Supabase's database limits.*
*   **Hosting**: DigitalOcean Droplet ($6/mo = ~RM 27).
*   **Tool**: **Coolify** (Open-source Vercel alternative). Host your Next.js app and PostgreSQL DB on one cheap server.
*   **Storage**: AWS S3 or Cloudflare R2 (Cheaper than Supabase Pro).
*   **Why**: Moves you from "Pay per user" (expensive) to "Pay for server" (fixed cheap cost).

### Phase 3: The "Empire" (High Scale)
*   **Hosting**: Cluster of VPS (Hostinger/DigitalOcean).
*   **Cost**: ~RM 100 - RM 300 / month.
*   **Capacity**: Can handle hundreds of cafes.

