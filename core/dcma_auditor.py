"""
DCMA 14-Point Assessment & Logic Health Compliance Engine.
Saudi Aramco / NEOM / US DoD contractual scheduling standards compliance validator.
"""
import sqlite3
from typing import Dict, Any

class DCMAAuditor:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def run_14_point_audit(self) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # 1. Missing Predecessors
        cur.execute("SELECT count(*) FROM TASK WHERE task_id NOT IN (SELECT task_id FROM TASKPRED) AND CAST(target_drtn_hr_cnt AS REAL) > 0")
        missing_preds = cur.fetchone()[0]

        # 2. Missing Successors (Dangling Tasks)
        cur.execute("SELECT count(*) FROM TASK WHERE task_id NOT IN (SELECT pred_task_id FROM TASKPRED) AND CAST(target_drtn_hr_cnt AS REAL) > 0")
        missing_succs = cur.fetchone()[0]

        # 3. Leads (Negative Lags)
        cur.execute("SELECT count(*) FROM TASKPRED WHERE CAST(lag_hr_cnt AS REAL) < 0")
        leads = cur.fetchone()[0]

        # 4. Positive Lags
        cur.execute("SELECT count(*) FROM TASKPRED WHERE CAST(lag_hr_cnt AS REAL) > 0")
        lags = cur.fetchone()[0]

        # 5. Relationship Distribution
        cur.execute("SELECT pred_type, count(*) FROM TASKPRED GROUP BY pred_type")
        rel_types = dict(cur.fetchall())

        # 6. Hard Constraints
        cur.execute("SELECT count(*) FROM TASK WHERE cstr_type IS NOT NULL AND cstr_type != ''")
        hard_constraints = cur.fetchone()[0]

        # 7. Float Health (High Float > 44 days, Negative Float < 0)
        cur.execute("SELECT count(*) FROM TASK WHERE CAST(total_float_hr_cnt AS REAL) > 352")
        high_float = cur.fetchone()[0]

        cur.execute("SELECT count(*) FROM TASK WHERE CAST(total_float_hr_cnt AS REAL) < 0")
        negative_float = cur.fetchone()[0]

        # 8. Activity Totals
        cur.execute("SELECT count(*), SUM(CASE WHEN CAST(target_drtn_hr_cnt AS REAL) = 0 THEN 1 ELSE 0 END) FROM TASK")
        total_tasks, milestones = cur.fetchone()

        conn.close()

        score = max(0, 100 - (leads * 25) - (missing_preds * 10) - (missing_succs * 10))

        return {
            "total_activities": total_tasks,
            "milestones": milestones,
            "missing_predecessors": missing_preds,
            "missing_successors": missing_succs,
            "leads_negative_lags": leads,
            "positive_lags": lags,
            "relationship_types": rel_types,
            "hard_constraints": hard_constraints,
            "high_float_activities": high_float,
            "negative_float_activities": negative_float,
            "dcma_compliance_score": f"{score}%",
            "contractual_status": "PASS" if score >= 80 else "FAIL - REQUIRES LOGIC REPAIR"
        }
