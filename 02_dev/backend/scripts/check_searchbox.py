with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('rounded-full shadow')
print(repr(content[idx-20:idx+150]))
