with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

results = []

# 1. hasMap 조건 수정 (회사도 지도 표시)
old1 = "hasMap = r.catKey === 'map' && r.lat && r.lot;"
new1 = "hasMap = r.lat && r.lot;"
if old1 in content:
    content = content.replace(old1, new1, 1)
    results.append('hasMap 수정 완료')
else:
    results.append('hasMap 이미 수정됨')

# 2. roadview 라이브러리 추가
old2 = 'dapi.kakao.com/v2/maps/sdk.js?appkey=533e5896630c1460c4349d33b3fab95a&autoload=false">'
new2 = 'dapi.kakao.com/v2/maps/sdk.js?appkey=533e5896630c1460c4349d33b3fab95a&autoload=false&libraries=services,roadview">'
if old2 in content:
    content = content.replace(old2, new2, 1)
    results.append('roadview 라이브러리 추가 완료')

# 3. 로드뷰 패널 추가
old3 = '<div id="resultMap"></div>\n</div>'
new3 = '<div id="resultMap"></div>\n  <div id="roadviewPanel" style="width:100%;height:300px;display:none;border-radius:8px;overflow:hidden;margin-top:8px;"></div>\n</div>'
if old3 in content:
    content = content.replace(old3, new3, 1)
    results.append('로드뷰 패널 추가 완료')

# 4. 로드뷰 JS 추가
old4 = '\nfunction focusMarker(lat, lot, name) {'
new4 = '''
let roadviewClient = null;

function showRoadview(lat, lng) {
  const panel = document.getElementById('roadviewPanel');
  panel.style.display = 'block';
  panel.innerHTML = '';
  if (!roadviewClient) roadviewClient = new kakao.maps.RoadviewClient();
  const roadview = new kakao.maps.Roadview(panel);
  roadviewClient.getNearestPanoId(new kakao.maps.LatLng(lat, lng), 50, function(panoId) {
    if (panoId) {
      roadview.setPanoId(panoId, new kakao.maps.LatLng(lat, lng));
    } else {
      panel.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#999;font-size:13px;background:#f5f5f5;border-radius:8px;">이 위치의 로드뷰를 제공하지 않습니다.</div>';
    }
  });
}

function focusMarker(lat, lot, name) {'''
if old4 in content:
    content = content.replace(old4, new4, 1)
    results.append('로드뷰 JS 추가 완료')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)

for r in results:
    print(r)
