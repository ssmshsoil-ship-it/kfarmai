with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('shadow-2xl flex')
print(repr(content[idx-10:idx+300]))
