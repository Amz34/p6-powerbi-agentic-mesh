"""
High-Performance Zero-Dependency Oracle Primavera P6 XER & SQLite Parser.
Complies with Oracle P6 schema definitions (Tables: TASK, TASKPRED, PROJWBS, CALENDAR, RSRC, ACTVCODE).
"""
import os
import sqlite3
import csv
from typing import Dict, List, Any, Optional

class XERParser:
    @staticmethod
    def parse_to_sqlite(xer_path: str, sqlite_db_path: str) -> bool:
        if os.path.exists(sqlite_db_path):
            os.remove(sqlite_db_path)
        conn = sqlite3.connect(sqlite_db_path)
        cur = conn.cursor()
        
        current_table = None
        fields = []
        with open(xer_path, 'r', encoding='latin-1', errors='ignore') as f:
            for line in f:
                line = line.rstrip('\r\n')
                if not line:
                    continue
                parts = line.split('\t')
                tag = parts[0]
                if tag == '%T':
                    current_table = parts[1]
                    fields = []
                elif tag == '%F':
                    fields = parts[1:]
                    cols = ', '.join([f'"{c}" TEXT' for c in fields])
                    cur.execute(f'CREATE TABLE IF NOT EXISTS "{current_table}" ({cols})')
                elif tag == '%R':
                    if current_table and fields:
                        row = parts[1:]
                        if len(row) < len(fields):
                            row += [''] * (len(fields) - len(row))
                        elif len(row) > len(fields):
                            row = row[:len(fields)]
                        placeholders = ', '.join(['?'] * len(fields))
                        cur.execute(f'INSERT INTO "{current_table}" VALUES ({placeholders})', row)
        conn.commit()
        conn.close()
        return True
