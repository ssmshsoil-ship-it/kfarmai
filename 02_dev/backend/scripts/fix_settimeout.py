with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''function renderMap(pestResults) {
  document.getElementById('mapPanel').style.display = 'block';
  kakao.maps.load(function() {'''

new = '''function renderMap(pestResults) {
  document.getElementById('mapPanel').style.display = 'block';
  setTimeout(function() {'''

if old in content:
    content = content.replace(old, new, 1)
    print('setTimeout 수정 완료')
else:
    print('실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
