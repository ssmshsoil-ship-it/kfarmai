import requests
from supabase import create_client
import time

KAKAO_KEY = "ccd258d6289344411bff3f3781632135"
SUPABASE_URL = "https://xzetqijeucldbfgjuoes.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def geocode(address):
    headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
    res = requests.get("https://dapi.kakao.com/v2/local/search/keyword.json", headers=headers, params={"query": address})
    docs = res.json().get("documents", [])
    if docs:
        return float(docs[0]["y"]), float(docs[0]["x"])
    return None, None

fixes = [
    {"name": "남해화학(주)", "address": "전남 여수시 여수산단로 1384"},
    {"name": "(주)카프로", "address": "울산광역시 남구 부곡동 402-1"},
    {"name": "(주)한국협화", "address": "경상북도 포항시 남구 대송로 253번길 63"},
    {"name": "(주)세기", "address": "경상북도 포항시 남구 철강산단로 202",
     "new_address": "경상북도 포항시 남구 철강산단로 202",
     "website": "https://www.segiglobal.co.kr/"},
]

for fix in fixes:
    lat, lng = geocode(fix["address"])
    update_data = {}
    if lat and lng:
        update_data["lat"] = lat
        update_data["lng"] = lng
    if fix.get("new_address"):
        update_data["address"] = fix["new_address"]
    if fix.get("website"):
        update_data["website"] = fix["website"]
    if update_data:
        supabase.table("agri_companies").update(update_data).eq("name", fix["name"]).execute()
        print(f"완료: {fix['name']} -> {lat}, {lng}")
    else:
        print(f"실패: {fix['name']}")
    time.sleep(0.1)

print("DB 업데이트 완료")
