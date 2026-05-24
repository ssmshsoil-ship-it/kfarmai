with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 드롭다운을 fixed position으로 변경
old = '#searchDrop { position:absolute; top:calc(100% + 8px); left:0; right:0; background:white; border-radius:12px; box-shadow:0 8px 32px rgba(0,0,0,0.15); overflow:hidden; z-index:9999; border:1px solid #f0f0f0; }'
new = '#searchDrop { position:fixed; background:white; border-radius:12px; box-shadow:0 8px 32px rgba(0,0,0,0.15); overflow:hidden; z-index:99999; border:1px solid #f0f0f0; }'

if old in content:
    content = content.replace(old, new, 1)
    print('CSS 수정 완료')
else:
    print('CSS 실패')

# JS에서 드롭다운 위치를 동적으로 계산
old_renderdrop = 'function renderDrop(res, q) {\n        const box = document.getElementById(\'searchDrop\');\n        if (!res.length) {'
new_renderdrop = '''function renderDrop(res, q) {
        const box = document.getElementById('searchDrop');
        const input = document.getElementById('heroSearch');
        const rect = input.getBoundingClientRect();
        box.style.top = (rect.bottom + 8) + 'px';
        box.style.left = rect.left + 'px';
        box.style.width = rect.width + 'px';
        if (!res.length) {'''

if old_renderdrop in content:
    content = content.replace(old_renderdrop, new_renderdrop, 1)
    print('JS 수정 완료')
else:
    print('JS 실패')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
