with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# renderMap 함수에서 mapPanel 먼저 표시 후 relayout
old = '''function renderMap(pestResults) {
  kakao.maps.load(function() {
    const container = document.getElementById('resultMap');
    if (!kakaoMap) {
      kakaoMap = new kakao.maps.Map(container, {'''

new = '''function renderMap(pestResults) {
  kakao.maps.load(function() {
    document.getElementById('mapPanel').style.display = 'block';
    const container = document.getElementById('resultMap');
    if (!kakaoMap) {
      kakaoMap = new kakao.maps.Map(container, {'''

if old in content:
    content = content.replace(old, new, 1)
    print('renderMap 수정 완료')
else:
    print('실패')
    idx = content.find('function renderMap')
    print(repr(content[idx:idx+200]))

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
