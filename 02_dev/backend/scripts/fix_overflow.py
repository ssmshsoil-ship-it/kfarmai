with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# overflow-x 방지 추가
old = '<body class="bg-[#F8F9FA] text-[#1A1D20] antialiased tracking-tight pb-20 md:pb-0">'
new = '<body class="bg-[#F8F9FA] text-[#1A1D20] antialiased tracking-tight pb-20 md:pb-0 overflow-x-hidden">'

if old in content:
    content = content.replace(old, new, 1)
    print('overflow 수정 완료')
else:
    print('실패')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
