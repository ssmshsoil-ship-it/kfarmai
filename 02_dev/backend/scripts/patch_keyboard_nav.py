with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'function closeDrop() { document.getElementById(\'searchDrop\').classList.remove(\'open\'); }'

new = '''function closeDrop() { document.getElementById('searchDrop').classList.remove('open'); }

// 키보드 화살표 + 엔터 지원
let dropIndex = -1;
document.addEventListener('keydown', function(e) {
  const box = document.getElementById('searchDrop');
  if (!box.classList.contains('open')) return;
  const items = box.querySelectorAll('.drop-item');
  if (!items.length) return;
  if (e.key === 'ArrowDown') {
    e.preventDefault();
    dropIndex = Math.min(dropIndex + 1, items.length - 1);
    items.forEach((el, i) => el.classList.toggle('drop-hover', i === dropIndex));
    items[dropIndex].scrollIntoView({block:'nearest'});
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    dropIndex = Math.max(dropIndex - 1, 0);
    items.forEach((el, i) => el.classList.toggle('drop-hover', i === dropIndex));
    items[dropIndex].scrollIntoView({block:'nearest'});
  } else if (e.key === 'Enter' && dropIndex >= 0) {
    e.preventDefault();
    items[dropIndex].click();
    dropIndex = -1;
  } else if (e.key === 'Escape') {
    closeDrop();
    dropIndex = -1;
  }
});'''

if old in content:
    content = content.replace(old, new, 1)
    # hover 스타일 추가
    content = content.replace(
        '.drop-item:hover {',
        '.drop-hover { background:#f0f7f2 !important; }\n.drop-item:hover {'
    )
    with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
else:
    print('실패')
