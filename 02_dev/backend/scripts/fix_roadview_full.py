with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

results = []

# 1. resultMap CSS 높이 고정
old1 = '#resultMap { width:100%;height:300px; }'
new1 = '#resultMap { width:100%;height:300px;min-height:300px; }\n#roadviewPanel { width:100%;height:300px;min-height:300px; }'
if old1 in content:
    content = content.replace(old1, new1, 1)
    results.append('지도 CSS 수정 완료')
else:
    results.append('지도 CSS 실패')

# 2. 지도+로드뷰 flex 레이아웃 높이 고정
old2 = '<div style="display:flex;gap:8px;">\n    <div id="resultMap" style="flex:1;min-height:220px;"></div>\n    <div id="roadviewPanel" style="flex:1;min-height:220px;display:none;border-radius:8px;overflow:hidden;"></div>\n  </div>'
new2 = '<div style="display:flex;gap:8px;height:300px;">\n    <div id="resultMap" style="flex:1;height:300px;"></div>\n    <div id="roadviewPanel" style="flex:1;height:300px;display:none;border-radius:8px;overflow:hidden;"></div>\n  </div>'
if old2 in content:
    content = content.replace(old2, new2, 1)
    results.append('레이아웃 높이 수정 완료')
else:
    results.append('레이아웃 높이 실패')

# 3. 로드뷰 버튼을 지도에서 보기 버튼 옆으로 이동
# 로드뷰 버튼을 헤더에서 제거하고 카드 내 버튼 옆에 추가
old3 = '''    <button id="roadviewToggleBtn" onclick="toggleRoadview()" style="font-size:12px;padding:4px 10px;background:#1e6b2e;color:white;border:none;border-radius:6px;cursor:pointer;display:none;">🚶 로드뷰 보기</button>'''
new3 = ''
if old3 in content:
    content = content.replace(old3, new3, 1)
    results.append('헤더 버튼 제거 완료')

# 4. hasMap 버튼에 로드뷰 버튼 추가
old4 = "hasMap ? `<button class=\"r-map-link\" onclick=\"focusMarker(${r.lat},${r.lot},'${r.name.replace(/'/g,\"\\\\'\")}')\">\U0001f4cd 지도에서 보기</button>` : ''}"
new4 = "hasMap ? `<button class=\"r-map-link\" onclick=\"focusMarker(${r.lat},${r.lot},'${r.name.replace(/'/g,\"\\\\'\")}')\">\U0001f4cd 지도에서 보기</button><button class=\"r-map-link\" onclick=\"focusMarker(${r.lat},${r.lot},'${r.name.replace(/'/g,\"\\\\'\")}');toggleRoadview();\" style=\"background:#eef4fb;color:#1a5c9e;margin-left:6px;\">\U0001f6b6 로드뷰</button>` : ''}"
if old4 in content:
    content = content.replace(old4, new4, 1)
    results.append('로드뷰 버튼 카드 추가 완료')
else:
    results.append('로드뷰 버튼 카드 실패')

# 5. focusMarker에서 로드뷰 버튼 display 제거 (더 이상 필요 없음)
old5 = "  const btn = document.getElementById('roadviewToggleBtn');\n  if (btn) btn.style.display = 'inline-block';\n  if (!kakaoMap) return;"
new5 = "  if (!kakaoMap) return;"
if old5 in content:
    content = content.replace(old5, new5, 1)
    results.append('focusMarker 정리 완료')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)

for r in results:
    print(r)
