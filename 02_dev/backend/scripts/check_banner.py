with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('intentBanner')
print('JS 코드:', idx != -1)

idx2 = content.find('<div id="intentBanner"')
print('HTML div:', idx2 != -1)
if idx2 != -1:
    print(content[idx2:idx2+80])
