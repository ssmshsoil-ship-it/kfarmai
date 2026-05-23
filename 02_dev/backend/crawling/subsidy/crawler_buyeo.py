import requests
from bs4 import BeautifulSoup
import urllib3
import json
import os
from datetime import datetime
urllib3.disable_warnings()

KEYWORDS = ['상토', '못자리', '수도용', '모판', '육묘']
BASE_URL = 'https://www.buyeo.go.kr/html/kr/news/news_040202.html'
SIGUNGU = '부여군'
RESULT_FILE = 'H:/내 드라이브/05_kfarmai_project/03_data/processed/alerts.json'

# 모드 설정
# 'init' : 전체 페이지 수집 (최초 1회)
# 'daily': 오늘 날짜 게시물만 감시 (매일 실행)
MODE = 'init'

def get_page(page=1):
    url = BASE_URL if page == 1 else f'{BASE_URL}?&GotoPage={page}'
    try:
        r = requests.get(url, verify=False,
                        headers={'User-Agent': 'Mozilla/5.0'},
                        timeout=10)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    except Exception as e:
        print(f"오류 (페이지 {page}): {e}")
        return None

def parse_posts(soup):
    posts = []
    rows = soup.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) >= 5:
            title = tds[2].get_text(strip=True)
            date = tds[4].get_text(strip=True)[:10]
            if title and date and '-' in date:
                posts.append({'title': title, 'date': date})
    return posts

today = datetime.now().strftime('%Y-%m-%d')
all_found = []
page = 1
max_pages = 50 if MODE == 'init' else 10

print(f"[{SIGUNGU}] 크롤링 시작 (모드: {MODE})")

while page <= max_pages:
    soup = get_page(page)
    if not soup:
        break

    posts = parse_posts(soup)
    if not posts:
        print(f"페이지 {page}: 게시물 없음 → 종료")
        break

    # daily 모드: 오늘 날짜 게시물 없으면 종료
    if MODE == 'daily':
        today_posts = [p for p in posts if p['date'] == today]
        if not today_posts:
            print(f"페이지 {page}: 오늘 날짜 게시물 없음 → 종료")
            break
        posts = today_posts

    # 키워드 감지
    found_in_page = []
    for post in posts:
        for keyword in KEYWORDS:
            if keyword in post['title']:
                found_in_page.append({
                    'sigungu': SIGUNGU,
                    'keyword': keyword,
                    'title': post['title'][:100],
                    'date': post['date'],
                    'page': page,
                    'found_at': today,
                    'url': BASE_URL if page == 1 else f'{BASE_URL}?&GotoPage={page}'
                })
                break

    if found_in_page:
        print(f"페이지 {page}: 🔴 {len(found_in_page)}건 감지")
        for f in found_in_page:
            print(f"  - [{f['keyword']}] {f['title'][:50]} ({f['date']})")
        all_found.extend(found_in_page)
    else:
        print(f"페이지 {page}: ⚪ 없음")

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

print(f"\n✅ 완료: 총 {len(all_found)}건 감지 → alerts.json 저장")