# P6 & Power BI Unified Agentic Mesh

Enterprise autonomous bridge connecting Oracle Primavera P6 Professional, Microsoft Power BI Desktop, and Headless Chromium agentic intelligence.

## Architecture (1+2+3 Unified Stack)
1. **VM Analytics Engine**: Ingests P6 SQLite `.db` / `.xer` schedules, runs DCMA 14-point audit, CPM driving float, and EVM (SPI/CPI) DAX calculations.
2. **Headless Chromium Execution**: Generates full executive dashboards via `google-chrome --headless` without requiring manual GUI interactions, saving snapshots for executive reporting & Telegram bots (`@AzGem_Bot`).
3. **Power BI Desktop Bridge**: Outputs clean, typed `P6_PowerBI_Feed.csv` ready for instant drag-and-drop or 1-click refresh inside Microsoft Power BI Desktop (`.pbix`).

## Quickstart
```bash
python3 p6_powerbi_mesh.py
```
- Outputs interactive web dashboard: `output/index.html`
- Outputs headless snapshot: `output/live_p6_powerbi_snapshot.png`
- Outputs Power BI feed: `output/P6_PowerBI_Feed.csv`
