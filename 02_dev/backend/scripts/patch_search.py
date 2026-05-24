with open("02_dev/frontend/search_result.html", "r", encoding="utf-8") as f:
    content = f.read()

old = '''doSearch(q) {
  if (!q) return [];
  return DB.filter(d =>
    d.name.includes(q) ||
    (d.addr && d.addr.includes(q)) ||
    d.cat.includes(q)
  );
}'''

new = '''doSearch(q) {
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

if old in content:
    content = content.replace(old, new)
    with open("02_dev/frontend/search_result.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("성공: API 연동 완료")
else:
    print("실패: 대상 함수를 찾지 못했습니다")
