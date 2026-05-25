with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'infowindow.close());\n    {\n\n    // 기존 마커 제거\n    ma'
new = 'infowindow.close());\n    // 기존 마커 제거\n    ma'

if old in content:
    content = content.replace(old, new, 1)
    print('완료')
else:
    print('실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
