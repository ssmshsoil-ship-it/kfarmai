import pandas as pd
import folium

df = pd.read_csv("C:/kfarmai_temp/pesticide_sellers.csv")

# 좌표 있는 것만 필터링
df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
df["lot"] = pd.to_numeric(df["lot"], errors="coerce")
df_geo = df.dropna(subset=["lat", "lot"])

print(f"지도 표시 대상: {len(df_geo)}건")

# 지도 생성 (한국 중심)
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 마커 추가
for _, row in df_geo.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lot"]],
        radius=5,
        color="green",
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(
            f"""
            <b>{row['bzentyNm']}</b><br>
            {row['ctpvNm']} {row['sggNm']}<br>
            {row['lctnRoadNmAddr']}<br>
            ☎ {row['telno']}<br>
            취급: {row['hndlItemSeNm']}
            """,
            max_width=200
        )
    ).add_to(m)

# 저장
save_path = "C:/kfarmai_temp/pesticide_map.html"
m.save(save_path)
print(f"✅ 지도 저장완료: {save_path}")
print("브라우저에서 열어서 확인하세요.")