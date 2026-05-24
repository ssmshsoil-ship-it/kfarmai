with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# renderMap 전체를 새로 교체
old_start = 'function renderMap(pestResults) {\n  document.getElementById(\'mapPanel\').style.display = \'block\';\n  const container = document.getElementById(\'resultMap\');\n  function doRenderMap() {'

# renderMap 함수 끝 찾기
idx = content.find(old_start)
if idx == -1:
    print('시작 못찾음')
    # 원래 형태로 찾기
    idx = content.find('function renderMap(pestResults)')
    print(repr(content[idx:idx+100]))
else:
    end_marker = '\n\n/* ── 특정 마커 포커스 ── */'
    end_idx = content.find(end_marker)
    
    old_func = content[idx:end_idx]
    
    # doRenderMap 내부 추출 (function doRenderMap() { 이후부터 마지막 }); } 전까지)
    inner_start = old_func.find('function doRenderMap() {') + len('function doRenderMap() {')
    inner = old_func[inner_start:]
    # 마지막 });} 제거
    inner = inner.rstrip()
    if inner.endswith('});'):
        inner = inner[:-3]
    elif inner.endswith('});'):
        inner = inner[:-3]
    
    new_func = '''function renderMap(pestResults) {
  document.getElementById('mapPanel').style.display = 'block';
  const container = document.getElementById('resultMap');
  function doRenderMap() {''' + inner + '''
  }
  if (typeof kakao !== 'undefined' && kakao.maps && kakao.maps.Map) {
    doRenderMap();
  } else {
    kakao.maps.load(doRenderMap);
  }
}'''
    
    content = content[:idx] + new_func + content[end_idx:]
    with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
