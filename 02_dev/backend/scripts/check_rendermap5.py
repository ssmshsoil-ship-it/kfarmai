with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('function renderMap')
end = content.find('\n/* ── 특정 마커', idx)
print(content[idx:end])
