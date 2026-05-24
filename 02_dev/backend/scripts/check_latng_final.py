import requests
import time

time.sleep(30)
res = requests.post('https://kfarmai.onrender.com/api/search', json={'keyword': '건곤', 'exact': True})
data = res.json()
print('companies:', data.get('companies'))
