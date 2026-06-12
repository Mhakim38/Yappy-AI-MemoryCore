# 🏛️ AP JKSM — Sistem Alasan Penghakiman JKSM
**Client**: 2Q Alliance (2QSC)
**Role**: Hakim — Jr. Software Developer (Laravel)
**Date Analysed**: June 4, 2026
**Repo**: `gitlab.com/2QSC/ap_jksm` (GitLab, private)
**Local path**: `/Users/hakim/holeeMonth/ap_jksm/ap_jksm`
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

### What is iPayment?
**Sistem Terimaan Elektronik Kerajaan Persekutuan** — JANM (Jabatan Akauntan Negara Malaysia) federal payment system.

### Channels
- **Collection Channel** (available now): Customer logs into iPayment portal. Agensi = data provider only.
- **Gateway Channel** (under planning): Customer logs into JKSM system. Agensi handles full payment, sends data to iPayment.
- **JKSM should use Gateway Channel** (customers already log into JKSM).

### Key API Processes
| Code | Direction | Purpose |
|------|-----------|---------|
| `BILEXT001` | JKSM → iPayment | Send bill/invoice info (real-time) |
| `BILEXT101` | JKSM → iPayment | Send bill/invoice info (batch) |
| `RECEXT001` | JKSM → iPayment | Confirm payment collected |
| `RECEXT201` | iPayment → JKSM | **Receipt callback** (this is where JKSM creates ReceiptDetail) |
| `RECEXT301` | iPayment → JKSM | Receipt batch |
| `ERROR9999` | iPayment → JKSM | Error notification batch |

### Auth & Security
- HTTP Basic Auth (username/password from JANM)
- IP whitelisting (JKSM server IPs must be registered)
- GPG encryption for batch SFTP files
- No HMAC signature (simpler than BillPlz)

### API Envelope Format (all calls)
```json
{
  "kod_proses": "BILEXT001",
  "kod_perkhidmatan_iPayment": "S0000X",
  "tarikh_dan_masa": "DDMMYYYYhh:mm:ss",
  "nombor_rujukan_message": "BILEXT0010100010001S0000X17052026XXXXXXX",
  "mesej": { ... }
}
```

### Amount Constraint
⚠️ **Amount must be multiple of RM 0.10 or RM 0.05 ONLY** — validation required before sending to iPayment.

### ESB Server
- **Domain**: `esb-ipayment.anm.gov.my`
- **SFTP Port**: 2222
- **HTTPS Port**: 443

---

## ❓ What We Need FROM JKSM/JANM (for iPayment integration)

| Item | Description | Who to ask |
|------|-------------|------------|
| `kod_agensi` | Agency code format `{Ministry:2}{Dept:4}{Agency:4}` | JANM / JKSM IT |
| `kod_perkhidmatan_iPayment` | Service code (S00001 format) | JANM |
| HTTP Basic Auth credentials | Username + password for API | JANM |
| JKSM server IP | For JANM to whitelist | DevOps / server admin |
| JANM ESB IP list | For JKSM firewall to allow | JANM |
| GPG public key | From JANM, to encrypt outgoing batch files | JANM |
| Sandbox/staging URL | Testing environment endpoint | JANM |
| `kod_lokasi` + `kod_sublokasi` | Location codes in master data | JKSM admin |
| `kod_penjenisan` | Classification codes (charge lines) | JKSM admin |
| `kumpulan_ptj_dan_ptj` | Department group codes | JKSM admin |

---

## 📄 iPayment IDD V1.9.1 — Deep API Analysis (Jun 10, 2026)
**Source**: `IDD - V 1.9.1.pdf` (108 pages) — JANM, dated 11 Mei 2026
**Analysed by**: Yappy (full document sweep)

### ⚙️ API Architecture — Important Notes
- **NOT FastAPI** — Built on **WSO2 Enterprise Service Bus**
- **ALL real-time calls use `POST`** — confirmed pg.83 testing section
- **Routing by `kod_proses`** — Same URL, different payload tells iPayment what to do
- **Auth**: HTTP Basic Auth (username + password supplied by JANM post-whitelist approval)
- **IP Whitelist**: Mandatory both ways. Hakim = vendor, NOT JKSM IT. Need: (A) JKSM IT gives server IP → register with JANM. (B) JANM gives ESB IP → JKSM IT opens in firewall for RECEXT201 callbacks. Status: 🔴 PENDING (2:30pm meeting Jun 10)
- **Whitelist status**: 🔴 PENDING — Hakim to confirm with JKSM at 2:30pm meeting (Jun 10)

