# 🏛️ AP JKSM — Sistem Alasan Penghakiman JKSM
**Client**: 2Q Alliance (2QSC)
**Role**: Hakim — Jr. Software Developer (Laravel)
**Date Analysed**: June 4, 2026
**Repo**: (GitLab, private)
**Local path**: `/Users/hakim/holeeMonth/2qa_projects/ap_jksm/ap_jksm`
**Status**: 🟢 Active development

---

## 🎯 What It Is
A judicial decision publication and management system for **Malaysian Islamic courts (JKSM — Jabatan Kehakiman Syariah Malaysia)**. Manages case decisions (Alasan Penghakiman), legal journals (Jurnal Hukum), publication workflows (PUUMAS), payment for document access, and external court system sync (ESV3).

---

## 🛠️ Tech Stack
| Layer | Tech |
|---|---|
| Framework | Laravel 10.10+ |
| PHP | ^8.1 |
| Database | MySQL |
| Frontend | Livewire 3.5 + Blade + Bootstrap 5 |
| Build tool | Vite 5 |
| Auth | Keycloak SSO (primary) + Laravel native (fallback) + Sanctum (API) |
| Roles/Permissions | Spatie Laravel Permission ^6 |
| PDF | DomPDF + PDF merging (iio/libmergepdf) + thumbnail generation |
| Payments | Stripe (cards) + Local Order (institutional) |
| Audit | owen-it/laravel-auditing |
| Excel | Maatwebsite/Excel |
| Media | Spatie MediaLibrary |
| Date | Hijri calendar (alkoumi/laravel-hijri-date) |
| HTTP client | Guzzle (external ESV3 API sync) |

---

## 🗄️ Key Database Tables
| Table | Purpose |
|---|---|
| `alasan_penghakiman` | Core case decision records |
| `ap_pihak` | Case parties (plaintiffs/defendants) |
| `ap_wakil` | Lawyers/representatives |
| `ap_hakim` | Judges |
| `ap_dokumen` | Case documents |
| `selection_ap` | Case selection for publication |
| `editor_selection` | Stage 1 editor assignments |
| `editor_p2_selection` | Stage 2 editor assignments |
| `jurnal_hukum` | Legal journal articles |
| `pu_puumas` | PUUMAS publication records (soft deletes) |
| `orders` | Purchase orders |
| `order_details` | Order line items |
| `bill_invoices` | Invoices |
| `bill_payments` | Payment records |
| `payment_gateway_txns` | Stripe/gateway logs |
| `lo_requests` | Local Order (institutional purchase) |
| `ref_*` tables (13) | Reference/lookup data (states, courts, status, etc.) |
| `ap_import_batches` | ESV3 import batches |
| `ap_import_staging` | Import validation staging |
| `esv3_logs` | External sync logs |
| `audits` | Full audit trail (all CRUD) |

**Notable patterns**: Soft deletes on key tables, `created_by`/`updated_by`/`deleted_by` audit columns, JSON fields (`jh_list`), status-driven workflows via `ref_status` (not enums).

---

## 🏗️ App Structure
- **79 Models** — domain-rich, Malay naming (reflects institutional context)
- **110 Livewire components** — organised by feature domain
- **9 Controllers** — mostly API + PDF + checkout
- **3 Services** — ExternalSyncService, PdfMergeService, PdfThumbnailService
- **8 Artisan commands** — ESV3 import pipeline, PDF sync, data migration
- **Route file**: `ap_jksm.php` (~600+ routes, all auth-protected)

---

## 🔄 Core Workflows

### Case Decision Workflow
```
Create AP → Import from ESV3 (or manual) → Selection & Editor Assignment
→ Stage 1 Review → Stage 2 Review (PJE) → Edit → Publish
```

### PUUMAS Publication Workflow
```
Create PUUMAS → Add cases + Journal articles → Committee selection
→ Screening Stage 1 → Screening Stage 2 → Edit → Publish with cover page
```

### Payment Workflow
```
Search/browse documents → Add to cart (Troli) → Checkout
→ Stripe (individual) OR Local Order/LO (institutional)
→ Payment verification → Invoice/receipt PDF
```

---

## 🔌 Key Integrations
| Integration | Purpose |
|---|---|
| **Keycloak** | Enterprise SSO for government users |
| **ESV3** (external court API) | Sync case data from court system via HTTP |
| **Stripe** | Credit card payments for document purchase |
| **Spatie MediaLibrary** | File/document management |

---

## 📁 Route Groups (URL prefixes)
- `/pentadbiran` — Admin panel (users, reference data, roles)
- `/pengurusan-alasan-penghakiman` — Case decision CRUD
- `/pemilihan-alasan-penghakiman` — Case selection + editor assignment
- `/saringan-alasan-penghakiman` — Stage 1 & 2 review
- `/suntingan` — Editing
- `/puumas` — Journal management + screening + publishing
- `/terbit-alasan-penghakiman-dan-jurnal-hukum` — Publication
- `/carian-interaktif` — Search (internal + external) + subscription
- `/pembayaran-dan-kewangan` — Payments, cart, orders, receipts
- `/pelaporan-dan-statistik` — Reports

