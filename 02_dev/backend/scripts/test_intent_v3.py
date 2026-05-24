DIAGNOSIS_KEYWORDS = ["왜","아파","죽","말려","노랗","노래","갈변","썩","벌레","병","증상","이상","시들","무르","곰팡이","진딧물","해충","방제","처방","잎이","뿌리"]
DIRECTORY_KEYWORDS = ["농약사","농약방","종자","비료","작물보호제","회사","업체","판매","어디","가게","찾","지점","매장"]
SUBSIDY_KEYWORDS = ["보조금","지원금","보조사업","신청","지자체","지원","혜택","정책","사업","공고","상토지원","상토 보조"]
EVENT_KEYWORDS = ["행사","박람회","클래스","교육","체험","축제","전시","강의","모임","가드닝"]

def classify_intent(keyword):
    for kw in SUBSIDY_KEYWORDS:
        if kw in keyword:
            return 'subsidy'
    for kw in EVENT_KEYWORDS:
        if kw in keyword:
            return 'event'
    for kw in DIAGNOSIS_KEYWORDS:
        if kw in keyword:
            return 'diagnosis'
    for kw in DIRECTORY_KEYWORDS:
        if kw in keyword:
            return 'directory'
    return 'directory'

tests = [
    '고추 잎이 말려요',
    '순천 농약사',
    '상토 보조금 신청',
    '정원 박람회',
    '몬스테라 잎이 노래요',
    '고추 방제약',
    '상토 회사',
    '토마토 병 증상',
]

for kw in tests:
    print(kw, '->', classify_intent(kw))
