with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()
import re
funcs = re.findall(r'function (\w+)\(', content)
print(funcs)
