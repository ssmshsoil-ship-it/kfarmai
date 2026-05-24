with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# renderResults에서 회사도 지도에 표시
old = '''  const pestResults = filtered.filter(r => r.catKey === 'map' && r.lat && r.lot);
  const mapPanel = document.getElementById('mapPanel');
  if (pestResults.length) {
    mapPanel.style.display = 'block';
    renderMap(pestResults);
  } else {
    mapPanel.style.display = 'none';
  }'''

new = '''  const mapResults = filtered.filter(r => r.lat && r.lot);
  const mapPanel = document.getElementById('mapPanel');
  if (mapResults.length) {
    mapPanel.style.display = 'block';
    renderMap(mapResults);
  } else {
    mapPanel.style.display = 'none';
  }'''

if old in content:
    content = content.replace(old, new, 1)
    print('지도 조건 수정 완료')
else:
    print('실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
