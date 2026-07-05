# ⚖️ AP JKSM — Project Reference
*First documented: Jun 16, 2026 by Yappy*
*Last updated: Jun 25, 2026 — iPayment flow confirmed, Bandar select implemented*
*Status: 🟢 Active FT development — Hakim is developer (2Q Alliance)*

---

## 📌 What Is This System?

**AP JKSM** — Malaysian Syariah court judgment payment and case management system for **Jabatan Kehakiman Syariah Malaysia (JKSM)**. Handles payment processing for court fines, billings, and legal administration.

**Repo**: `/Users/hakim/holeeMonth/2qa_projects/ap_jksm/ap_jksm`
**Branch**: `Hakim-test`
**Mode**: FT Mode — 2Q Alliance. NEVER commit without Hakim's manual review.

---

## 🛠️ Tech Stack

| Layer | Detail |
|---|---|
| Framework | Laravel 10 |
| PHP | ^8.1 |
| Frontend | Blade + **Livewire 3.5** |
| CSS | Bootstrap |
| Payment | iPayment (JANM) integration — BILEXT001 + RECEXT001 complete |
| Auth | Standard Laravel Auth |

---

## 💳 iPayment (JANM) Integration

### IDD Reference
`/Users/hakim/Sweet/2Q Alliance/Projects/JKSM/iPayment/IDD - V 1.9.1.pdf`

### Payment Methods
- Option 1 = FPX
- Option 2 = Visa
- Option 3 = iPayment (BILEXT001 + RECEXT001) ← in progress

### Flow Sequence (confirmed Jun 25 from sequence diagram in IDD V1.9.2)
```
1 ↓  BILEXT001  (3.2.1) — We → iPayment  (register bill)
2 ↓  iPayment   → Customer   (Maklumat Bil/Invois displayed on iPayment portal)
3 ↓  Customer pays on iPayment portal (FPX/DuitNow/etc. — not our concern)
4 ↓  RECEXT001  (3.2.2) — We → iPayment  (Maklumat Pembayaran — auto-called after BILEXT001 when JMT=01)
5 ← RECEXT201  (3.3.1) — iPayment → Us  (official receipt callback — ends here)
        → HTTP JSON response (kod_respond 00/01) is MANDATORY (Real-Time HTTP, connection waits)
        → reconcile order → BAYARAN_DITERIMA
5a ← ERROR9999 (3.4.1) — iPayment → Us  (ONLY if error occurs — Batch SFTP)
6 ← RECEXT302  (3.3.2) — iPayment → Us  (batch receipt report via SFTP — ends here, optional)
```

### CRITICAL: RECEXT201 HTTP Response
The response we return IS the HTTP response to iPayment's POST. This is NOT us "calling iPayment back".
iPayment makes the POST and waits — if we don't return JSON, the connection hangs/times out.
IDD page 71-72 explicitly defines the response format (kod_respond, perihal_respond, mesej).
Our IPaymentCallbackController is correct and must stay.

---

## 📐 BILEXT001 — Maklumat Terimaan Sistem Luar (3.2.1)

**Direction:** We call iPayment  
**Trigger:** User clicks Hantar when `$jenisPembayaran == '3'`

### Dictionary
- **JP** = Jenis Proses: 01=Baharu, 02=Penambahan Amaun, 03=Pengurangan Amaun, 04=Batal, 05=Kemas Kini
- **JMT** = Jenis Maklumat Terimaan: 01=Bil, 02=Bil Tanpa Amaun, 03=Bayaran Tanpa Bil & Amaun, 04=Bayaran Tanpa Kadar
- **JIP** = Kategori Identiti Pelanggan: 01=Individu, 02=Organisasi
- **KIP** = Kod Identiti Pelanggan: JIP:01→JPN/JIM/NA; JIP:02→ROS/SKM/SSM/NA

### Payload Structure (3 layers)
- **Outer**: `kod_proses=BILEXT001`, `kod_perkhidmatan_iPayment`, `tarikh_dan_masa`, `no_rujukan_mesej`, `mesej`
- **Layer 1 (mesej)**: `kod_agensi`, `kod_perkhidmatan_iPayment`, `jumlah_maklumat_terimaan`, `jumlah_amaun`, `maklumat_terimaan`
- **Layer 2 (maklumat_terimaan)**: JP/JMT-conditional fields + customer identity + address + `no_rujukan_1=order_no`
- **Layer 3 (maklumat_chargeline)**: 1 per OrderDetail — all config-driven

