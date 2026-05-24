import glob

NEW_HEADER = '<header style="position:sticky;top:0;z-index:50;background:rgba(255,255,255,0.9);backdrop-filter:blur(8px);border-bottom:1px solid #f0f0f0;padding:10px 16px;display:flex;align-items:center;justify-content:space-between;">\n  <a href="index.html" style="display:flex;align-items:center;gap:10px;text-decoration:none;">\n    <img src="static/logo.png" alt="kFarmAI" style="width:36px;height:36px;border-radius:8px;object-fit:cover;">\n    <div style="line-height:1;">\n      <div style="font-size:18px;font-weight:900;letter-spacing:-0.5px;"><span style="color:#0F4C43;">kFarm</span><span style="color:#FF6B35;">AI</span></div>\n      <div style="font-size:9px;letter-spacing:1.5px;color:#9ca3af;font-weight:600;text-transform:uppercase;margin-top:1px;">Agricultural AI Hub</div>\n    </div>\n  </a>\n  <button style="width:40px;height:40px;border-radius:50%;border:none;background:none;cursor:pointer;font-size:20px;" onclick="openMenu()">&#9776;</button>\n</header>'

results = []

# 1. map.html 헤더 교체
with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()
start = content.find('<header>')
end = content.find('</header>') + 9
if start != -1:
    content = content[:start] + NEW_HEADER + content[end:]
    with open('02_dev/frontend/map.html', 'w', encoding='utf-8') as f:
        f.write(content)
    results.append('map.html 완료')

# 2. search_result.html 헤더 교체
with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
start = content.find('<header')
end = content.find('</header>') + 9
if start != -1 and 'logo.png' not in content[start:end]:
    content = content[:start] + NEW_HEADER + content[end:]
    with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
        f.write(content)
    results.append('search_result.html 완료')
else:
    results.append('search_result.html 이미 최신')

# 3. index.html 검색창 모바일 한줄 고정
with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
old = 'flex flex-col md:flex-row items-center gap-2'
new = 'flex flex-row items-center gap-2'
if old in content:
    content = content.replace(old, new, 1)
    results.append('검색창 한줄 완료')
with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

for r in results:
    print(r)
print('전체 완료')
