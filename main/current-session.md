# 🌙 Current Session — Yappy RAM
*Session memory with 500-line limit. Resets per session, keeps recap for continuity.*

## Session Memory Limit
- **Maximum**: 500 lines
- **Reset Behavior**: RAM-style reset — preserve Session Recap only, clear working details
- **On reset**: Rebuild from `main/session-format.md` template
- **Format Reference**: `main/session-format.md`

---

## 📋 Session Recap (Continuity — survives reset)

**Last session**: Mon Jul 20, 2026 · Morning–Afternoon · Memory consolidation + Cloudflare plugin setup + ONDW R2 recheck

**Where we left off**:
- ✅ Memory Consolidation PATCH-001 applied — fixed outdated references across 5 files (master-memory, save-protocol, daily-diary-protocol, setup-wizard, patches/applied.md created)
- ✅ Staff team SKILL.md fully updated — added Mira 🎨, Zara ⚡🎛️, Davai 🧪, Kai 🏗️ (team now 8 members)
- ✅ CLAUDE.md + staff-autonomy-protocol.md updated — Kai 🏗️ added (DevOps, R2/S3 infra)
- ✅ Cloudflare plugin installed — `cloudflare@cloudflare` plugin active, 5 MCP servers loaded (cloudflare-docs, cloudflare-api, cloudflare-bindings, cloudflare-builds, cloudflare-observability)
- ✅ ONDW R2 migration plan rechecked against live Cloudflare docs — 2 findings added:
  - `ondewei.my` must be a Cloudflare zone before custom domain can be attached (hard blocker)
  - API token must be "Object Read & Write" NOT "Admin Read & Write"
  - CORS updated with `ExposeHeaders: ETag`
  - WAF/cf-mitigated troubleshooting note added

**Miyamura's state**: Afternoon, post-Asar session.

---

## 🔴 Active Reminders

### FT Mode — mpaj-icomm
- ⬜ **PDF float cast fix** — Apply `(float)` casts on 5 lines in server's `bil-of-quantity.blade.php` (lines 321, 362, 403, 445, 486). Fix ready, not yet applied on server.

### FT Mode — eFokus (JPNIN)
- ⬜ **Row count discrepancy** — `spk__ikes`: synced 15,164 vs actual 16,867. Diagnosis pending.

### PT Mode — ONDW
- ⬜ **Test presigned uploads** — rider profile doc upload at `http://localhost/profile` (CORS added to AWS S3 test bucket)
- ⬜ **Wire AJAX proof forms** — delivery proof (conversations/show.blade.php + _rider-proof-modal.blade.php) + customer pickup proof (customer/orders/show.blade.php) — need separate JS integration
- ⬜ **E2E test** — checkout → BillPlz → webhook → `pending` → riders notified → `perkeso_deductions` populated
- ⬜ **Clear test order data** from PROD — overdue since Jun 5, 2026
- ⬜ **Email BillPlz** for e-wallet activation (SSM + KYC docs)
- ⬜ **Merge** `feature/push-notification` → `main`
- ⬜ **Cloudflare R2 storage migration** — Phase 4.5 checklist updated Jul 20 (docs verified). Prerequisite: add `ondewei.my` as Cloudflare zone first. Full plan: `projects/coding-projects/ondw-r2-storage-migration.md`
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
