with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = "pestResults = filtered.filter(r => r.catKey === 'map' && r.lat && r.lot);"
new = "pestResults = filtered.filter(r => r.lat && r.lot);"

if old in content:
    content = content.replace(old, new, 1)
    print('완료')
else:
    print('실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