---

## 🚩 Notable Findings / Things to Know

1. **Dual auth system** — Keycloak SSO + Laravel native. Guard configured in `auth.php`. Keycloak config at `config/keycloak-web.php`.

2. **Malay naming throughout** — Models, routes, Livewire components all in Bahasa Malaysia. Normal for government system.

3. **ESV3 integration is in progress** — Mock API endpoints (`/api/mock/esv3`) and multiple import commands suggest ongoing work. `esv3_logs` table tracks sync history.

4. **PDF-heavy** — DomPDF + merge + thumbnail services. Most output is document-centric. Test PDF routes (`/test-jurnal-hukum-cover`) are dev-only.

5. **Two payment paths** — Stripe (individual buyers) + LO/Local Order (government/institutional buyers who can't use cards). Both paths generate invoices + receipts.

6. **No `.lock` file on clone** — Had to run `composer install --no-audit` due to security advisories on `livewire/livewire 3.5` (CVEs) and `firebase/php-jwt` (via Keycloak guard). Not production-blocking for local dev.

7. **`ReadForHamizan.md`** in repo — internal note from a previous developer. "Saya stress gaji tak masuk" (April 1, 2026) — context note, previous dev had payroll issues. Worth knowing for team dynamics.

8. **`config/leftbar.php`** — Custom sidebar navigation config. Route/menu changes may need to update this file.

9. **`UserRolePermission`** custom table — additional custom RBAC layer on top of Spatie. Check this when dealing with permission issues.

---

## 🔑 Config Files to Know
| File | Purpose |
|---|---|
| `config/keycloak-web.php` | Keycloak SSO (base_url, realm, client_id, client_secret) |
| `config/leftbar.php` | Sidebar navigation menu |
| `config/permission.php` | Spatie roles/permissions |
| `config/audit.php` | Audit logging |
| `config/dompdf.php` | PDF generation |

---

## ⚙️ Setup (Local)
```bash
git clone git@gitlab.com:2QSC/ap_jksm.git
cd ap_jksm
composer install --no-audit   # bypass security advisories on locked packages
cp .env.example .env
php artisan key:generate
# Configure DB + Keycloak in .env
php artisan migrate
php artisan db:seed (if seeders exist)
npm install && npm run dev
```

---

## 🧾 LO (Local Order) Payment Flow — Detailed Findings
*(Added Jun 8, 2026 — Hana deep-dive)*

### Flow Summary
```
AGENSI submits LO → lo_status=15 (SEMAKAN)
ADMIN reviews    → lo_status=13 (LULUS) or 14 (TOLAK)
FINANCE confirms → lo_status=16 (BAYARAN_DITERIMA)
RESIT viewed     → Resit.php → downloadResitPembayaranPdf()
```

### Key Files
| Step | File | Method | Line |
|------|------|--------|------|
| Submit LO | `TroliPembelian.php` | `saveButiranPembayranLO()` | 123 |
| Admin review | `Semakan.php` | `hantarSemakan()` | 30 |
| Finance confirm | `Catatan.php` | `sahkan()` | 31 |
| View receipt | `Resit.php` | `downloadResitPembayaranPdf()` | 30 |

All under: `app/Http/Livewire/PembayaranDanKewangan/`

### Status Codes (ref_status)
`12=DRAF` | `13=LULUS` | `14=TOLAK` | `15=SEMAKAN` | `16=BAYARAN_DITERIMA` | `17=BAYARAN_GAGAL` | `18=BAYARAN_DIKEMBALIKAN`

---

## 🔴 Known Bugs

### BUG #1 — CRITICAL: ReceiptDetail NOT created on LO payment confirmation
**File**: `Catatan.php:31-75` (`PengesahanPembayaran/Catatan.php`)
**Impact**: Receipt download crashes — `$receipt` is NULL, PDF generation fails
**Cause**: `sahkan()` creates `BillPayment` + updates `Order`/`LoRequest` but never calls `ReceiptDetail::create()`
**Fix needed** (add after BillPayment creation):
```php
$receiptNo = 'RCP-' . strtoupper(uniqid());
ReceiptDetail::create([
    'payable_type'      => BillPayment::class,
    'payable_id'        => $billPayment->id,
    'receipt_no'        => $receiptNo,
    'receipt_date'      => now(),
    'grand_total'       => $totalAmount,
    'status_receipt_id' => ReceiptDetail::BAYARAN_DITERIMA,
    'is_final'          => null,
    'created_by'        => auth()->id(),
    'updated_by'        => auth()->id(),
]);
```

### BUG #2: Sebut Harga PDF never persisted
**File**: `TroliPembelian.php:218` → `downloadSebutHargaPdf()`
**Impact**: No audit trail, regenerated content may differ over time

### BUG #3: Invois PDF never persisted
**File**: `TroliPembelianPengesahanLo.php:169` → `downloadInvois()`
**Impact**: No version control of what invoice was presented

---

## 🏦 iPayment Integration — Analysis (Jun 8, 2026)

