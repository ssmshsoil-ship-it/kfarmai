import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib3
urllib3.disable_warnings()

BASE = "http://www.sangto.org"
LIST_URL = f"{BASE}/bbs/board.php?bo_table=b2"

def get_list_page(page=1):
    url = LIST_URL if page == 1 else f"{LIST_URL}&page={page}"
    try:
        r = requests.get(url, verify=False,
                        headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.encoding = 'utf-8'
        return BeautifulSoup(r.text, 'html.parser')
    except Exception as e:
        print(f"오류: {e}")
        return None

def get_detail(wr_id):
    url = f"{BASE}/bbs/board.php?bo_table=b2&wr_id={wr_id}"
    try:
        r = requests.get(url, verify=False,
                        headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        # 제목
        title_tag = soup.find('span', id='bo_v_title') or soup.find('h2')
        title = title_tag.get_text(strip=True) if title_tag else ''

        # 회사명 (sca 카테고리)
        company = ''
        cat_tag = soup.find('span', class_='bo_v_sca')
        if cat_tag:
            company = cat_tag.get_text(strip=True)

        # 본문
        content_tag = soup.find('div', id='bo_v_con')
        content = content_tag.get_text(strip=True)[:300] if content_tag else ''

        return title, company, content, url
    except Exception as e:
        print(f"상세 오류 wr_id={wr_id}: {e}")
        return '', '', '', url

# 전체 페이지에서 wr_id 수집
all_wr_ids = []
all_companies = []

print("게시물 목록 수집중...")
for page in range(1, 12):
    soup = get_list_page(page)
    if not soup:
        break

    links = soup.find_all('a', href=True)
    page_ids = []

    for link in links:
        href = link.get('href', '')
        company_text = ''

        if 'wr_id=' in href and 'bo_table=b2' in href:
            wr_id = href.split('wr_id=')[-1].split('&')[0]

            # 이전 링크에서 회사명 찾기
            prev_sibling = link.find_previous('a', href=lambda h: h and 'sca=' in h)
            if prev_sibling:
                company_text = prev_sibling.get_text(strip=True)

            if wr_id not in [x[0] for x in page_ids]:
                page_ids.append((wr_id, company_text))

    print(f"페이지 {page}: {len(page_ids)}건")
    all_wr_ids.extend(page_ids)
    time.sleep(0.5)

print(f"\n총 {len(all_wr_ids)}건 상세 수집 시작...")

results = []
for i, (wr_id, company) in enumerate(all_wr_ids):
    title, company_detail, content, url = get_detail(wr_id)
    final_company = company_detail if company_detail else company

    results.append({
        'wr_id': wr_id,
        'company': final_company,
        'title': title,
        'content_preview': content,
        'url': url
    })

    if (i+1) % 10 == 0:
        print(f"{i+1}/{len(all_wr_ids)} 완료")
    time.sleep(0.3)

df = pd.DataFrame(results)
save_path = "H:/내 드라이브/05_kfarmai_project/04_docs/sangto_products.csv"
df.to_csv(save_path, index=False, encoding='utf-8-sig')

print(f"\n✅ 완료: {len(df)}건")
print(df['company'].value_counts())