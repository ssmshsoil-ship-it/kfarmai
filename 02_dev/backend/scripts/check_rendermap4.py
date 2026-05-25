with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('function renderMap')
print(repr(content[idx-100:idx+50]))
