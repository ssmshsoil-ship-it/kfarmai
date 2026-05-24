import requests
requests.get('https://kfarmai.onrender.com/api/health')
res = requests.post('https://kfarmai.onrender.com/api/search', json={'keyword': '건곤지오텍', 'exact': True})
print(res.json())
