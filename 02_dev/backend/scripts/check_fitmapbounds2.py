with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()
# 모든 fitMapToBounds 호출 위치 찾기
import re
for m in re.finditer(r'fitMapToBounds\([^)]+\)', content):
    print(repr(content[m.start()-20:m.end()+50]))
    print('---')
