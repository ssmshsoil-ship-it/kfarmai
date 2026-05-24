from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
import os

app = Flask(__name__)
CORS(app, origins=["https://kfarmai.com", "https://www.kfarmai.com", "http://127.0.0.1:8080", "http://localhost:8080"])

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://xzetqijeucldbfgjuoes.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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

@app.route("/api/search/shops", methods=["GET"])
def search_shops():
    keyword = request.args.get("keyword", "")
    sido = request.args.get("sido", "")
    sigungu = request.args.get("sigungu", "")
    query = supabase.table("pesticide_shops").select("*")
    if sido:
        query = query.eq("sido", sido)
    if sigungu:
        query = query.eq("sigungu", sigungu)
    if keyword:
        query = query.ilike("name", f"%{keyword}%")
    result = query.limit(50).execute()
    return jsonify({"status": "ok", "count": len(result.data), "data": result.data})

@app.route("/api/search/companies", methods=["GET"])
def search_companies():
    keyword = request.args.get("keyword", "")
    category = request.args.get("category", "")
    query = supabase.table("agri_companies").select("*")
    if category:
        query = query.eq("category", category)
    if keyword:
        query = query.ilike("name", f"%{keyword}%")
    result = query.limit(50).execute()
    return jsonify({"status": "ok", "count": len(result.data), "data": result.data})

@app.route("/api/search", methods=["POST", "OPTIONS"])
def search():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    body = request.get_json()
    keyword = body.get("keyword", "")
    intent = classify_intent(keyword)
    shops = []
    companies = []
    if intent in ["directory", "diagnosis"]:
        shops_res = supabase.table("pesticide_shops").select("id, name, sido, sigungu, address, phone, lat, lng").ilike("name", f"%{keyword}%").limit(20).execute()
        companies_res = supabase.table("agri_companies").select("id, name, category, address, website").ilike("name", f"%{keyword}%").limit(20).execute()
        shops = shops_res.data
        companies = companies_res.data
    return jsonify({
        "status": "ok",
        "keyword": keyword,
        "intent": intent,
        "shops": shops,
        "companies": companies
    })

@app.route("/api/intent", methods=["POST", "OPTIONS"])
def intent_only():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    body = request.get_json()
    keyword = body.get("keyword", "")
    intent = classify_intent(keyword)
    return jsonify({"status": "ok", "keyword": keyword, "intent": intent})

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "kFarmAI API 서버 정상 작동"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
