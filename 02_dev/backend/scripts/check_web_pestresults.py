with open('H:/내 드라이브/kfarmai-web/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('pestResults = filtered')
print(repr(content[idx:idx+100]))
