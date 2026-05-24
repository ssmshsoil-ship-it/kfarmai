with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''function renderMap(pestResults) {
  kakao.maps.load(function() {
    document.getElementById('mapPanel').style.display = 'block';
    const container = document.getElementById('resultMap');'''

new = '''function renderMap(pestResults) {
  document.getElementById('mapPanel').style.display = 'block';
  const container = document.getElementById('resultMap');
  function doRenderMap() {'''

if old in content:
    content = content.replace(old, new, 1)
    print('renderMap 수정 완료')
else:
    print('실패')

# 닫는 괄호 수정 - kakao.maps.load 콜백 닫는 부분 제거
old2 = '''  }); // kakao.maps.load end
}'''
new2 = '''  } // doRenderMap end
  if (typeof kakao !== 'undefined' && kakao.maps) {
    doRenderMap();
  } else {
    kakao.maps.load(doRenderMap);
  }
}'''

if old2 in content:
    content = content.replace(old2, new2, 1)
    print('load 조건 수정 완료')
else:
    # 다른 방식으로 닫는 부분 찾기
    idx = content.find('function renderMap')
    end = content.find('\nfunction ', idx + 10)
    print('닫는 부분 실패 - 수동 확인 필요')
    print(repr(content[end-100:end+50]))

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