### Conditional Rules
- JMT:01/02 → address fields (alamat1, poskod, bandar, negeri, negara) required
- JP:01/02/03 → `no_rujukan_1` + `tarikh_dan_masa_no_rujukan_1`
- JP:02/03/04/05 → `no_rujukan_2` + `sebab`
- JMT:01/04 → amount fields (`jumlah_tanpa_cukai` etc.)
- JP:04/05 → `tarikh_dan_masa_batal_atau_kemaskini` + `kategori`

### Key Files
| File | Purpose |
|---|---|
| `app/Http/Livewire/PembayaranDanKewangan/TroliPembelian.php` | Main component — `sendIPaymentBilext001()` |
| `resources/views/livewire/pembayaran-dan-kewangan/troli-pembelian.blade.php` | Cart blade — iPayment UI block under `@if($jenisPembayaran == '3')` |
| `config/ipayment.php` | All env-driven config |

---

## 📐 RECEXT001 — Maklumat Pembayaran Sistem Luar (3.2.2)

**Direction:** We call iPayment  
**Trigger:** Auto-called from `sendIPaymentBilext001()` when JMT=01 (Bil) AND HTTP 202  
**NOT a button** — no blade UI, purely internal

### Dictionary
- **JPMP** = Jenis Proses Maklumat Pembayaran: 01=Bayaran, 02=Batal Maklumat Pembayaran

### Payload Structure (3 layers)
- **Outer**: `kod_proses=RECEXT001`, `kod_perkhidmatan_iPayment`, `tarikh_dan_masa`, `no_rujukan_mesej`, `mesej`
- **Layer A (mesej)**: `kod_agensi`, `kod_perkhidmatan_iPayment`, `jumlah_bilangan_maklumat_pembayaran`, `jumlah_amaun_maklumat_pembayaran`, `maklumat_pembayaran`
- **Layer B (maklumat_pembayaran)**:
  - `jenis_resit` = 'N' (hardcoded)
  - `jenis_proses_maklumat_pembayaran` = JPMP param
  - `no_rujukan_maklumat_pembayaran` = `$order->billPayment->receipt->receipt_no`
  - `tarikh_dan_masa_maklumat_pembayaran` = `$receipt->receipt_date` or `now()`
  - `amaun_maklumat_pembayaran` = `$receipt->grand_total`
  - `no_rujukan_maklumat_terimaan` = `$order->order_no` ← **linkback to BILEXT001**
  - JPMP:02 only → `sebab_batal_maklumat_pembayaran`, `tarikh_dan_masa_batal_maklumat_pembayaran`
- **Layer C (maklumat_chargeline)**: JPMP:01 only — identical to BILEXT001

### Function Signature (reusable)
```php
// Normal flow (auto-called internally):
$this->sendIPaymentRecext001();                        // JPMP=01

// Cancellation (future use):
$this->sendIPaymentRecext001('02', $sebab, $tarikh);   // JPMP=02
```

---

## 🖥️ Blade UI — iPayment Section (`@if($jenisPembayaran == '3')`)

### Form Fields (in order)
1. **Jenis Proses** — `wire:model.live="jenisProses"` select (JP 01-05)
2. **Jenis Maklumat Terimaan** — `wire:model.live="jenisMaklumatTerimaan"` select (JMT 01-04)
3. **Sebab** — text input, shows only JP:02/03/04/05
4. **Kategori** — select, shows only JP:04/05
5. PTJ, LO No, Tarikh LO, Tarikh Akhir Pembekalan, Dokumen LO
6. **Perihal Bil** — text input
7. **Kod Identiti Pelanggan** — `wire:model.live`, options from `$userType`
8. **Jenis Identiti Pelanggan** — cascading from KIP
9. **No. Identiti Pelanggan** — Alpine.js `x-data` on wrapper div:
   - `:maxlength="({'JPN':12,'SSM':12}[$wire.kodIndentitiPelanggan]) ?? 20"`
   - `x-text` hint: "Maksimum X aksara"
