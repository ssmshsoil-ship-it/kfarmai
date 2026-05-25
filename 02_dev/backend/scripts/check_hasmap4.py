with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('hasMap')
print(repr(content[idx:idx+60]))
idx2 = content.find('r-map-link')
print(repr(content[idx2:idx2+100]))
