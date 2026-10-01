import sqlite3
import pandas as pd
conn = sqlite3.connect('database/energy.db')
df = pd.read_sql_query("SELECT * FROM energy_readings ORDER BY id DESC LIMIT 5", conn)
print(df.columns)
print(df[['id', 'appliance', 'state', 'occupancy']])
conn.close()
