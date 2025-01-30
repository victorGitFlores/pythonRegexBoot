import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import re
import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_sql(db_name):
    try:
        sqlite3.register_adapter(datetime.datetime, lambda d: d.isoformat())
        sqlite3.register_converter("DATETIME", lambda s: datetime.datetime.fromisoformat(s.decode()))

        conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = conn.cursor()
        logging.info("Database connected with datetime support.")
        return conn, cursor
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        raise

def cvt_log_table(db_name, log_name, table_name, patt_log):
    try:
        conn, cursor = init_sql(db_name)
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(f"""
            CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                type TEXT,
                module TEXT,
                code INTEGER,
                message TEXT
            )
        """)
        conn.commit()

        with open(log_name, "r") as file:
            logs = [
                (match.group(1), match.group(2), match.group(3), match.group(4), match.group(5))
                for line in file if (match := re.search(patt_log, line))
            ]

        cursor.executemany(f"INSERT INTO {table_name} (timestamp, type, module, code, message) VALUES (?, ?, ?, ?, ?)", logs)
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error converting log to table: {e}")
        raise

def split_logs_db(db_name, table_name):
    try:
        conn, cursor = init_sql(db_name)
        cursor.execute(f"SELECT DISTINCT type FROM {table_name}")
        distinct_types = [row[0] for row in cursor.fetchall()]

        for distinct_type in distinct_types:
            log_table_by_type = "log_tab_" + distinct_type
            cursor.execute(f"DROP TABLE IF EXISTS {log_table_by_type}")
            cursor.execute(f"CREATE TABLE {log_table_by_type} AS SELECT * FROM {table_name} WHERE type = '{distinct_type}'")
            conn.commit()

        conn.close()
        return distinct_types
    except Exception as e:
        logging.error(f"Error splitting logs: {e}")
        raise

def get_options(db_name, table_name, column_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT {column_name} FROM {table_name} ORDER BY {column_name}")
        options = [row[0] for row in cursor.fetchall()]
        conn.close()
        return options
    except Exception as e:
        logging.error(f"Error fetching options: {e}")
        raise

def fetch_filtered_logs(db_name, table_name, log_type, origin_code):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        query = f"SELECT timestamp, type, message FROM {table_name} WHERE 1=1"
        params = []

        if log_type != "ALL":
            query += " AND type = ?"
            params.append(log_type)

        if origin_code != "ALL":
            query += " AND message LIKE ?"
            params.append(f"%code={origin_code}%")

        cursor.execute(query, params)
        logs = cursor.fetchall()
        conn.close()
        return logs
    except Exception as e:
        logging.error(f"Error fetching filtered logs: {e}")
        raise

def run_app():
    log_name = "log_ch_11.txt"
    db_name = "workfiles.db"
    table_name = "log_table"
    log_patt = r"(\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2})\s\[(\w+)\]\s\(module=(\w+)\,\scode=(\d+)\):\s(.+)"

    try:
        cvt_log_table(db_name, log_name, table_name, log_patt)
        distinct_types = split_logs_db(db_name, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to initialize database: {e}")
        return

    root = tk.Tk()
    root.title("Log Filtering Report")

    log_type_label = tk.Label(root, text="Select Log Type:")
    log_type_label.pack()

    log_types = ["ALL"] + get_options(db_name, table_name, "type")
    log_type_var = tk.StringVar(value=log_types[0])
    log_type_dropdown = ttk.Combobox(root, textvariable=log_type_var, values=log_types, state="readonly")
    log_type_dropdown.pack()

    origin_code_label = tk.Label(root, text="Select Origin Code:")
    origin_code_label.pack()

    origin_codes = ["ALL"] + get_options(db_name, table_name, "code")
    origin_code_var = tk.StringVar(value=origin_codes[0])
    origin_code_dropdown = ttk.Combobox(root, textvariable=origin_code_var, values=origin_codes, state="readonly")
    origin_code_dropdown.pack()

    result_text = tk.Text(root, width=80, height=20)
    result_text.pack()

    def filter_logs():
        log_type = log_type_var.get()
        origin_code = origin_code_var.get()
        try:
            logs = fetch_filtered_logs(db_name, table_name, log_type, origin_code)
            result_text.delete("1.0", tk.END)
            if logs:
                result_text.insert(tk.END, f"Logs for Type: {log_type}, Code: {origin_code}\n\n")
                for log in logs:
                    result_text.insert(tk.END, f"{log[0]} [{log[1]}]: {log[2]}\n")
            else:
                result_text.insert(tk.END, "No matching logs found.\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter logs: {e}")

    filter_button = tk.Button(root, text="Filter Logs", command=filter_logs)
    filter_button.pack()

    root.mainloop()

if __name__ == "__main__":
    run_app()