from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
import os

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://xzetqijeucldbfgjuoes.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZXRxaWpldWNsZGJmZ2p1b2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1NjIwODYsImV4cCI6MjA5NTEzODA4Nn0.QAizDLXQC1DrRi5C0sPahK6s_-6X4zkTEjzJZ6CFprw")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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

@app.route("/api/search", methods=["POST"])
def search():
    body = request.get_json()
    keyword = body.get("keyword", "")
    shops = supabase.table("pesticide_shops").select("id, name, sido, sigungu, address, phone, lat, lng").ilike("name", f"%{keyword}%").limit(20).execute()
    companies = supabase.table("agri_companies").select("id, name, category, address, website").ilike("name", f"%{keyword}%").limit(20).execute()
    return jsonify({
        "status": "ok",
        "keyword": keyword,
        "shops": shops.data,
        "companies": companies.data
    })

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "kFarmAI API 서버 정상 작동"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
