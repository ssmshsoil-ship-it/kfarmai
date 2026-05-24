with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# flex 레이아웃 제거하고 단순 구조로 변경
old = '''<div style="display:flex;gap:8px;height:300px;">\n    <div id="resultMap" style="flex:1;height:300px;"></div>\n    <div id="roadviewPanel" style="flex:1;height:300px;display:none;border-radius:8px;overflow:hidden;"></div>\n  </div>'''

new = '''<div id="resultMap" style="width:100%;height:300px;"></div>
  <div id="roadviewPanel" style="width:100%;height:300px;display:none;border-radius:8px;overflow:hidden;margin-top:8px;"></div>'''

if old in content:
    content = content.replace(old, new, 1)
    print('레이아웃 단순화 완료')
else:
    print('실패')
    idx = content.find('resultMap')
    print(repr(content[idx-50:idx+150]))

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
