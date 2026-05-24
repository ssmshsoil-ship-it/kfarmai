with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
count = 0

# fitMapToBounds(list) 호출 후 applyClusterer() 추가 (함수 정의 제외)
def add_clusterer(m):
    global count
    full = m.group(0)
    if 'function fitMapToBounds' in content[max(0,m.start()-5):m.start()+30]:
        return full
    count += 1
    return full + '\n            applyClusterer();'

# moveMap 조건이 있는 호출들 처리
old1 = 'if (moveMap) fitMapToBounds(list);\n                return;'
new1 = 'if (moveMap) fitMapToBounds(list);\n                applyClusterer();\n                return;'
if old1 in content:
    content = content.replace(old1, new1, 1)
    print('호출1 완료')

old2 = 'pending && moveMap) fitMapToBounds(list);\n                });\n            });'
new2 = 'pending && moveMap) fitMapToBounds(list);\n                applyClusterer();\n                });\n            });'
if old2 in content:
    content = content.replace(old2, new2, 1)
    print('호출2 완료')

old3 = 'if (moveMap) fitMapToBounds(list);\n        }\n\n        function getFilteredItems'
new3 = 'if (moveMap) fitMapToBounds(list);\n            applyClusterer();\n        }\n\n        function getFilteredItems'
if old3 in content:
    content = content.replace(old3, new3, 1)
    print('호출3 완료')

with open('02_dev/frontend/map.html', 'w', encoding='utf-8') as f:
    f.write(content)
