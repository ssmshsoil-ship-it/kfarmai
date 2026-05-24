with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
print('overflow-x-hidden in body:', 'overflow-x-hidden' in content)
print('max-w count:', content.count('max-w-'))
