with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('renderItems(')
print(repr(content[idx-50:idx+200]))
