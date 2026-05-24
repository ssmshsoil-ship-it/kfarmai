with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 로고 jpg -> png 교체
content = content.replace('static/logo.jpg', 'static/logo.png')

# 2. 메뉴 z-index 수정 (검색창보다 위로)
content = content.replace(
    'class="fixed top-0 bottom-0 right-[-320px] w-[300px] bg-white z-50 shadow-2xl transition-all duration-300 overflow-y-auto"',
    'class="fixed top-0 bottom-0 right-[-320px] w-[300px] bg-white z-[99999] shadow-2xl transition-all duration-300 overflow-y-auto"'
)
content = content.replace(
    'class="fixed inset-0 bg-black/50 z-50 hidden"',
    'class="fixed inset-0 bg-black/50 z-[99998] hidden"'
)

# 3. 농약사 지도 메뉴 항목 수정
content = content.replace(
    '<a href="map.html" class="block p-3 rounded-lg hover:bg-gray-50">📍 농약사 지도</a>',
    '<a href="map.html" class="block p-3 rounded-lg hover:bg-gray-50">&#128205; 농약사 지도</a>'
)

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('완료')
