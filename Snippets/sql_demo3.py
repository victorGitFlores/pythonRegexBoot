# Filter by Range:
# execute a sql, get results iterable, iterate over results.
cursor.execute("""
    SELECT timestamp, type, message
    FROM logs
    WHERE type = 'ERROR' AND timestamp BETWEEN ? AND ?
""", ('2025-01-16 09:00:00', '2025-01-16 10:30:00'))
results = cursor.fetchall()
for row in results:
    print(row)