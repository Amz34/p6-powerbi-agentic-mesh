import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.dcma_auditor import DCMAAuditor

class TestP6Mesh(unittest.TestCase):
    def test_dcma_contract_integrity(self):
        db_path = "/home/ubuntu/projects/p6_lab/user_project/EC00501.db"
        if not os.path.exists(db_path):
            self.skipTest("Sample database not present in local test environment")
        auditor = DCMAAuditor(db_path)
        report = auditor.run_14_point_audit()
        self.assertIn("dcma_compliance_score", report)
        self.assertEqual(report["leads_negative_lags"], 0, "Negative lags (leads) must be strictly 0")

if __name__ == '__main__':
    unittest.main()
