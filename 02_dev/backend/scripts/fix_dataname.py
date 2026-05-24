with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# data-name 단순화
old = 'data-name="${r.name.replace(/"/g,\'&quot;\')}"'
new = 'data-name="${r.name}"'

if old in content:
    content = content.replace(old, new, 1)
    print('data-name 수정 완료')
else:
    # 혹시 다른 형태로 저장되어 있을 수 있으므로 강제 교체
    import re
    content, n = re.subn(r'data-name="\$\{r\.name[^"]*\}"', 'data-name="${r.name}"', content)
    if n:
        print(f'regex로 data-name 수정 완료 ({n}건)')
    else:
        print('실패')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
