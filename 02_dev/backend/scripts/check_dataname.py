with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('data-name')
print(repr(content[idx-50:idx+100]))
