with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'dapi.kakao.com/v2/maps/sdk.js?appkey=533e5896630c1460c4349d33b3fab95a&autoload=false&libraries=services,roadview">'
new = 'dapi.kakao.com/v2/maps/sdk.js?appkey=533e5896630c1460c4349d33b3fab95a&autoload=false&libraries=services">'

if old in content:
    content = content.replace(old, new, 1)
    print('완료')
else:
    print('실패')
    import re
    sdk = re.findall(r'dapi\.kakao.*?(?:">)', content)
    print('현재 SDK:', sdk)

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
