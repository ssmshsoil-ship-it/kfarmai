with open('02_dev/frontend/santo.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('<header')
print(content[idx:idx+500])
