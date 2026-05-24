with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '<div class="result-header">\n  <span id="resultCount">검색 중...</span>\n</div>'
new = '<div id="intentBanner" style="display:none;margin-bottom:12px;"></div>\n<div class="result-header">\n  <span id="resultCount">검색 중...</span>\n</div>'

if old in content:
    content = content.replace(old, new, 1)
    with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
else:
    print('실패')
