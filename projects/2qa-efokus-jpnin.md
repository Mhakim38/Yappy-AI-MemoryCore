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
  - EXTENDED (Jun 9): now also accepts `parlimen_id`, `dun_id`, `kluster_id`, `bulan`, `tahun` (non-breaking; Negara tab unaffected). Used by BOTH tabs.
- `GET /api/ikes/parlimens?state_id=` — parlimen dropdown (NEW Jun 9)
- `GET /api/ikes/duns?parlimen_id=&state_id=` — DUN dropdown (NEW Jun 9)
- ~~`comparison-chart`~~ — REMOVED Jun 9 (old state-grouping method; superseded by kluster-chart per-set)

**i-Kes Kluster Types + Colors:**
- 1=Politik (#4a78dc), 3=Keselamatan (#d38de3), 8=Perkauman (#6fd2e7)
- 9=Agama (#f6c748), 10=Kenyataan Kebencian (#e56a7a), 11=Tadbir Urus (#9f8be6)

**`ikes.blade.php`** — 2 tabs: Analisis Negara | Perbandingan  
**`ikes_negara.blade.php`** — filter row + stat cards + Google Maps iframe + kluster Chart.js bar chart. Jun 9 updates: per-bar value labels on the "Taburan Kluster Mengikut Bulan" chart (custom `ikesBarValues` plugin, each grouped bar's count on top, zeros skipped); layout made bigger via `.ikes-negara-layout` — map (`.ikes-map-frame`) flex-fills its card, chart (`.ikes-chart-fill`) grows to full viewport height.  
**`ikes_perbandingan.blade.php`** — ✅ DONE (Jun 9): dual-set comparison. + Tambah/Buang for up to 2 independent "Carian Data" sets (stacked vertically). Each set: Tarikh/Bulan/Tahun/Negeri/Daerah/Parlimen/DUN/Kluster (cascading). Grouped+stacked Chart.js bar — 2 sets side-by-side per month, stacked by kluster; per-stack total on top + sideways year label under each bar (custom `ikpStackLabels` plugin). Empty state on load; renders on Cari. Title: "Perbandingan Data Kluster Mengikut Tahun". Filter grid: row1 Tarikh→Daerah, row2 Parlimen/DUN/Kluster.

**spk__ikes key FK cols**: state_id, daerah_id, parlimen_id, dun_id, kluster_id, ikes_tarikh_berlaku. Ref tables ref__parlimens/ref__duns cascade by state→parlimen→dun.

**`partials/chart-tools.blade.php`** — NEW Jun 9: shared reusable chart toolbar (PNG/CSV/PDF download + fullscreen zoom). Generic, keyed by `data-chart-action`/`data-chart-id` via `Chart.getChart()`. Reuses iramal download logic (white-bg snapshot + FileSaver + jsPDF) + datastatik zoom-modal pattern. Zoom clones live chart config, reattaches source chart's inline plugins (so totals/year/month labels carry over) and dedupes legend for grouped stacks. Loads FileSaver+jsPDF @once; `@include`'d once in `ikes.blade.php`. Wired into both i-Kes charts. Reuse it for any future Chart.js canvas.

### Latest commits (branch `iKes-Hakim`, NOT yet pushed):
- `92f1285 feat: i-Kes Negara — bigger map + full-height chart layout` (Jun 9, latest)
- `aff5618 feat: i-Kes Negara — per-bar value labels on Taburan Kluster chart`
- `bfadb0f feat: i-Kes chart toolbar — PNG/CSV/PDF download + fullscreen zoom`
- `4357bb6 feat: i-Kes Perbandingan — dual-set kluster comparison (grouped stacked bar)`

---

## 🔑 Key Config Notes
- DB: `emaklumatv2` (MySQL)
- Google Maps API key in env
- Auth uses Livewire Flux with 2FA columns on users table
- `user_access_menu` + `user_menu` = custom RBAC for menu visibility

---

**Last updated**: June 9, 2026 (PM) by Yappy — Perbandingan tab + chart toolbar (PNG/CSV/PDF/zoom) + Negara per-bar labels + Negara bigger-map/full-height layout. 4 commits on `iKes-Hakim` (latest 92f1285), none pushed yet.
**Analysed by**: Yappy (direct codebase sweep)
