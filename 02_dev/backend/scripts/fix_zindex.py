with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '.search-drop { display:none; position:absolute; top:calc(100% + 8px); left:0; right:0; background:white; border-radius:16px; box-shadow:0 8px 32px rgba(0,0,0,0.18); overflow:hidden; z-index:100; }'
new = '.search-drop { display:none; position:absolute; top:calc(100% + 8px); left:0; right:0; background:white; border-radius:16px; box-shadow:0 8px 32px rgba(0,0,0,0.18); overflow:hidden; z-index:9999; }'

if old in content:
    content = content.replace(old, new, 1)
    with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
else:
    print('실패: 직접 확인 필요')
