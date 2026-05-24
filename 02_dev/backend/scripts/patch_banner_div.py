with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '<div id="resultCount">'
new = '<div id="intentBanner" style="display:none;margin-bottom:12px;"></div>\n  <div id="resultCount">'

if old in content:
    content = content.replace(old, new, 1)
    with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
else:
    print('실패: resultCount div 찾지 못함')
