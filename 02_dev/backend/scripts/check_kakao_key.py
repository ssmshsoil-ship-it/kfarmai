with open('02_dev/frontend/agri_map.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('appkey=')
print(content[idx:idx+60])
