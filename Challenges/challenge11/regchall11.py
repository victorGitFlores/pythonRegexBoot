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

    # lastly, close the connection
    conn.close()

def split_logs_db(db_name, table_name): # returns distinct_types list
    conn, cursor = init_sql(db_name)

    # select distinct types from log_table, use this to create new tables
    cursor.execute(f"SELECT DISTINCT type FROM {table_name}")
    distinct_types = [row[0] for row in cursor.fetchall()]

    for distinct_type in distinct_types:
        log_table_by_type = "log_tab_" + distinct_type
        cursor.execute(f"DROP TABLE IF EXISTS {log_table_by_type}")  # Remove old table
        cursor.execute(f"CREATE TABLE {log_table_by_type} AS SELECT * FROM {table_name} WHERE type = '{distinct_type}'")
        conn.commit()

    # lastly, close the connection
    conn.close()

    return distinct_types

def summarize_data(db_name, table_name):
    conn, cursor = init_sql(db_name)

    # summary by type
    cursor.execute("""
    SELECT type, COUNT(*)
    FROM log_table
    GROUP BY type
    ORDER BY type
    """)
    results = cursor.fetchall()
    print("\n\nLog Type Summary:")
    for type, count in results:
        print(f"{type}: {count} logs")

    # summary by module
    cursor.execute("""
    SELECT module, COUNT(*)
    FROM log_table
    GROUP BY module
    ORDER BY module
    """)
    results = cursor.fetchall()
    print("\n\nModule Summary:")
    for module, count in results:
        print(f"{module}: {count} logs")



    
    # lastly, close the connection
    conn.close()







def get_options(db_name, table_name, column_name):
    """Retrieve unique, sorted options from a column in the database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"SELECT DISTINCT {column_name} FROM {table_name} ORDER BY {column_name}")
    options = [row[0] for row in cursor.fetchall()]

    conn.close()
    return options

def fetch_filtered_logs(db_name, table_name, log_type, origin_code):
    """Fetch logs filtered by log_type and origin_code."""
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






    #-----------------------------------------------------------------------------------




#--------------------------------------------------------------------------------------
def run_app():  # mainline
#--------------------------------------------------------------------------------------
    log_name = "log_ch_11.txt"
    db_name = "workfiles.db"
    table_name = "log_table"
    log_patt   = r"(\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2})\s\[(\w+)\]\s\(module=(\w+)\,\scode=(\d+)\):\s(.+)"

    # convert log to table:
    cvt_log_table(db_name, log_name, table_name, log_patt) 
    distinct_types = split_logs_db(db_name, table_name)



    # Set up GUI
    root = tk.Tk()
    root.title("Log Filtering Report")

    # Dropdown for log types
    log_type_label = tk.Label(root, text="Select Log Type:")
    log_type_label.pack()

    log_types = ["ALL"] + get_options(db_name, table_name, "type")
    log_type_var = tk.StringVar(value=log_types[0])
    log_type_dropdown = ttk.Combobox(root, textvariable=log_type_var, values=log_types, state="readonly")
    log_type_dropdown.pack()

    # Dropdown for origin codes
    origin_code_label = tk.Label(root, text="Select Origin Code:")
    origin_code_label.pack()




    origin_codes = ["ALL"] + get_options(db_name, table_name, "code")
    origin_code_var = tk.StringVar(value=origin_codes[0])
    origin_code_dropdown = ttk.Combobox(root, textvariable=origin_code_var, values=origin_codes, state="readonly")
    origin_code_dropdown.pack()



    # Text area to display results
    result_text = tk.Text(root, width=80, height=20)
    result_text.pack()

    def btn_cmd_filter_logs():
        log_type = log_type_var.get()
        origin_code = origin_code_var.get()
        logs = fetch_filtered_logs(db_name, table_name, log_type, origin_code)

        result_text.delete("1.0", tk.END)
        if logs:
            result_text.insert(tk.END, f"Logs for Type: {log_type}, Code: {origin_code}\n\n")
            for log in logs:
                result_text.insert(tk.END, f"{log[0]} [{log[1]}]: {log[2]}\n")
        else:
            result_text.insert(tk.END, "No matching logs found.\n")

    # Filter button
    filter_button = tk.Button(root, text="Filter Logs", command=btn_cmd_filter_logs)
    filter_button.pack()

    root.mainloop()


    distinct_type = get_options(db_name, table_name, "type")
    distinct_code = get_options(db_name, table_name, "code")


if __name__ == "__main__":
    run_app()