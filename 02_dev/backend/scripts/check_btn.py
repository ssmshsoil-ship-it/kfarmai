with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('검색하기')
print(repr(content[idx-200:idx+50]))
