import pandas as pd
from supabase import create_client
import os

SUPABASE_URL = "https://xzetqijeucldbfgjuoes.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 1. 농약사 CSV 마이그레이션
print("농약사 데이터 마이그레이션 시작...")
df = pd.read_csv("03_data/processed/pesticide_sellers.csv", encoding="utf-8-sig")
print(f"컬럼 목록: {df.columns.tolist()}")
print(df.head(2))
