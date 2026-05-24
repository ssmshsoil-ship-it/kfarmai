with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. intentBanner div 추가 (결과 카운트 위에)
old_count = '<div id="resultCount">'
new_count = '<div id="intentBanner" style="display:none;margin-bottom:12px;"></div>\n  <div id="resultCount">'
content = content.replace(old_count, new_count, 1)

# 2. intent 처리 코드 추가
old_render = '    allResults = [...shops, ...companies];\n    renderResults();'
new_render = '''    const intent = data.intent || "directory";
    const bannerEl = document.getElementById("intentBanner");
    if (bannerEl) {
      const map = {
        diagnosis: {text: "🌿 AI 진단 기능 준비 중입니다. 아래 관련 농약사를 참고하세요.", color: "#1e6b2e", bg: "#f0faf2"},
        subsidy:   {text: "📋 보조금 정보 기능 준비 중입니다. 지역 농업기술센터에 문의하세요.", color: "#1a56a0", bg: "#f0f5ff"},
        event:     {text: "🎪 행사 정보 기능 준비 중입니다.", color: "#7c3aed", bg: "#f5f0ff"},
        directory: {text: "", color: "", bg: ""}
      };
      const info = map[intent] || map["directory"];
      if (info.text) {
        bannerEl.style.cssText = "display:block;background:" + info.bg + ";border-left:4px solid " + info.color + ";padding:12px 16px;margin-bottom:16px;border-radius:8px;color:" + info.color + ";font-weight:500;";
        bannerEl.textContent = info.text;
      } else {
        bannerEl.style.display = "none";
      }
    }
    allResults = [...shops, ...companies];
    renderResults();'''

content = content.replace(old_render, new_render, 1)

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('완료')
