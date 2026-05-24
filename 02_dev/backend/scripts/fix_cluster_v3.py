with open('02_dev/frontend/map.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'markers.push(marker);\n            return marker;\n        }\n\n        function fitMapToBounds'

new = '''markers.push(marker);
            return marker;
        }
        function applyClusterer() {
            if (clusterer) clusterer.clear();
            clusterer = new kakao.maps.MarkerClusterer({
                map: map,
                averageCenter: true,
                minLevel: 5,
                styles: [{
                    width: '42px', height: '42px',
                    background: 'rgba(30,107,46,0.9)',
                    borderRadius: '50%',
                    color: '#fff',
                    textAlign: 'center',
                    fontWeight: 'bold',
                    lineHeight: '42px',
                    fontSize: '13px'
                }]
            });
            clusterer.addMarkers(markers);
        }

        function fitMapToBounds'''

if old in content:
    content = content.replace(old, new, 1)
    print('applyClusterer 추가 완료')
else:
    print('실패')

# fitMapToBounds 호출 후 applyClusterer 호출
old2 = 'fitMapToBounds(activeList);'
new2 = 'fitMapToBounds(activeList);\n            applyClusterer();'
if old2 in content:
    content = content.replace(old2, new2, 1)
    print('applyClusterer 호출 완료')
else:
    print('호출 실패')

with open('02_dev/frontend/map.html', 'w', encoding='utf-8') as f:
    f.write(content)
