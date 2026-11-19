import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connectors.pathizer_p7.p7_bridge import PathizerP7Bridge

class TestPathizerP7Bridge(unittest.TestCase):
    def test_p7_compatibility(self):
        xer_path = "/home/ubuntu/projects/p6_lab/user_project/EC00501.xer"
        if not os.path.exists(xer_path):
            self.skipTest("Sample XER not found")
        bridge = PathizerP7Bridge(xer_path)
        res = bridge.inspect_xer_compatibility()
        self.assertEqual(res["status"], "COMPLIANT")
        self.assertTrue(res["pathizer_p7_ready"])

if __name__ == '__main__':
    unittest.main()
