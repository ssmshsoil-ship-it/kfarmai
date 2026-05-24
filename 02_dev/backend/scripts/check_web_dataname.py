with open('H:/내 드라이브/kfarmai-web/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('data-name=')
print(repr(content[idx:idx+60]))
