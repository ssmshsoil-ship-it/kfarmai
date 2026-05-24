with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('function renderMarkers') 
if idx == -1:
    idx = content.find('fitMapToBounds')
print(content[idx:idx+400])
