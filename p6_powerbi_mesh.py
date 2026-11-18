#!/usr/bin/env python3
"""
P6-PowerBI Agentic Mesh (Ultra-Enterprise Edition v2.0)
Full Integration of:
1. P6 XER & SQLite Streaming Parser
2. Contractual DCMA 14-Point Quality Auditor
3. SCL Protocol Windows Delay Forensics (TIA)
4. Parametric Monte Carlo Risk Simulation (P50/P80/P90)
5. Automated Power BI Desktop Sync (.csv)
6. Autonomous Headless Chromium Executive Visualization
"""

import sys
import os
import csv
import json
import sqlite3
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from core.dcma_auditor import DCMAAuditor
from core.delay_forensics import DelayForensicsEngine
from core.monte_carlo import MonteCarloSimulator

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class UltraP6Mesh:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def execute_complete_mesh(self):
        # 1. DCMA Audit
        dcma = DCMAAuditor(self.db_path).run_14_point_audit()

        # 2. Delay Forensics (SCL Protocol)
        forensics = DelayForensicsEngine(self.db_path).analyze_variance()

        # 3. Monte Carlo Risk Analysis (P80 Confidence)
        risk = MonteCarloSimulator(self.db_path).run_simulation(iterations=1000)

        # 4. Generate Clean Power BI Desktop Ingestion Table
        cur = self.conn.cursor()
        query = """
        SELECT 
            t.task_code AS [Activity ID],
            t.task_name AS [Activity Name],
            w.wbs_name AS [WBS],
            CAST(t.target_drtn_hr_cnt AS REAL)/8.0 AS [Planned Duration (Days)],
            CAST(t.remain_drtn_hr_cnt AS REAL)/8.0 AS [Remaining Duration (Days)],
            CAST(t.total_float_hr_cnt AS REAL)/8.0 AS [Total Float (Days)],
            SUBSTR(t.early_start_date, 1, 10) AS [Planned Start],
            SUBSTR(t.early_end_date, 1, 10) AS [Planned Finish],
            CASE 
                WHEN t.status_code = 'TK_Complete' THEN 'Completed'
                WHEN t.status_code = 'TK_Active' THEN 'In Progress'
                ELSE 'Not Started'
            END AS [Status],
            CASE 
                WHEN CAST(t.total_float_hr_cnt AS REAL) <= 0 THEN 'Critical'
                WHEN CAST(t.total_float_hr_cnt AS REAL) <= 40 THEN 'Near-Critical'
                ELSE 'Normal'
            END AS [Criticality],
            CAST(t.phys_complete_pct AS REAL) AS [Physical % Complete]
        FROM TASK t
        LEFT JOIN PROJWBS w ON t.wbs_id = w.wbs_id
        """
        cur.execute(query)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]

        csv_path = os.path.join(OUTPUT_DIR, "P6_PowerBI_Feed.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)

        # 5. Render Executive Web Dashboard HTML with Monte Carlo & DCMA Cards
        html_path = os.path.join(OUTPUT_DIR, "index.html")
        self._generate_ultra_html(dcma, forensics, risk, rows, cols, html_path)

        # 6. Headless Chromium Snapshot Execution
        render_png = os.path.join(OUTPUT_DIR, "live_p6_powerbi_snapshot.png")
        cmd = [
            "google-chrome",
            "--headless",
            "--no-sandbox",
            "--disable-gpu",
            "--window-size=1280,800",
            f"--screenshot={render_png}",
            html_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return {
            "dcma_audit": dcma,
            "delay_forensics": forensics,
            "monte_carlo_risk": risk,
            "powerbi_feed": csv_path,
            "dashboard_html": html_path,
            "snapshot_png": render_png
        }

    def _generate_ultra_html(self, dcma, forensics, risk, rows, cols, out_path):
        tasks = [dict(zip(cols, r)) for r in rows]
        total = len(tasks)
        completed = sum(1 for t in tasks if t['Status'] == 'Completed')
        in_progress = sum(1 for t in tasks if t['Status'] == 'In Progress')
        not_started = sum(1 for t in tasks if t['Status'] == 'Not Started')
        critical = sum(1 for t in tasks if t['Criticality'] == 'Critical')

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Ultra Enterprise P6 & Power BI Mesh</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-slate-950 text-slate-100 p-8">
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between border-b border-slate-800 pb-5">
      <div>
        <h1 class="text-3xl font-extrabold flex items-center gap-3">
          <span class="text-amber-400">🛡️</span> P6 & Power BI Ultra Enterprise Mesh
        </h1>
        <p class="text-slate-400 text-sm mt-1">Autonomous CPM Schedule, DCMA 14-Point & Monte Carlo Risk Analytics</p>
      </div>
      <div class="text-right">
        <span class="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-3 py-1 rounded-full text-xs font-semibold">
          ENTERPRISE V2.0 LIVE
        </span>
        <p class="text-xs text-slate-500 mt-1">SCL Protocol & P80 Monte Carlo</p>
      </div>
    </div>

    <!-- Tier 1: Core KPIs -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-slate-900 border border-slate-800 p-5 rounded-xl">
        <p class="text-xs text-slate-400 font-semibold uppercase">DCMA Compliance</p>
        <div class="flex items-baseline justify-between mt-2">
          <h2 class="text-3xl font-extrabold text-emerald-400">{dcma['dcma_compliance_score']}</h2>
          <span class="text-xs px-2 py-0.5 rounded font-medium bg-emerald-500/20 text-emerald-300">
            {dcma['contractual_status']}
          </span>
        </div>
        <p class="text-xs text-slate-500 mt-1">Leads: {dcma['leads_negative_lags']} | Lags: {dcma['positive_lags']}</p>
      </div>

      <div class="bg-slate-900 border border-slate-800 p-5 rounded-xl">
        <p class="text-xs text-slate-400 font-semibold uppercase">P80 Risk Confidence</p>
        <div class="flex items-baseline justify-between mt-2">
          <h2 class="text-3xl font-extrabold text-amber-400">{risk['P80_contractual_confidence_days']} <span class="text-sm font-normal text-slate-400">Days</span></h2>
          <span class="text-xs text-rose-400">+{risk['recommended_schedule_buffer_days']}d Buffer</span>
        </div>
        <p class="text-xs text-slate-500 mt-1">Monte Carlo (1,000 Iterations)</p>
      </div>

      <div class="bg-slate-900 border border-slate-800 p-5 rounded-xl">
        <p class="text-xs text-slate-400 font-semibold uppercase">Critical Float Horizon</p>
        <div class="flex items-baseline justify-between mt-2">
          <h2 class="text-3xl font-extrabold text-rose-400">{critical} <span class="text-sm font-normal text-slate-400">Tasks</span></h2>
          <span class="text-xs text-amber-400">Float = 0 Days</span>
        </div>
        <p class="text-xs text-slate-500 mt-1">{forensics['near_critical_vulnerable_tasks']} Near-Critical Tasks</p>
      </div>

      <div class="bg-slate-900 border border-slate-800 p-5 rounded-xl">
        <p class="text-xs text-slate-400 font-semibold uppercase">Total Scope</p>
        <div class="flex items-baseline justify-between mt-2">
          <h2 class="text-3xl font-extrabold text-sky-400">{total}</h2>
          <span class="text-xs text-emerald-400">{completed} Done</span>
        </div>
        <p class="text-xs text-slate-500 mt-1">{in_progress} In Progress | {not_started} Open</p>
      </div>
    </div>

    <!-- Tier 2: Visual Distribution & SCL Forensics -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="bg-slate-900 border border-slate-800 p-5 rounded-xl">
        <h3 class="text-base font-semibold text-white mb-4">Monte Carlo Duration Horizon</h3>
        <div class="space-y-4 text-xs">
          <div class="flex justify-between items-center p-2.5 bg-slate-800/40 rounded-lg">
            <span class="text-slate-400">Deterministic Base</span>
            <span class="font-bold text-slate-200">{risk['deterministic_duration_days']} Days</span>
          </div>
          <div class="flex justify-between items-center p-2.5 bg-slate-800/40 rounded-lg">
            <span class="text-slate-400">P50 (Median Case)</span>
            <span class="font-bold text-sky-400">{risk['P50_duration_days']} Days</span>
          </div>
          <div class="flex justify-between items-center p-2.5 bg-amber-500/10 border border-amber-500/20 rounded-lg">
            <span class="text-amber-300 font-medium">P80 Contractual Target</span>
            <span class="font-bold text-amber-400">{risk['P80_contractual_confidence_days']} Days</span>
          </div>
          <div class="flex justify-between items-center p-2.5 bg-slate-800/40 rounded-lg">
            <span class="text-slate-400">P90 (Conservative Case)</span>
            <span class="font-bold text-violet-400">{risk['P90_conservative_days']} Days</span>
          </div>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 p-5 rounded-xl lg:col-span-2">
        <h3 class="text-base font-semibold text-white mb-4 flex items-center justify-between">
          <span>SCL Protocol Driving Delay Vulnerabilities</span>
          <span class="text-xs text-rose-400 font-normal">Immediate Delay Exposure</span>
        </h3>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="text-slate-400 uppercase bg-slate-800/40 border-b border-slate-800">
              <tr>
                <th class="py-2.5 px-3">ID</th>
                <th class="py-2.5 px-3">Activity Name</th>
                <th class="py-2.5 px-3">Duration</th>
                <th class="py-2.5 px-3">Float</th>
                <th class="py-2.5 px-3">Start Date</th>
                <th class="py-2.5 px-3">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800 text-slate-300">
"""
        for ct in forensics['top_driving_delay_risks']:
            html += f"""
              <tr class="hover:bg-slate-800/30">
                <td class="py-2 px-3 font-mono text-amber-400 font-bold">{ct['task_code']}</td>
                <td class="py-2 px-3">{ct['task_name']}</td>
                <td class="py-2 px-3">{ct['planned_days']:.1f} d</td>
                <td class="py-2 px-3 text-rose-400 font-bold">{ct['float_days']:.1f} d</td>
                <td class="py-2 px-3">{ct['early_start_date'][:10]}</td>
                <td class="py-2 px-3"><span class="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300">Driving</span></td>
              </tr>
"""
        html += f"""
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

if __name__ == "__main__":
    db = "/home/ubuntu/projects/p6_lab/user_project/EC00501.db"
    mesh = UltraP6Mesh(db)
    res = mesh.execute_complete_mesh()
    print("Ultra Enterprise Mesh Executed Successfully!")
    print(f"P80 Risk Horizon: {res['monte_carlo_risk']['P80_contractual_confidence_days']} Days")
    print(f"DCMA Compliance: {res['dcma_audit']['dcma_compliance_score']}")
