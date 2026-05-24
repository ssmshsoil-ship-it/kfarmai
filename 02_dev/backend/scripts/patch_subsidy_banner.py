with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = "subsidy:   {text: \"📋 보조금 정보 기능 준비 중입니다. 지역 농업기술센터에 문의하세요.\", color: \"#1a56a0\", bg: \"#f0f5ff\"},"

new = "subsidy:   {text: \"📋 보조금 정보 수집 중입니다. 아래에서 우리 지역을 선택하면 보조사업 시즌(12~3월)에 알림을 드립니다.\", color: \"#1a56a0\", bg: \"#f0f5ff\"},"

if old in content:
    content = content.replace(old, new, 1)
    with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
else:
    print('실패')
