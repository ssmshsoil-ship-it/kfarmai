with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('new kakao.maps.Marker')
print(repr(content[idx:idx+300]))
