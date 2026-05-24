with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. hero 섹션 overflow 제거
content = content.replace(
    'overflow:hidden;',
    'overflow:visible;'
)

# 2. 화살표 키 스크롤 방지 + 드롭다운 내부 이동으로 수정
old = '''// 키보드 화살표 + 엔터 지원
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

new = '''// 키보드 화살표 + 엔터 지원
let dropIndex = -1;
document.getElementById('heroSearch').addEventListener('keydown', function(e) {
  const box = document.getElementById('searchDrop');
  if (!box.classList.contains('open')) return;
  const items = box.querySelectorAll('.drop-item');
  if (!items.length) return;
  if (e.key === 'ArrowDown') {
    e.preventDefault();
    e.stopPropagation();
    dropIndex = Math.min(dropIndex + 1, items.length - 1);
    items.forEach((el, i) => el.classList.toggle('drop-hover', i === dropIndex));
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    e.stopPropagation();
    dropIndex = Math.max(dropIndex - 1, 0);
    items.forEach((el, i) => el.classList.toggle('drop-hover', i === dropIndex));
  } else if (e.key === 'Enter') {
    if (dropIndex >= 0) {
      e.preventDefault();
      items[dropIndex].click();
      dropIndex = -1;
    }
  } else if (e.key === 'Escape') {
    closeDrop();
    dropIndex = -1;
  }
});'''

if old in content:
    content = content.replace(old, new, 1)
    with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
else:
    print('실패')
