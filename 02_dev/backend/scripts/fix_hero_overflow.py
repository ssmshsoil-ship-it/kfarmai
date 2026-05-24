with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '<section class="bg-[#0F4C43] text-white px-6 py-16 md:py-24 relative">'
new = '<section class="bg-[#0F4C43] text-white px-6 py-16 md:py-24 relative overflow-hidden">'

if old in content:
    content = content.replace(old, new, 1)
    print('완료')
else:
    print('실패')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
