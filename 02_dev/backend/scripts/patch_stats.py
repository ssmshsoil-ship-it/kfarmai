with open('02_dev/backend/api/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_endpoint = '''
@app.route("/api/stats", methods=["GET"])
def stats():
    shops = supabase.table("pesticide_shops").select("id", count="exact").execute()
    companies = supabase.table("agri_companies").select("id", count="exact").execute()
    santo = supabase.table("agri_companies").select("id", count="exact").eq("category", "상토").execute()
    seed = supabase.table("agri_companies").select("id", count="exact").eq("category", "종자").execute()
    cpa = supabase.table("agri_companies").select("id", count="exact").eq("category", "작물보호제").execute()
    fert = supabase.table("agri_companies").select("id", count="exact").eq("category", "비료").execute()
    return jsonify({
        "status": "ok",
        "pesticide_shops": shops.count,
        "santo": santo.count,
        "seed": seed.count,
        "cpa": cpa.count,
        "fert": fert.count,
    })

'''

content = content.replace(
    '@app.route("/api/health"',
    new_endpoint + '@app.route("/api/health"'
)

with open('02_dev/backend/api/server.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('완료')