10. Alamat 1/2/3, Poskod, Bandar — `*`/`(Pilihan)` conditional on JMT:01/02
11. **Negeri** — select with 17 IDD codes (01-16 + 98)
12. **Negara** — readonly, default MALAYSIA, plain label
13. Info notice: "Maklumat diperlukan untuk penghantaran ke iPayment (JANM)."

### Submit Buttons
- **Hantar / Sahkan Pembayaran** (teal `#00C8B3`) — `wire:click="sendIPaymentBilext001"` or `saveButiranPembayaran`
- Both buttons have `wire:loading.attr="disabled"` + Bootstrap `spinner-border-sm`

---

## 🗃️ Livewire Properties (TroliPembelian.php)

```php
public string $perananPembeli = '';
public ?Order $order = null;
public string $userType = '';
public ?float $jumlahHargaPembelian = 0.00;
public ?int $jenisPembayaran = null;
public string $ptj = '';
public string $loNo = '';
public ?string $loDate = null;
public ?string $supplyDeadline = null;
public $loFile = null;
public string $alamat1 = '';
public string $alamat2 = '';
public string $alamat3 = '';
public string $poskod = '';
public string $bandar = '';
public string $negeri = '';
public string $negara = 'MALAYSIA';
public string $perihal = '';
public string $sebab = '';
public string $kategori = '';
public string $kodIndentitiPelanggan = '';
public string $jenisIdentitiPelanggan = '';
public string $noIdentitiPelanggan = '';
public string $jenisProses = '01';
public string $jenisMaklumatTerimaan = '01';
public array $bandarOptions = [];    // loaded by updatedNegeri() — from config/ipayment_bandar.php
```

---

## 🐛 Known Issues / Pending Work

### ⬜ PENDING: Remove dd($payload)
Both `sendIPaymentBilext001()` and `sendIPaymentRecext001()` have `dd($payload)` for UAT debugging. Remove before go-live.

### ⬜ PENDING: UAT credentials
All `IPAYMENT_*` env keys are empty. iPayment team to provide at UAT. Key TBD values: `vot_dana`, `kumpulan_ptj_*`, `pegawai_pengawal`, `program_aktiviti`, `projek`, `kod_akaun`.

### ✅ DONE: Bandar dropdown + field reorder + wire.live fix — Jun 25, 2026, NOT committed
**Files changed:**
- `config/ipayment_bandar.php` — NEW. 443 unique bandars from Lampiran_7_Bandar.xlsx, keyed by negeri code (01-16)
- `TroliPembelian.php` — added `public array $bandarOptions = []` property + `updatedNegeri()` Livewire hook that loads bandars from config
- `troli-pembelian.blade.php` — bandar changed to `<select>`; **negeri changed to `wire:model.live`** (was `wire:model` — deferred in Livewire 3, updatedNegeri() never fired); field order: Negeri → Bandar → Poskod → Alamat 1 → Alamat 2 → Alamat 3 → Negara; bandar shows `cursor:not-allowed + opacity:0.65 + "Pilih Negeri dahulu"` until negeri selected

**Bandar purpose**: sent as customer billing address in BILEXT001 `maklumat_pelanggan` layer — printed on official government receipt (Resit Rasmi). Must match iPayment reference list exactly.

**Poskod note**: Kota Bharu alone has 86 postcodes — a `<datalist>` autocomplete (not `<select>`) was proposed for cascading from bandar. Not yet implemented — pending Miyamura confirmation.
- `troli-pembelian.blade.php` — bandar changed from `<input type="text">` to `<select>` (disabled when no negeri selected, options from `$bandarOptions`)

**Source**: `Lampiran_7_Bandar.xlsx` in Integration Kit V1.9.2 — 2,784 rows (Negeri + Bandar + Poskod), deduplicated to 443 unique bandars grouped by negeri code

