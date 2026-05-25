with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = "'<div style=\"padding:11px 12px;font-size:13px;min-width:220px;max-width:300px;line-height:1.75;\">'"
new = "'<div style=\"padding:11px 12px;font-size:13px;min-width:220px;max-width:260px;line-height:1.75;word-break:keep-all;overflow-wrap:break-word;\">'"

if old in content:
    content = content.replace(old, new, 1)
    print('완료')
else:
    print('실패')

with open('02_dev/frontend/map.html', 'w', encoding='utf-8') as f:
    f.write(content)