### 🌐 Server Details
| Item | Value |
|------|-------|
| Base URL | `https://esb-ipayment.anm.gov.my` |
| SFTP server | `esb-ipayment.anm.gov.my` |
| HTTPS Port | `443` |
| SFTP Port | `2222` |

### 📦 Universal Outer Wrapper (ALL real-time requests AND responses)
```json
{
  "kod_proses": "BILEXT001",
  "kod_perkhidmatan_iPayment": "S00001",
  "tarikh_dan_masa": "DDMMYYYYhh:mm:ss",
  "nombor_rujukan_message": "KodProses(9)+KodAgensi(10)+KodPerkhidmatan(6)+Tarikh(8)+RunNo(7)",
  "mesej": { ... }
}
```
Response adds: `kod_respond` (`00`=Berjaya, `01`=Business rules error, `02`=Destination not available) + `perihal_respond` (if not berjaya) + `mesej`

### 🗂️ All 5 Endpoints / Processes

| # | Process ID | Direction | Method | URL / Channel | Purpose |
|---|-----------|-----------|--------|---------------|---------|
| 1 | **BILEXT001** | JKSM → iPayment | `POST` | `https://esb-ipayment.anm.gov.my/api/maklumatterimaan-realtime-inv` | Submit bill records |
| 2 | **RECEXT001** | JKSM → iPayment | `POST` | Same URL as BILEXT001 (routed by `kod_proses`) | Submit payment info |
| 3 | **RECEXT201** | iPayment → JKSM | `POST` | JKSM's own URL (must register with JANM) | Receive receipts from iPayment |
| 4 | **RECEXT302** | iPayment → JKSM | SFTP pull | `XXXX@esb-ipayment.anm.gov.my:2222/OUT` | Batch receipt report (GPG encrypted) |
| 5 | **ERROR9999** | iPayment → JKSM | SFTP push | Batch to JKSM server | Error notifications |

---

### ENDPOINT 1: BILEXT001 — Maklumat Terimaan (Bill Submission)
**URL:** `POST https://esb-ipayment.anm.gov.my/api/maklumatterimaan-realtime-inv`

**5 Jenis Proses:** `01`=Baharu · `02`=Tambah Amaun · `03`=Kurang Amaun · `04`=Batal · `05`=Kemas Kini

**4 Jenis Maklumat Terimaan** (from IDD; 5th type on pg.21 needs JKSM confirmation):
- `01` = Bil (e.g. Sewa, Bill Hospital) — Multiple charge lines, requires jumlah amounts
- `02` = Bil Tanpa Amaun (e.g. bayaran balik pinjaman) — Single charge line only
- `03` = Bayaran Tanpa Bil dan Amaun (e.g. Sumbangan) — Single charge line
- `04` = Bayaran Tanpa Kadar (e.g. Yuran Kursus, Tender) — Multiple charge lines, requires amounts

⚠️ **Amount constraint**: `jumlah_amaun_perlu_dibayar` and `amaun` per charge line MUST be **multiples of 0.10 or 0.05**

**Header Section (inside `mesej`):**
| Field | Type | M/O |
|-------|------|-----|
| `kod_agensi` | VARCHAR(10) | **M** — KodKementerian(2)+KodJabatan(4)+KodAgensi(4) e.g. `0100010001` |
| `kod_perkhidmatan_iPayment` | VARCHAR(6) | **M** — e.g. `S00001` |
| `jumlah_maklumat_terimaan` | VARCHAR(7) | **M** — count of records |
| `jumlah_amaun` | DECIMAL(13,2) | **M** if jenis `01`/`04` |

