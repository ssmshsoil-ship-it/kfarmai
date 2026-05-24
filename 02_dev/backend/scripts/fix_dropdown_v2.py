with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. fixed -> absolute 복구
old = '#searchDrop { position:fixed; background:white; border-radius:12px; box-shadow:0 8px 32px rgba(0,0,0,0.15); overflow:hidden; z-index:99999; border:1px solid #f0f0f0; }'
new = '#searchDrop { position:absolute; top:calc(100% + 8px); left:0; right:0; background:white; border-radius:12px; box-shadow:0 8px 32px rgba(0,0,0,0.15); overflow:hidden; z-index:99999; border:1px solid #f0f0f0; }'
if old in content:
    content = content.replace(old, new, 1)
    print('CSS 복구 완료')

# 2. JS 위치계산 코드 제거
old2 = """        const input = document.getElementById('heroSearch');
        const rect = input.getBoundingClientRect();
        box.style.top = (rect.bottom + 8) + 'px';
        box.style.left = rect.left + 'px';
        box.style.width = rect.width + 'px';"""
new2 = ""
if old2 in content:
    content = content.replace(old2, new2, 1)
    print('JS 복구 완료')

# 3. 히어로 섹션 overflow-hidden 제거
old3 = '<section class="bg-[#0F4C43] text-white px-6 py-16 md:py-24 relative overflow-hidden">'
new3 = '<section class="bg-[#0F4C43] text-white px-6 py-16 md:py-24 relative">'
if old3 in content:
    content = content.replace(old3, new3, 1)
    print('섹션 overflow 제거 완료')

# 4. search-wrap z-index 최상위로
old4 = '.search-wrap { position: relative; z-index: 9999; }'
new4 = '.search-wrap { position: relative; z-index: 99999; }'
if old4 in content:
    content = content.replace(old4, new4, 1)
    print('search-wrap z-index 완료')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
