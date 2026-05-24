with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('getFilteredItems')
print(content[idx:idx+400])
