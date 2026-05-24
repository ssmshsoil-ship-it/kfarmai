with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'data-name=""'
new = 'data-name=""'

if old in content:
    content = content.replace(old, new, 1)
    print('data-name 수정 완료')
else:
    print('실패')

# 뒤로가기 시 검색창 초기화
old2 = 'window.addEventListener(\'DOMContentLoaded\', buildDB);'
new2 = """window.addEventListener('DOMContentLoaded', buildDB);
window.addEventListener('pageshow', function(e) {
    if (e.persisted) {
        document.getElementById('heroSearch').value = '';
        closeDrop();
    }
});"""

if old2 in content:
    content = content.replace(old2, new2, 1)
    print('뒤로가기 초기화 완료')
else:
    print('뒤로가기 실패')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
