import requests

res = requests.post('https://kfarmai.onrender.com/api/search', json={'keyword': '건곤', 'exact': True})
data = res.json()
print('shops:', data.get('shops', []))
print('companies:', data.get('companies', []))