**Detail Section 1 — Per Bill (1:1):**
| Field | Type | M/O | Notes |
|-------|------|-----|-------|
| `jumlah_charge_line` | VARCHAR(7) | **M** | |
| `jenis_proses` | VARCHAR(2) | **M** | 01-05 |
| `jenis_maklumat_terimaan` | VARCHAR(2) | **M** | 01-04 |
| `no_rujukan_1` | VARCHAR(25) | **M** if proses `01`,`02`,`03` | Bill ref no. Key field |
| `tarikh_dan_masa_no_rujukan_1` | DATETIME | **M** | DDMMYYYYhh:mm:ss |
| `no_rujukan_2` | VARCHAR(25) | **M** if proses `02`,`03`,`04`,`05` | Original ref for mapping |
| `perihal` | VARCHAR(255) | **M** | e.g. "Bil sewa bangunan" |
| `jumlah_tanpa_cukai` | DECIMAL(13,2) | **M** if jenis `01`/`04` | |
| `jumlah_cukai` | DECIMAL(13,2) | **M** if jenis `01`/`04` with tax | |
| `jumlah_dengan_cukai` | DECIMAL(13,2) | **M** if jenis `01`/`04` | tanpa_cukai + cukai |
| `jumlah_amaun_perlu_dibayar` | DECIMAL(13,2) | **M** if jenis `01`/`04` | ⚠️ must be multiple of 0.10/0.05 |
| `tarikh_dan_masa_batal_atau_kemaskini` | DATETIME | **M** if proses `04`/`05` | |
| `tarikh_dan_masa_mula_bayaran` | DATETIME | **O** | Payment start date |
| `tarikh_dan_masa_akhir_bayaran` | DATETIME | **O** | Must be > mula_bayaran |
| `sebab` | VARCHAR(100) | **M** if proses `02`,`03`,`04`,`05` | |
| `kategori` | VARCHAR(2) | **M** if proses `04`/`05` | 04: `01`=Hapus Kira,`02`=Lain. 05: `03`=Ubah Perkhidmatan,`04`=Ubah Master,`05`=Lain |
| `kod_lokasi` | VARCHAR(5) | **M** | Transaction location code |
| `kod_sublokasi` | VARCHAR(5) | **M** | |

**Detail Section 2 — Pelanggan (1:1, wajib for jenis_proses `01` & `05`):**
| Field | Type | M/O |
|-------|------|-----|
| `nombor_rujukan_pelanggan` | VARCHAR(25) | **O** |
| `kategori_identiti_pelanggan` | VARCHAR(2) | **M** if jenis `01`/`02` — `01`=Individu,`02`=Organisasi |
| `kod_identiti_pelanggan` | VARCHAR(10) | **M** — Individu: JIM/JPN/NA. Organisasi: ROS/SKM/SSM/NA |
| `jenis_identiti_pelanggan` | VARCHAR(25) | **M** — JPN→MyKad/MyKAS/MyPR. JIM→Pasport. ROS→Organisasi. SSM→Syarikat. SKM→Koperasi |
| `nombor_identiti_pelanggan` | VARCHAR(20) | **M** — JPN/SSM max 12, ROS/SKM max 20 |
| `nama` | VARCHAR(100) | **M** if jenis `01`/`02` |
| `alamat_1` | VARCHAR(35) | **M** if jenis `01`/`02` |
| `alamat_2` | VARCHAR(35) | **O** |
| `alamat_3` | VARCHAR(35) | **O** |
| `poskod` | VARCHAR(10) | **M** if jenis `01`/`02` — local max 5 chars; overseas max 10 |
| `bandar` | VARCHAR(35) | **M** if jenis `01`/`02` — Lampiran 8 |
| `negeri` | VARCHAR(2) | **M** if jenis `01`/`02` — Lampiran 2 |
| `negara` | VARCHAR(2) | **M** if jenis `01`/`02` — Lampiran 3, e.g. `MY` |
| `no_tel` | VARCHAR(20) | **O** — for SMS notification |
| `emel` | VARCHAR(100) | **O** — for email notification |

