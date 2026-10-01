import sqlite3
try:
    conn = sqlite3.connect('database/energy.db')
    conn.execute("ALTER TABLE energy_readings ADD COLUMN occupancy VARCHAR DEFAULT 'UNOCCUPIED'")
    conn.commit()
    conn.close()
    print('Success')
except Exception as e:
    print('Error:', e)
