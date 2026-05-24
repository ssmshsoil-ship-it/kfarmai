with open('H:/내 드라이브/kfarmai-web/agri_map.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('<header')
print(content[idx:idx+200])
