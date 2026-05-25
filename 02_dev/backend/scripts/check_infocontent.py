with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('function infoContent')
print(content[idx:idx+500])
