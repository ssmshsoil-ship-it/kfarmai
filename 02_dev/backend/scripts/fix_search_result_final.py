with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

results = []

# 1. Kakao SDK에 roadview 라이브러리 추가
old1 = 'dapi.kakao.com/v2/maps/sdk.js?appkey=533e5896630c1460c4349d33b3fab95a&autoload=false">'
new1 = 'dapi.kakao.com/v2/maps/sdk.js?appkey=533e5896630c1460c4349d33b3fab95a&autoload=false&libraries=services,roadview">'
if old1 in content:
    content = content.replace(old1, new1, 1)
    results.append('SDK roadview 추가 완료')

# 2. 지도 패널에 로드뷰 div 추가
old2 = '''<div id="mapPanel" style="display:none;">
  <div class="map-panel-title">📍 지도에서 위치 확인</div>
  <div id="resultMap"></div>
</div>'''
new2 = '''<div id="mapPanel" style="display:none;">
  <div class="map-panel-title">📍 지도에서 위치 확인</div>
  <div id="resultMap"></div>
  <div id="roadviewPanel" style="width:100%;height:300px;display:none;border-radius:8px;overflow:hidden;margin-top:8px;"></div>
</div>'''
if old2 in content:
    content = content.replace(old2, new2, 1)
    results.append('로드뷰 패널 추가 완료')

# 3. renderMap을 kakao.maps.load 없이 직접 실행하도록 수정
old3 = '''function renderMap(pestResults) {
  kakao.maps.load(function() {
    const container = document.getElementById('resultMap');
    if (!kakaoMap) {
      kakaoMap = new kakao.maps.Map(container, {
        center: new kakao.maps.LatLng(36.5, 127.8),
        level: 7
      });
      infowindow = new kakao.maps.InfoWindow({ zIndex:1 });
      kakao.maps.event.addListener(kakaoMap, 'click', () => infowindow.close());
    }'''
new3 = '''function renderMap(pestResults) {
  document.getElementById('mapPanel').style.display = 'block';
  const container = document.getElementById('resultMap');
  kakaoMap = new kakao.maps.Map(container, {
    center: new kakao.maps.LatLng(36.5, 127.8),
    level: 7
  });
  infowindow = new kakao.maps.InfoWindow({ zIndex:1 });
  kakao.maps.event.addListener(kakaoMap, 'click', () => infowindow.close());
  {'''
if old3 in content:
    content = content.replace(old3, new3, 1)
    results.append('renderMap 수정 완료')

# 4. kakao.maps.load 닫는 괄호 제거
old4 = '  });\n}\n\n/* ── 특정 마커 포커스 ── */'
new4 = '  }\n}\n\n/* ── 특정 마커 포커스 ── */'
if old4 in content:
    content = content.replace(old4, new4, 1)
    results.append('load 닫기 수정 완료')

# 5. hasMap 버튼에 로드뷰 버튼 추가
old5 = "hasMap ? `<button class=\"r-map-link\" onclick=\"focusMarker(${r.lat},${r.lot},'${r.name.replace(/'/g,\"\\\\'\")}')\">\U0001f4cd 지도에서 보기</button>` : ''}"
new5 = "hasMap ? `<button class=\"r-map-link\" onclick=\"focusMarker(${r.lat},${r.lot},'${r.name.replace(/'/g,\"\\\\'\")}')\">\U0001f4cd 지도에서 보기</button> <button class=\"r-map-link\" onclick=\"focusMarker(${r.lat},${r.lot},'${r.name.replace(/'/g,\"\\\\'\")}');showRoadview(${r.lat},${r.lot});\" style=\"background:#eef4fb;color:#1a5c9e;\">\U0001f6b6 로드뷰</button>` : ''}"
if old5 in content:
    content = content.replace(old5, new5, 1)
    results.append('로드뷰 버튼 추가 완료')

# 6. 로드뷰 JS 추가 (focusMarker 함수 앞에)
old6 = '\nfunction focusMarker(lat, lot, name) {'
new6 = '''
let roadviewClient = null;
let currentLat = null;
let currentLng = null;

function showRoadview(lat, lng) {
  currentLat = lat;
  currentLng = lng;
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
if old6 in content:
    content = content.replace(old6, new6, 1)
    results.append('로드뷰 JS 추가 완료')

# 7. 의도 분기 처리 (기존 코드 유지)
old7 = "    const intent = data.intent || \"directory\";\n    const bannerEl = document.getElementById(\"intentBanner\");"
if old7 in content:
    results.append('의도 분기 코드 확인 완료')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)

for r in results:
    print(r)
