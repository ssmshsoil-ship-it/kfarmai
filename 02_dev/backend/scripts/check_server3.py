with open('02_dev/backend/api/server.py', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('companies_res = supabase.table("agri_companies")')
print(repr(content[idx:idx+300]))
