
# read thru text file...converting to table data

import re
import sqlite3

tabnam = "log_table"
# Regex pattern for parsing logs
pattern = r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s(\w+):\s(.+)"

# Open the text file and extract data
with open("system_logs.txt", "r") as file:
    logs = [
        (match.group(1), match.group(2), match.group(3))  # timestamp, type, message
        for line in file
        if (match := re.search(pattern, line))
    ]

# Insert data into SQLite table
# notice how executemany is used to insert multiple records from a list!
# but first...
# Set up database connection and cursor (done once per program/session)
conn = sqlite3.connect("workfiles.db")  # Connect to the SQLite database
cursor = conn.cursor()  # Cursor for executing SQL commands
cursor.executemany(f"INSERT INTO {tabnam} (timestamp, type, message) VALUES (?, ?, ?)", logs)
conn.commit()
print(f"Inserted {len(logs)} records into the database!")