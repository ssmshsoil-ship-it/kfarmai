import json
import re
from supabase import create_client
import math

SUPABASE_URL = "https://xzetqijeucldbfgjuoes.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 기존 데이터 전체 삭제
print("기존 농약사 데이터 삭제 중...")
supabase.table("pesticide_shops").delete().neq("id", 0).execute()
print("삭제 완료")

# pesticide_data.js 읽기
with open("02_dev/frontend/static/pesticide_data.js", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("const data = ", "").rstrip(";").strip()
data = json.loads(content)
print(f"총 {len(data)}건 로드")

def clean(val):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    return str(val).strip()

records = []
for row in data:
    addr = clean(row.get("addr", ""))
    sido = clean(row.get("sido", ""))
    sigungu = addr.replace(sido, "").strip().split(" ")[0] if addr and sido else ""
    records.append({
        "name": clean(row.get("name")),
        "sido": sido,
        "sigungu": sigungu,
        "address": addr,
        "lat": float(row["lat"]) if row.get("lat") else None,
        "lng": float(row["lot"]) if row.get("lot") else None,
        "phone": clean(row.get("tel")),
    })

batch_size = 100
for i in range(0, len(records), batch_size):
    batch = records[i:i+batch_size]
    supabase.table("pesticide_shops").insert(batch).execute()
    print(f"{i+len(batch)}/{len(records)} 완료")

print("마이그레이션 완료!")
