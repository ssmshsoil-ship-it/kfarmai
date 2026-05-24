import glob

META_CACHE = '<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n    <meta http-equiv="Pragma" content="no-cache">\n    <meta http-equiv="Expires" content="0">'

files = glob.glob('02_dev/frontend/*.html')
for f in files:
    content = open(f, encoding='utf-8').read()
    if 'Cache-Control' not in content:
        content = content.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n    ' + META_CACHE, 1)
        open(f, 'w', encoding='utf-8').write(content)
        print(f.split('\\')[-1], '완료')
    else:
        print(f.split('\\')[-1], '이미 있음')
