with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('dapi.kakao.com')
print(content[idx:idx+200])
