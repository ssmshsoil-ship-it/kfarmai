import requests
import pandas as pd
import urllib3
urllib3.disable_warnings()

urls = [
    ('강원특별자치도', '철원군', 'https://www.cwg.go.kr'),
    ('경기도', '김포시', 'https://www.gimpo.go.kr'),
    ('경기도', '강화군', 'https://www.ganghwa.go.kr'),
    ('경기도', '화성시', 'https://www.hscity.go.kr'),
    ('충청북도', '진천군', 'https://www.jincheon.go.kr'),
    ('충청남도', '천안시', 'https://www.cheonan.go.kr'),
    ('충청남도', '당진시', 'https://www.dangjin.go.kr'),
    ('충청남도', '아산시', 'https://www.asan.go.kr'),
    ('충청남도', '서산시', 'https://www.seosan.go.kr'),
    ('충청남도', '홍성군', 'https://www.hongseong.go.kr'),
    ('충청남도', '예산군', 'https://www.yesan.go.kr'),
    ('충청남도', '태안군', 'https://www.taean.go.kr'),
    ('충청남도', '보령시', 'https://www.brcn.go.kr'),
    ('충청남도', '서천군', 'https://www.seocheon.go.kr'),
    ('충청남도', '청양군', 'https://www.cheongyang.go.kr'),
    ('충청남도', '공주시', 'https://www.gongju.go.kr'),
    ('충청남도', '논산시', 'https://www.nonsan.go.kr'),
    ('충청남도', '계룡시', 'https://www.gyeryong.go.kr'),
    ('충청남도', '부여군', 'https://www.buyeo.go.kr'),
    ('전북특별자치도', '고창군', 'https://www.gochang.go.kr'),
    ('전북특별자치도', '무주군', 'https://www.muju.go.kr'),
    ('전북특별자치도', '전주시', 'https://www.jeonju.go.kr'),
    ('전북특별자치도', '남원시', 'https://www.namwon.go.kr'),
    ('전북특별자치도', '장수군', 'https://www.jangsu.go.kr'),
    ('전북특별자치도', '순창군', 'https://www.sunchang.go.kr'),
    ('전북특별자치도', '임실군', 'https://www.imsil.go.kr'),
    ('전북특별자치도', '정읍시', 'https://www.jeongeup.go.kr'),
    ('전북특별자치도', '완주군', 'https://www.wanju.go.kr'),
    ('전라남도', '화순군', 'https://www.hwasun.go.kr'),
    ('전라남도', '구례군', 'https://www.gurye.go.kr'),
    ('전라남도', '담양군', 'https://www.damyang.go.kr'),
    ('전라남도', '무안군', 'https://www.muan.go.kr'),
    ('전라남도', '해남군', 'https://www.haenam.go.kr'),
    ('전라남도', '신안군', 'https://www.shinan.go.kr'),
    ('광주광역시', '북구', 'https://bukgu.gwangju.kr'),
    ('경상북도', '울진군', 'https://www.uljin.go.kr'),
    ('경상북도', '칠곡군', 'https://www.chilgok.go.kr'),
    ('강원특별자치도', '원주시', 'https://www.wonju.go.kr'),
]

results = []
for sido, sigungu, url in urls:
    try:
        r = requests.get(url, timeout=20, verify=False,
                        headers={"User-Agent": "Mozilla/5.0"})
        status = "✅ 정상" if r.status_code == 200 else f"⚠️ {r.status_code}"
    except Exception as e:
        status = "❌ 접속불가"
    results.append([sido, sigungu, url, status])
    print(f"{sigungu}: {status}")

df = pd.DataFrame(results, columns=['광역시도', '시군구', 'URL', '상태'])
df.to_csv('H:/내 드라이브/05_kfarmai_project/04_docs/url_검증결과.csv',
          index=False, encoding='utf-8-sig')
print(f"\n✅ 검증완료 → url_검증결과.csv 저장")