from nationwide_subsidy_agent import (
    categorize_subsidy,
    clean_text,
    contains_keyword,
    parse_posts_from_html,
    to_kfarm_record,
    validate_records,
)


def test_clean_text_removes_markup_and_escapes():
    assert clean_text("상토<br>지원\\n사업 <b>공고</b>") == "상토 지원 사업 공고"


def test_categorize_subsidy_multiple_categories():
    categories = categorize_subsidy("상토 및 유기질비료 지원 농기계 보조")
    assert "상토 지원" in categories
    assert "비료 지원" in categories
    assert "농기계 지원" in categories


def test_generic_support_keyword_requires_agriculture_context():
    assert contains_keyword("2026년 농업인 지원사업 공고")
    assert not contains_keyword("2026년 작은도서관 자료구입 지원사업 공고")


def test_polymorphic_table_and_list_parser():
    html = """
    <table>
      <tr><td>1</td><td><a href="/notice/1">2026년 수도용 상토 지원사업 공고</a></td><td>농업정책과</td><td>2026.01.15</td></tr>
    </table>
    <ul>
      <li><a href="/notice/2">농기계 지원사업 신청 안내</a><span>2026-02-01</span></li>
    </ul>
    """
    posts = parse_posts_from_html(html, "https://example.go.kr/list", "전라남도 순천시")
    assert len(posts) == 2
    assert posts[0].post_date == "2026-01-15"
    assert posts[1].original_url == "https://example.go.kr/notice/2"


def test_kfarm_schema_validation():
    html = """
    <table>
      <tr><td>1</td><td><a href="/notice/1">2026년 상토 지원사업 공고</a></td><td>농업정책과</td><td>2026-01-15</td></tr>
    </table>
    """
    post = parse_posts_from_html(html, "https://example.go.kr/list", "충청남도 부여군")[0]
    record = to_kfarm_record(post, 1)
    validated = validate_records([record])
    assert validated[0]["id"] == "KFarm-SUB-2026-0001"
    assert validated[0]["categories"] == ["상토 지원"]
