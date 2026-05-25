with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
print('한글 확인:', '농약사' in content)
print('지도에서 보기:', '지도에서 보기' in content)
