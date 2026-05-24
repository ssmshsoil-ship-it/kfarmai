import requests
from supabase import create_client

KAKAO_KEY = "ccd258d6289344411bff3f3781632135"
SUPABASE_URL = "https://xzetqijeucldbfgjuoes.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def geocode(address):
    if not address:
        return None, None
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
    res = requests.get(url, headers=headers, params={"query": address})
    print(f"  HTTP {res.status_code}: {res.text[:100]}")
    data = res.json()
    docs = data.get("documents", [])
    if docs:
        return float(docs[0]["y"]), float(docs[0]["x"])
    # 주소 검색 실패시 키워드 검색 시도
    url2 = "https://dapi.kakao.com/v2/local/search/keyword.json"
    res2 = requests.get(url2, headers=headers, params={"query": address})
    data2 = res2.json()
    docs2 = data2.get("documents", [])
    if docs2:
        return float(docs2[0]["y"]), float(docs2[0]["x"])
    return None, None

# 첫 3건만 테스트
companies = supabase.table("agri_companies").select("id, name, address, lat, lng").is_("lat", "null").limit(3).execute()
for c in companies.data:
    print(f"테스트: {c['name']} ({c.get('address', '')})")
    lat, lng = geocode(c.get("address", ""))
    print(f"결과: {lat}, {lng}")
