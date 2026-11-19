"""
Smart Resource & Cost Loading Engine for Oracle Primavera P6 (Zero Excel Roundtrips).
Enables conversational loading of Labor, Non-Labor, and Material Resources,
Budgeted Units, Rates, and Cost Calculations directly into P6 schema.
"""

import sqlite3
from typing import Dict, List, Any, Optional

class SmartResourceLoader:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def list_resources(self) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT rsrc_id, rsrc_short_name, rsrc_name, rsrc_type, def_qty_per_hr FROM RSRC LIMIT 50")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def get_resource_assignments(self, proj_id: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        query = """
        SELECT 
            tr.taskrsrc_id,
            t.task_code,
            t.task_name,
            r.rsrc_short_name,
            r.rsrc_name,
            tr.target_qty,
            tr.target_cost,
            tr.remain_qty,
            tr.act_reg_qty
        FROM TASKRSRC tr
        JOIN TASK t ON tr.task_id = t.task_id
        JOIN RSRC r ON tr.rsrc_id = r.rsrc_id
        """
        cur.execute(query)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def audit_resource_distribution(self) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Check total assigned vs unassigned tasks
        cur.execute("SELECT count(*) FROM TASK WHERE CAST(target_drtn_hr_cnt AS REAL) > 0")
        total_work_tasks = cur.fetchone()[0]

        cur.execute("SELECT count(DISTINCT task_id) FROM TASKRSRC")
        assigned_tasks = cur.fetchone()[0]

        cur.execute("SELECT count(DISTINCT rsrc_id) FROM RSRC")
        total_resources = cur.fetchone()[0]

        # Total Budgeted Cost
        cur.execute("SELECT SUM(CAST(target_cost AS REAL)) FROM TASKRSRC")
        total_cost = cur.fetchone()[0] or 0.0

        # Total Units (Hours / Material)
        cur.execute("SELECT SUM(CAST(target_qty AS REAL)) FROM TASKRSRC")
        total_qty = cur.fetchone()[0] or 0.0

        conn.close()

        coverage_pct = round((assigned_tasks / total_work_tasks) * 100, 1) if total_work_tasks > 0 else 0.0

        return {
            "total_work_activities": total_work_tasks,
            "resource_loaded_activities": assigned_tasks,
            "resource_loading_coverage": f"{coverage_pct}%",
            "total_available_resources": total_resources,
            "total_budgeted_cost": round(total_cost, 2),
            "total_budgeted_units": round(total_qty, 2),
            "loading_health": "OPTIMAL" if coverage_pct >= 80 else "PARTIAL_UNLOADED"
        }
