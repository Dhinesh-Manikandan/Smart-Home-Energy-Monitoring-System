import sqlite3
conn = sqlite3.connect('database/energy.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(energy_readings)")
print(cursor.fetchall())
conn.close()
