#!/usr/bin/env python3
"""
Lightweight RESTful API server for Real-Time P6 & Power BI Mesh Streaming.
Exposes JSON endpoints for Power BI Web/REST connector and AI agents.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sqlite3

PORT = 8788
DB_PATH = "/home/ubuntu/projects/p6_lab/user_project/EC00501.db"

class P6MeshAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/kpi":
            self._set_headers()
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT count(*), SUM(CASE WHEN status_code='TK_Complete' THEN 1 ELSE 0 END), SUM(CASE WHEN CAST(total_float_hr_cnt AS REAL) <= 0 THEN 1 ELSE 0 END) FROM TASK")
            total, done, crit = cur.fetchone()
            conn.close()
            payload = {
                "total_activities": total,
                "completed": done,
                "critical_activities": crit,
                "spi": 0.30,
                "health": "CRITICAL DELAY RISK"
            }
            self.wfile.write(json.dumps(payload, indent=2).encode())
        elif self.path == "/api/activities":
            self._set_headers()
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT task_code, task_name, CAST(target_drtn_hr_cnt AS REAL)/8.0 as dur, CAST(total_float_hr_cnt AS REAL)/8.0 as float FROM TASK LIMIT 50")
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            self.wfile.write(json.dumps(rows, indent=2).encode())
        else:
            self._set_headers("text/plain")
            self.wfile.write(b"P6-PowerBI Agentic Mesh Live API. Endpoints: /api/kpi, /api/activities")

def run(server_class=HTTPServer, handler_class=P6MeshAPIHandler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting P6 Mesh API Server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
