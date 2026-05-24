with open('02_dev/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '</body>'
new = '''<script>
fetch("https://kfarmai.onrender.com/api/stats")
  .then(r => r.json())
  .then(data => {
    const els = {
      pesticide_shops: document.querySelector('.trust-item:nth-child(1) .trust-num'),
      santo: document.querySelector('.trust-item:nth-child(2) .trust-num'),
      seed: document.querySelector('.trust-item:nth-child(3) .trust-num'),
      cpa: document.querySelector('.trust-item:nth-child(4) .trust-num'),
      fert: document.querySelector('.trust-item:nth-child(5) .trust-num'),
    };
    if (els.pesticide_shops) els.pesticide_shops.textContent = data.pesticide_shops.toLocaleString();
    if (els.santo) els.santo.textContent = data.santo.toLocaleString();
    if (els.seed) els.seed.textContent = data.seed.toLocaleString();
    if (els.cpa) els.cpa.textContent = data.cpa.toLocaleString();
    if (els.fert && data.fert) els.fert.textContent = data.fert.toLocaleString();
  })
  .catch(e => console.log("stats 로드 실패:", e));
</script>
</body>'''

content = content.replace(old, new, 1)
with open('02_dev/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('완료')
