# ⚖️ AP JKSM — Project Reference
*First documented: Jun 16, 2026 by Yappy*
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
| Frontend | Blade + **Livewire 3.5** (Hakim confirmed Livewire 3, NOT 2) |
| CSS | Bootstrap |
| Payment | iPayment (JANM) integration — BILEXT001 in progress |
| Auth | Standard Laravel Auth |

---

## 💳 iPayment (JANM) Integration — BILEXT001

### What is BILEXT001?
External billing submission to **iPayment** (Jabatan Akauntan Negara Malaysia / JANM) for government agency payment processing. Government agencies pay through this channel instead of SenangPay/FPX.

### Payment Method
- Option 1 = FPX
- Option 2 = Visa
- Option 3 = iPayment (BILEXT001) ← new

### Config File
`config/ipayment.php` — all env-driven:
```
IPAYMENT_ENDPOINT=
IPAYMENT_AUTH_USER=
IPAYMENT_AUTH_PASS=
IPAYMENT_KOD_AGENSI=
IPAYMENT_KOD_PERKHIDMATAN=
IPAYMENT_KOD_LOKASI=
IPAYMENT_KOD_SUBLOKASI=
IPAYMENT_KOD_PENJENISAN=
IPAYMENT_CALLBACK_URL=
# TBD from iPayment team at UAT:
IPAYMENT_KUMPULAN_PTJ_MENYEDIA=
IPAYMENT_PEGAWAI_PENGAWAL=
IPAYMENT_KUMPULAN_PTJ_DIPERTANGGUNG=
IPAYMENT_VOT_DANA=         # B/T = Vot Mengurus, P/S = Vot Pembangunan
IPAYMENT_PROGRAM_AKTIVITI= # Only if VOT_DANA = B or T
IPAYMENT_PROJEK=           # Only if VOT_DANA = P or S
IPAYMENT_KOD_AKAUN=
```

### BILEXT001 Payload Structure (3 Layers)

**Outer Layer:**
- `kod_proses` = "BILEXT001"
- `kod_perkhidmatan_ipayment`
- `tarikh_dan_masa` = "ddMMYYYY HH:mm:ss" (confirm space vs no-space with iPayment team)
- `no_rujukan_mesej` = "BILEXT001" + kod_agensi + kod_perkhidmatan + ddMMYYYY + 7-digit order ID
- `mesej` = [Layer 1]

**Layer 1 (inside mesej):**
- `kod_agensi`, `kod_perkhidmatan_ipayment`
- `jumlah_maklumat_terimaan` = "1"
- `jumlah_amaun` = formatted 2dp
- `maklumat_terimaan` = [Layer 2]

**Layer 2 (inside maklumat_terimaan) — built for JP:01, JMT:01:**
- `jumlah_charge_line`, `jenis_proses`="01", `jenis_maklumat_terimaan`="01"
- `no_rujukan_1` = order_no (JP:01)
- `tarikh_dan_masa_rujukan_1` = from loDate (Tarikh LO) or fallback now()
- `perihal` = item names joined with ", "
- Tax fields: `jumlah_tanpa_cukai`, `jumlah_cukai`="0.00", `jumlah_dengan_cukai`, `jumlah_amaun_perlu_dibayar`
- `tarikh_dan_masa_akhir_bayaran` = from supplyDeadline (optional, only if set)
- `kod_lokasi`, `kod_sublokasi` = from config (Layer 2, NOT Layer 3)
- Customer identity (usertype='1'→IC, usertype='2'→SSM/company):
  - `kategori_identiti_pelanggan`, `kod_identiti_pelanggan`, `jenis_identiti_pelanggan`
  - `nombor_identiti_pelanggan` = ic_number ?? username (individual)
  - `nama` = full_name (individual) or company name
- Address: `alamat_1`, `alamat_2`(opt), `alamat_3`(opt), `poskod`, `bandar`, `negeri`, `negara`
- `no_tel`, `emel` = from user/company
- `no_rujukan_pelanggan` = loNo (optional LO number)
- `maklumat_chargeline` = [Layer 3] × N (one per orderDetail)

