with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('function renderMap')
end = content.find('/* ── 특정 마커 포커스 ── */')
print(content[idx:end])
