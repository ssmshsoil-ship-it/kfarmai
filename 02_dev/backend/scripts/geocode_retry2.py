import requests
from supabase import create_client
import time

KAKAO_KEY = "ccd258d6289344411bff3f3781632135"
SUPABASE_URL = "https://xzetqijeucldbfgjuoes.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def geocode(address):
    if not address:
        return None, None
    headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
    res = requests.get("https://dapi.kakao.com/v2/local/search/address.json", headers=headers, params={"query": address})
    docs = res.json().get("documents", [])
    if docs:
        return float(docs[0]["y"]), float(docs[0]["x"])
    res2 = requests.get("https://dapi.kakao.com/v2/local/search/keyword.json", headers=headers, params={"query": address})
    docs2 = res2.json().get("documents", [])
    if docs2:
        return float(docs2[0]["y"]), float(docs2[0]["x"])
    return None, None

manual_fixes = [
    {"name": "㈜신성미네랄", "address": "충북 괴산군 청안면 조천로 2길 34"},
    {"name": "니치노코리아(주)", "address": "서울시 강남구 삼성로 508"},
    {"name": "남해화학(주)", "address": "전라남도 여수시 중흥로 112"},
    {"name": "(주)카프로", "address": "울산광역시 남구 산업로 915"},
    {"name": "(주)한국협화", "address": "울산광역시 남구 산업로 915"},
    {"name": "(주)세기", "address": "경기도 안산시 단원구 원시로 351"},
    {"name": "㈜이엑스아이디", "address": "충북 충주시 용탄농공1길 31"},
    {"name": "(주)장유산업", "address": "충청북도 청주시 흥덕구 옥산면 옥산산단1로 117"},
    {"name": "태평에이지(주)", "address": "경북 영천시 채신2공단길 74"},
    {"name": "팜아그로텍(주)", "address": "충청북도 음성군 생극면 생극산단1길 59"},
]

for fix in manual_fixes:
    lat, lng = geocode(fix["address"])
    if lat and lng:
        supabase.table("agri_companies").update({"lat": lat, "lng": lng}).eq("name", fix["name"]).execute()
        print(f"완료: {fix['name']} -> {lat}, {lng}")
    else:
        print(f"실패: {fix['name']}")
    time.sleep(0.1)

print("완료")
