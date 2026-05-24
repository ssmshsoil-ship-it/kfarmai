with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 초기 줌 레벨을 13에서 유지하되 마커는 줌 8 이하일 때만 표시
old = '''const map = new kakao.maps.Map(mapContainer, {
            center: new kakao.maps.LatLng(36.5, 127.8),
            level: 13
        });'''

new = '''const map = new kakao.maps.Map(mapContainer, {
            center: new kakao.maps.LatLng(36.5, 127.8),
            level: 10
        });'''

if old in content:
    content = content.replace(old, new, 1)
    print('초기 줌 수정 완료')
else:
    print('실패')

with open('02_dev/frontend/map.html', 'w', encoding='utf-8') as f:
    f.write(content)
