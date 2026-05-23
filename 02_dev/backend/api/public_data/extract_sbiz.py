import pandas as pd
import os
import glob

# 소상공인 데이터 폴더
DATA_DIR = "C:/Users/PCuser/Downloads/소상공인시장진흥공단_상가(상권)정보_20260331"
OUTPUT_PATH = "C:/kfarmai_temp/sbiz_pesticide.csv"

# 검색 키워드 (상호명 기준)
KEYWORDS = ['농약', '농자재', '비료', '농협경제', '농업협동', '종묘']

# 제외 키워드 (주유소, 식당 등 관련없는 것)
EXCLUDE_KEYWORDS = ['주유소', '식당', '음식', '카페', '편의점', '마트', '슈퍼', '세탁', '병원']

# 전국 CSV 파일 목록
csv_files = glob.glob(f"{DATA_DIR}/*.csv")
print(f"총 {len(csv_files)}개 파일 발견")

all_results = []

for csv_file in csv_files:
    region = os.path.basename(csv_file).split('_')[3]
    print(f"{region} 처리중...", end=" ")

    try:
        df = pd.read_csv(csv_file, encoding='utf-8-sig', low_memory=False)

        # 키워드 필터링
        mask = df['상호명'].str.contains('|'.join(KEYWORDS), na=False)
        result = df[mask].copy()

        # 제외 키워드 필터링
        exclude_mask = result['상권업종소분류명'].str.contains('|'.join(EXCLUDE_KEYWORDS), na=False)
        result = result[~exclude_mask]

        # 필요한 컬럼만 추출
        result = result[[
            '상호명', '상권업종소분류명', '시도명', '시군구명',
            '도로명주소', '경도', '위도'
        ]].copy()

        result.columns = ['name', 'category', 'sido', 'sigungu', 'addr', 'lot', 'lat']

        all_results.append(result)
        print(f"{len(result)}건")

    except Exception as e:
        print(f"오류: {e}")

# 전체 합치기
final_df = pd.concat(all_results, ignore_index=True)

# 좌표 없는 항목 제거
final_df = final_df.dropna(subset=['lat', 'lot'])
final_df = final_df[final_df['lat'] != 0]

print(f"\n✅ 총 {len(final_df)}건 추출")
final_df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8-sig')
print(f"저장완료: {OUTPUT_PATH}")
print(final_df['sido'].value_counts())