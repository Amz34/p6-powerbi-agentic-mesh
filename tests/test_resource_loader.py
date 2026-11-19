import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.smart_resource_loader import SmartResourceLoader

class TestSmartResourceLoader(unittest.TestCase):
    def test_audit_resource_distribution(self):
        db_path = "/home/ubuntu/projects/p6_lab/user_project/EC00501.db"
        if not os.path.exists(db_path):
            self.skipTest("Database not found")
        loader = SmartResourceLoader(db_path)
        audit = loader.audit_resource_distribution()
        self.assertIn("resource_loading_coverage", audit)
        self.assertIn("total_available_resources", audit)

if __name__ == '__main__':
    unittest.main()
