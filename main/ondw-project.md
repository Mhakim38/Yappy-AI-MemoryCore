# 🍱 ONDW — Project Reference
*Last updated: Jun 16, 2026 · 03:00 MYT*

---

## 📌 What Is ONDW?
**ONDEWEI** — a food delivery PWA for Malaysia. Hakim's part-time (PT mode) project.
- **URL (preprod)**: `https://preprod.ondewei.my`
- **URL (prod)**: `https://ondewei.my`
- **Repo**: `/Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM`
- **Hosting**: Hostinger shared hosting (no Node.js, no persistent workers, no cron — use Laravel scheduler via cPanel)

---

## 🧱 Tech Stack
| Layer | Detail |
|---|---|
| Backend | Laravel 10.10 |
| Frontend | Blade + Vite (built locally, committed to git — Hostinger has no Node.js) |
| Database | MySQL |
| Queue | `QUEUE_CONNECTION=sync` (no persistent workers on shared hosting) |
| Auth | Email + Google OAuth |
| Roles | Customer, Vendor, Rider, Admin |
| PWA | Active (service worker, VAPID push notifications) |

---

## 👥 Team
- **Hakim** — lead / owner (PT mode)
- **AimanDhaifullah** — team dev. His branch: `origin/AI-integration`. Big Jun 14, 2026 commit `f699549` (AI chat-ordering, admin overhaul, full BillPlz + PERKESO).

---

## 🌿 Branch Structure
| Branch | Purpose |
|---|---|
| `feature/push-notification` | **Preprod deploy branch** — server pulls this |
| `main` | Production |
| `origin/AI-integration` | Aiman's dev branch — **merged into feature/push-notification on Jun 16** |
| `preprod` | OLD — 150+ commits behind, ignore |

**Deploy flow**: push to `feature/push-notification` → SSH preprod → `git pull` → `php artisan migrate` → `php artisan config:cache`

---

## 💳 Payment Architecture (locked Jun 7–16, 2026)

### BillPlz
- **V3 bills** — customer checkout (`POST /api/v3/bills`, form-encoded)
- **V5 Payment Orders** — vendor/rider disbursements (weekly batch + manual)
- **Webhook**: `POST https://preprod.ondewei.my/webhooks/billplz` (CSRF-exempt)
- **X-Signature fix** (Jun 8, commit `7780573`): replaced `ksort` with `uksort` comparator in `BillplzService.php` — BillPlz uses longer-key-wins prefix ordering

### PAYMENT_GATEWAY_ENABLED
- `true` = real BillPlz flow (preprod/prod)
- `false` = demo mode: checkout settles instantly, order goes straight to `pending`, no BillPlz call. Used by Aiman for dev.
- **Preprod must be `true`**

### Order Lifecycle
```
pending_payment → (BillPlz webhook paid=true) → pending → (rider accepts) → processing → delivered
```
- Delivery chat created AFTER payment confirmed (not at order creation)
- `scopeActive()` excludes `pending_payment` — rider/vendor never see unpaid orders

### PERKESO
- 1.25% of `delivery_fee` per order, per rider
- Annual cap: RM 157.20 / rider / calendar year
- **Intended**: fire at `delivered` status — `rider_id`, `ic_no`, and `delivery_proof_lat/lng` all available only at delivery
- **Bug (Jun 16)**: currently placed in BillPlz webhook where `rider_id` is NULL → silently skipped. `perkeso_deductions` table stays empty. Fix planned: move to `Rider/OrderController::deliver()`.
- If API fails: `SubmitPerkesoDeductionJob` retries with delay (5 attempts)
- `perkeso_deductions` table tracks every submission

### Disbursements (BillPlz V5 PO)
- Weekly batch: Monday 09:00 MYT (`disbursements:process-weekly` in Kernel)
- Manual: admin can trigger per-vendor or per-rider from `/admin/disbursements`
- `DisbursementService::pendingBalances()` — batch query (no N+1)

---

## 🤖 AI Chat-Ordering (Aiman, Jun 14)
- Customer can order via AI chat (OpenAI)
- Config: `CHAT_ORDER_AI_ENABLED`, `CHAT_ORDER_AI_MODEL=gpt-5.4-mini`, `OPENAI_API_KEY`
- **Disable on preprod** until ready: `CHAT_ORDER_AI_ENABLED=false`
- Chat messages auto-pruned every 24 hours (`chat-order:prune` at 03:30 MYT)

---

## ⚙️ Key `.env` Keys (preprod)
```
PAYMENT_GATEWAY_ENABLED=true        ← must be true
BILLPLZ_ENV=sandbox                 ← or production when live
BILLPLZ_SANDBOX_URL=https://www.billplz-sandbox.com
BILLPLZ_PRODUCTION_URL=https://www.billplz.com
BILLPLZ_SECRET_KEY=                 ← production key
BILLPLZ_X_SIGNATURE_KEY=           ← production X-Signature key
BILLPLZ_COLLECTION_ID=             ← bill collection
BILLPLZ_PO_COLLECTION_ID=          ← payment order collection
CHAT_ORDER_AI_ENABLED=false        ← keep false until ready
OPENAI_API_KEY=                    ← blank until enabling AI chat
CHAT_ORDER_AI_MODEL=gpt-5.4-mini
```

---

## 🔴 Outstanding (pre-launch checklist)
- [x] Run `php artisan migrate` on preprod ✅ Jun 16
- [x] Add 3 env keys to preprod `.env` (`PAYMENT_GATEWAY_ENABLED=true`, `CHAT_ORDER_AI_ENABLED=false`, `OPENAI_API_KEY=`) ✅ Jun 16
- [ ] **Fix bill_url redirect**: `PaymentController::pending()` → add PaymentTransaction lookup → redirect to `bill_url` when status=pending
- [ ] **Fix rider history earnings**: `history.blade.php` lines 64+115 change `$order->total_amount` → `$order->delivery_fee`
- [ ] E2E test on preprod: checkout → BillPlz → webhook → `pending` → riders notified → `perkeso_deductions` populated
- [ ] Clear test order data from PROD (overdue since Jun 5)
- [ ] Email BillPlz for e-wallet activation (SSM + KYC docs)
- [ ] Enable all payment channels in admin
- [ ] Legacy data migration on PROD at launch day
- [ ] Merge `feature/push-notification` → `main` (production deploy)

## 🟡 Feature / Fix Backlog (added Jun 20, 2026)
- [ ] **Payout** — vendor/rider payout flow (BillPlz V5 PO, review full cycle)
- [ ] **Cancellation customer process** — customer-side order cancellation flow (rules, refund trigger, status update)
- [ ] **PERKESO deduction bug** — remove from BillPlz webhook (rider_id is NULL there), move to `Rider/OrderController::deliver()` where rider_id + IC + delivery coords are available
- [ ] **New pricing fee system** — implement updated delivery fee pricing model
- [ ] **Register rider & vendor: new inputs** — add fields required by PERKESO (IC no, etc.) and BillPlz (bank acc, etc.) to registration forms

---

## 📜 Key Commits (Jun 2026)
| Commit | Date | What |
|---|---|---|
| `aff2513` | Jun 8 | ENUM fix: `pending_payment` to `order_status_history.status` |
| `7780573` | Jun 8 | **X-Signature fix**: ksort → uksort in BillplzService.php |
| `f699549` | Jun 14 | Aiman: AI chat, admin overhaul, full BillPlz + PERKESO (162 files) |
| `caf06b2` | Jun 16 | Merge: AI-integration → feature/push-notification (7 conflicts resolved) |
| `dda7e4f` | Jun 16 | Vite build artifacts committed (fixed preprod 500) |
