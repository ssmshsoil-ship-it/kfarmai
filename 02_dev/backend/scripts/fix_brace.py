with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 불필요한 중괄호 제거
idx = content.find("infowindow.close());\n    {\n    // 기존 마커")
if idx != -1:
    content = content[:idx] + "infowindow.close());\n    // 기존 마커" + content[idx + len("infowindow.close());\n    {\n    // 기존 마커"):]
    print('완료')
else:
    # 다른 형태 찾기
    idx2 = content.find("infowindow.close());\n    {")
    if idx2 != -1:
        print(repr(content[idx2:idx2+50]))
    else:
        print('실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
