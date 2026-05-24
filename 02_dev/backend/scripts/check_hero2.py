with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
# 히어로 섹션 찾기
idx = content.find('농자재 정보')
print(repr(content[idx-50:idx+300]))
