# 1. SQLite Connection
# Connect to an SQLite database and set up a cursor
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("workfiles.db")  # Creates 'workfiles.db' if it doesn't exist
cursor = conn.cursor()  # Create a cursor for executing SQL commands
print("Database connected.")

# Always close the connection when done
conn.close()

#--------------------------------------------------------------------------------------
# 2. Create Table
def create_table(cursor, tablename):
    cursor.execute(f"DROP TABLE IF EXISTS {tablename}")  # Remove old table
    cursor.execute(
        f"""
        CREATE TABLE {tablename} (
            timestamp TEXT,
            type TEXT,
            message TEXT
        )
        """
    )
    print(f"Table '{tablename}' created.")

#--------------------------------------------------------------------------------------
# 3. Insert Into Table
# Insert multiple rows into a table using executemany.
logs = [
    ("2025-01-16 08:15:30", "INFO", "System booted successfully."),
    ("2025-01-16 08:20:45", "ERROR", "Failed to connect to database."),
]

cursor.executemany(
    "INSERT INTO log_table (timestamp, type, message) VALUES (?, ?, ?)", logs
)
conn.commit()
print(f"Inserted {len(logs)} rows.")

#--------------------------------------------------------------------------------------
# 4. Select From Table
# Fetch rows from a table and iterate over results.
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
# Count the number of rows matching a condition.
cursor.execute("""
SELECT COUNT(*)
FROM log_table
WHERE type = 'WARNING'
""")
count = cursor.fetchone()[0]
print(f"Number of warnings: {count}")

#--------------------------------------------------------------------------------------
# 6. Using BETWEEN for Range Queries
# Select rows within a datetime range.
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
# Print all rows from a table for debugging purposes.
cursor.execute("SELECT * FROM log_table")
all_rows = cursor.fetchall()

for row in all_rows:
    print(row)

#--------------------------------------------------------------------------------------
# 8. Indexing for Faster Queries
# Add an index to a column to improve query performance.
cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON log_table(timestamp)")
conn.commit()
print("Index created on 'timestamp'.")

#--------------------------------------------------------------------------------------
# 9. Delete Data
# Remove rows based on a condition.

cursor.execute("""
DELETE FROM log_table
WHERE type = 'INFO'
""")
conn.commit()
print("Deleted rows where type = 'INFO'.")

#--------------------------------------------------------------------------------------
# 10. Closing the Connection
# Always ensure the database connection is closed when finished.

conn.close()
print("Database connection closed.")

#--------------------------------------------------------------------------------------

