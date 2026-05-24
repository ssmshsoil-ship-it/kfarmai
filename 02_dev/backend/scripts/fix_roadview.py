with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

results = []

# 1. 지도+로드뷰 레이아웃 변경
old1 = '''<div id="mapPanel" style="display:none;">
  <div class="map-panel-title">📍 지도에서 위치 확인</div>
  <div id="resultMap"></div>
</div>'''

new1 = '''<div id="mapPanel" style="display:none;">
  <div class="map-panel-title" style="display:flex;justify-content:space-between;align-items:center;">
    <span>📍 지도에서 위치 확인</span>
    <button id="roadviewToggleBtn" onclick="toggleRoadview()" style="font-size:12px;padding:4px 10px;background:#1e6b2e;color:white;border:none;border-radius:6px;cursor:pointer;display:none;">🚶 로드뷰 보기</button>
  </div>
  <div style="display:flex;gap:8px;">
    <div id="resultMap" style="flex:1;"></div>
    <div id="roadviewPanel" style="flex:1;display:none;border-radius:8px;overflow:hidden;"></div>
  </div>
</div>'''

if old1 in content:
    content = content.replace(old1, new1, 1)
    results.append('지도 패널 수정 완료')
else:
    results.append('지도 패널 실패')

# 2. 로드뷰 JS 추가 - focusMarker 함수 찾아서 로드뷰 버튼 활성화 추가
old2 = 'function focusMarker(lat, lot, name) {'
new2 = '''let roadviewClient = null;
let currentLat = null;
let currentLng = null;

function toggleRoadview() {
  const panel = document.getElementById('roadviewPanel');
  const btn = document.getElementById('roadviewToggleBtn');
  const mapEl = document.getElementById('resultMap');
  if (panel.style.display === 'none') {
    panel.style.display = 'block';
    mapEl.style.flex = '1';
    btn.textContent = '🗺️ 지도만 보기';
    if (currentLat && currentLng) {
      showRoadview(currentLat, currentLng);
    }
  } else {
    panel.style.display = 'none';
    btn.textContent = '🚶 로드뷰 보기';
  }
}

function showRoadview(lat, lng) {
  const roadviewContainer = document.getElementById('roadviewPanel');
  roadviewContainer.style.display = 'block';
  if (!roadviewClient) {
    roadviewClient = new kakao.maps.RoadviewClient();
  }
  const roadview = new kakao.maps.Roadview(roadviewContainer);
  const position = new kakao.maps.LatLng(lat, lng);
  roadviewClient.getNearestPanoId(position, 50, function(panoId) {
    if (panoId) {
      roadview.setPanoId(panoId, position);
    } else {
      roadviewContainer.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#999;font-size:13px;">이 위치의 로드뷰를<br>제공하지 않습니다.</div>';
    }
  });
}

function focusMarker(lat, lot, name) {'''

if old2 in content:
    content = content.replace(old2, new2, 1)
    results.append('로드뷰 JS 추가 완료')
else:
    results.append('로드뷰 JS 실패')

# 3. focusMarker 함수 내에 로드뷰 버튼 활성화 + 좌표 저장
old3 = 'function focusMarker(lat, lot, name) {\n  if (!kakaoMap) return;'
new3 = 'function focusMarker(lat, lot, name) {\n  currentLat = lat;\n  currentLng = lot;\n  const btn = document.getElementById(\'roadviewToggleBtn\');\n  if (btn) btn.style.display = \'inline-block\';\n  if (!kakaoMap) return;'

if old3 in content:
    content = content.replace(old3, new3, 1)
    results.append('focusMarker 수정 완료')
else:
    results.append('focusMarker 실패')

# 4. Kakao Maps SDK에 roadview 라이브러리 추가
old4 = 'dapi.kakao.com/v2/maps/sdk.js?appkey=533e5896630c1460c4349d33b3fab95a&autoload=false">'
new4 = 'dapi.kakao.com/v2/maps/sdk.js?appkey=533e5896630c1460c4349d33b3fab95a&autoload=false&libraries=services,roadview">'

if old4 in content:
    content = content.replace(old4, new4, 1)
    results.append('SDK roadview 라이브러리 추가 완료')
else:
    results.append('SDK 실패')

with open('02_dev/frontend/search_result.html', 'w', encoding='utf-8') as f:
    f.write(content)

for r in results:
    print(r)
