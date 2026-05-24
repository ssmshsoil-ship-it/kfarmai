with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 히어로 섹션 overflow
old1 = '<section class="bg-[#0F4C43] text-white px-6 py-16 md:py-24 relative">'
new1 = '<section class="bg-[#0F4C43] text-white px-6 py-16 md:py-24 relative overflow-hidden">'
if old1 in content:
    content = content.replace(old1, new1, 1)
    print('overflow 완료')
else:
    print('overflow 실패')

# 2. 쉼표 마침표 제거
old2 = '농자재 정보,<br><span class="text-[#FF6B35]">한 곳에서.</span>'
new2 = '농자재 정보<br><span class="text-[#FF6B35]">한 곳에서</span>'
if old2 in content:
    content = content.replace(old2, new2, 1)
    print('쉼표 마침표 제거 완료')
else:
    print('쉼표 마침표 실패')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
