"""
4D BIM & IFC4 Integration Engine for Primavera P6 & Power BI.
Maps Oracle Primavera P6 CPM Activities to IFC4 Building Elements & Storeys:
- IfcBuildingStorey (Substructure, Ground Floor, Level 1, Level 2, Plant Room / Roof)
- IfcBuildingElement (Piles, Slab, Columns, Walls, Beams, Roof)
- IfcDistributionElement (HVAC Ducts, Heat Pump, Plumbing, Electrical Trays, Fixtures)
Computes 4D Simulation States (Not Started, In Progress, Completed, Critical Delay).
Generates 3D WebGL / Three.js parametric mesh geometry for interactive browser simulation.
"""

from typing import Dict, List, Any, Optional
import json
import hashlib

class BIM4DEngine:
    STOREY_MAPPING = {
        "Substructure": {
            "elevation": -3.0,
            "height": 3.0,
            "ifc_type": "IfcFooting",
            "keywords": ["foundation", "slab", "substructure", "excavat", "pour slab"]
        },
        "Ground Floor": {
            "elevation": 0.0,
            "height": 3.8,
            "ifc_type": "IfcSlab",
            "keywords": ["ground", "first floor", "rough-in", "grade"]
        },
        "Level 1": {
            "elevation": 3.8,
            "height": 3.6,
            "ifc_type": "IfcBeam",
            "keywords": ["second floor", "structure", "framing", "deck"]
        },
        "Level 2": {
            "elevation": 7.4,
            "height": 3.6,
            "ifc_type": "IfcWall",
            "keywords": ["drywall", "finishes", "carpentry", "flooring", "millwork"]
        },
        "Roof & Plant Room": {
            "elevation": 11.0,
            "height": 4.2,
            "ifc_type": "IfcDistributionFlowElement",
            "keywords": ["roof", "hvac", "heat pump", "chiller", "duct", "plant room", "mechanical"]
        }
    }

    @staticmethod
    def generate_ifc_guid(task_code: str, category: str) -> str:
        """Generates a deterministic pseudo-IFC GUID (22 characters Base64-like)."""
        h = hashlib.sha256(f"{task_code}_{category}".encode("utf-8")).hexdigest()
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_$"
        num = int(h[:16], 16)
        guid = []
        for _ in range(22):
            guid.append(chars[num % len(chars)])
            num //= len(chars)
        return "".join(guid)

    @classmethod
    def map_activity_to_bim(cls, activity: Dict[str, Any]) -> Dict[str, Any]:
        """Maps a P6 activity dictionary to an IFC4-compliant building element."""
        code = activity.get("Activity ID", "")
        name = activity.get("Activity Name", "")
        wbs = activity.get("WBS", "")
        pct = float(activity.get("Physical % Complete", 0.0) or 0.0)
        status = activity.get("Status", "Not Started")
        float_days = float(activity.get("Total Float (Days)", 0.0) or 0.0)
        start_date = activity.get("Planned Start", "")
        finish_date = activity.get("Planned Finish", "")

        target_str = f"{name} {wbs}".lower()
        matched_storey = "Ground Floor"
        for storey, cfg in cls.STOREY_MAPPING.items():
            if any(kw in target_str for kw in cfg["keywords"]):
                matched_storey = storey
                break

        storey_cfg = cls.STOREY_MAPPING[matched_storey]
        element_type = storey_cfg["ifc_type"]

        # 4D Simulation Status calculation
        if status == "Completed" or pct >= 100.0:
            sim_state = "COMPLETED"
            color_hex = "#10b981" # Emerald Green
            opacity = 0.95
        elif status == "In Progress" or pct > 0:
            if float_days <= 0:
                sim_state = "CRITICAL_IN_PROGRESS"
                color_hex = "#f43f5e" # Rose / Critical Red
            else:
                sim_state = "IN_PROGRESS"
                color_hex = "#f59e0b" # Amber / Construction Orange
            opacity = 0.85
        else:
            sim_state = "NOT_STARTED"
            color_hex = "#64748b" # Ghost / Slate Wireframe
            opacity = 0.25

        guid = cls.generate_ifc_guid(code, element_type)

        # Parametric 3D bounding geometry for Three.js WebGL rendering
        elevation = storey_cfg["elevation"]
        height = storey_cfg["height"]
        
        # Spatial placement based on activity code hash
        seed = int(hashlib.md5(code.encode()).hexdigest()[:6], 16)
        x_pos = ((seed % 100) / 100.0 - 0.5) * 16.0
        z_pos = (((seed // 100) % 100) / 100.0 - 0.5) * 12.0
        width = 2.0 + (seed % 3)
        depth = 2.0 + ((seed // 3) % 3)

        return {
            "ifc_guid": guid,
            "activity_id": code,
            "activity_name": name,
            "wbs": wbs,
            "ifc_storey": matched_storey,
            "ifc_element_type": element_type,
            "physical_pct_complete": pct,
            "planned_start": start_date,
            "planned_finish": finish_date,
            "total_float_days": float_days,
            "simulation_state": sim_state,
            "visual_style": {
                "color": color_hex,
                "opacity": opacity,
                "wireframe": sim_state == "NOT_STARTED"
            },
            "spatial_box": {
                "x": round(x_pos, 2),
                "y": round(elevation + height / 2.0, 2),
                "z": round(z_pos, 2),
                "width": round(width, 2),
                "height": round(height, 2),
                "depth": round(depth, 2)
            }
        }

    @classmethod
    def synthesize_4d_model(cls, activities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compiles all activities into an interactive 4D BIM scene payload."""
        elements = [cls.map_activity_to_bim(a) for a in activities]
        
        storeys_summary = {}
        for el in elements:
            s = el["ifc_storey"]
            storeys_summary[s] = storeys_summary.get(s, 0) + 1

        state_summary = {
            "COMPLETED": sum(1 for e in elements if e["simulation_state"] == "COMPLETED"),
            "IN_PROGRESS": sum(1 for e in elements if "IN_PROGRESS" in e["simulation_state"]),
            "NOT_STARTED": sum(1 for e in elements if e["simulation_state"] == "NOT_STARTED")
        }

        return {
            "project_name": "P6-PowerBI 4D BIM Simulation",
            "ifc_schema": "IFC4_ADD2_TC1",
            "total_elements": len(elements),
            "storeys_distribution": storeys_summary,
            "simulation_states": state_summary,
            "elements": elements
        }
