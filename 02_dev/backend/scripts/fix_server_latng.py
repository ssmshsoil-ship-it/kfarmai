with open('02_dev/backend/api/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. companies select에 lat, lng 추가
old1 = 'companies_res = supabase.table("agri_companies").select("id, name, category, address, website, phone").eq("name", keyword).limit(5).execute()'
new1 = 'companies_res = supabase.table("agri_companies").select("id, name, category, address, website, phone, lat, lng").ilike("name", f"%{keyword}%").limit(5).execute()'

if old1 in content:
    content = content.replace(old1, new1, 1)
    print("exact 회사 검색 수정 완료")
else:
    print("exact 실패")

old2 = 'companies_res = supabase.table("agri_companies").select("id, name, category, address, website, phone").ilike("name", f"%{keyword}%").limit(20).execute()'
new2 = 'companies_res = supabase.table("agri_companies").select("id, name, category, address, website, phone, lat, lng").ilike("name", f"%{keyword}%").limit(20).execute()'

if old2 in content:
    content = content.replace(old2, new2, 1)
    print("일반 회사 검색 수정 완료")
else:
    print("일반 실패")

with open('02_dev/backend/api/server.py', 'w', encoding='utf-8') as f:
    f.write(content)
