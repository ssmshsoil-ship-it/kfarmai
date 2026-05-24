import pandas as pd
from supabase import create_client
import math

SUPABASE_URL = "https://xzetqijeucldbfgjuoes.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def clean(val):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    return str(val).strip()

def upload(records, label):
    batch_size = 100
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        supabase.table("agri_companies").insert(batch).execute()
        print(f"{label}: {i+len(batch)}/{len(records)} 완료")

# 1. 상토회사
df = pd.read_excel("04_docs/상토회사_목록.xlsx")
records = []
for _, row in df.iterrows():
    records.append({
        "name": clean(row.get("회사명")),
        "category": "상토",
        "address": clean(row.get("소재지")),
        "website": clean(row.get("홈페이지")),
    })
upload(records, "상토회사")

# 2. 종자회사
df = pd.read_excel("04_docs/종자회사_목록.xlsx")
records = []
for _, row in df.iterrows():
    records.append({
        "name": clean(row.get("회사명")),
        "category": "종자",
        "address": clean(row.get("주소")),
        "phone": clean(row.get("연락처")),
        "website": clean(row.get("홈페이지")),
    })
upload(records, "종자회사")

# 3. 작물보호협회
df = pd.read_excel("04_docs/작물보호협회_회원사.xlsx")
records = []
for _, row in df.iterrows():
    records.append({
        "name": clean(row.get("company")),
        "category": "작물보호제",
        "address": clean(row.get("addr")),
        "phone": clean(row.get("tel")),
        "website": clean(row.get("homepage")),
    })
upload(records, "작물보호협회")

print("전체 회사 마이그레이션 완료!")
