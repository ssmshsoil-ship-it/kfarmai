with open('02_dev/backend/api/server.py', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('def search()')
print(repr(content[idx:idx+600]))
