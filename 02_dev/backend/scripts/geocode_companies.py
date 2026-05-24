import requests
from supabase import create_client

KAKAO_KEY = "533e5896630c1460c4349d33b3fab95a"
SUPABASE_URL = "https://xzetqijeucldbfgjuoes.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def geocode(address):
    if not address:
        return None, None
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
    res = requests.get(url, headers=headers, params={"query": address})
    data = res.json()
    docs = data.get("documents", [])
    if docs:
        return float(docs[0]["y"]), float(docs[0]["x"])
    return None, None

# 좌표 없는 회사 조회
companies = supabase.table("agri_companies").select("id, name, address, lat, lng").is_("lat", "null").execute()
print(f"좌표 없는 회사: {len(companies.data)}건")

success = 0
for c in companies.data:
    lat, lng = geocode(c.get("address", ""))
    if lat and lng:
        supabase.table("agri_companies").update({"lat": lat, "lng": lng}).eq("id", c["id"]).execute()
        print(f"완료: {c['name']} → {lat}, {lng}")
        success += 1
    else:
        print(f"실패: {c['name']} ({c.get('address', '')})")

print(f"\n총 {success}/{len(companies.data)}건 좌표 변환 완료")
