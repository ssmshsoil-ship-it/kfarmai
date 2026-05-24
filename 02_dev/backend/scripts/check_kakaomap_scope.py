with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('kakaoMap')
print(repr(content[idx-20:idx+50]))
