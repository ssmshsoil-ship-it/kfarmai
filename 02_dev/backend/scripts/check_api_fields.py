import requests

requests.get('https://kfarmai.onrender.com/api/health')

# 농약사 검색
res = requests.post('https://kfarmai.onrender.com/api/search', json={'keyword': '금성농약사'})
data = res.json()
if data.get('shops'):
    print('shops[0]:', data['shops'][0])
if data.get('companies'):
    print('companies[0]:', data['companies'][0])
