with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 지도에서 보기 버튼 찾기
idx = content.find('지도에서 보기</button>`')
if idx != -1:
    insert_pos = idx + len('지도에서 보기</button>')
    roadview_btn = ' <button class="r-map-link" onclick="showRoadview(${r.lat},${r.lot})" style="background:#eef4fb;color:#1a5c9e;">\U0001f6b6 로드뷰</button>'
    content = content[:insert_pos] + roadview_btn + content[insert_pos:]
    print('로드뷰 버튼 추가 완료')
else:
    print('실패 - 버튼 위치 못찾음')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
