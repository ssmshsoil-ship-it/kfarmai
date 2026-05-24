with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 잘못된 subsidy UI 코드 제거 후 깔끔하게 재작성
old = """      bannerEl.textContent = info.text;
      if (intent === 'subsidy') {
        const form = document.createElement('div');
        form.style.cssText = 'margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;';
        form.innerHTML = '<select id="sidoSelect" style="padding:6px 10px;border:1px solid #1a56a0;border-radius:6px;font-size:13px;"><option value="">시/도 선택</option><option>서울특별시</option><option>경기도</option><option>강원도</option><option>충청북도</option><option>충청남도</option><option>전라북도</option><option>전라남도</option><option>경상북도</option><option>경상남도</option><option>제주특별자치도</option><option>부산광역시</option><option>대구광역시</option><option>인천광역시</option><option>광주광역시</option><option>대전광역시</option><option>울산광역시</option><option>세종특별자치시</option></select><button onclick="alert(document.getElementById(\'sidoSelect\').value ? document.getElementById(\'sidoSelect\').value + \' 보조사업 시즌 알림을 등록했습니다.' : '지역을 선택해주세요.')" style="padding:6px 14px;background:#1a56a0;color:white;border:none;border-radius:6px;font-size:13px;cursor:pointer;">알림 신청</button>';
        bannerEl.appendChild(form);
      }"""

new = "      bannerEl.textContent = info.text;"

if old in content:
    content = content.replace(old, new, 1)
    with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
else:
    print('실패')
