import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.mep_matrix_engine import MEPMonitoringEngine

class TestMEPMonitoringEngine(unittest.TestCase):
    def test_mep_progress_matrix(self):
        sample_tasks = [
            {"Activity ID": "EC1510", "Activity Name": "Rough-In Plumbing/Piping", "WBS": "Plumbing", "Physical % Complete": 50.0, "Planned Duration (Days)": 10.0},
            {"Activity ID": "EC1500", "Activity Name": "Install HVAC Ducts", "WBS": "Mechanical", "Physical % Complete": 0.0, "Planned Duration (Days)": 20.0},
            {"Activity ID": "EC1010", "Activity Name": "Concrete Slab", "WBS": "Civil", "Physical % Complete": 100.0, "Planned Duration (Days)": 15.0}
        ]
        matrix = MEPMonitoringEngine.generate_mep_progress_matrix(sample_tasks)
        self.assertEqual(matrix["total_mep_work_packages"], 2)
        self.assertIn("boq_weighted_progress", matrix)

if __name__ == '__main__':
    unittest.main()
