"""
kFarmAI nationwide local crawler.

Mission:
- Run safely on the owner's local PC for long nationwide crawls.
- Use Playwright for dynamic municipal boards.
- Keep a hard-coded starter list of 50+ Korean city/county/agricultural-center notice URLs.
- Parse heterogeneous boards and append validated JSON records to kfarm_nationwide_subsidy.json.

Install:
    pip install playwright beautifulsoup4
    playwright install chromium

Local smoke test only:
    python crawling/subsidy/kfarm_nationwide_production_crawler.py --self-test

Run production crawl:
    python crawling/subsidy/kfarm_nationwide_production_crawler.py --max-agencies 0 --max-pages 2
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import logging
import random
import re
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

try:
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    from playwright.sync_api import sync_playwright
except Exception:
    PlaywrightError = Exception
    PlaywrightTimeoutError = TimeoutError
    sync_playwright = None


OUTPUT_FILE = "kfarm_nationwide_subsidy.json"
ERROR_LOG_FILE = "kfarm_nationwide_subsidy_errors.log"

KEYWORDS = [
    "보조",
    "지원",
    "육성",
    "농기계",
    "상토",
    "못자리",
    "비료",
    "종자",
    "유기질",
    "작물보호제",
    "농약",
    "개량제",
    "방제",
]

GENERIC_KEYWORDS = {"보조", "지원", "육성"}
AGRI_CONTEXT_KEYWORDS = {
    "농업",
    "농가",
    "농민",
    "농촌",
    "영농",
    "농림",
    "원예",
    "축산",
    "작물",
    "식량",
    "친환경",
    "귀농",
    "스마트팜",
    "농업기술센터",
    "농정",
    "벼",
    "쌀",
    "과수",
    "시설하우스",
    "버섯",
    "양송이",
    "딸기",
    "고추",
}

CATEGORY_RULES = {
    "상토 지원": ["상토", "못자리", "모판", "육묘"],
    "비료 지원": ["비료", "유기질", "퇴비", "토양개량제", "개량제"],
    "종자 지원": ["종자", "종묘", "씨앗", "육묘"],
    "농약 지원": ["농약", "작물보호제", "방제", "병해충"],
    "농기계 지원": ["농기계", "기계화", "관리기", "트랙터", "이앙기", "농업기계", "드론"],
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
]

DATE_PATTERN = re.compile(
    r"(20[2-6]\d)\s*(?:[.\-/]\s*(1[0-2]|0?[1-9])\s*[.\-/]\s*(3[01]|[12]\d|0?[1-9])|"
    r"년\s*(1[0-2]|0?[1-9])\s*월\s*(3[01]|[12]\d|0?[1-9])\s*일?)"
)

PERIOD_PATTERN = re.compile(
    r"(20[2-6]\d\s*(?:[.\-/]\s*(?:1[0-2]|0?[1-9])\s*[.\-/]\s*(?:3[01]|[12]\d|0?[1-9])|"
    r"년\s*(?:1[0-2]|0?[1-9])\s*월\s*(?:3[01]|[12]\d|0?[1-9])\s*일?))"
    r"\s*(?:~|∼|-|부터|에서)\s*"
    r"(20[2-6]\d\s*(?:[.\-/]\s*(?:1[0-2]|0?[1-9])\s*[.\-/]\s*(?:3[01]|[12]\d|0?[1-9])|"
    r"년\s*(?:1[0-2]|0?[1-9])\s*월\s*(?:3[01]|[12]\d|0?[1-9])\s*일?))"
)


# Starter targets. Add the remaining municipalities later using the same shape.
# URLs are official city/county/provincial or agricultural-center public notice pages.
target_agencies: list[dict[str, str]] = [
    # 경기
    {"province": "경기도", "region": "경기도 수원시", "agency": "수원시청", "url": "https://www.suwon.go.kr/web/board/BD_board.list.do?bbsCd=1042"},
    {"province": "경기도", "region": "경기도 용인시", "agency": "용인시청", "url": "https://www.yongin.go.kr/user/bbs/BD_selectBbsList.do?q_bbsCode=1001"},
    {"province": "경기도", "region": "경기도 성남시", "agency": "성남시청", "url": "https://www.seongnam.go.kr/city/1000052/30001/bbsList.do"},
    {"province": "경기도", "region": "경기도 고양시", "agency": "고양시청", "url": "https://www.goyang.go.kr/www/user/bbs/BD_selectBbsList.do?q_bbsCode=1030"},
    {"province": "경기도", "region": "경기도 화성시", "agency": "화성시청", "url": "https://www.hscity.go.kr/www/user/bbs/BD_selectBbsList.do?q_bbsCode=1070"},
    {"province": "경기도", "region": "경기도 평택시", "agency": "평택시청", "url": "https://www.pyeongtaek.go.kr/pyeongtaek/bbs/list.do?bIdx=41"},
    {"province": "경기도", "region": "경기도 안성시", "agency": "안성시청", "url": "https://www.anseong.go.kr/portal/bbs/list.do?mId=0401020000"},
    {"province": "경기도", "region": "경기도 이천시", "agency": "이천시청", "url": "https://www.icheon.go.kr/portal/selectBbsNttList.do?bbsNo=14"},
    {"province": "경기도", "region": "경기도 여주시", "agency": "여주시청", "url": "https://www.yeoju.go.kr/brd/board/277/L/menu/599"},
    {"province": "경기도", "region": "경기도 양평군", "agency": "양평군청", "url": "https://www.yp21.go.kr/www/selectBbsNttList.do?bbsNo=1"},
    # 강원
    {"province": "강원특별자치도", "region": "강원특별자치도 춘천시", "agency": "춘천시농업기술센터", "url": "https://www.chuncheon.go.kr/agriculture/"},
    {"province": "강원특별자치도", "region": "강원특별자치도 원주시", "agency": "원주시청", "url": "https://www.wonju.go.kr/www/selectBbsNttList.do?bbsNo=140"},
    {"province": "강원특별자치도", "region": "강원특별자치도 강릉시", "agency": "강릉시청", "url": "https://www.gn.go.kr/www/selectBbsNttList.do?bbsNo=12"},
    {"province": "강원특별자치도", "region": "강원특별자치도 홍천군", "agency": "홍천군청", "url": "https://www.hongcheon.go.kr/www/selectBbsNttList.do?bbsNo=48"},
    {"province": "강원특별자치도", "region": "강원특별자치도 횡성군", "agency": "횡성군청", "url": "https://www.hsg.go.kr/www/selectBbsNttList.do?bbsNo=1"},
    {"province": "강원특별자치도", "region": "강원특별자치도 평창군", "agency": "평창군청", "url": "https://www.pc.go.kr/portal/selectBbsNttList.do?bbsNo=21"},
    {"province": "강원특별자치도", "region": "강원특별자치도 정선군", "agency": "정선군청", "url": "https://www.jeongseon.go.kr/portal/bbs/list.do?bIdx=1"},
    {"province": "강원특별자치도", "region": "강원특별자치도 인제군", "agency": "인제군청", "url": "https://www.inje.go.kr/portal/adm/notice"},
    # 충남
    {"province": "충청남도", "region": "충청남도 천안시", "agency": "천안시청", "url": "https://www.cheonan.go.kr/cop/bbs/BBSMSTR_000000000462/selectBoardList.do"},
    {"province": "충청남도", "region": "충청남도 공주시", "agency": "공주시청", "url": "https://www.gongju.go.kr/prog/saeolGosi/GOSI_03/sub04_03_03/list.do"},
    {"province": "충청남도", "region": "충청남도 보령시", "agency": "보령시청", "url": "https://eminwon.brcn.go.kr/emwp/gov/mogaha/ntis/web/ofr/action/OfrAction.do?context=NTIS&jndinm=OfrNotAncmtEJB&method=selectOfrNotAncmt"},
    {"province": "충청남도", "region": "충청남도 아산시", "agency": "아산시청", "url": "https://www.asan.go.kr/main/cms/?m_mode=list&PageNo=1&site_menu=02_02_01"},
    {"province": "충청남도", "region": "충청남도 서산시", "agency": "서산시청", "url": "https://www.seosan.go.kr/www/selectBbsNttList.do?bbsNo=97"},
    {"province": "충청남도", "region": "충청남도 논산시", "agency": "논산시청", "url": "https://www.nonsan.go.kr/kor/html/sub03/030101.html"},
    {"province": "충청남도", "region": "충청남도 부여군", "agency": "부여군청", "url": "https://www.buyeo.go.kr/html/kr/news/news_040202.html"},
    {"province": "충청남도", "region": "충청남도 홍성군", "agency": "홍성군청", "url": "https://www.hongseong.go.kr/prog/saeolGosi/kor/sub03_0204/GOSI_ALL/list.do"},
    # 충북
    {"province": "충청북도", "region": "충청북도 청주시", "agency": "청주시청", "url": "https://www.cheongju.go.kr/www/selectBbsNttList.do?bbsNo=40"},
    {"province": "충청북도", "region": "충청북도 충주시", "agency": "충주시청", "url": "https://www.chungju.go.kr/www/selectBbsNttList.do?bbsNo=1"},
    {"province": "충청북도", "region": "충청북도 제천시", "agency": "제천시청", "url": "https://www.jecheon.go.kr/www/selectBbsNttList.do?bbsNo=1"},
    {"province": "충청북도", "region": "충청북도 보은군", "agency": "보은군청", "url": "https://www.boeun.go.kr/www/selectBbsNttList.do?bbsNo=1"},
    {"province": "충청북도", "region": "충청북도 옥천군", "agency": "옥천군청", "url": "https://www.oc.go.kr/www/selectBbsNttList.do?bbsNo=1"},
    {"province": "충청북도", "region": "충청북도 영동군", "agency": "영동군청", "url": "https://www.yd21.go.kr/kr/html/sub02/020101.html"},
    {"province": "충청북도", "region": "충청북도 진천군", "agency": "진천군청", "url": "https://www.jincheon.go.kr/home/sub.do?menukey=2908"},
    {"province": "충청북도", "region": "충청북도 음성군", "agency": "음성군청", "url": "https://www.eumseong.go.kr/www/selectBbsNttList.do?bbsNo=6"},
    # 전남
    {"province": "전라남도", "region": "전라남도 목포시", "agency": "목포시청", "url": "https://www.mokpo.go.kr/www/open_administration/city_news/notice"},
    {"province": "전라남도", "region": "전라남도 여수시", "agency": "여수시청", "url": "https://www.yeosu.go.kr/www/govt/news/notice"},
    {"province": "전라남도", "region": "전라남도 순천시", "agency": "순천시청", "url": "https://www.suncheon.go.kr/kr/news/0001/0001/"},
    {"province": "전라남도", "region": "전라남도 나주시", "agency": "나주시청", "url": "https://www.naju.go.kr/www/administration/notice/notice"},
    {"province": "전라남도", "region": "전라남도 광양시", "agency": "광양시청", "url": "https://www.gwangyang.go.kr/kr/board/list.gwangyang?boardId=BBS_0000004"},
    {"province": "전라남도", "region": "전라남도 담양군", "agency": "담양군청", "url": "https://www.damyang.go.kr/board/list.damyang?boardId=BBS_0000001"},
    {"province": "전라남도", "region": "전라남도 고흥군", "agency": "고흥군청", "url": "https://www.goheung.go.kr/boardList.do?boardId=BD_00001"},
    {"province": "전라남도", "region": "전라남도 해남군", "agency": "해남군청", "url": "https://www.haenam.go.kr/planweb/board/list.9is?boardUid=18e3368f5d745106015d754d1c070147"},
    # 전북
    {"province": "전북특별자치도", "region": "전북특별자치도 전주시", "agency": "전주시청", "url": "https://www.jeonju.go.kr/planweb/board/list.9is?boardUid=9be517a74f8dee91014f90e8502d0602"},
    {"province": "전북특별자치도", "region": "전북특별자치도 군산시", "agency": "군산시청", "url": "https://www.gunsan.go.kr/main/m100/list"},
    {"province": "전북특별자치도", "region": "전북특별자치도 익산시", "agency": "익산시청", "url": "https://www.iksan.go.kr/board/list.iksan?boardId=BBS_IKSAN_NEWS"},
    {"province": "전북특별자치도", "region": "전북특별자치도 정읍시", "agency": "정읍시청", "url": "https://www.jeongeup.go.kr/board/list.jeongeup?boardId=BBS_0000012"},
    {"province": "전북특별자치도", "region": "전북특별자치도 남원시", "agency": "남원시청", "url": "https://www.namwon.go.kr/board/list.do?boardId=BBS_0000001"},
    {"province": "전북특별자치도", "region": "전북특별자치도 김제시", "agency": "김제시청", "url": "https://www.gimje.go.kr/board/list.gimje?boardId=BBS_0000044"},
    {"province": "전북특별자치도", "region": "전북특별자치도 완주군", "agency": "완주군청", "url": "https://www.wanju.go.kr/board/list.wanju?boardId=BBS_0000001"},
    {"province": "전북특별자치도", "region": "전북특별자치도 고창군", "agency": "고창군청", "url": "https://www.gochang.go.kr/board/list.gochang?boardId=BBS_0000083"},
    # 경남
    {"province": "경상남도", "region": "경상남도 창원시", "agency": "창원시청", "url": "https://www.changwon.go.kr/cwportal/10310/10438/10439.web"},
    {"province": "경상남도", "region": "경상남도 진주시", "agency": "진주시청", "url": "https://www.jinju.go.kr/00130/02730/00136.web"},
    {"province": "경상남도", "region": "경상남도 김해시", "agency": "김해시청", "url": "https://www.gimhae.go.kr/03360/00023/00024.web"},
    {"province": "경상남도", "region": "경상남도 양산시", "agency": "양산시청", "url": "https://www.yangsan.go.kr/portal/bbs/list.do?ptIdx=293"},
    {"province": "경상남도", "region": "경상남도 밀양시", "agency": "밀양시청", "url": "https://www.miryang.go.kr/web/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000071"},
    {"province": "경상남도", "region": "경상남도 거창군", "agency": "거창군청", "url": "https://www.geochang.go.kr/news/board/List.do?gcode=1002"},
    {"province": "경상남도", "region": "경상남도 하동군", "agency": "하동군농업기술센터", "url": "https://www.hadong.go.kr/02138/03461.web?gcode=4083"},
    {"province": "경상남도", "region": "경상남도 함양군", "agency": "함양군청", "url": "https://www.hygn.go.kr/media/00111/00112.web"},
    # 경북
    {"province": "경상북도", "region": "경상북도 포항시", "agency": "포항시청", "url": "https://www.pohang.go.kr/portal/bbs/list.do?ptIdx=101"},
    {"province": "경상북도", "region": "경상북도 경주시", "agency": "경주시청", "url": "https://www.gyeongju.go.kr/open_content/ko/page.do?mnu_uid=417"},
    {"province": "경상북도", "region": "경상북도 김천시", "agency": "김천시청", "url": "https://www.gc.go.kr/portal/bbs/list.do?ptIdx=1807"},
    {"province": "경상북도", "region": "경상북도 안동시", "agency": "안동시청", "url": "https://www.andong.go.kr/portal/bbs/list.do?ptIdx=103"},
    {"province": "경상북도", "region": "경상북도 구미시", "agency": "구미시청", "url": "https://www.gumi.go.kr/portal/bbs/list.do?ptIdx=100"},
    {"province": "경상북도", "region": "경상북도 영주시", "agency": "영주시청", "url": "https://www.yeongju.go.kr/open_content/main/page.do?mnu_uid=1527"},
    {"province": "경상북도", "region": "경상북도 상주시", "agency": "상주시청", "url": "https://www.sangju.go.kr/board/list.tc?mn=2850"},
    {"province": "경상북도", "region": "경상북도 의성군", "agency": "의성군청", "url": "https://www.usc.go.kr/board/list.tc?mn=1274"},
    # 제주
    {"province": "제주특별자치도", "region": "제주특별자치도 제주시", "agency": "제주시청", "url": "https://www.jejusi.go.kr/information/intro/news.do"},
    {"province": "제주특별자치도", "region": "제주특별자치도 서귀포시", "agency": "서귀포시청", "url": "https://www.seogwipo.go.kr/info/news/notice.htm"},
    {"province": "제주특별자치도", "region": "제주특별자치도", "agency": "제주농업기술센터", "url": "https://agri.jeju.go.kr/agri/notice/notice.htm"},
]


@dataclass
class ParsedPost:
    region: str
    agency: str
    title: str
    post_date: str
    original_url: str
    department: str = ""
    raw_text: str = ""


def setup_logging(base_dir: Path) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    try:
        handlers.append(logging.FileHandler(base_dir / ERROR_LOG_FILE, encoding="utf-8"))
    except OSError:
        pass
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers,
    )


def clean_text(text: Any) -> str:
    value = html.unescape(str(text or ""))
    value = re.sub(r"<\s*br\s*/?\s*>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    value = value.replace("\\n", " ").replace("\\r", " ").replace("\\t", " ")
    value = re.sub(r"[\r\n\t]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_date(value: str) -> str | None:
    match = DATE_PATTERN.search(clean_text(value))
    if not match:
        return None
    year = match.group(1)
    month = match.group(2) or match.group(4)
    day = match.group(3) or match.group(5)
    try:
        return date(int(year), int(month), int(day)).isoformat()
    except ValueError:
        return None


def find_dates(text: str) -> list[str]:
    dates: list[str] = []
    for match in DATE_PATTERN.finditer(clean_text(text)):
        normalized = normalize_date(match.group(0))
        if normalized and normalized not in dates:
            dates.append(normalized)
    return dates


def extract_period(text: str, fallback: str) -> tuple[str, str]:
    source = clean_text(text)
    period = PERIOD_PATTERN.search(source)
    if period:
        start = normalize_date(period.group(1))
        end = normalize_date(period.group(2))
        if start and end:
            return start, end
    return fallback, fallback


def has_agri_keyword(text: str) -> bool:
    source = clean_text(text)
    specific = [word for word in KEYWORDS if word not in GENERIC_KEYWORDS]
    if any(word in source for word in specific):
        return True
    return any(word in source for word in GENERIC_KEYWORDS) and any(
        word in source for word in AGRI_CONTEXT_KEYWORDS
    )


def categorize_subsidy(text: str) -> list[str]:
    source = clean_text(text)
    categories = [
        category
        for category, words in CATEGORY_RULES.items()
        if any(word in source for word in words)
    ]
    return categories or ["기타"]


def summarize(text: str, default: str, limit: int = 80) -> str:
    source = clean_text(text) or default
    return source[:limit]


def status_from_dates(start_date: str, end_date: str, today: date | None = None) -> str:
    today = today or date.today()
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return "마감"
    return "진행중" if start <= today <= end else "마감"


def absolute_url(base_url: str, href: str | None) -> str:
    if not href:
        return base_url
    href = href.strip()
    if not href or href.startswith("#"):
        return base_url
    if href.lower().startswith("javascript:"):
        return base_url
    return urljoin(base_url, href)


def pick_title_from_node(node: Any) -> tuple[str, str]:
    link = node.select_one("a") if hasattr(node, "select_one") else None
    if link:
        title = clean_text(link.get("title") or link.get_text(" "))
        href = link.get("href")
        if title:
            return title, href or ""

    for selector in [".title", ".subject", ".tit", "[class*='title']", "[class*='subject']"]:
        found = node.select_one(selector)
        if found:
            title = clean_text(found.get_text(" "))
            if title:
                link = found.select_one("a")
                return title, link.get("href") if link else ""

    text = clean_text(node.get_text(" "))
    title = re.split(r"\s+20[2-6]\d[.\-/년]", text)[0].strip()
    return title[:180], ""


def guess_department(text: str) -> str:
    source = clean_text(text)
    match = re.search(r"(담당부서|부서|작성부서)\s*[:：]?\s*([가-힣A-Za-z0-9·\-\s]{2,24})", source)
    if match:
        return clean_text(match.group(2))[:40]
    candidates = re.findall(r"([가-힣A-Za-z0-9·]{2,18}(?:과|팀|센터|소|읍|면|동))", source)
    return candidates[0] if candidates else ""


def parse_table_posts(soup: BeautifulSoup, agency: dict[str, str]) -> list[ParsedPost]:
    posts: list[ParsedPost] = []
    for row in soup.select("tr"):
        cells = [clean_text(cell.get_text(" ")) for cell in row.find_all(["td", "th"])]
        if len(cells) < 2:
            continue
        row_text = clean_text(" ".join(cells))
        post_date = normalize_date(row_text)
        if not post_date:
            continue
        title, href = pick_title_from_node(row)
        if not title or not has_agri_keyword(f"{title} {row_text}"):
            continue
        posts.append(
            ParsedPost(
                region=agency["region"],
                agency=agency["agency"],
                title=title,
                post_date=post_date,
                original_url=absolute_url(agency["url"], href),
                department=guess_department(row_text),
                raw_text=row_text,
            )
        )
    return posts


def parse_list_or_div_posts(soup: BeautifulSoup, agency: dict[str, str]) -> list[ParsedPost]:
    posts: list[ParsedPost] = []
    selectors = [
        "li",
        "article",
        ".board-list > div",
        ".bbs-list > div",
        ".list > div",
        ".notice-list > div",
        "[class*='board'] [class*='item']",
        "[class*='bbs'] [class*='item']",
        "[class*='notice'] [class*='item']",
    ]
    seen: set[str] = set()
    for selector in selectors:
        for node in soup.select(selector):
            text = clean_text(node.get_text(" "))
            if len(text) < 12 or text in seen:
                continue
            seen.add(text)
            post_date = normalize_date(text)
            if not post_date:
                continue
            title, href = pick_title_from_node(node)
            if not title or not has_agri_keyword(f"{title} {text}"):
                continue
            posts.append(
                ParsedPost(
                    region=agency["region"],
                    agency=agency["agency"],
                    title=title,
                    post_date=post_date,
                    original_url=absolute_url(agency["url"], href),
                    department=guess_department(text),
                    raw_text=text,
                )
            )
    return posts


def universal_parse(html_text: str, agency: dict[str, str]) -> list[ParsedPost]:
    soup = BeautifulSoup(html_text, "html.parser")
    posts = parse_table_posts(soup, agency) + parse_list_or_div_posts(soup, agency)
    deduped: dict[str, ParsedPost] = {}
    for post in posts:
        key = hashlib.sha1(f"{post.region}|{post.title}|{post.post_date}".encode("utf-8")).hexdigest()
        deduped[key] = post
    return list(deduped.values())


def extract_iframe_urls(html_text: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html_text, "html.parser")
    return [
        urljoin(base_url, iframe.get("src"))
        for iframe in soup.select("iframe[src]")
        if iframe.get("src")
    ]


def to_record(post: ParsedPost, seq: int) -> dict[str, Any]:
    source = clean_text(f"{post.title} {post.raw_text}")
    start_date, end_date = extract_period(source, post.post_date)
    return {
        "id": f"KFarm-SUB-2026-{seq:04d}",
        "region": post.region,
        "title": clean_text(post.title),
        "department": summarize(post.department, post.agency, 50),
        "post_date": post.post_date,
        "start_date": start_date,
        "end_date": end_date,
        "categories": categorize_subsidy(source),
        "target_audience": summarize(source, "지역 농업인 및 신청 자격 충족자", 80),
        "support_detail": summarize(source, "농자재·영농 관련 보조 또는 지원", 80),
        "original_url": post.original_url,
        "status": status_from_dates(start_date, end_date),
    }


def validate_record(record: dict[str, Any]) -> bool:
    for key in ["title", "region", "original_url"]:
        if not clean_text(record.get(key)):
            return False
    for key in ["post_date", "start_date", "end_date"]:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(record.get(key, ""))):
            return False
    for key in ["title", "department", "target_audience", "support_detail"]:
        value = str(record.get(key, ""))
        if "\n" in value or "\t" in value or "<br" in value.lower() or "<" in value:
            return False
    return isinstance(record.get("categories"), list) and bool(record["categories"])


def load_existing(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def save_records(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(path)


def merge_records(existing: list[dict[str, Any]], incoming: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key: dict[str, dict[str, Any]] = {}
    for record in existing + incoming:
        key = hashlib.sha1(
            f"{record.get('region')}|{record.get('title')}|{record.get('post_date')}|{record.get('original_url')}".encode("utf-8")
        ).hexdigest()
        by_key[key] = record
    merged = list(by_key.values())
    merged.sort(key=lambda item: (item.get("post_date", ""), item.get("region", "")), reverse=True)
    for index, record in enumerate(merged, 1):
        record["id"] = f"KFarm-SUB-2026-{index:04d}"
    return merged


class KFarmCrawler:
    def __init__(
        self,
        agencies: list[dict[str, str]],
        output_path: Path,
        min_delay: float = 3.0,
        max_delay: float = 7.0,
        timeout_ms: int = 30000,
        max_pages: int = 1,
    ) -> None:
        self.agencies = agencies
        self.output_path = output_path
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.timeout_ms = timeout_ms
        self.max_pages = max_pages

    def polite_sleep(self) -> None:
        delay = random.uniform(self.min_delay, self.max_delay)
        logging.info("sleep %.1fs", delay)
        time.sleep(delay)

    def crawl(self) -> list[dict[str, Any]]:
        if sync_playwright is None:
            raise RuntimeError("Playwright is not installed. Run: pip install playwright && playwright install chromium")

        parsed_posts: list[ParsedPost] = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for index, agency in enumerate(self.agencies, 1):
                logging.info("[%s/%s] %s %s", index, len(self.agencies), agency["region"], agency["url"])
                self.polite_sleep()
                ua = random.choice(USER_AGENTS)
                context = browser.new_context(user_agent=ua, locale="ko-KR", viewport={"width": 1366, "height": 900})
                page = context.new_page()
                try:
                    response = page.goto(agency["url"], wait_until="networkidle", timeout=self.timeout_ms)
                    status = response.status if response else 0
                    if status in {403, 404}:
                        logging.error("skip %s status=%s url=%s", agency["region"], status, agency["url"])
                        context.close()
                        continue
                    html_text = page.content()
                    posts = universal_parse(html_text, agency)
                    for iframe_url in extract_iframe_urls(html_text, agency["url"]):
                        try:
                            iframe_page = context.new_page()
                            iframe_page.goto(iframe_url, wait_until="networkidle", timeout=self.timeout_ms)
                            iframe_agency = dict(agency)
                            iframe_agency["url"] = iframe_url
                            posts.extend(universal_parse(iframe_page.content(), iframe_agency))
                            iframe_page.close()
                        except (PlaywrightTimeoutError, PlaywrightError) as iframe_error:
                            logging.warning("iframe skip %s %s", iframe_url, iframe_error)
                    parsed_posts.extend(posts)
                    logging.info("found %s candidate posts from %s", len(posts), agency["region"])
                except (PlaywrightTimeoutError, PlaywrightError) as exc:
                    logging.error("skip %s error=%s", agency["region"], exc)
                except Exception as exc:
                    logging.exception("unexpected skip %s error=%s", agency["region"], exc)
                finally:
                    context.close()
            browser.close()

        existing = load_existing(self.output_path)
        start_seq = len(existing) + 1
        incoming = [to_record(post, start_seq + i) for i, post in enumerate(parsed_posts)]
        incoming = [record for record in incoming if validate_record(record)]
        merged = merge_records(existing, incoming)
        save_records(self.output_path, merged)
        return incoming


def run_self_test() -> None:
    fake_agency = {
        "province": "전라남도",
        "region": "전라남도 순천시",
        "agency": "순천시청",
        "url": "https://example.go.kr/notice/list",
    }
    table_html = """
    <table>
      <tr>
        <td>1</td>
        <td><a href="/notice/100">2026년 수도용 상토 지원사업 신청 공고</a></td>
        <td>농업정책과</td>
        <td>2026.01.15</td>
      </tr>
    </table>
    """
    list_html = """
    <ul>
      <li>
        <a href="/notice/200">농기계 지원사업 대상자 모집</a>
        <span>2026-02-03</span>
        <span>농업기술센터</span>
      </li>
    </ul>
    """
    posts = universal_parse(table_html, fake_agency) + universal_parse(list_html, fake_agency)
    assert len(posts) == 2, posts
    records = [to_record(post, i + 1) for i, post in enumerate(posts)]
    assert all(validate_record(record) for record in records), records
    assert records[0]["categories"] == ["상토 지원"], records[0]
    assert "농기계 지원" in records[1]["categories"], records[1]
    assert clean_text("상토<br>지원\\n사업\t공고") == "상토 지원 사업 공고"
    print("self-test passed: universal parser, cleaner, classifier, schema validator")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="kFarmAI nationwide municipal/agricultural subsidy crawler")
    parser.add_argument("--output", default=OUTPUT_FILE, help="Output JSON path")
    parser.add_argument("--max-agencies", type=int, default=0, help="0 means all embedded agencies")
    parser.add_argument("--max-pages", type=int, default=1, help="Reserved for future pagination expansion")
    parser.add_argument("--min-delay", type=float, default=3.0)
    parser.add_argument("--max-delay", type=float, default=7.0)
    parser.add_argument("--timeout-ms", type=int, default=30000)
    parser.add_argument("--self-test", action="store_true", help="Run fake HTML tests only; no network crawl")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_dir = Path.cwd()
    setup_logging(base_dir)

    if len(target_agencies) < 50:
        raise RuntimeError("target_agencies must contain at least 50 agencies")

    if args.self_test:
        run_self_test()
        return

    selected = target_agencies if args.max_agencies == 0 else target_agencies[: args.max_agencies]
    crawler = KFarmCrawler(
        agencies=selected,
        output_path=Path(args.output),
        min_delay=args.min_delay,
        max_delay=args.max_delay,
        timeout_ms=args.timeout_ms,
        max_pages=args.max_pages,
    )
    incoming = crawler.crawl()
    logging.info("new valid records: %s", len(incoming))
    logging.info("output: %s", Path(args.output).resolve())


if __name__ == "__main__":
    main()
