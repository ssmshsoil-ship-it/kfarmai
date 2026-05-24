import glob
for f in glob.glob('02_dev/frontend/*.html'):
    content = open(f, encoding='utf-8').read()
    name = f.split('\\')[-1]
    if 'index.html' in f:
        continue
    if 'logo.png' in content:
        print(name, ': 최신 (logo.png 있음)')
    elif 'kf-logo' in content:
        print(name, ': 구버전 (kf-logo)')
    else:
        print(name, ': 확인필요')
