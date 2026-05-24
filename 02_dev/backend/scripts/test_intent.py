import requests

tests = [
    '고추 잎이 말려요',
    '순천 농약사',
    '상토 보조금 신청',
    '정원 박람회'
]

for kw in tests:
    res = requests.post('http://127.0.0.1:5000/api/intent', json={'keyword': kw})
    data = res.json()
    print(kw, '->', data['intent'])
