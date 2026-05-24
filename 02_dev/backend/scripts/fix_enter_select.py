with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = """            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (dropIndex >= 0 && dropNames[dropIndex]) {
                    closeDrop();
                    window.location.href = 'search_result.html?q=' + encodeURIComponent(dropNames[dropIndex]) + '&exact=true';
                } else { goSearch(); }"""

new = """            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (dropIndex >= 0 && dropNames[dropIndex]) {
                    const selectedName = dropNames[dropIndex];
                    closeDrop();
                    window.location.href = 'search_result.html?q=' + encodeURIComponent(selectedName) + '&exact=true';
                } else { goSearch(); }"""

if old in content:
    content = content.replace(old, new, 1)
    print('완료')
else:
    print('실패')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
