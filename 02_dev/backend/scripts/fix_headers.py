import os
import glob

# 통일된 헤더 HTML
NEW_HEADER = '''<header style="position:sticky;top:0;z-index:50;background:rgba(255,255,255,0.9);backdrop-filter:blur(8px);border-bottom:1px solid #f0f0f0;padding:10px 16px;display:flex;align-items:center;justify-content:space-between;">
  <a href="index.html" style="display:flex;align-items:center;gap:10px;text-decoration:none;">
    <img src="static/logo.png" alt="kFarmAI" style="width:36px;height:36px;border-radius:8px;object-fit:cover;">
    <div style="line-height:1;">
      <div style="font-size:18px;font-weight:900;letter-spacing:-0.5px;"><span style="color:#0F4C43;">kFarm</span><span style="color:#FF6B35;">AI</span></div>
      <div style="font-size:9px;letter-spacing:1.5px;color:#9ca3af;font-weight:600;text-transform:uppercase;margin-top:1px;">Agricultural AI Hub</div>
    </div>
  </a>
  <button style="width:40px;height:40px;border-radius:50%;border:none;background:none;cursor:pointer;font-size:20px;" onclick="openMenu()">☰</button>
</header>'''

# 수정할 HTML 파일 목록
files = glob.glob('02_dev/frontend/*.html')
files = [f for f in files if 'index.html' not in f]

results = []
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<header class="kf-header">' in content:
        old = content[content.find('<header class="kf-header">'):content.find('</header>')+9]
        content = content.replace(old, NEW_HEADER, 1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        results.append(f'수정완료: {os.path.basename(filepath)}')
    else:
        results.append(f'헤더없음: {os.path.basename(filepath)}')

for r in results:
    print(r)
print('전체 완료')
