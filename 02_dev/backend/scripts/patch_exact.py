with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'function getQuery() {'
new = '''function getExact() {
  const p = new URLSearchParams(window.location.search);
  return p.get('exact') === 'true';
}

function getQuery() {'''

if old in content:
    content = content.replace(old, new, 1)
    with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
else:
    print('실패')
