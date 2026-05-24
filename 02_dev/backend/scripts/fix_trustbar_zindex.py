with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'trust-bar { background:#0a3d18; padding:12px 6px; display:flex; justify-content:space-around; }'
new = 'trust-bar { background:#0a3d18; padding:12px 6px; display:flex; justify-content:space-around; position:relative; z-index:1; }'

if old in content:
    content = content.replace(old, new, 1)
    with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
else:
    print('실패')
