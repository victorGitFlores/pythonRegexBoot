#----------------------------------------------------------------------------
# 1. SQLite Connection
#---------------------------------------------------------------------------
import sqlite3
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

# whenever you need to connect to the database, 
# call init_sql() to get the connection and cursor objects.




#--------------------------------------------------------------------------------------
# 2. Create Table
#--------------------------------------------------------------------------------------
def create_table(cursor, tablename):
    cursor.execute(f"DROP TABLE IF EXISTS {tablename}")  # Remove old table
    cursor.execute(f"""
        CREATE TABLE {tablename} (
            id INTEGER PRIMARY KEY,  -- Auto-incrementing ID
            timestamp TEXT,
            type TEXT,
            message TEXT
        )
    """)
    conn.commit()  # Commit the transaction
    print(f"Table '{tablename}' created.")





#--------------------------------------------------------------------------------------
# 3. Insert Into Table
#--------------------------------------------------------------------------------------
# Insert multiple rows into a table using executemany
with open("system_logs.txt", "r") as file:
    logs = [
        (match.group(1), match.group(2), match.group(3))  # timestamp, type, message
        for line in file
        if (match := re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (\w+): (.+)", line))
    ]

cursor.executemany(
    f"INSERT INTO {log_table} (timestamp, type, message) VALUES (?, ?, ?)", logs
)
conn.commit()
print(f"Inserted {len(logs)} rows.")





#--------------------------------------------------------------------------------------
# 4. Select From Table
#--------------------------------------------------------------------------------------
# Fetch rows from a table and iterate over results
cursor.execute("""
SELECT timestamp, type, message
FROM log_table
WHERE type = 'ERROR'
""")
results = cursor.fetchall()

for row in results:
    print(row)




#--------------------------------------------------------------------------------------
# 5. Handling count()
#--------------------------------------------------------------------------------------
# Count the number of rows matching a condition
cursor.execute("""
SELECT COUNT(*)
FROM log_table
WHERE type = 'WARNING'
""")
count = cursor.fetchone()[0]
print(f"Number of warnings: {count}")





#--------------------------------------------------------------------------------------
# 6. Using BETWEEN for Range Queries
#--------------------------------------------------------------------------------------
# Select rows within a datetime range
ts_from = "2025-01-16 09:00:00"
ts_to = "2025-01-16 10:30:00"

cursor.execute("""
SELECT timestamp, type, message
FROM log_table
WHERE timestamp BETWEEN ? AND ?
""", (ts_from, ts_to))

results = cursor.fetchall()
for row in results:
    print(row)




#--------------------------------------------------------------------------------------
# 7. Debugging: View Table Data
#--------------------------------------------------------------------------------------
# Print all rows from a table for debugging purposes
cursor.execute("SELECT * FROM log_table")
all_rows = cursor.fetchall()

for row in all_rows:
    print(row)




#--------------------------------------------------------------------------------------
# 8. Indexing for Faster Queries
#--------------------------------------------------------------------------------------
# Add an index to a column to improve query performance
cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON log_table(timestamp)")
conn.commit()
print("Index created on 'timestamp'.")    




#--------------------------------------------------------------------------------------
# 9. Delete Data
#--------------------------------------------------------------------------------------
# Remove rows based on a condition
cursor.execute("""
DELETE FROM log_table
WHERE type = 'INFO'
""")
conn.commit()
print("Deleted rows where type = 'INFO'.")




#--------------------------------------------------------------------------------------
# 10. Closing the Connection
#--------------------------------------------------------------------------------------
# the database is expected to be opened once and closed once 
# in the entire lifetime of the program.
conn.close()
print("Database connection closed.")





#--------------------------------------------------------------------------------------
# 11. Get Distinct Types and Create Type-Specific Tables
#--------------------------------------------------------------------------------------
# Create distinct tables for each type of log entry
cursor.execute("""
SELECT DISTINCT type
FROM log_table
""")
types = cursor.fetchall()

for (my_type,) in types:  # Unpack tuple
    tabname = f"table_log_{my_type}"

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
    conn.commit()  # Commit the transaction

    # Populate the table
    cursor.execute(f"""
    SELECT timestamp, type, message
    FROM log_table
    WHERE type = ? AND timestamp BETWEEN ? AND ?
    """, (my_type, stamp_from, stamp_to))
    results = cursor.fetchall()

    # Insert the data into the table for this type
    cursor.executemany(
        f"INSERT INTO {tabname} (timestamp, type, message) VALUES (?, ?, ?)", results
    )
    conn.commit()  # Commit the transaction