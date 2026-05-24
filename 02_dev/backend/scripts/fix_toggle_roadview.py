with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''function toggleRoadview() {
  const panel = document.getElementById('roadviewPanel');
  const btn = document.getElementById('roadviewToggleBtn');
  const mapEl = document.getElementById('resultMap');
  if (panel.style.display === 'none') {
    panel.style.display = 'block';
    mapEl.style.flex = '1';
    btn.textContent = '🗺️ 지도만 보기';
    if (currentLat && currentLng) {
      showRoadview(currentLat, currentLng);
    }
  } else {
    panel.style.display = 'none';
    btn.textContent = '🚶 로드뷰 보기';
  }
}'''

new = '''function toggleRoadview() {
  const panel = document.getElementById('roadviewPanel');
  const mapEl = document.getElementById('resultMap');
  if (!panel) return;
  if (panel.style.display === 'none') {
    panel.style.display = 'block';
    mapEl.style.flex = '1';
    if (currentLat && currentLng) {
      showRoadview(currentLat, currentLng);
    }
  } else {
    panel.style.display = 'none';
  }
}'''

if old in content:
    content = content.replace(old, new, 1)
    print('toggleRoadview 수정 완료')
else:
    print('실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
