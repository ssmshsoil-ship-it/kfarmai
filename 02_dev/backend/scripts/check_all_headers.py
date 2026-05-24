import glob
for f in glob.glob('02_dev/frontend/*.html'):
    content = open(f, encoding='utf-8').read()
    idx = content.find('<header')
    if idx != -1:
        print(f.split('/')[-1], ':', repr(content[idx:idx+80]))
