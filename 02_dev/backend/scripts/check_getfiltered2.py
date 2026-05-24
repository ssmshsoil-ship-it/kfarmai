with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('getFilteredItems')
# 함수 전체 찾기
end = content.find('\n        function ', idx+10)
print(content[idx:end])
