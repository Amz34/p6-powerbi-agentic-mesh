# P6 & Power BI Unified Agentic Mesh (Ultra Enterprise Edition)

[![CI & Automated Verification](https://github.com/Amz34/p6-powerbi-agentic-mesh/actions/workflows/ci.yml/badge.svg)](https://github.com/Amz34/p6-powerbi-agentic-mesh/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Architecture: 1+2+3 Unified Stack](https://img.shields.io/badge/Architecture-1%2B2%2B3%20Unified%20Mesh-emerald.svg)](docs/ARCHITECTURE.md)

Production-grade autonomous engineering mesh connecting **Oracle Primavera P6 Professional**, **Microsoft Power BI Desktop**, and **Cloud-Native Headless Chromium** agentic telemetry.

---

## 🌟 Key Capabilities

1. **High-Performance Ingestion (`core/`)**:
   - Zero-dependency streaming parser converting Oracle P6 `.XER` files directly into optimized SQLite tables.
   - Live synchronization with local Primavera P6 SQLite standalone databases (`PPMDBSQLite.db`).

2. **Automated DCMA 14-Point Quality Auditor (`core/dcma_auditor.py`)**:
   - Rigorous contractual auditing adhering to **Saudi Aramco**, **NEOM**, and **US DoD** standards.
   - Detects negative lags (leads), circular loops, open ends, hard constraints, and excessive float.

3. **Enterprise DAX Measure Library (`dax/`)**:
   - Production DAX measures for Earned Value Management (**PV, EV, SPI, CPI, SV, CV, EAC_t**).
   - Dynamic conditional formatting indicators (Green / Amber / Red).

4. **Autonomous Headless Chromium Engine (`p6_powerbi_mesh.py`)**:
   - Generates pixel-perfect executive dashboards using Headless Google Chrome without requiring manual desktop clicks.
   - Automated visual snapshot rendering for executive reporting and instant Telegram notifications (`@AzGem_Bot`).

5. **Streaming REST API (`api/server.py`)**:
   - Embedded REST server serving dynamic KPI endpoints (`/api/kpi`, `/api/activities`) for live web slicing and remote data connectors.

---

## 📁 Repository Structure

```
├── .github/workflows/       # Automated CI & logic regression testing
├── api/                     # Streaming REST API for Power BI Web connectors
│   └── server.py
├── core/                    # Core scheduling & parsing engines
│   ├── dcma_auditor.py      # Contractual DCMA 14-point audit engine
│   └── xer_parser.py        # High-performance XER to SQLite parser
├── dax/                     # Production DAX measure formulas
│   └── p6_enterprise_measures.dax
├── docs/                    # Architecture and engineering specs
│   └── ARCHITECTURE.md
├── output/                  # Generated feeds, dashboards & renders
│   ├── P6_PowerBI_Feed.csv  # Desktop Power BI (.pbix) feed
│   ├── index.html           # Cloud interactive dashboard
│   └── live_p6_powerbi_snapshot.png
├── tests/                   # Automated regression test suites
│   └── test_mesh.py
├── p6_powerbi_mesh.py       # Main agentic execution engine
├── sync_p6_laptop_watcher.ps1 # Laptop PowerShell sync watcher
└── README.md
```

---

## 🚀 Quickstart

### 1. Run Complete Mesh Processing & Headless Render
```bash
python3 p6_powerbi_mesh.py
```
Outputs:
- Live Executive HTML: `output/index.html`
- HD Chromium Render: `output/live_p6_powerbi_snapshot.png`
- Power BI Desktop Feed: `output/P6_PowerBI_Feed.csv`

### 2. Start Live Streaming API
```bash
python3 api/server.py
```
Access endpoints at `http://localhost:8788/api/kpi`.

### 3. Connect to Microsoft Power BI Desktop
1. Open Power BI Desktop on your laptop.
2. Select **Get Data** -> **Text/CSV** -> Select `output/P6_PowerBI_Feed.csv`.
3. Copy DAX measures from `dax/p6_enterprise_measures.dax` for instant EVM KPIs.
