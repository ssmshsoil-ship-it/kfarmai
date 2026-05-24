import requests
from supabase import create_client

KAKAO_KEY = "ccd258d6289344411bff3f3781632135"
SUPABASE_URL = "https://xzetqijeucldbfgjuoes.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 카프로 좌표 조회
headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
res = requests.get("https://dapi.kakao.com/v2/local/search/keyword.json", 
                   headers=headers, 
                   params={"query": "울산광역시 남구 부곡동 300"})
docs = res.json().get("documents", [])
lat, lng = (float(docs[0]["y"]), float(docs[0]["x"])) if docs else (35.4862, 129.3798)
print(f"카프로 좌표: {lat}, {lng}")

# DB 업데이트
supabase.table("agri_companies").update({
    "lat": lat,
    "lng": lng,
    "address": "울산광역시 남구 부곡동 300"
}).eq("name", "(주)카프로").execute()
print("카프로 DB 완료")

# fert.html 수정
with open('02_dev/frontend/fert.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 카프로 주소 수정
old_capro = '울산광역시 남구 산업로 915'
new_capro = '울산광역시 남구 부곡동 300'
if content.count(old_capro) > 0:
    content = content.replace(old_capro, new_capro)
    print(f"fert.html 카프로 주소 수정 완료")

# 세기 주소 + 홈피 수정
content = content.replace('경기도 안산시 단원구 원시로 351', '경상북도 포항시 남구 철강산단로 202')

with open('02_dev/frontend/fert.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("fert.html 전체 수정 완료")
