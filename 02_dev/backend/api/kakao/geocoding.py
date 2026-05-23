import requests
import os
import time
import pandas as pd
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings()

load_dotenv("H:/내 드라이브/05_kfarmai_project/02_dev/config/.env")
KAKAO_KEY = os.getenv("KAKAO_REST_API_KEY")

src_path = "C:/kfarmai_temp/pesticide_sellers.csv"
geo_path = "C:/kfarmai_temp/pesticide_sellers_geo.csv"

# 배치 크기: 한번에 처리할 건수
BATCH_SIZE = 1048

if os.path.exists(geo_path):
    df = pd.read_csv(geo_path)
    print("이전 작업 이어서 진행")
else:
    df = pd.read_csv(src_path)
    print("처음부터 시작")

df["lat"] = df["lat"].astype(object)
df["lot"] = df["lot"].astype(object)

# 좌표 없는 항목만 추출
empty_idx = [idx for idx, row in df.iterrows()
             if pd.isna(pd.to_numeric(row["lat"], errors="coerce"))]

print(f"전체 {len(df)}건 / 남은 항목 {len(empty_idx)}건")
print(f"이번 배치: {BATCH_SIZE}건 처리")

def get_coords(address):
    if not address or str(address).strip() in ["", "nan"]:
        return None, None
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": KAKAO_KEY}
    params = {"query": address}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        result = response.json()
        if result["documents"]:
            return float(result["documents"][0]["y"]), float(result["documents"][0]["x"])
    except Exception as e:
        print(f"오류: {e}")
    return None, None

# 이번 배치만 처리
batch = empty_idx[:BATCH_SIZE]
count = 0

for idx in batch:
    addr = df.at[idx, "lctnRoadNmAddr"]
    lat, lot = get_coords(addr)
    df.at[idx, "lat"] = lat
    df.at[idx, "lot"] = lot
    count += 1
    print(f"{count}/{BATCH_SIZE}: {str(addr)[:20]} → {lat}, {lot}")
    time.sleep(0.2)

df.to_csv(geo_path, index=False, encoding="utf-8-sig")

remaining = len(empty_idx) - count
print(f"\n✅ 이번 배치 {count}건 완료")
print(f"남은 항목: {remaining}건")
print(f"다시 실행하면 다음 {BATCH_SIZE}건 처리됩니다")