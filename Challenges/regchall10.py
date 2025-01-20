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

if __name__ == "__main__":
    main()
