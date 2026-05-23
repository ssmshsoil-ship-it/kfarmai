import requests
import os
import time
import pandas as pd
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings()

load_dotenv("H:/내 드라이브/05_kfarmai_project/02_dev/config/.env")
KAKAO_KEY = os.getenv("KAKAO_REST_API_KEY")

df = pd.read_csv("H:/내 드라이브/05_kfarmai_project/03_data/processed/pesticide_sellers.csv")

print(f"전체 {len(df)}건")
print(f"좌표 없는 항목: {df['lat'].isna().sum() + (df['lat']=='').sum()}건")

def get_coords(address):
    if not address or str(address).strip() == "":
        return None, None
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
    params = {"query": address}
    try:
        time.sleep(0.1)
        response = requests.get(url, headers=headers, params=params, timeout=10)
        result = response.json()
        if result["documents"]:
            x = result["documents"][0]["x"]  # 경도
            y = result["documents"][0]["y"]  # 위도
            return y, x
    except Exception as e:
        print(f"오류: {address} - {e}")
    return None, None

# 좌표 없는 항목만 변환
count = 0
for idx, row in df.iterrows():
    if str(row["lat"]).strip() in ["", "nan"] or pd.isna(row["lat"]):
        lat, lot = get_coords(row["lctnRoadNmAddr"])
        df.at[idx, "lat"] = lat
        df.at[idx, "lot"] = lot
        count += 1
        if count % 50 == 0:
            print(f"{count}건 변환중...")

save_path = "H:/내 드라이브/05_kfarmai_project/03_data/processed/pesticide_sellers_geo.csv"
df.to_csv(save_path, index=False, encoding="utf-8-sig")

print(f"\n✅ 저장완료: {save_path}")
print(f"좌표 변환 완료: {count}건")