**Detail Section 3 — Charge Line (1:N, Multiple for jenis `01`/`04`, Single for `02`/`03`):**
| Field | Type | M/O |
|-------|------|-----|
| `no_rekod` | VARCHAR(7) | **M** — right-justified, leading zeros |
| `kod_penjenisan` | VARCHAR(20) | **M** — unique per PTJ/PTJ Menyedia. e.g. `INV_H0161199` |
| `kumpulan_ptj_dan_ptj_menyedia` | VARCHAR(8) | **M** — Kump.PTJ(2)+PTJ(6) e.g. `28020101` |
| `vot_dana` | VARCHAR(5) | **M** if Vot Mengurus/Pembangunan/PFI/Amanah |
| `pegawai_pengawal_dipertanggung` | VARCHAR(2) | **M** |
| `kumpulan_ptj_dan_ptj_dipertanggung` | VARCHAR(8) | **M** |
| `program_aktiviti` | VARCHAR(9) | **M** if Vot Mengurus |
| `projek` | VARCHAR(16) | **M** if Vot Pembangunan/PFI — Vot(3)+Butiran(5)+Setia(3)+SubSetia(4)+CaraPembiayaan(1) |
| `kod_akaun` | VARCHAR(8) | **M** — e.g. `H0171101` |
| `amaun` | DECIMAL(13,2) | **M** if jenis `01`/`04` — ⚠️ must be multiple of 0.10/0.05 |

---

### ENDPOINT 2: RECEXT001 — Maklumat Pembayaran (Payment Submission)
**URL:** `POST https://esb-ipayment.anm.gov.my/api/maklumatterimaan-realtime-inv` (same as BILEXT001)
**Only for** `jenis_maklumat_terimaan = 01` (Bil). **2 Jenis Proses:** `01`=Bayaran, `02`=Batal.

**Header:** `kod_agensi`, `kod_perkhidmatan_iPayment`, `jumlah_bilangan_maklumat_pembayaran`, `jumlah_amaun_maklumat_pembayaran`

**Detail Section 1 (1:1):**
| Field | Type | M/O |
|-------|------|-----|
| `jenis_resit` | VARCHAR(1) | **M** — `N`=Normal |
| `jenis_proses_maklumat_pembayaran` | VARCHAR(2) | **M** — `01`=Bayaran,`02`=Batal |
| `no_rujukan_maklumat_pembayaran` | VARCHAR(25) | **M** — Receipt no from JKSM system |
| `tarikh_dan_masa_maklumat_pembayaran` | DATETIME | **M** |
| `amaun_maklumat_pembayaran` | DECIMAL(13,2) | **M** |
| `sebab_batal_maklumat_pembayaran` | VARCHAR(100) | **M** if proses `02` |
| `tarikh_dan_masa_batal_maklumat_pembayaran` | DATETIME | **M** if proses `02` |
| `no_rujukan_maklumat_terimaan` | VARCHAR(25) | **M** — original bill ref (key) |

**Detail Section 2 — Charge Line (1:N):** Same structure as BILEXT001 Sec 3

---

### ENDPOINT 3: RECEXT201 — Maklumat Resit (Receipt INCOMING to JKSM)
**iPayment POSTs to JKSM's URL** — JKSM must register endpoint URL with JANM
**2 Jenis Proses:** `01`=Bayaran, `02`=Batal/Ganti

**Detail Section 1 (1:1) — Key fields iPayment sends:**
| Field | Type | Notes |
|-------|------|-------|
| `jenis_resit` | VARCHAR(1) | `N`=Normal Receipt |
| `jenis_proses_resit` | VARCHAR(2) | `01`=Bayaran,`02`=Batal/Ganti |
| `nombor_rujukan_1` | VARCHAR(20) | iPayment receipt no. Format: `R{RCPTTYPE}{YY}{MM}{PTJID}{RN}` |
| `tarikh_dan_masa_resit` | DATETIME | |
| `saluran_pembayaran` | VARCHAR(1) | `1`=Portal,`2`=EDC,`3`=App |
| `mod_pembayaran` | VARCHAR(2) | `01`=DuitNow DOBW,`02`=DuitNow QR,`03`=Debit Temp,`04`=Debit Intl,`05`=Kredit Temp,`06`=Kredit Intl,`07`=Prabayar,`08`=Caj,`09`=eDompet |
| `rangkaian` | VARCHAR(3) | `001`=Semasa/Simpanan,`002`=KadKredit,`003`=eDompet,`004`=Visa,`005`=MasterCard,`006`=MyDebit,`007`=AmExpress |
| `pengeluar` | VARCHAR(8) | Issuing bank — Lampiran 4 & 5 |
| `nombor_rujukan_transaksi_iPayment` | VARCHAR(20) | iPayment txn ref |
| `amaun_resit` | DECIMAL(13,2) | |
| `no_rujukan_maklumat_terimaan` | VARCHAR(25) | JKSM's original bill no |
| `no_rujukan_2` | VARCHAR(20) | **M** if proses `02` — cancelled receipt no |
| `sebab_batal_resit` | VARCHAR(100) | **M** if proses `02` |
| `kategori_batal_resit` | VARCHAR(25) | **M** if proses `02` — `01`=Ubah perkhidmatan,`02`=Ubah master,`03`=Lain |

