with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 검색창 모바일 한줄 고정
old = '''            <div class="bg-white p-2 rounded-xl md:rounded-full shadow-2xl flex flex-col md:flex-row items-center gap-2">
                    <div class="flex-1 flex items-center w-full px-4 py-2 md:py-0">'''

new = '''            <div class="bg-white p-2 rounded-full shadow-2xl flex flex-row items-center gap-2">
                    <div class="flex-1 flex items-center w-full px-4 py-2">'''

if old in content:
    content = content.replace(old, new, 1)
    print('검색창 수정 완료')
else:
    print('검색창 실패')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
