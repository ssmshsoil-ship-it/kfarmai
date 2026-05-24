with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    const shops = (data.shops || []).map(d => ({
      name: d.name, addr: d.address, cat: "농약사",
      lat: d.lat, lot: d.lng, tel: d.phone
    }));
    const companies = (data.companies || []).map(d => ({
      name: d.name, addr: d.address, cat: d.category,
      website: d.website
    }));'''

new = '''    const shops = (data.shops || []).map(d => ({
      name: d.name, addr: d.address, cat: "농약사", catKey: "map",
      lat: d.lat, lot: d.lng, tel: d.phone, homepage: null
    }));
    const companies = (data.companies || []).map(d => ({
      name: d.name, addr: d.address, cat: d.category,
      catKey: d.category === "상토" ? "santo" : d.category === "종자" ? "seed" : d.category === "작물보호제" ? "cpa" : d.category === "비료" ? "fert" : "santo",
      lat: null, lot: null, tel: d.phone, homepage: d.website
    }));'''

if old in content:
    content = content.replace(old, new, 1)
    print('매핑 수정 완료')
else:
    print('실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)
