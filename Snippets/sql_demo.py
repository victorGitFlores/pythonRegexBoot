import sqlite3

import datetime


dbname = "workfiles.db"
# Register datetime adapter and converter
sqlite3.register_adapter(datetime.datetime, lambda d: d.isoformat())
sqlite3.register_converter("DATETIME", lambda s: datetime.datetime.fromisoformat(s.decode()))

# Create the connection with the correct converter
conn = sqlite3.connect(
    dbname, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
)
cursor = conn.cursor()
print("DB connected, cursor created.")
# return conn, cursor       (<- you would do this from a function)


# Create a table for the input log
tabnam = "log_table"
cursor.execute(
    f"""
    CREATE TABLE IF NOT EXISTS {tabnam} (
        id INTEGER PRIMARY KEY,  -- Auto-incrementing ID
        timestamp DATETIME,
        type TEXT,
        message TEXT
    )
    """
)
conn.commit()
print("DBTable created.")
