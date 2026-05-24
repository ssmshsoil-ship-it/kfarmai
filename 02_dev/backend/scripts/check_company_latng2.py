import requests
import time

# 서버 깨우기
res = requests.get('https://kfarmai.onrender.com/api/health')
print('서버 상태:', res.json())
time.sleep(3)

# 다시 검색
res = requests.post('https://kfarmai.onrender.com/api/search', json={'keyword': '건곤지오텍', 'exact': True})
data = res.json()
print('companies:', data.get('companies'))
