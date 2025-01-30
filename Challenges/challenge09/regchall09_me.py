# regchall09_me.py
# this is regchall09_m enhanced!   featuring sqlite3
# [2025-01-16 08:15:30] INFO: System booted successfully.
# timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
# MY TASK: 
# Extract all lines with the word ERROR that occurred between 09:00:00 and 10:30:00

import re
import datetime
import sqlite3

#--------------------------------------------------------------------------------------
def init_sql():
    # Register datetime adapter and converter
    sqlite3.register_adapter(datetime.datetime, lambda d: d.isoformat())
    sqlite3.register_converter("DATETIME", lambda s: datetime.datetime.fromisoformat(s.decode()))

    # Create the connection with the correct converter
    conn = sqlite3.connect(
        "workfiles.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    cursor = conn.cursor()
    print("DB connected, cursor created.")
    return conn, cursor


def create_workfile(conn, cursor, tabnam):
    cursor.execute(f"""
        DROP TABLE IF EXISTS {tabnam}
    """) # drop table if it exists

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {tabnam} (
            timestamp TEXT,
            type TEXT,
            message TEXT
        )
        """
    )
    conn.commit()
    print(f"{tabnam} created.")

def check_for_warnings(ts_from, ts_to, workfile, cursor):
    # returns True if any warnings found
    cursor.execute(f"""
    SELECT count(*)
    FROM {workfile}
    WHERE type = 'WARNING' AND timestamp BETWEEN ? AND ?
    """, (ts_from,ts_to))
    results = cursor.fetchall()
    # if count() > 0, return True
    return results[0][0] > 0

#--------------------------------------------------------------------------------------

def main():

    patt = r"\[(\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2})\]\s(\w+)\:\s(.+)"
    tot_err = 0
    ts_from = "2025-01-16 09:00:00"
    ts_to   = "2025-01-16 10:30:00"
    infile  = "system_logs.txt"
    outfile = "filtered_errors.txt"
    workfile = "log_table"
    my_tups = []
    # set up db...
    conn, cursor = init_sql()
    # create work table
    create_workfile(conn, cursor, workfile)
    print("workfile created")
    # insert flatfile into log_table:

    with open(infile,"r") as input:
        # flat into list of tups
        my_tups = [
            (match.group(1), match.group(2), match.group(3))
            for line in input
            if (match := re.search(patt, line))
        ]
        # Insert data into SQLite table
        # notice how executemany is used to insert multiple records from a list!
        # also notice the cool unpacking of the tuples into 3 vars! ? ? ? !!!
        cursor.executemany(f"INSERT INTO {workfile} (timestamp, type, message) VALUES (?, ?, ?)", my_tups)
        conn.commit()
    # get the errors within the datetime range
    cursor.execute(f"""
    SELECT timestamp, type, message
    FROM {workfile}
    WHERE type = 'ERROR' AND timestamp BETWEEN ? AND ?
    """, (ts_from, ts_to)) #doesnt like classic f string {fields}
    results = cursor.fetchall()
    # print the errors
    for row in results:
        tot_err += 1
        print(row)



    print(f"Total Errors: {tot_err}")
    print(f"File written: {outfile}")
    # lastly, any errors in the datetime range?
    if check_for_warnings(ts_from, ts_to, workfile, cursor):
        print("Warnings found in the datetime range.")
    else:
        print("No warnings found in the datetime range.")


#--------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#--------------------------------------------------------------------------------------

""" actual output:
/c/_home/learning/python ai bootcamp 2025/challenges> python regchall09_me.py
DB connected, cursor created.
log_table created.
workfile created
Data in log_table:
('2025-01-16 08:15:30', 'INFO', 'System booted successfully.')
('2025-01-16 08:20:45', 'ERROR', 'Failed to connect to database.')
('2025-01-16 09:00:10', 'INFO', 'User login successful.')
('2025-01-16 09:05:45', 'ERROR', 'Disk space critically low.')
('2025-01-16 09:30:20', 'INFO', 'Backup completed.')
('2025-01-16 10:00:00', 'ERROR', 'Failed to write to log file.')
('2025-01-16 10:15:45', 'WARNING', 'High memory usage detected.')
('2025-01-16 10:20:30', 'ERROR', 'Database connection timeout.')
('2025-01-16 11:00:00', 'INFO', 'System maintenance started.')
('2025-01-16 11:30:00', 'INFO', 'Maintenance completed.')
('2025-01-16 09:05:45', 'ERROR', 'Disk space critically low.')
('2025-01-16 10:00:00', 'ERROR', 'Failed to write to log file.')
('2025-01-16 10:20:30', 'ERROR', 'Database connection timeout.')
Total Errors: 3
File written: filtered_errors.txt
Warnings found in the datetime range.
/c/_home/learning/python ai bootcamp 2025/challenges>
"""
