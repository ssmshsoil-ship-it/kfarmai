import pandas as pd
from supabase import create_client
import math

SUPABASE_URL = "https://xzetqijeucldbfgjuoes.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("농약사 데이터 마이그레이션 시작...")
df = pd.read_csv("03_data/processed/pesticide_sellers.csv", encoding="utf-8-sig")
print(f"총 {len(df)}건 로드")

def clean(val):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    return str(val).strip()

records = []
for _, row in df.iterrows():
    records.append({
        "name": clean(row.get("bzentyNm")),
        "sido": clean(row.get("ctpvNm")),
        "sigungu": clean(row.get("sggNm")),
        "address": clean(row.get("lctnRoadNmAddr")),
        "lat": float(row["lat"]) if pd.notna(row.get("lat")) else None,
        "lng": float(row["lot"]) if pd.notna(row.get("lot")) else None,
        "phone": clean(row.get("telno")),
        "region_code": clean(row.get("insttCode")),
    })

# 100건씩 배치 업로드
batch_size = 100
for i in range(0, len(records), batch_size):
    batch = records[i:i+batch_size]
    supabase.table("pesticide_shops").insert(batch).execute()
    print(f"{i+len(batch)}/{len(records)} 완료")

print("농약사 마이그레이션 완료!")
