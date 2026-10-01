import sys
sys.path.append('dashboard')
from api_client import get_all_readings
df = get_all_readings()
print(df.columns)
if 'occupancy' in df.columns:
    print(df['occupancy'].tail())
else:
    print("NO OCCUPANCY COLUMN")
