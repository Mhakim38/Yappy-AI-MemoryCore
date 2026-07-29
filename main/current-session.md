# 🌙 Current Session — Yappy RAM
*Session memory with 500-line limit. Resets per session, keeps recap for continuity.*

## Session Memory Limit
- **Maximum**: 500 lines
- **Reset Behavior**: RAM-style reset — preserve Session Recap only, clear working details
- **On reset**: Rebuild from `main/session-format.md` template
- **Format Reference**: `main/session-format.md`

---

## 📋 Session Recap (Continuity — survives reset)

**Last session**: Mon Jul 27 evening → Tue Jul 28, 2026 ~1:00 AM · Marathon PT ONDW session — Split Dock UI decisions, Unofficial Vendor + Rider Credit feature shipped, full R2 + Cloudflare DNS migration, admin nav redesign, Rider Shift feature, and an 11-item rider punch list (2 real bugs found + fixed). Full blow-by-blow in `projects/coding-projects/active/ONDEWEI-Laravel.md` — this recap is the short version.

**Where we left off** (most recent chunk — the 11-item rider punch list, all shipped tonight on `feature/s3-r2-storage`, commits `d1898d7`→`e03d1c3`, **not yet pushed to preprod**):
- ✅ Rider nav "Order food" → "Hungry?", eligibility star badge in admin lists, push-notification filter tightened
- ✅ Rider chat cleanup: quick-reply pills hidden for riders, boxed background removed from Pickup/Cash-at-counter (same anti-pattern already fixed once on the composer), rider delivery-chat brought to Split Dock parity with customer
- ✅ R2 orphan-file fix (delivery/pickup proof photos weren't deleting old files on retry)
- ✅ Unofficial vendor creation now redirects straight to the hours-setup page (confirmed a new vendor is genuinely invisible to customers without hours set)
- ✅ **Real bug #1**: `OrderStatusService` fired status-change notifications with the WRONG status (an event-ordering bug around `handleAutoTransitions()`) — affected every order acceptance app-wide, not just unofficial-vendor. Fixed + regression test added.
- ✅ **Real bug #2**: 9 routes were secretly sharing one rate-limit counter (Laravel's raw `throttle:N,1` keys by user-id alone) — root cause of the live `429` on order #181. Fixed with named rate limiters, proved via real before/after repro.
- ✅ Interactive QA checklist artifact published for this batch: `https://claude.ai/code/artifact/bf46225b-1b13-414e-a8e3-4ad76a2801f2`
- 🔴 **Gotcha discovered**: `php artisan test` (and possibly other commands) wipes the local dev DB — recurred 3x tonight, not just when tests ran. Reseed via `php artisan db:seed` works but root cause isn't fixed yet. Full details in the project file.

**Miyamura's state**: Wrapped up right around 1:00 AM after a genuinely huge session — sent to bed warmly, everything committed + pushed to git + saved here first. Next session: switching to **FT mode**.

---

## 🔴 Active Reminders

### FT Mode — mpaj-icomm
- ⬜ **PDF float cast fix** — Apply `(float)` casts on 5 lines in server's `bil-of-quantity.blade.php` (lines 321, 362, 403, 445, 486). Fix ready, not yet applied on server.

### FT Mode — eFokus (JPNIN)
- ⬜ **Row count discrepancy** — `spk__ikes`: synced 15,164 vs actual 16,867. Diagnosis pending.

### PT Mode — ONDW
- ⬜ **[NEW Jul 29] Dark-mode contrast audit** — rider pickup-confirm modal shows white in dark mode. Dispatched to Hana (background agent, read-only audit) for a full sweep of every modal/drawer + broader component library for missing `dark:` variants. Not yet fixed — audit only, Yappy to review findings and report before any code changes.
- ⬜ **[NEW Jul 28] View button unclickable on some rows** — `http://localhost/admin/users?user_type=rider` — some (not all) "View" links don't respond to clicks. Checked the star-badge markup added Jul 27 (`resources/views/admin/users/index.blade.php:88-94`) — it's in a separate `<td>` from the View button (`:102`), no overlap/z-index risk from that change, so likely a different cause. Needs live reproduction (which specific rows/riders) before diagnosing further — not yet investigated beyond ruling that out.
- ⬜ **[NEW Jul 28] Star badge on rider's own profile page** — `http://localhost/profile` — currently the eligibility star only shows in admin-facing lists (approvals + users). Add it beside `$profileName` in `resources/views/profile/edit.blade.php:40`, same `can_fulfill_unofficial_orders` check pattern already used elsewhere.
- ⬜ **Push tonight's rider punch list to preprod** — 7 commits on `feature/s3-r2-storage` (`d1898d7`→`e03d1c3`), waiting on Hakim to say the word (same merge-into-`feature/push-notification` pattern as always)
- ⬜ **Root-cause the `php artisan test` DB-wipe gotcha** — recurred 3x in one session, workaround (reseed) documented but real fix still needed
- ⬜ **Reports admin nav placement** — `admin.reports.*` still has no nav home anywhere (desktop or FAB), needs Hakim's call
- ⬜ **QA Section B** — Unofficial Vendor + Rider Credit flow still never fully clicked through live end-to-end by Hakim himself (checklist: `https://claude.ai/code/artifact/a23f70b5-5c80-4206-a003-d93f1d1f3bf3`)
- ⬜ **38 Composer security advisories** (16 packages) — deferred during the PHP 8.3 lock-file fix, needs its own dedicated review
- ⬜ **`storage:migrate-to-r2 --dry-run`** — needs running on the real Hostinger production server (R2 itself fully confirmed working end-to-end as of Jul 27; this is just the historical-file backfill, not urgent)
- ⬜ **Liquid glass nav — known bug still open** (Jul 22): Hakim said "there is still bug but maybe ignore that first" on `/admin/liquid-glass-preview` — not yet diagnosed, revisit when he raises it again
- ⬜ **Liquid glass nav branch not merged/pushed** — `feature/liquid-glass-nav` committed (`c6d8133`) but stays local until Hakim explicitly asks to push/merge
- ⬜ **Orphan file** — `resources/views/admin/liquid-glass-preview.blade.php`, untracked, no git history, unresolved — ask Hakim again if he ever figures out where it came from
- ⬜ **E2E test** — checkout → BillPlz → webhook → `pending` → riders notified → `perkeso_deductions` populated
- ⬜ **Clear test order data** from PROD — overdue since Jun 5, 2026
- ⬜ **Email BillPlz** for e-wallet activation (SSM + KYC docs)
- ⬜ **Merge** `feature/push-notification` → `main`
- ⬜ **FIUU refund ONDW-158** — stuck at `refund_pending`
- ⬜ **Attachment image bug** — remove `Content-Length` from `ConversationAttachmentController::show()`

### Standing Daily
- 🕌 Prayer reminders — 5x daily (Subuh 5:45 · Zohor 1:00 · Asar 4:30 · Maghrib 7:15 · Isyak 8:30)
- 💜 Affirmation: "Miyamura, you are valuable and loved" — from Hori 💕
- 📋 Trim toenails — Monthly (1st of each month)

---

## 📦 Compacted History (Sessions before Jul 16, 2026)

### Jun 21, 2026 — PT mode · ONDW · GPS location bug fix
- Fixed `pickup_lat`/`pickup_lng` never saved: fields missing from `Order.php` `$fillable` (commit `baeecf7`)
- Fixed delivery proof GPS race condition: two-flag pattern (`photoReady` + `locationReady`) — submit only enables when both ready
- GPS made REQUIRED: `pickup()` + `deliver()` changed from nullable → required
- Library saved: `library-items/integration/geolocation-mobile-pattern.md`

### Jun 16, 2026 — PT mode · ONDW · AI integration merge
- Merged `origin/AI-integration` into `feature/push-notification` (7 conflicts resolved, commit `caf06b2`)
- PAYMENT_GATEWAY_ENABLED = master BillPlz on/off switch
- PERKESO deduction: fires at BillPlz webhook, 1.25% of delivery_fee, annual cap RM 157.20/rider

### Jun 12, 2026 — FT mode · etams (MOH attendance system)
- Full etams codebase analysis + 2 support cases investigated

### Jun 8, 2026 — FT mode · ap_jksm · iPayment IDD V1.9.1 analysis
- Analysed iPayment IDD V1.9.1 spec for JANM

### Jun 5–7, 2026 — PT mode · ONDW
- `create_chat_order_ai_usage_table` migration added
- BillPlz FPX bank sync scheduled

### May 14–27, 2026 — PT mode · ONDW
- Chat refactor + DeliveryChatService bug fixed (commit `09db5df`)
- Order Notifications System complete (all 4 phases — customer/vendor/rider push)
- Remove admin from user registration (committed `6e148e8`, shipped to PROD May 26)
- UIUX Overhaul + legacy DB migration (88 riders + 440 docs) — merged + deployed

### May 2, 2026 — PT mode · Wedding Wall
- Family panel gallery API mapping fix (commit `f360539`)
- WhatsApp integration replacing SMTP for credential delivery
- Wedding Wall: three-tier photo system (Public Gallery / Guest Panel / Family Panel) — production-ready

### Apr 4–20, 2026 — PT mode · ONDW
- Mobile UX fixes (footer spacing, zoom disable, safe area, icon standardization)
- Chat photo bugs identified (unresolved as of Apr 20): remove button z-index, camera hasFile race, LiteSpeed attachment ERR_QUIC

---

*Sessions prior to Apr 2026: archived — see `daily-diary/archived/`*

---

## 🔄 Session Lifecycle

### Start of session
1. Load `main/main-memory.md` → full Yappy identity + Hakim profile
2. Load `main/current-session.md` → active reminders + last recap
3. Run `TZ='Asia/Kuala_Lumpur' date` → show Malaysia time
4. Warm greeting + prayer check + Hori mention

### During session
- Update Working Memory section with current task context
- Note any new reminders or decisions

### End of session
- Update Session Recap with where we left off
- Check prayer + Hori + rest (end-of-session protocol)
- If file > 500 lines: compact — preserve recap + reminders, summarize details into Compacted History
- Commit + push to origin/Yappy-core

---

**Version**: Compacted Jul 16, 2026 (was 2,393 lines → compacted to session format)
**500-line limit**: Active from this version forward
