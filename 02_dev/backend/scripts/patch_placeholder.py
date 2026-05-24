with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '업체명, 지역, 품목 검색...',
    '식물 증상, 작물 고민, 지역 농약사 검색...'
)

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('완료')
