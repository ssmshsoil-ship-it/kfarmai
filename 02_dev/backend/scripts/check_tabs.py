with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
# 탭 텍스트 확인
idx = content.find('tab-btn')
print(content[idx:idx+200])
