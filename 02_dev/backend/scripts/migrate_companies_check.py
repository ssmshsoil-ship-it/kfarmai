import pandas as pd

files = {
    "상토회사": "04_docs/상토회사_목록.xlsx",
    "종자회사": "04_docs/종자회사_목록.xlsx",
    "작물보호협회": "04_docs/작물보호협회_회원사.xlsx",
}

for name, path in files.items():
    df = pd.read_excel(path)
    print(f"\n[{name}]")
    print(f"컬럼: {df.columns.tolist()}")
    print(df.head(2))
