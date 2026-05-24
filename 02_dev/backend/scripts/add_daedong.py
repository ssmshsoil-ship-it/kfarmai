from supabase import create_client
import requests

KAKAO_KEY = "ccd258d6289344411bff3f3781632135"
SUPABASE_URL = "https://xzetqijeucldbfgjuoes.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
res = requests.get("https://dapi.kakao.com/v2/local/search/address.json", headers=headers, params={"query": "전라남도 보성군 벌교읍 남하로 266"})
docs = res.json().get("documents", [])
lat = float(docs[0]["y"]) if docs else None
lng = float(docs[0]["x"]) if docs else None
print(f"좌표: {lat}, {lng}")

result = supabase.table("agri_companies").insert({
    "name": "(주)대동산업",
    "category": "상토",
    "address": "전라남도 보성군 벌교읍 남하로 266",
    "phone": "061-858-0660",
    "website": None,
    "lat": lat,
    "lng": lng,
    "is_member": True
}).execute()
print(f"DB 추가 완료")
