from supabase import create_client

SUPABASE_URL = "https://xzetqijeucldbfgjuoes.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

fert_companies = [
    {"name": "남해화학(주)", "category": "비료", "phone": "061-680-2000", "address": "전라남도 여수시 중흥로 112", "website": "https://www.namhae.co.kr"},
    {"name": "(주)팜한농", "category": "비료", "phone": "02-3159-5500", "address": "서울시 영등포구 여의대로 24", "website": "https://www.farmhannong.com"},
    {"name": "(주)조비", "category": "비료", "phone": "055-280-4000", "address": "경상남도 창원시 성산구 외동반림로 62", "website": "https://www.jobi.co.kr"},
    {"name": "(주)카프로", "category": "비료", "phone": "052-279-1114", "address": "울산광역시 남구 산업로 915", "website": "https://www.capro.co.kr"},
    {"name": "(주)풍농", "category": "비료", "phone": "02-712-8791", "address": "서울특별시 마포구 마포대로 8", "website": "https://www.pungnong.com"},
    {"name": "(주)한국협화", "category": "비료", "phone": "052-279-3000", "address": "울산광역시 남구 산업로 915", "website": None},
    {"name": "(주)세기", "category": "비료", "phone": "031-490-5700", "address": "경기도 안산시 단원구 원시로 351", "website": None},
    {"name": "KG 케미칼(주)", "category": "비료", "phone": "02-6202-5500", "address": "서울특별시 강남구 테헤란로 114", "website": "https://www.kgchemical.co.kr"},
]

result = supabase.table("agri_companies").insert(fert_companies).execute()
print(f"비료회사 {len(result.data)}건 마이그레이션 완료")
