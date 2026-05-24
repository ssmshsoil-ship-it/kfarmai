with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('h1 class=')
print(repr(content[idx:idx+300]))
