import requests

tests = ['고추 잎이 말려요', '상토 보조금', '순천 농약사']

for kw in tests:
    res = requests.post('https://kfarmai.onrender.com/api/intent', json={'keyword': kw})
    data = res.json()
    print(kw, '->', data['intent'])
