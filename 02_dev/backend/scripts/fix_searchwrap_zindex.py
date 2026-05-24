with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'search-wrap { position:relative; z-index:10; }',
    'search-wrap { position:relative; z-index:9999; }'
)

with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('완료')
