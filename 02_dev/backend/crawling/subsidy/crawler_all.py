import requests
from bs4 import BeautifulSoup
import urllib3
import json
import os
from datetime import datetime
urllib3.disable_warnings()

KEYWORDS = ['상토', '못자리', '수도용', '모판', '육묘']
RESULT_FILE = 'H:/내 드라이브/05_kfarmai_project/03_data/processed/alerts.json'
MODE = 'init'  # 'init' or 'daily'

# 지자체 설정
# method: 'get' or 'post'
# page_param: 페이지 파라미터명
SITES = [
    {
        'sigungu': '부여군',
        'url': 'https://www.buyeo.go.kr/html/kr/news/news_040202.html',
        'method': 'get',
        'page_param': 'GotoPage',
        'title_idx': 2,
        'date_idx': 4,
    },
    {
        'sigungu': '홍성군',
        'url': 'https://www.hongseong.go.kr/prog/saeolGosi/kor/sub03_0204/GOSI_ALL/list.do',
        'method': 'post',
        'page_param': 'pageIndex',
        'title_idx': 2,
        'date_idx': 4,
    },
]

def get_page(site, page=1):
    url = site['url']
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        if site['method'] == 'get':
            if page > 1:
                url = f"{url}?&{site['page_param']}={page}"
            r = requests.get(url, verify=False, headers=headers, timeout=10)
        else:
            data = {site['page_param']: str(page)}
            r = requests.post(url, data=data, verify=False, headers=headers, timeout=10)
        r.encoding = 'utf-8'
        return BeautifulSoup(r.text, 'html.parser')
    except Exception as e:
        print(f"오류: {e}")
        return None

def parse_posts(soup, title_idx, date_idx):
    posts = []
    for row in soup.find_all('tr'):
        tds = row.find_all('td')
        if len(tds) > max(title_idx, date_idx):
            title = tds[title_idx].get_text(strip=True)
            date = tds[date_idx].get_text(strip=True)[:10]
            if title and date and '-' in date:
                posts.append({'title': title, 'date': date})
    return posts

today = datetime.now().strftime('%Y-%m-%d')
all_found = []

for site in SITES:
    print(f"\n[{site['sigungu']}] 크롤링 시작")
    page = 1
    max_pages = 50 if MODE == 'init' else 10

    while page <= max_pages:
        soup = get_page(site, page)
        if not soup:
            break

        posts = parse_posts(soup, site['title_idx'], site['date_idx'])
        if not posts:
            print(f"  페이지 {page}: 종료")
            break

        if MODE == 'daily':
            today_posts = [p for p in posts if p['date'] == today]
            if not today_posts:
                print(f"  페이지 {page}: 오늘 날짜 없음 → 종료")
                break
            posts = today_posts

        found = []
        for post in posts:
            for kw in KEYWORDS:
                if kw in post['title']:
                    found.append({
                        'sigungu': site['sigungu'],
                        'keyword': kw,
                        'title': post['title'][:100],
                        'date': post['date'],
                        'page': page,
                        'found_at': today,
                        'url': site['url']
                    })
                    break

        if found:
            print(f"  페이지 {page}: 🔴 {len(found)}건 감지")
            for f in found:
                print(f"    [{f['keyword']}] {f['title'][:50]} ({f['date']})")
            all_found.extend(found)
        else:
            print(f"  페이지 {page}: ⚪ 없음")

        page += 1

# 결과 저장
if os.path.exists(RESULT_FILE):
    with open(RESULT_FILE, 'r', encoding='utf-8') as f:
        existing = json.load(f)
else:
    existing = []

existing.extend(all_found)
with open(RESULT_FILE, 'w', encoding='utf-8') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"\n✅ 완료: 총 {len(all_found)}건 감지")