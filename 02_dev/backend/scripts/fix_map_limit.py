with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()

# list.forEach(addMarker) 부분에 제한 추가
old = 'list.forEach(addMarker)'
new = '''(list.length > 500 ? list.slice(0, 500) : list).forEach(addMarker)'''

if old in content:
    content = content.replace(old, new, 1)
    print('마커 500개 제한 완료')
else:
    print('실패')

# 초기 줌 레벨도 낮춰서 로딩 시 마커 적게 표시
old2 = 'level: 10'
new2 = 'level: 8'
if old2 in content:
    content = content.replace(old2, new2, 1)
    print('줌 레벨 수정 완료')

with open('02_dev/frontend/map.html', 'w', encoding='utf-8') as f:
    f.write(content)
