import sqlite3

# Initialize SQLite database
conn = sqlite3.connect("workfiles.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS log_table (
    timestamp TEXT,
    type TEXT,
    message TEXT
)
""")
conn.commit()

# Insert data
logs = [
    ("2025-01-16 08:15:30", "INFO", "System booted successfully."),
    ("2025-01-16 08:20:45", "ERROR", "Failed to connect to database."),
]
cursor.executemany("INSERT INTO log_table (timestamp, type, message) VALUES (?, ?, ?)", logs)
conn.commit()

# Query data
cursor.execute("""
SELECT timestamp, type, message
FROM log_table
WHERE type = 'ERROR'
""")
results = cursor.fetchall()
for row in results:
    print(row)

# Close connection
conn.close()