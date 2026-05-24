with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx_start = content.find('<script>')
idx_end = content.rfind('</script>') + 9
print(content[idx_start:idx_end])
