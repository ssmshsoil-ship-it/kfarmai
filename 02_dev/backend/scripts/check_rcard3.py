with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('r-map-link')
print(content[idx-200:idx+300])
