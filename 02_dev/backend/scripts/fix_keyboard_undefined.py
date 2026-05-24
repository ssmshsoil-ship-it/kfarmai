with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

results = []

# 1. data-name 속성 추가
old1 = 'class="drop-item" onmouseover="this.style.background=\'#f9fafb\'" onmouseout="this.style.background=\'\'" onclick="pickResult(\'${r.name.replace(/\'/g,\"\\\\\'\")}\''
new1 = 'class="drop-item" data-name="${r.name.replace(/"/g,\'&quot;\')}" onmouseover="this.style.background=\'#f9fafb\'" onmouseout="this.style.background=\'\'" onclick="pickResult(\'${r.name.replace(/\'/g,\"\\\\\'\")}\''
if old1 in content:
    content = content.replace(old1, new1, 1)
    results.append('드롭다운 data-name 추가 완료')
else:
    results.append('드롭다운 실패 - 직접 확인 필요')

# 2. 키보드 네비게이션 data-name 방식으로 변경
old2 = "            dropNames = Array.from(items).map(el => el.querySelector('.drop-name') ? el.querySelector('.drop-name').textContent : '');"
new2 = "            dropNames = Array.from(items).map(el => el.getAttribute('data-name') || '');"
if old2 in content:
    content = content.replace(old2, new2, 1)
    results.append('키보드 네비 수정 완료')
else:
    results.append('키보드 네비 실패')

# 3. 모바일 검색버튼 수정
old3 = 'w-full md:w-auto bg-[#FF6B35] hover:bg-[#e05621] text-white font-bold px-7 py-3 rounded-lg md:rounded-full text-sm transition-all'
new3 = 'w-auto bg-[#FF6B35] hover:bg-[#e05621] text-white font-bold px-6 py-2.5 rounded-full text-sm transition-all flex-shrink-0'
if old3 in content:
    content = content.replace(old3, new3, 1)
    results.append('버튼 수정 완료')
else:
    results.append('버튼 실패')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

for r in results:
    print(r)
