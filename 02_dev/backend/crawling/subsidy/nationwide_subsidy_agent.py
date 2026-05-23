from __future__ import annotations

import argparse
import html
import json
import os
import random
import re
import time
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urljoin

import requests
from bs4 import BeautifulSoup

try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    from playwright.sync_api import sync_playwright
except Exception:  # pragma: no cover - exercised only when dependency exists.
    PlaywrightTimeoutError = None
    sync_playwright = None


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

GENERIC_KEYWORDS = ["보조", "지원", "육성"]

AGRI_CONTEXT_KEYWORDS = [
    "농업",
    "농가",
    "농민",
    "농촌",
    "영농",
    "축산",
    "원예",
    "작물",
    "식량",
    "벼",
    "쌀",
    "양송이",
    "버섯",
    "스마트팜",
    "농업기술센터",
    "농림",
    "친환경",
]

CATEGORY_RULES = {
    "상토 지원": ["상토", "못자리", "모판", "육묘"],
    "비료 지원": ["비료", "유기질", "퇴비", "토양개량제", "개량제"],
    "종자 지원": ["종자", "종묘", "씨앗", "육묘"],
    "농약 지원": ["농약", "작물보호제", "방제", "병해충"],
    "농기계 지원": ["농기계", "기계", "장비", "트랙터", "이앙기", "드론"],
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

DATE_PATTERN = re.compile(
    r"(20[2-6]\d)\s*(?:[.\-/]\s*(1[0-2]|0?[1-9])\s*[.\-/]\s*(3[01]|[12]\d|0?[1-9])|"
    r"년\s*(1[0-2]|0?[1-9])\s*월\s*(3[01]|[12]\d|0?[1-9])\s*일?)"
)


@dataclass
class RawPost:
    region: str
    title: str
    post_date: str
    original_url: str
    department: str = ""
    support_detail: str = ""


def clean_text(text: Any) -> str:
    value = html.unescape(str(text or ""))
    value = re.sub(r"<\s*br\s*/?\s*>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    value = value.replace("\\n", " ").replace("\\r", " ").replace("\\t", " ")
    value = re.sub(r"[\r\n\t]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_date(value: str) -> str | None:
    text = clean_text(value)
    match = DATE_PATTERN.search(text)
    if not match:
        return None
    year = match.group(1)
    month = match.group(2) or match.group(4)
    day = match.group(3) or match.group(5)
    try:
        return date(int(year), int(month), int(day)).isoformat()
    except ValueError:
        return None


def categorize_subsidy(text: str) -> list[str]:
    source = clean_text(text)
    categories = [
        category
        for category, words in CATEGORY_RULES.items()
        if any(word in source for word in words)
    ]
    return categories or ["기타"]


def contains_keyword(text: str) -> bool:
    source = clean_text(text)
    specific_keywords = [keyword for keyword in KEYWORDS if keyword not in GENERIC_KEYWORDS]
    if any(keyword in source for keyword in specific_keywords):
        return True
    return any(keyword in source for keyword in GENERIC_KEYWORDS) and any(
        keyword in source for keyword in AGRI_CONTEXT_KEYWORDS
    )


def summarize(text: str, default: str, limit: int = 50) -> str:
    cleaned = clean_text(text)
    if not cleaned:
        cleaned = default
    return cleaned[:limit]


def classify_status(start_date: str, end_date: str, today: date | None = None) -> str:
    today = today or date.today()
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return "마감"
    return "진행중" if start <= today <= end else "마감"


def extract_date_range(text: str, fallback: str) -> tuple[str, str]:
    matches = [normalize_date(m.group(0)) for m in DATE_PATTERN.finditer(clean_text(text))]
    dates = [d for d in matches if d]
    if len(dates) >= 2:
        return dates[0], dates[1]
    return fallback, fallback


def normalize_region(region: str, title: str = "", url: str = "") -> str:
    value = clean_text(region)
    if value:
        return value
    text = f"{title} {url}"
    match = re.search(r"([가-힣]+도|[가-힣]+특별자치도|[가-힣]+광역시|서울특별시)\s*([가-힣]+[시군구])", text)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return "지자체명 미확인"


def make_absolute_url(base_url: str, href: str | None) -> str:
    if not href or href.startswith("#") or href.lower().startswith("javascript:"):
        return base_url
    return urljoin(base_url, href)


def parse_table_posts(soup: BeautifulSoup, base_url: str, region: str) -> list[RawPost]:
    posts: list[RawPost] = []
    for row in soup.select("tr"):
        cells = [clean_text(cell.get_text(" ")) for cell in row.find_all(["td", "th"])]
        if len(cells) < 2:
            continue
        row_text = clean_text(" ".join(cells))
        post_date = normalize_date(row_text)
        if not post_date:
            continue
        title_link = row.select_one("a")
        title = clean_text(title_link.get_text(" ") if title_link else "")
        if not title:
            candidates = [c for c in cells if c and not normalize_date(c) and len(c) > 4]
            title = max(candidates, key=len, default="")
        if not title or not contains_keyword(title):
            continue
        department = ""
        for cell in cells:
            if 2 <= len(cell) <= 20 and any(token in cell for token in ["과", "팀", "센터", "읍", "면"]):
                department = cell
                break
        posts.append(
            RawPost(
                region=normalize_region(region, title, base_url),
                title=title,
                post_date=post_date,
                original_url=make_absolute_url(base_url, title_link.get("href") if title_link else None),
                department=department,
                support_detail=row_text,
            )
        )
    return posts


def parse_card_posts(soup: BeautifulSoup, base_url: str, region: str) -> list[RawPost]:
    posts: list[RawPost] = []
    selectors = [
        "li",
        "article",
        ".board-list > div",
        ".list > div",
        ".bbs-list > div",
        ".gallery-list > div",
        "[class*='board'] [class*='item']",
    ]
    seen_texts: set[str] = set()
    for selector in selectors:
        for node in soup.select(selector):
            text = clean_text(node.get_text(" "))
            if len(text) < 8 or text in seen_texts:
                continue
            seen_texts.add(text)
            post_date = normalize_date(text)
            if not post_date or not contains_keyword(text):
                continue
            link = node.select_one("a")
            title = clean_text(link.get_text(" ") if link else "")
            if not title or len(title) < 4:
                title = re.split(r"\s*20[2-6]\d[.\-/년]", text)[0].strip()
            if not contains_keyword(title):
                continue
            posts.append(
                RawPost(
                    region=normalize_region(region, title, base_url),
                    title=title[:160],
                    post_date=post_date,
                    original_url=make_absolute_url(base_url, link.get("href") if link else None),
                    support_detail=text,
                )
            )
    return posts


def parse_posts_from_html(html_text: str, base_url: str, region: str = "") -> list[RawPost]:
    soup = BeautifulSoup(html_text, "html.parser")
    posts = parse_table_posts(soup, base_url, region)
    posts.extend(parse_card_posts(soup, base_url, region))
    deduped: dict[tuple[str, str], RawPost] = {}
    for post in posts:
        deduped[(post.title, post.post_date)] = post
    return list(deduped.values())


def discover_iframes(html_text: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html_text, "html.parser")
    return [
        urljoin(base_url, iframe.get("src"))
        for iframe in soup.select("iframe[src]")
        if iframe.get("src")
    ]


def build_page_url(target: dict[str, Any], page_no: int) -> str:
    base = target["url"]
    page_param = target.get("page_param")
    if page_no <= 1 or not page_param:
        return base
    separator = "&" if "?" in base else "?"
    return f"{base}{separator}{page_param}={page_no}"


class NationwideSubsidyAgent:
    def __init__(
        self,
        target_urls: list[dict[str, Any]],
        mode: str = "auto",
        min_delay: float = 0.7,
        max_delay: float = 2.2,
        timeout_ms: int = 20000,
    ) -> None:
        self.target_urls = target_urls
        self.mode = mode
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.timeout_ms = timeout_ms
        self.session = requests.Session()

    def sleep(self) -> None:
        time.sleep(random.uniform(self.min_delay, self.max_delay))

    def request_html(self, target: dict[str, Any], page_no: int = 1) -> tuple[str, str]:
        url = build_page_url(target, page_no)
        headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "ko-KR,ko;q=0.9"}
        method = clean_text(target.get("method", "get")).lower()
        if method == "post" and page_no > 1:
            response = self.session.post(
                target["url"],
                data={target.get("page_param", "pageIndex"): str(page_no)},
                headers=headers,
                timeout=self.timeout_ms / 1000,
                verify=False,
            )
        else:
            response = self.session.get(url, headers=headers, timeout=self.timeout_ms / 1000, verify=False)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"
        return response.text, response.url

    def playwright_html(self, target: dict[str, Any], page_no: int = 1) -> tuple[str, str, list[dict[str, Any]]]:
        if sync_playwright is None:
            raise RuntimeError("playwright 패키지가 설치되어 있지 않습니다. pip install playwright 후 playwright install chromium 실행 필요")
        url = build_page_url(target, page_no)
        api_payloads: list[dict[str, Any]] = []
        ua = random.choice(USER_AGENTS)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=ua, locale="ko-KR")
            page = context.new_page()

            def on_response(response: Any) -> None:
                ctype = response.headers.get("content-type", "")
                if "json" not in ctype.lower():
                    return
                try:
                    payload = response.json()
                except Exception:
                    return
                api_payloads.append({"url": response.url, "payload": payload})

            page.on("response", on_response)
            try:
                page.goto(url, wait_until="networkidle", timeout=self.timeout_ms)
            except Exception:
                page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            html_text = page.content()
            final_url = page.url
            context.close()
            browser.close()
        return html_text, final_url, api_payloads

    def google_fallback(self, target: dict[str, Any]) -> list[RawPost]:
        host = re.sub(r"^https?://", "", target["url"]).split("/")[0]
        query = f'site:{host} "상토 지원" "고시" OR "공고"'
        google_url = f"https://www.google.com/search?q={quote_plus(query)}"
        try:
            html_text, final_url = self.request_html({"url": google_url}, 1)
        except Exception:
            return []
        posts = parse_card_posts(BeautifulSoup(html_text, "html.parser"), final_url, target.get("region", ""))
        return posts

    def crawl_target(self, target: dict[str, Any]) -> list[RawPost]:
        all_posts: list[RawPost] = []
        max_pages = int(target.get("max_pages", 3))
        for page_no in range(1, max_pages + 1):
            self.sleep()
            try:
                if self.mode == "playwright" or (self.mode == "auto" and sync_playwright is not None):
                    html_text, final_url, _api_payloads = self.playwright_html(target, page_no)
                else:
                    html_text, final_url = self.request_html(target, page_no)
            except Exception as exc:
                print(f"[WARN] fetch failed: {target.get('region','')} page={page_no} error={exc}")
                break

            posts = parse_posts_from_html(html_text, final_url, target.get("region", ""))
            for iframe_url in discover_iframes(html_text, final_url):
                try:
                    iframe_html, iframe_final_url = self.request_html({"url": iframe_url}, 1)
                    posts.extend(parse_posts_from_html(iframe_html, iframe_final_url, target.get("region", "")))
                except Exception:
                    continue
            if not posts and page_no == 1:
                posts = self.google_fallback(target)
            if not posts and page_no > 1:
                break
            all_posts.extend(posts)
        deduped: dict[tuple[str, str, str], RawPost] = {}
        for post in all_posts:
            deduped[(post.region, post.title, post.post_date)] = post
        return list(deduped.values())

    def run(self) -> list[dict[str, Any]]:
        raw_posts: list[RawPost] = []
        for target in self.target_urls:
            print(f"[INFO] crawl start: {target.get('region', '')} {target.get('url')}")
            raw_posts.extend(self.crawl_target(target))
        records = [to_kfarm_record(post, index + 1) for index, post in enumerate(raw_posts)]
        return validate_records(records)


def to_kfarm_record(post: RawPost, seq: int) -> dict[str, Any]:
    source_text = clean_text(f"{post.title} {post.support_detail}")
    start_date, end_date = extract_date_range(source_text, post.post_date)
    categories = categorize_subsidy(source_text)
    default_target = "지역 농업인 및 신청 자격 충족자"
    default_support = "농자재·영농 관련 보조 또는 지원"
    return {
        "id": f"KFarm-SUB-2026-{seq:04d}",
        "region": normalize_region(post.region, post.title, post.original_url),
        "title": clean_text(post.title),
        "department": summarize(post.department, "미확인", 50),
        "post_date": post.post_date,
        "start_date": start_date,
        "end_date": end_date,
        "categories": categories,
        "target_audience": summarize(source_text, default_target, 50),
        "support_detail": summarize(source_text, default_support, 50),
        "original_url": post.original_url,
        "status": classify_status(start_date, end_date),
    }


def validate_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    required = ["title", "region", "original_url"]
    date_fields = ["post_date", "start_date", "end_date"]
    clean_fields = ["title", "department", "target_audience", "support_detail"]
    valid_records: list[dict[str, Any]] = []
    for record in records:
        for key in required:
            assert clean_text(record.get(key)), f"missing required field: {key}"
        for key in date_fields:
            assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", record.get(key, "")), f"invalid date: {key}"
        assert isinstance(record.get("categories"), list) and record["categories"], "categories must be non-empty list"
        for key in clean_fields:
            value = record.get(key, "")
            assert "\n" not in value and "<br" not in value.lower() and "<" not in value, f"unclean field: {key}"
        assert record["status"] in ["진행중", "마감"], "invalid status"
        valid_records.append(record)
    return valid_records


def load_targets(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("target_urls JSON must be an array")
    for target in data:
        if "url" not in target:
            raise ValueError("each target must include url")
    return data


def write_json(records: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
        f.write("\n")


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    return argparse.ArgumentParser(description="kFarmAI nationwide subsidy crawling agent").parse_args()


def main() -> None:
    parser = argparse.ArgumentParser(description="kFarmAI nationwide subsidy crawling agent")
    here = Path(__file__).resolve().parent
    parser.add_argument("--targets", default=str(here / "target_urls.json"))
    parser.add_argument("--output", default=str(here / "kfarm_nationwide_subsidy_2026.json"))
    parser.add_argument("--mode", choices=["auto", "playwright", "requests"], default="auto")
    parser.add_argument("--min-delay", type=float, default=0.7)
    parser.add_argument("--max-delay", type=float, default=2.2)
    args = parser.parse_args()

    targets = load_targets(Path(args.targets))
    agent = NationwideSubsidyAgent(
        target_urls=targets,
        mode=args.mode,
        min_delay=args.min_delay,
        max_delay=args.max_delay,
    )
    records = agent.run()
    write_json(records, Path(args.output))
    print(f"[DONE] wrote {len(records)} records -> {args.output}")


if __name__ == "__main__":
    main()
