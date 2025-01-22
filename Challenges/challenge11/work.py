import sqlite3
import tkinter as tk
from tkinter import ttk
import re
import datetime


def init_sql(db_name):
    # Register datetime adapter and converter for proper handling of datetime fields
    sqlite3.register_adapter(datetime.datetime, lambda d: d.isoformat())
    sqlite3.register_converter("DATETIME", lambda s: datetime.datetime.fromisoformat(s.decode()))

    # Connect to SQLite database with support for datetime parsing
    conn = sqlite3.connect(
        db_name,
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    cursor = conn.cursor()
    print("Database connected with datetime support.")
    return conn, cursor  # Return connection and cursor for reuse


def cvt_log_table(db_name, log_name, table_name, patt_log):
    conn, cursor = init_sql(db_name)
    # Create table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")  # Remove old table
    cursor.execute(f"""
        CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY,  -- Auto-incrementing ID
            timestamp TEXT,
            type TEXT,
            module TEXT,
            code INTEGER,
            message TEXT
        )
    """)
    conn.commit()  # Commit the transaction
    
    # Insert from log file into table
    with open(log_name, "r") as file:
        logs = [
            (match.group(1), match.group(2), match.group(3), match.group(4), match.group(5), )  
            # timestamp, type, module, code, message
            for line in file
            if (match := re.search(patt_log, line))
        ]

    cursor.executemany(
        f"INSERT INTO {table_name} (timestamp, type, module, code, message) VALUES (?, ?, ?, ?, ?)", logs
    )
    conn.commit()  # Commit the transaction

def split_logs_db(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # select distinct types from log_table, use this to create new tables
    cursor.execute(f"SELECT DISTINCT type FROM {table_name}")
    distinct_types = [row[0] for row in cursor.fetchall()]

    for distinct_type in distinct_types:
        log_table_by_type = "log_tab_" + distinct_type
        cursor.execute(f"CREATE TABLE {log_table_by_type} AS SELECT * FROM {table_name} WHERE type = '{distinct_type}'")
        conn.commit()



def run_app():
    db_name = "workfiles.db"
    log_name = "log_ch_11.txt"
    table_name = "log_table"
    log_patt   = r"(\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2})\s\[(\w+)\]\s\(module=(\w+)\,\scode=(\d+)\):\s(.+)"

    # convert log to table:
    cvt_log_table(db_name, log_name, table_name, log_patt)
    split_logs_db(db_name, table_name)

if __name__ == "__main__":
    run_app()
    print("Done.")