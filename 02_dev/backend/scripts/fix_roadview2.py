with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'mapPanel" style="display:none;">\n  <div class="map-panel-title">\U0001f4cd 지도에서 위치 확인</div>\n  <div id="resultMap"></div>\n</div>'

new = '''mapPanel" style="display:none;">
  <div class="map-panel-title" style="display:flex;justify-content:space-between;align-items:center;">
    <span>📍 지도에서 위치 확인</span>
    <button id="roadviewToggleBtn" onclick="toggleRoadview()" style="font-size:12px;padding:4px 10px;background:#1e6b2e;color:white;border:none;border-radius:6px;cursor:pointer;display:none;">🚶 로드뷰 보기</button>
  </div>
  <div style="display:flex;gap:8px;">
    <div id="resultMap" style="flex:1;min-height:220px;"></div>
    <div id="roadviewPanel" style="flex:1;min-height:220px;display:none;border-radius:8px;overflow:hidden;"></div>
  </div>
</div>'''

if old in content:
    content = content.replace(old, new, 1)
    print('완료')
else:
    # 이모지 없이 시도
    old2 = 'mapPanel" style="display:none;">\n  <div class="map-panel-title">'
    idx = content.find(old2)
    if idx != -1:
        end = content.find('</div>\n</div>', idx)
        end += len('</div>\n</div>')
        content = content[:idx] + new + content[end:]
        print('대체 방식 완료')
    else:
        print('실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
