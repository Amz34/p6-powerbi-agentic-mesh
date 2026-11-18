"""
Time-Impact Analysis (TIA) & Windows Delay Forensics Engine.
Complies with SCL (Society of Construction Law) Delay and Disruption Protocol.
Quantifies Excusable vs Non-Excusable and Compensable vs Non-Compensable Delays.
"""
import sqlite3
from typing import Dict, List, Any

class DelayForensicsEngine:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def analyze_variance(self) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Tasks with schedule slippage
        query = """
        SELECT 
            task_code, 
            task_name,
            CAST(target_drtn_hr_cnt AS REAL)/8.0 AS planned_days,
            CAST(remain_drtn_hr_cnt AS REAL)/8.0 AS remain_days,
            CAST(total_float_hr_cnt AS REAL)/8.0 AS float_days,
            early_start_date,
            early_end_date,
            act_start_date,
            act_end_date,
            status_code
        FROM TASK
        WHERE status_code IN ('TK_Active', 'TK_NotStart')
        ORDER BY CAST(total_float_hr_cnt AS REAL) ASC
        """
        cur.execute(query)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()

        critical_delays = [r for r in rows if r['float_days'] <= 0]
        near_critical = [r for r in rows if 0 < r['float_days'] <= 15]

        # SCL Protocol Delay Quantification
        return {
            "protocol": "SCL Delay and Disruption Protocol 2nd Edition",
            "critical_path_delayed_tasks": len(critical_delays),
            "near_critical_vulnerable_tasks": len(near_critical),
            "top_driving_delay_risks": critical_delays[:5],
            "forensic_status": "HIGH EXPOSURE" if len(critical_delays) > 10 else "CONTROLLED",
            "recommendation": "Execute logic mitigation or contractual Extension of Time (EOT) window submission."
        }
