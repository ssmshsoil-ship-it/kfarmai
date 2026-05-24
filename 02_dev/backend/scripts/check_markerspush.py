with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('markers.push')
print(content[idx-200:idx+200])
