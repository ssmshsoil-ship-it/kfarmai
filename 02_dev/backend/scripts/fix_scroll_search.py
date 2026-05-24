with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 헤더에 검색바 추가 + 스크롤 감지 JS
old_header = '</header>'
new_header = '''</header>
<!-- 스크롤 검색바 -->
<div id="scrollSearchBar" style="display:none;position:fixed;top:0;left:0;right:0;z-index:99999;background:white;border-bottom:1px solid #e5e7eb;padding:8px 16px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
  <div style="max-width:800px;margin:0 auto;display:flex;align-items:center;gap:12px;">
    <a href="index.html" style="display:flex;align-items:center;gap:8px;text-decoration:none;flex-shrink:0;">
      <img src="static/logo.png" style="width:28px;height:28px;border-radius:6px;object-fit:cover;">
      <span style="font-size:15px;font-weight:900;"><span style="color:#0F4C43;">kFarm</span><span style="color:#FF6B35;">AI</span></span>
    </a>
    <div style="flex:1;display:flex;align-items:center;background:#f3f4f6;border-radius:30px;padding:6px 16px;gap:8px;">
      <span style="color:#9ca3af;">🔍</span>
      <input id="scrollSearch" type="text" placeholder="식물 증상, 작물 고민, 지역 농약사 검색..."
        style="flex:1;border:none;background:none;outline:none;font-size:13px;font-weight:500;"
        oninput="document.getElementById('heroSearch').value=this.value;onInput(this.value)"
        onkeydown="if(event.key==='Enter'){document.getElementById('heroSearch').value=this.value;goSearch();}">
    </div>
    <button onclick="document.getElementById('heroSearch').value=document.getElementById('scrollSearch').value;goSearch();"
      style="background:#FF6B35;color:white;border:none;border-radius:30px;padding:7px 18px;font-size:13px;font-weight:700;cursor:pointer;flex-shrink:0;">검색</button>
  </div>
</div>'''

content = content.replace(old_header, new_header, 1)

# 스크롤 감지 JS 추가
old_body = '</body>'
new_body = '''<script>
(function() {
  var heroSearch = document.querySelector('.search-wrap');
  var scrollBar = document.getElementById('scrollSearchBar');
  if (!heroSearch || !scrollBar) return;
  window.addEventListener('scroll', function() {
    var rect = heroSearch.getBoundingClientRect();
    if (rect.bottom < 0) {
      scrollBar.style.display = 'block';
    } else {
      scrollBar.style.display = 'none';
      document.getElementById('scrollSearch').value = '';
    }
  });
})();
</script>
</body>'''

content = content.replace(old_body, new_body, 1)

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('완료')