**Layer 3 (inside maklumat_chargeline) — one per order item:**
- `no_rekod`, `kod_penjenisan`
- `kumpulan_ptj_dan_ptj_menyedia` = $this->ptj (from UI) or config
- `vot_dana` = from config (B/T/P/S/Amanah)
- `pegawai_pengawal_dipertanggung`, `kumpulan_ptj_dan_ptj_dipertanggung`
- `program_aktiviti` = only if vot_dana B or T
- `projek` = only if vot_dana P or S
- `kod_akaun`
- `amaun` = harga_perunit × quantity, 2dp

### Key Files
| File | Purpose |
|---|---|
| `app/Http/Livewire/PembayaranDanKewangan/TroliPembelian.php` | Main cart/payment Livewire component. Has `sendIPaymentBilext001()` method |
| `resources/views/livewire/pembayaran-dan-kewangan/troli-pembelian.blade.php` | Cart blade view, iPayment UI section under `@if($jenisPembayaran == '3')` |
| `config/ipayment.php` | iPayment config, all env-driven |

### Current Status (Jun 16, 2026)
- ✅ `config/ipayment.php` — complete with all keys (TBD keys default to '')
- ✅ `sendIPaymentBilext001()` — complete 3-layer payload built
- ✅ `troli-pembelian.blade.php` — iPayment UI with wire:model bindings + address fields
- ⚠️ `dd($payload)` still in method — intentional, for UAT debugging. REMOVE before go-live.
- ⏳ UAT credentials expected Thu/Fri Jun 18-19, 2026 from JKSM + iPayment team

### Pending at UAT
1. Confirm `tarikh_dan_masa` format: with or without space between date and time
2. Fill all `IPAYMENT_*` env keys (endpoint, auth, kod values)
3. Fill TBD keys (vot_dana, kumpulan_ptj, pegawai_pengawal, kod_akaun)
4. Remove `dd($payload)` from `sendIPaymentBilext001()`
5. Test full flow end-to-end

---

## 🐛 Known Issues / Pending Work

### ✅ FIXED (Jun 16, 2026): ic_number not saving on registration
`ic_number` and `ssm_number` were missing from `User.php $fillable`. Fix applied, NOT committed.
- File: `app/Models/User.php`
- Added: `'ic_number'` to `$fillable` array

### ⬜ PENDING: BILEXT001 go-live
Remove `dd($payload)` after UAT credential testing passes.

### ⬜ PENDING: BILEXT001 RECEXT201 callback
After BILEXT001 sends the bill, iPayment will call back RECEXT201 (payment received notification). Controller for this NOT YET BUILT.

### ⬜ PENDING: Remove dd($payload) in TroliPembelian.php
Line ~207. Remove when confirmed payload format is accepted by iPayment sandbox.

---

## 📦 Data Models

### Order
- Table: `orders`
- Key fields: `order_no`, `customer_id`, `payment_method_id`, `payment_status_id`, `remarks`
- Accessors: `total_amount` (sum of orderDetails), `is_paid`, `is_failed`, `is_pending`
- Relationships: `customer()→User`, `orderDetails()→OrderDetail`, `loRequest()`, `billInvoice()`

### OrderDetail
- Table: `order_details`
- Key fields: `item_id`, `item_name`, `harga_perunit`, `quantity`
- Accessors: `subtotal`, `item_type`, `item_title`

### User
- Table: `users`
- Key fields: `username` (IC/login), `full_name`, `phone`, `email`, `usertype` ('1'=individual, '2'=company), `ic_number`, `ssm_number`
- **No address fields on User** — address must be entered via UI for iPayment

### UserCompany
- Table: `user_companies`
- Key fields: `user_company_name`, `user_company_phone`, `user_company_email`, `user_ssmno`

---

## 🔴 FT MODE RULES
- NEVER `git add`, `git commit`, `git push` on this project
- Hakim reviews and commits manually
- All changes: apply + confirm + mark "NOT committed"