### ✅ DONE: RECEXT201 callback controller (3.3.1) — Jun 22 2026, NOT committed
**Files changed:**
- `app/Http/Controllers/IPaymentCallbackController.php` — NEW (pure inbound, no auth)
- `routes/web.php` — added `POST /ipayment/recext201` with `->withoutMiddleware(VerifyCsrfToken)`
- `app/Http/Middleware/VerifyCsrfToken.php` — added `'ipayment/recext201'` to `$except`

**How it works:**
- iPayment POSTs JSON to `/ipayment/recext201` (Section 3.3.1 — Outgoing from iPayment)
- Reconciles via `mesej[0].maklumat_resit[].no_rujukan_maklumat_terimaan` → `orders.order_no`
- `jenis_proses_resit = '01'` (Bayaran): `BillPayment::updateOrCreate` + `ReceiptDetail::updateOrCreate`, order → BAYARAN_DITERIMA (16)
- `jenis_proses_resit = '02'` (Batal): order → BAYARAN_DIKEMBALIKAN (18), receipt → cancelled
- Returns `kod_respond: '00'` (Berjaya) or `'01'` (error) per IDD spec (page 71–72)
- Date format: `DDMMYYYYhh:mm:ss` parsed with `Carbon::createFromFormat('dmYH:i:s', ...)`

### ✅ FIXED (Jun 22, 2026 — NOT committed)
All changes below are applied but NOT committed (FT mode — Hakim commits manually):
- **RECEXT201 controller** — `app/Http/Controllers/IPaymentCallbackController.php` (new)
- **Route** — `POST /ipayment/recext201` in `routes/web.php` with `->withoutMiddleware(VerifyCsrfToken)`
- **CSRF** — `VerifyCsrfToken::$except` → `'ipayment/recext201'`
- **UAT reminder** — set `IPAYMENT_CALLBACK_URL=https://yourdomain/ipayment/recext201` in `.env` and share with iPayment team

### ✅ FIXED (Jun 19, 2026 — NOT committed)
All changes below are applied but NOT committed (FT mode — Hakim commits manually):
- All 25 Livewire properties declared
- Full BILEXT001 3-layer payload with JP/JMT conditional builder
- Conditional validate (JMT:01/02 → address required)
- All selects with `wire:model.live` (JP, JMT, KIP, Negeri)
- Negara readonly + default MALAYSIA
- Alamat 1/2/3 + address conditional `*`/(Pilihan) per JMT
- No. Identiti Alpine.js maxlength + visible hint (`x-text`)
- Sebab + Kategori positioned after JMT (JP-related, not address-related)
- Bootstrap `spinner-border-sm` on both submit buttons
- `$jumlahAmaun` fix — removed invalid `* $this->quantity`
- Git divergent branches — merged cleanly (`75a3dc8`)
- RECEXT001 `sendIPaymentRecext001()` — auto-called from BILEXT001 when JMT=01
- RECEXT001 reusable for JPMP=02 via function params

### ✅ FIXED (Jun 16, 2026 — NOT committed)
- `ic_number` added to `User.php $fillable`

---

## 📦 Data Models

### Order
- Table: `orders`
- Key fields: `order_no`, `customer_id`, `payment_method_id`, `payment_status_id`
- Relationships: `customer()→User`, `orderDetails()→OrderDetail`, `billPayment()→BillPayment`

### OrderDetail
- Table: `order_details`
- Key fields: `item_name`, `harga_perunit`, `quantity`

### User
- Table: `users`
- Key fields: `username`, `full_name`, `phone`, `email`, `usertype` ('1'=individual, '2'=company), `ic_number`, `ssm_number`
- **No address fields** — address entered via UI for iPayment

### BillPayment
- Table: `bill_payments`
- Key fields: `order_id`, `payment_method_id`, `total_bill`, `paid_amount`, `payment_date`
- Relationship: `morphOne(ReceiptDetail, 'payable')` → `receipt()`

### ReceiptDetail
- Table: `receipt_details` (polymorphic)
- Key fields: `receipt_no`, `receipt_date`, `grand_total`, `pdf_path`
- `receipt_no` = `no_rujukan_maklumat_pembayaran` source for RECEXT001

---

## 🔴 FT MODE RULES
- NEVER `git add`, `git commit`, `git push` on this project
- Hakim reviews and commits manually
- All changes: apply + confirm + mark "NOT committed"
