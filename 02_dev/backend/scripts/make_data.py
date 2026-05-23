import pandas as pd
import json

# geo 파일 사용 (좌표 변환 완료된 파일)
df = pd.read_csv("C:/kfarmai_temp/pesticide_sellers_geo.csv")

df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
df["lot"] = pd.to_numeric(df["lot"], errors="coerce")
df_geo = df.dropna(subset=["lat", "lot"])

data = []
for _, row in df_geo.iterrows():
    data.append({
        "name": str(row["bzentyNm"]),
        "sido": str(row["ctpvNm"]),
        "addr": str(row["lctnRoadNmAddr"]),
        "tel": str(row["telno"]),
        "item": str(row["hndlItemSeNm"]),
        "lat": round(float(row["lat"]), 6),
        "lot": round(float(row["lot"]), 6)
    })

js_content = f"const data = {json.dumps(data, ensure_ascii=False, indent=2)};"

save_path = "H:/내 드라이브/05_kfarmai_project/02_dev/web/static/pesticide_data.js"
with open(save_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"✅ 완료: {len(data)}건 저장")