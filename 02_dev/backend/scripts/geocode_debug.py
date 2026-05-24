import requests

KAKAO_KEY = "ccd258d6289344411bff3f3781632135"

def geocode_debug(name, address):
    headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
    res = requests.get("https://dapi.kakao.com/v2/local/search/address.json", headers=headers, params={"query": address})
    print(f"{name}: {res.status_code} -> {res.text[:200]}")

geocode_debug("남해화학", "전라남도 여수시 중흥로 112")
geocode_debug("카프로", "울산광역시 남구 산업로 915")
geocode_debug("한국협화", "울산광역시 남구 산업로 915")
geocode_debug("세기", "경기도 안산시 단원구 원시로 351")
