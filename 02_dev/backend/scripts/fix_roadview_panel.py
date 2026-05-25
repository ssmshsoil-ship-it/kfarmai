with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '<div id="resultMap"></div>\n</div>'
new = '<div id="resultMap"></div>\n  <div id="roadviewPanel" style="width:100%;height:300px;display:none;border-radius:8px;overflow:hidden;margin-top:8px;"></div>\n</div>'

if old in content:
    content = content.replace(old, new, 1)
    print('완료')
else:
    print('실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
