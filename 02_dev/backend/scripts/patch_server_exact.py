with open('02_dev/backend/api/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    keyword = body.get("keyword", "")
    intent = classify_intent(keyword)
    shops = []
    companies = []
    if intent in ["directory", "diagnosis"]:
        shops_res = supabase.table("pesticide_shops").select("id, name, sido, sigungu, address, phone, lat, lng").ilike("name", f"%{keyword}%").limit(20).execute()
        companies_res = supabase.table("agri_companies").select("id, name, category, address, website").ilike("name", f"%{keyword}%").limit(20).execute()
        shops = shops_res.data
        companies = companies_res.data'''

new = '''    keyword = body.get("keyword", "")
    exact = body.get("exact", False)
    intent = classify_intent(keyword)
    shops = []
    companies = []
    if intent in ["directory", "diagnosis"]:
        if exact:
            shops_res = supabase.table("pesticide_shops").select("id, name, sido, sigungu, address, phone, lat, lng").eq("name", keyword).limit(5).execute()
            companies_res = supabase.table("agri_companies").select("id, name, category, address, website, phone").eq("name", keyword).limit(5).execute()
        else:
            shops_res = supabase.table("pesticide_shops").select("id, name, sido, sigungu, address, phone, lat, lng").ilike("name", f"%{keyword}%").limit(20).execute()
            companies_res = supabase.table("agri_companies").select("id, name, category, address, website, phone").ilike("name", f"%{keyword}%").limit(20).execute()
        shops = shops_res.data
        companies = companies_res.data'''

if old in content:
    content = content.replace(old, new, 1)
    with open('02_dev/backend/api/server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('완료')
else:
    print('실패')
