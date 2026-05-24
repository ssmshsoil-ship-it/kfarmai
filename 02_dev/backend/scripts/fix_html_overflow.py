with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '<html lang="ko" class="scroll-smooth">'
new = '<html lang="ko" class="scroll-smooth overflow-x-hidden">'

if old in content:
    content = content.replace(old, new, 1)
    print('html 태그 수정 완료')
else:
    print('실패')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
