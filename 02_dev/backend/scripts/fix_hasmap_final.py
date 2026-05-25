with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. hasMap 조건 수정 (모든 lat/lng 있는 항목)
old1 = "hasMap = r.catKey === 'map' && r.lat && r.lot;"
new1 = "hasMap = r.lat && r.lot;"
if old1 in content:
    content = content.replace(old1, new1, 1)
    print('hasMap 수정 완료')
else:
    print('hasMap 실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
