with open('H:/내 드라이브/kfarmai-web/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('kakaoMap = new kakao.maps.Map')
print(repr(content[idx-20:idx+200]))
