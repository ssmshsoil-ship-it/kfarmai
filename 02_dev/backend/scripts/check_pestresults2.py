with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('pestResults = filtered')
print(repr(content[idx:idx+100]))