---

### BATCH PROCESSES (SFTP — NOT HTTP API)

**RECEXT302** — Laporan Resit (Batch via SFTP)
- Format: Column Separator `|` (Single Pipe), GPG encrypted
- Filename: `RECEXT302{KodAgensi:10}{KodPerkhidmatan:6}{DDMMYYYY:8}{RunNo:3}.GPG`
- Key fields: section_indicator, no_rekod, nombor_resit, tarikh_dan_masa_resit, mod_pembayaran, rangkaian, pengeluar, amaun_resit

**ERROR9999** — Notifikasi Ralat (Batch)
- 3 error types: (1) Incoming Upfront (decrypt/filename wrong), (2) Incoming Data (validation fail), (3) Fund Transfer fail
- Header: section_indicator`00`, nama_fail, tarikh_dan_masa_fail, kod_agensi, kod_proses, jumlah_bilangan_transaksi
- Detail: section_indicator`01`, bilangan, no_rujukan, perihal, kod_ralat (Lampiran 6), keterangan_ralat

---

### ❓ Outstanding Questions for JKSM/JANM

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | **IP Whitelist** | 🔴 PENDING | **Vendor POV**: (A) JKSM IT must give Hakim the production+staging server IP → Hakim registers it with JANM so API calls are accepted. (B) JANM provides their ESB IP → Hakim passes to JKSM IT to open in their firewall so RECEXT201 receipt callbacks can reach the system. Ask JKSM at 2:30pm meeting Jun 10 to coordinate both sides. |
| 2 | **`kod_agensi`** | 🔴 PENDING | VARCHAR(10). Format: KodKementerian(2)+KodJabatan(4)+KodAgensi(4). **See pg.35 of IDD** — this is registered in iPayment master data. JKSM + JANM must confirm |
| 3 | **`kod_perkhidmatan_iPayment`** | 🔴 PENDING | VARCHAR(6). Format: KategoriPerkhidmatan(1)+NomborLarian(5). Issued by JANM after service registration |
| 4 | **HTTP Basic Auth credentials** | 🔴 PENDING | Username + password from JANM |
| 5 | **Which `jenis_maklumat_terimaan`** | 🟡 PARTIAL | Pg.21 lists 5 business types. IDD has 4 codes (01-04). JKSM to confirm which they use (affects charge line structure + mandatory fields). Likely `01` Bil + `04` Bayaran Tanpa Kadar at minimum |
| 6 | **JKSM callback URL for RECEXT201** | 🔴 PENDING | URL JKSM exposes for iPayment to POST receipts to |
| 7 | **`kod_lokasi` + `kod_sublokasi`** | 🔴 PENDING | From iPayment master data, ask JKSM admin |
| 8 | **`kod_penjenisan`** | 🔴 PENDING | Classification codes, unique per PTJ. Must be set up in iPayment master data FIRST |
| 9 | **`kumpulan_ptj_dan_ptj`** | 🔴 PENDING | JKSM department/PTJ codes |
| 10 | **Sandbox/staging URL** | 🔴 PENDING | For testing before production |
| 11 | **GPG public key** | 🔴 PENDING | For batch SFTP encryption |

---

## 📝 Integration Flow (Based on IDD Analysis)
```
1. JKSM creates invoice/bil → POST BILEXT001 → iPayment registers bill
2. Citizen pays on JKSM portal
3. JKSM confirms payment → POST RECEXT001 → iPayment records payment
4. iPayment processes → POST RECEXT201 → JKSM receives official receipt
5. iPayment sends batch report → SFTP RECEXT302 → JKSM reconciles
6. Errors (if any) → SFTP ERROR9999 → JKSM handles errors
```

---

**Last updated**: June 10, 2026 by Yappy — Full IDD V1.9.1 deep analysis
**Analysed by**: Yappy (direct PDF sweep, 108 pages)
