with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 메인 히어로 텍스트 교체
old = '''            <h1 class="text-3xl md:text-5xl font-black leading-tight tracking-tighter mb-4">
                농자재 정보,<br class="md:hidden"> <span class="text-[#FF6B35]">한 곳에서</span> 정밀하게.
            </h1>
            <p class="text-sm md:text-base text-gray-200/80 max-w-lg mx-auto mb-10 font-medium">
                농약사·상토·종자·비료·작물보호제 등 공공데이터와 연동된 전국 인프라 정보를 실시간 초고속 검색하세요.
            </p>'''

new = '''            <h1 class="text-4xl md:text-6xl font-black leading-tight tracking-tighter mb-6">
                농자재 정보,<br><span class="text-[#FF6B35]">한 곳에서.</span>
            </h1>
            <p class="text-sm md:text-base text-gray-200/80 max-w-lg mx-auto mb-10 font-medium">
                전국 농약사 · 상토 · 종자 · 비료 · 작물보호제
            </p>'''

if old in content:
    content = content.replace(old, new, 1)
    print('메인 텍스트 수정 완료')
else:
    print('실패 - 직접 확인 필요')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
