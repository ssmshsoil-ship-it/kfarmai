import pandas as pd

data = [
    ('강원특별자치도', '철원군', '시군구청', 'https://www.cwg.go.kr', '', 'Y', '', ''),
    ('경기도', '김포시', '시군구청', 'https://www.gimpo.go.kr', '', 'Y', '', ''),
    ('경기도', '강화군', '시군구청', 'https://www.ganghwa.go.kr', '', 'Y', '', ''),
    ('경기도', '화성시', '시군구청', 'https://www.hscity.go.kr', '', 'Y', '', ''),
    ('충청북도', '진천군', '시군구청', 'https://www.jincheon.go.kr', '', 'Y', '', ''),
    ('충청남도', '천안시', '시군구청', 'https://www.cheonan.go.kr', '', 'Y', '', ''),
    ('충청남도', '당진시', '시군구청', 'https://www.dangjin.go.kr', '', 'Y', '', ''),
    ('충청남도', '아산시', '시군구청', 'https://www.asan.go.kr', '', 'Y', '', ''),
    ('충청남도', '서산시', '시군구청', 'https://www.seosan.go.kr', '', 'Y', '', ''),
    ('충청남도', '홍성군', '시군구청', 'https://www.hongseong.go.kr', '', 'Y', '', ''),
    ('충청남도', '예산군', '시군구청', 'https://www.yesan.go.kr', '', 'Y', '', ''),
    ('충청남도', '태안군', '시군구청', 'https://www.taean.go.kr', '', 'Y', '', ''),
    ('충청남도', '보령시', '시군구청', 'https://www.brcn.go.kr', '', 'Y', '', ''),
    ('충청남도', '서천군', '시군구청', 'https://www.seocheon.go.kr', '', 'Y', '', ''),
    ('충청남도', '청양군', '시군구청', 'https://www.cheongyang.go.kr', '', 'Y', '', ''),
    ('충청남도', '공주시', '농업기술센터', 'https://www.gongju.go.kr', '', 'Y', '', ''),
    ('충청남도', '논산시', '시군구청', 'https://www.nonsan.go.kr', '', 'Y', '', ''),
    ('충청남도', '계룡시', '시군구청', 'https://www.gyeryong.go.kr', '', 'Y', '', ''),
    ('충청남도', '부여군', '시군구청', 'https://www.buyeo.go.kr', '', 'Y', '', ''),
    ('전북특별자치도', '고창군', '시군구청', 'https://www.gochang.go.kr', '', 'Y', '', ''),
    ('전북특별자치도', '무주군', '시군구청', 'https://www.muju.go.kr', '', 'Y', '', ''),
    ('전북특별자치도', '전주시', '농업기술센터', 'https://www.jeonju.go.kr', '', 'Y', '', ''),
    ('전북특별자치도', '남원시', '시군구청', 'https://www.namwon.go.kr', '', 'Y', '', '나라장터 입찰'),
    ('전북특별자치도', '장수군', '시군구청', 'https://www.jangsu.go.kr', '', 'Y', '', ''),
    ('전북특별자치도', '순창군', '시군구청', 'https://www.sunchang.go.kr', '', 'Y', '', ''),
    ('전북특별자치도', '임실군', '시군구청', 'https://www.imsil.go.kr', '', 'Y', '', ''),
    ('전북특별자치도', '정읍시', '시군구청', 'https://www.jeongeup.go.kr', '', 'Y', '', ''),
    ('전북특별자치도', '완주군', '시군구청', 'https://www.wanju.go.kr', '', 'Y', '', ''),
    ('전라남도', '화순군', '시군구청', 'https://www.hwasun.go.kr', '', 'Y', '', ''),
    ('전라남도', '구례군', '시군구청', 'https://www.gurye.go.kr', '', 'Y', '', '나라장터 입찰'),
    ('전라남도', '담양군', '시군구청', 'https://www.damyang.go.kr', '', 'Y', '', ''),
    ('전라남도', '무안군', '시군구청', 'https://www.muan.go.kr', '', 'Y', '', ''),
    ('전라남도', '해남군', '시군구청', 'https://www.haenam.go.kr', '', 'Y', '', ''),
    ('전라남도', '신안군', '시군구청', 'https://www.shinan.go.kr', '', 'Y', '', ''),
    ('광주광역시', '북구', '북구청', 'https://bukgu.gwangju.kr', '', 'Y', '', ''),
    ('경상북도', '울진군', '시군구청', 'https://www.uljin.go.kr', '', 'Y', '', ''),
    ('경상북도', '칠곡군', '시군구청', 'https://www.chilgok.go.kr', '', 'Y', '', ''),
    ('강원특별자치도', '원주시', '시군구청', 'https://www.wonju.go.kr', '', 'Y', '', ''),
]

columns = ['광역시도', '시군구', '담당기관', '지자체_공식홈페이지', '농업부서_공고게시판_URL', '보조사업_실시여부', '공고URL_확인일', '비고']

df = pd.DataFrame(data, columns=columns)
df.to_excel('H:/내 드라이브/05_kfarmai_project/04_docs/지자체_URL목록.xlsx', index=False)
print(f'완료: {len(df)}개 지자체')