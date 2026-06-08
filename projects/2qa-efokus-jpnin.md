# 📊 eFokus JPNIN — Dashboard Perpaduan Negara
**Client**: 2Q Alliance (2QSC)
**Role**: Hakim — Jr. Software Developer (Laravel)
**Date Analysed**: June 8, 2026
**Repo**: `gitlab.com/2QSC/efokus` (GitLab, private)
**Local path**: `/Users/hakim/holeeMonth/2qa_projects/efokus/`
**Status**: 🟢 Active development — Hakim's branch: `iKes-Hakim`

---

## 🎯 What It Is
A **national unity analytics dashboard** for **JPNIN (Jabatan Perpaduan Negara dan Integrasi Nasional)**. Monitors racial harmony, conflict incidents, social media, and national unity metrics across Malaysia. Government analytics platform.

---

## 🛠️ Tech Stack
| Layer | Tech |
|---|---|
| Framework | Laravel 11+ |
| Frontend | Blade + Alpine.js + Chart.js + Livewire (Flux) |
| Build tool | Vite |
| Auth | Livewire Flux auth (2FA supported) |
| Maps | Google Maps API |
| DB | MySQL — database: `emaklumatv2` |

---

## 📦 Key Modules
| Module | Route | Table | Purpose |
|--------|-------|-------|---------|
| **i-Kes** | `/analisis/ikes` | `spk__ikes` | Conflict/incident case analytics |
| **eSepakat / PDRM** | `/eSepakat/datapdrm` | `spk__esp_pdrm` | Police racial conflict data |
| **Populasi Penduduk** | `/eSepakat/populasipenduduk` | `penduduk` | Population by state/daerah |
| **iRamal** | `/analisis/iramal` | `iramals` | Incident forecasting |
| **iModerator** | `/analisis/imoderator` | — | Social media monitoring |
| **Heatmap** | `/analisis/heatmap` | `heatmap_locations` | Geo heatmap |
| **Dashboard** | `/dashboard` | — | 3-tab: Petunjuk/Pengurusan/Jentera Perpaduan |

---

## 🗄️ Key Database Tables
| Table | Purpose |
|---|---|
| `spk__ikes` | i-Kes conflict cases (kluster_id, state_id, daerah_id, ikes_tarikh_berlaku) |
| `spk__esp_pdrm` | PDRM racial conflict incidents |
| `penduduk` | Population data |
| `iramals` | Forecast records |
| `heatmap_locations` | Geo coordinates for heatmap |
| `ref__states` | States reference (state_id, state_description) |
| `ref__daerahs` | Districts reference (daerah_id, daerah_description, state_id) |
| `ref__spk_ikes_kluster` | i-Kes cluster types (6 types) |
| `unity_metrics` | Unity index metrics |
| `users` / `user_profiles` | Auth with 2FA |

---

## 🔧 Hakim's Work — `iKes-Hakim` Branch

### What's done:
**`IkesController.php`** (`app/Http/Controllers/Api/IkesController.php`):
- `GET /api/ikes/current-year-total` — total kes for current year
- `GET /api/ikes/states` — state dropdown data
- `GET /api/ikes/daerahs?state_id=` — daerah dropdown (filtered by state)
- `GET /api/ikes/stats?tarikh_from&tarikh_to&state_id&daerah_id` — tahun/kuarter/bulan totals
- `GET /api/ikes/kluster-chart` — monthly bar chart by kluster (6 types)
  - Handles multi-year ranges (dynamic month labels e.g. "Jan 26")
  - Single-year view (Jan–Dis fixed labels)

**i-Kes Kluster Types + Colors:**
- 1=Politik (#4a78dc), 3=Keselamatan (#d38de3), 8=Perkauman (#6fd2e7)
- 9=Agama (#f6c748), 10=Kenyataan Kebencian (#e56a7a), 11=Tadbir Urus (#9f8be6)

**`ikes.blade.php`** — 2 tabs: Analisis Negara | Perbandingan  
**`ikes_negara.blade.php`** — filter row + stat cards + Google Maps iframe + kluster Chart.js bar chart  
**`ikes_perbandingan.blade.php`** — state comparison (TBD)

### Latest commit:
`37b9fd5 i-Kes: Pull Data from DB (Queries)` — API queries completed

---

## 🔑 Key Config Notes
- DB: `emaklumatv2` (MySQL)
- Google Maps API key in env
- Auth uses Livewire Flux with 2FA columns on users table
- `user_access_menu` + `user_menu` = custom RBAC for menu visibility

---

**Last updated**: June 8, 2026 by Yappy
**Analysed by**: Yappy (direct codebase sweep)
