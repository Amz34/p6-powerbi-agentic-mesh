"""
Parametric Monte Carlo Schedule Risk Analysis (SRA).
Simulates 1,000 project completion iterations using triangular duration distributions (O-M-P).
Computes P50, P80 (Contractual Standard), and P90 completion confidence dates.
"""
import random
import math
import sqlite3
from typing import Dict, Any

class MonteCarloSimulator:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def run_simulation(self, iterations: int = 1000) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT CAST(target_drtn_hr_cnt AS REAL)/8.0 FROM TASK WHERE CAST(target_drtn_hr_cnt AS REAL) > 0")
        durations = [r[0] for r in cur.fetchall()]
        conn.close()

        if not durations:
            return {"error": "No durations found"}

        base_duration = sum(durations)
        simulated_durations = []

        # Triangular distribution simulation: Optimistic (0.85), Most Likely (1.0), Pessimistic (1.45)
        for _ in range(iterations):
            iter_total = 0
            for d in durations:
                optimistic = d * 0.85
                likely = d * 1.0
                pessimistic = d * 1.45
                iter_total += random.triangular(optimistic, pessimistic, likely)
            simulated_durations.append(iter_total)

        simulated_durations.sort()
        p50 = simulated_durations[int(iterations * 0.50)]
        p80 = simulated_durations[int(iterations * 0.80)]
        p90 = simulated_durations[int(iterations * 0.90)]

        schedule_contingency_p80 = round(p80 - base_duration, 1)

        return {
            "iterations": iterations,
            "deterministic_duration_days": round(base_duration, 1),
            "P50_duration_days": round(p50, 1),
            "P80_contractual_confidence_days": round(p80, 1),
            "P90_conservative_days": round(p90, 1),
            "recommended_schedule_buffer_days": schedule_contingency_p80,
            "confidence_assessment": f"P80 benchmark requires a {schedule_contingency_p80}-day risk contingency buffer."
        }
