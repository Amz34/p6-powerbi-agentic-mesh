import unittest
from core.bim_4d_engine import BIM4DEngine

class TestBIM4DEngine(unittest.TestCase):
    def setUp(self):
        self.sample_activities = [
            {
                "Activity ID": "EC1090",
                "Activity Name": "Begin Building Construction",
                "WBS": "Foundation",
                "Physical % Complete": 100.0,
                "Status": "Completed",
                "Total Float (Days)": 0.0,
                "Planned Start": "2011-05-01",
                "Planned Finish": "2011-05-01"
            },
            {
                "Activity ID": "EC1290",
                "Activity Name": "Fabricate and Deliver Heat Pump",
                "WBS": "HVAC",
                "Physical % Complete": 14.0,
                "Status": "In Progress",
                "Total Float (Days)": 0.0,
                "Planned Start": "2011-05-02",
                "Planned Finish": "2012-08-09"
            },
            {
                "Activity ID": "EC1500",
                "Activity Name": "Install HVAC Ducts",
                "WBS": "HVAC",
                "Physical % Complete": 0.0,
                "Status": "Not Started",
                "Total Float (Days)": 174.0,
                "Planned Start": "2011-11-03",
                "Planned Finish": "2011-12-02"
            }
        ]

    def test_bim_element_mapping(self):
        scene = BIM4DEngine.synthesize_4d_model(self.sample_activities)
        self.assertEqual(scene["total_elements"], 3)
        self.assertEqual(scene["ifc_schema"], "IFC4_ADD2_TC1")
        
        # Verify Completed Element
        el_comp = scene["elements"][0]
        self.assertEqual(el_comp["simulation_state"], "COMPLETED")
        self.assertEqual(el_comp["ifc_storey"], "Substructure")
        self.assertEqual(len(el_comp["ifc_guid"]), 22)
        
        # Verify Critical In Progress Element
        el_crit = scene["elements"][1]
        self.assertEqual(el_crit["simulation_state"], "CRITICAL_IN_PROGRESS")
        self.assertEqual(el_crit["ifc_storey"], "Roof & Plant Room")
        self.assertEqual(el_crit["visual_style"]["color"], "#f43f5e")

        # Verify Not Started Ghost Element
        el_ghost = scene["elements"][2]
        self.assertEqual(el_ghost["simulation_state"], "NOT_STARTED")
        self.assertTrue(el_ghost["visual_style"]["wireframe"])

if __name__ == "__main__":
    unittest.main()
