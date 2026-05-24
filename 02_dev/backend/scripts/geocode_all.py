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

companies = supabase.table("agri_companies").select("id, name, address, lat, lng").is_("lat", "null").execute()
print(f"총 {len(companies.data)}건 처리 시작")

success = 0
fail = 0
for c in companies.data:
    lat, lng = geocode(c.get("address", ""))
    if lat and lng:
        supabase.table("agri_companies").update({"lat": lat, "lng": lng}).eq("id", c["id"]).execute()
        print(f"완료: {c['name']}")
        success += 1
    else:
        print(f"실패: {c['name']} ({c.get('address', '')})")
        fail += 1
    time.sleep(0.1)

print(f"\n완료: {success}건 / 실패: {fail}건")
