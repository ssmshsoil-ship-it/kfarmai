with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 지도에서 보기 버튼 뒤에 로드뷰 버튼 추가
old = 'r-map-link" onclick="focusMarker(${r.lat},${r.lot},\'${r.name.replace(/\'/g,"\\\\\'")}\')">'
# 버튼 전체 찾기
idx = content.find(old)
if idx != -1:
    # 버튼 끝 찾기
    end = content.find('</button>` : \'\'}\n      </div>', idx)
    end += len('</button>')
    
    roadview_btn = ' <button class="r-map-link" onclick="showRoadview(${r.lat},${r.lot})" style="background:#eef4fb;color:#1a5c9e;">\U0001f6b6 로드뷰</button>'
    
    content = content[:end] + roadview_btn + content[end:]
    print('로드뷰 버튼 추가 완료')
else:
    print('버튼 위치 못찾음')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
