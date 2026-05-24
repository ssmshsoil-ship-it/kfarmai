with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = "        dropIndex = -1;\n    }\n\n    let dropIndex = -1;"
new = "    }\n\n    let dropIndex = -1;"

if old in content:
    content = content.replace(old, new, 1)
    print('완료')
else:
    print('실패')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
