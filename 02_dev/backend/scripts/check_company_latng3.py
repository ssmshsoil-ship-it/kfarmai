import requests
import time

time.sleep(2)
res = requests.post('https://kfarmai.onrender.com/api/search', json={'keyword': '건곤', 'exact': False})
data = res.json()
print('companies:', data.get('companies'))
