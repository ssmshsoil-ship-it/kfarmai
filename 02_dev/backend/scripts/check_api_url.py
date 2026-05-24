with open('02_dev/frontend/search_result.html', 'r', encoding='utf-8') as f:
    content = f.read()
print('onrender' in content)
idx = content.find('onrender')
print(content[idx-20:idx+60])
