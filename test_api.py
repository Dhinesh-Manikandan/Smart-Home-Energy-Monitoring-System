import requests
response = requests.get("http://127.0.0.1:8000/api/readings")
data = response.json()
print("Last reading:", data[-1] if data else "Empty")
print("Keys:", data[-1].keys() if data else "Empty")
