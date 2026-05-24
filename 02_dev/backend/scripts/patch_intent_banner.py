with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''doSearch(q) {
  if (!q) return [];
  fetch("http://127.0.0.1:5000/api/search", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({keyword: q})
  })
  .then(r => r.json())
  .then(data => {
    const shops = (data.shops || []).map(d => ({
      name: d.name, addr: d.address, cat: "농약사",
      lat: d.lat, lot: d.lng, tel: d.phone
    }));
    const companies = (data.companies || []).map(d => ({
      name: d.name, addr: d.address, cat: d.category,
      website: d.website
    }));
    allResults = [...shops, ...companies];
    renderResults();
  })
  .catch(e => console.error("API 오류:", e));
  return [];
}'''

new = '''doSearch(q) {
  if (!q) return [];
  fetch("https://kfarmai.onrender.com/api/search", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({keyword: q})
  })
  .then(r => r.json())
  .then(data => {
    const intent = data.intent || "directory";
    showIntentBanner(intent, q);
    const shops = (data.shops || []).map(d => ({
      name: d.name, addr: d.address, cat: "농약사",
      lat: d.lat, lot: d.lng, tel: d.phone
    }));
    const companies = (data.companies || []).map(d => ({
      name: d.name, addr: d.address, cat: d.category,
      website: d.website
    }));
    allResults = [...shops, ...companies];
    renderResults();
  })
  .catch(e => console.error("API 오류:", e));
  return [];
}

function showIntentBanner(intent, q) {
  const bannerEl = document.getElementById("intentBanner");
  if (!bannerEl) return;
  const map = {
    diagnosis: { icon: "🌿", text: "AI 진단 기능을 준비 중입니다. 아래 관련 농약사를 참고하세요.", color: "#1e6b2e", bg: "#f0faf2" },
    subsidy:   { icon: "📋", text: "보조금 정보 기능을 준비 중입니다. 지역 농업기술센터에 문의하세요.", color: "#1a56a0", bg: "#f0f5ff" },
    event:     { icon: "🎪", text: "행사 정보 기능을 준비 중입니다.", color: "#7c3aed", bg: "#f5f0ff" },
    directory: { icon: "🔍", text: "", color: "", bg: "" }
  };
  const info = map[intent] || map["directory"];
  if (intent === "directory" || !info.text) {
    bannerEl.style.display = "none";
    return;
  }
  bannerEl.style.display = "block";
  bannerEl.style.background = info.bg;
  bannerEl.style.borderLeft = "4px solid " + info.color;
  bannerEl.style.padding = "12px 16px";
  bannerEl.style.marginBottom = "16px";
  bannerEl.style.borderRadius = "8px";
  bannerEl.innerHTML = info.icon + " <strong style=\\"color:" + info.color + "\\">" + info.text + "</strong>";
}'''

if old in content:
    content = content.replace(old, new)
    with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('성공')
else:
    print('실패: 대상 찾지 못함')
