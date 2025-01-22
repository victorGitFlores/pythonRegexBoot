# Implement a command-line argument to specify the time range for the query..
# 2025-01-16 08:15:30 INFO: System booted successfully


import re 
import sqlite3

#----------------------------------------------------------------------------------------
# functions:
#----------------------------------------------------------------------------------------
def get_user_timestamp(from_to, patt, ts_from = "0000-01-01 00:00:00"):
    # get timestamp range from/to in format: 2025-01-16 08:15:30
    # has to be in this format:
    # YYYY-MM-DD HH:MM:SS
    while True:
        usr_str = input(f"Give me {from_to} timestamp in format: YYYY-MM-DD HH:MM:SS: ") 
        # good code...re.match() works fine for this...
        match = re.match(patt, usr_str)
        if match:
            # sanity check:
            good = True
            if not (match.group(1) > "0001" and match.group(1) <= "9999"):
                good = False
            if not (match.group(2) >= "01" and match.group(2) <= "12"):
                good = False
            if not (match.group(3) >= "01" and match.group(3) <= "31"):
                good = False
            if not (match.group(4) >= "00" and match.group(4) <= "23"):
                good = False
            if not (match.group(5) >= "00" and match.group(5) <= "59"):
                good = False
            if not (match.group(6) >= "00" and match.group(6) <= "59"):
                good = False
            # still sanity? break the loop
            if good:
                # sanity check: TO timestamp has to be greater than FROM timestamp                
                if usr_str > ts_from:
                    return usr_str
                else:
                    print("TO timestamp has to be greater than FROM timestamp. Try again.")
            else:
                print("Check carefully, Try again")
        else:
            print("Wrong format. Try again.")
#----------------------------------------------------------------------------------------

def cvt_log_table(db_name, log_name, log_table_name, patt_log):
    #connect to db
    # Connect to SQLite database
    conn = sqlite3.connect(db_name)  # Creates 'workfiles.db' if it doesn't exist
    cursor = conn.cursor()  # Create a cursor for executing SQL commands
    print("Database connected.")
    
    # create table
    cursor.execute(f"DROP TABLE IF EXISTS {log_table_name}")  # Remove old table
    cursor.execute(
        f"""
        CREATE TABLE {log_table_name} (
            id INTEGER PRIMARY KEY,  -- Auto-incrementing ID
            timestamp TEXT,
            type TEXT,
            message TEXT
        )
        """
    )
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_timestamp ON {log_table_name}(timestamp)")
    conn.commit()

    print(f"Table '{log_table_name}' created.")

    # Open the text file and extract data into logs list    here here here here here **************
    with open(log_name, "r") as file:
        logs = [
            (match.group(1), match.group(2), match.group(3))  # timestamp, type, message
            for line in file
            if (match := re.search(patt_log, line))
        ]

    # Insert data into SQLite table from logs list
    cursor.executemany(
        f"INSERT INTO {log_table_name} (timestamp, type, message) VALUES (?, ?, ?)", logs
    )
    conn.commit()
    print(f"Inserted {len(logs)} rows.")



    
    # lastly...close the connection
    conn.close()

def parse_log_by_type(db_name, log_table_name, stamp_from, stamp_to):
    # returns a list of distinct types of log entries

    # get the distinct types of log entries...
    #      Connect to SQLite database
    conn = sqlite3.connect(db_name)  # Creates 'workfiles.db' if it doesn't exist
    cursor = conn.cursor()  # Create a cursor for executing SQL commands
    # print("Database connected.")
    cursor.execute("""
    SELECT distinct type
    FROM log_table
    """)
    types = cursor.fetchall()

    for (my_type,) in types:  # Unpack tuple
        tabname = "table_log_" + my_type

        # Drop and create the table
        cursor.execute(f"DROP TABLE IF EXISTS {tabname}")
        cursor.execute(f"""
            CREATE TABLE {tabname} (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                type TEXT,
                message TEXT
            )
        """)
        conn.commit() # Commit the transaction
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_timestamp ON {tabname}(timestamp)")
        conn.commit()


        # Populate the table
        cursor.execute(f"""
        SELECT timestamp, type, message
        FROM {log_table_name}
        WHERE type = ? AND timestamp BETWEEN ? AND ?
        """, (my_type, stamp_from, stamp_to))
        results = cursor.fetchall()

        # Insert the data into the table for this type
        cursor.executemany(
            f"INSERT INTO {tabname} (timestamp, type, message) VALUES (?, ?, ?)", results
        )
        conn.commit() # Commit the transaction



    # Always close the connection when done
    conn.close()
    # return distinct types as list of strings...
    return [t[0] for t in types]

def print_hmany_by_type(db_name, log_table_name, log_types):
    #connect to db
    # Connect to SQLite database
    conn = sqlite3.connect(db_name)  # Creates 'workfiles.db' if it doesn't exist
    cursor = conn.cursor()  # Create a cursor for executing SQL commands

    for log_type in log_types:
        log_name = "table_log_" + log_type
        cursor.execute(f"""
        SELECT COUNT(*)
        FROM {log_name}
        WHERE type = '{log_type}'
        """)
        count = cursor.fetchone()[0]
        print(f"{log_type}: {count} logs")

    # print detail for ERROR type
    log_name = "table_log_ERROR"
    print("ERRORS in time range:")
    cursor.execute(f"""
    SELECT timestamp, type, message
    FROM {log_name}
    WHERE type = 'ERROR'
    """)
    results = cursor.fetchall()

    for row in results:
        print(row)







    # lastly...close the connection
    conn.close()

def main():
    patt_ts = r"(\d{4})\-(\d{2})\-(\d{2})\s(\d{2})\:(\d{2})\:(\d{2})"
    patt_log = r"\[(\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2})\]\s(\w+)\:\s(.+)"
    log_name = "system_logs_multi.txt"
    log_table_name = "log_table"
    db_name = "workfiles.db"
    
    # get from/to timestamps from user
    stamp_from = get_user_timestamp("FROM", patt_ts)
    stamp_to = get_user_timestamp("TO", patt_ts, stamp_from)
    
    # convert log to table:
    cvt_log_table(db_name, log_name, log_table_name, patt_log)
    
    # parse log entries by type into tables
    working_types = parse_log_by_type(db_name, log_table_name, stamp_from, stamp_to)

    # print type/how many entries
    print_hmany_by_type(db_name, log_table_name, working_types)

if __name__ == "__main__":
    main()


# actual output:
""""
/c/_home/learning/python ai bootcamp 2025/challenges> python regchall10.py
Give me FROM timestamp in format: YYYY-MM-DD HH:MM:SS: 2025-01-16 00:00:00
Give me TO timestamp in format: YYYY-MM-DD HH:MM:SS: 2025-01-16 23:59:59
Database connected.
Table 'log_table' created.
Inserted 12 rows.
INFO: 4 logs
ERROR: 3 logs
DEBUG: 3 logs
WARNING: 2 logs
ERRORS in time range:
('2025-01-16 08:20:45', 'ERROR', 'Failed to connect to database.')
('2025-01-16 09:00:45', 'ERROR', 'Disk space critically low.')
('2025-01-16 09:40:00', 'ERROR', 'Failed to write to log file.')
/c/_home/learning/python ai bootcamp 2025/challenges>
"""
