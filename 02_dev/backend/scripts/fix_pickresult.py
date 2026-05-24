with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = """function pickResult(name) {
  document.getElementById('heroSearch').value = name;
  closeDrop();
  goSearch();
}"""

new = """function pickResult(name) {
  document.getElementById('heroSearch').value = name;
  closeDrop();
  window.location.href = 'search_result.html?q=' + encodeURIComponent(name) + '&exact=true';
}"""

if old in content:
    content = content.replace(old, new, 1)
    with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
else:
    print('실패')
