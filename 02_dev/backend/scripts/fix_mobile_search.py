with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. search-utils.js 로드 추가
old1 = '<script src="static/pesticide_data.js"></script>'
new1 = '<script src="static/search-utils.js"></script>\n    <script src="static/pesticide_data.js"></script>'
if old1 in content:
    content = content.replace(old1, new1, 1)
    print('search-utils.js 연결 완료')

# 2. search 함수를 smartSearch로 교체
old2 = "function search(q) {\n        if (!q || q.length < 1) return [];\n        return DB.filter(d => d.name.includes(q) || (d.addr && d.addr.includes(q)) || d.cat.includes(q));\n    }"
new2 = "function search(q) {\n        if (!q || q.length < 1) return [];\n        return smartSearch(q, DB);\n    }"
if old2 in content:
    content = content.replace(old2, new2, 1)
    print('search 함수 교체 완료')

# 3. 모바일 검색버튼 크기 축소
old3 = 'w-auto bg-[#FF6B35] hover:bg-[#e05621] text-white font-bold px-6 py-2.5 rounded-full text-sm transition-all flex-shrink-0'
new3 = 'w-auto bg-[#FF6B35] hover:bg-[#e05621] text-white font-bold px-4 py-2 rounded-full text-xs md:text-sm md:px-6 md:py-2.5 transition-all flex-shrink-0'
if old3 in content:
    content = content.replace(old3, new3, 1)
    print('검색버튼 크기 수정 완료')

# 4. 스크롤 검색바 잘림 수정
old4 = 'id="scrollSearchBar" style="display:none;position:fixed;top:0;left:0;right:0;z-index:99999;background:white;border-bottom:1px solid #e5e7eb;padding:8px 16px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">'
new4 = 'id="scrollSearchBar" style="display:none;position:fixed;top:0;left:0;right:0;z-index:99999;background:white;border-bottom:1px solid #e5e7eb;padding:6px 12px;box-shadow:0 2px 8px rgba(0,0,0,0.1);box-sizing:border-box;">'
if old4 in content:
    content = content.replace(old4, new4, 1)
    print('스크롤바 수정 완료')

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
