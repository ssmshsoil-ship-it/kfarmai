with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = """let dropIndex = -1;
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
});"""

new = """let dropIndex = -1;
let dropNames = [];
document.getElementById('heroSearch').addEventListener('keydown', function(e) {
  const box = document.getElementById('searchDrop');
  if (!box.classList.contains('open')) return;
  const items = box.querySelectorAll('.drop-item');
  if (!items.length) return;
  dropNames = Array.from(items).map(el => el.querySelector('.drop-name') ? el.querySelector('.drop-name').textContent : '');
  if (e.key === 'ArrowDown') {
    e.preventDefault();
    e.stopPropagation();
    dropIndex = Math.min(dropIndex + 1, items.length - 1);
    items.forEach((el, i) => el.classList.toggle('drop-hover', i === dropIndex));
    if (dropNames[dropIndex]) document.getElementById('heroSearch').value = dropNames[dropIndex];
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    e.stopPropagation();
    dropIndex = Math.max(dropIndex - 1, 0);
    items.forEach((el, i) => el.classList.toggle('drop-hover', i === dropIndex));
    if (dropNames[dropIndex]) document.getElementById('heroSearch').value = dropNames[dropIndex];
  } else if (e.key === 'Enter') {
    e.preventDefault();
    if (dropIndex >= 0 && dropNames[dropIndex]) {
      closeDrop();
      window.location.href = 'search_result.html?q=' + encodeURIComponent(dropNames[dropIndex]) + '&exact=true';
      dropIndex = -1;
    } else {
      goSearch();
    }
  } else if (e.key === 'Escape') {
    closeDrop();
    dropIndex = -1;
  }
});"""

if old in content:
    content = content.replace(old, new, 1)
    with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
else:
    print('실패')
